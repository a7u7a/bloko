import sys
import os
import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import uuid
import json
from PIL import Image
from json_parser import parse_stocks_data
from rgbmatrix import graphics
from tickers import TickerData

# Import samplebase from parent directory 'samples'
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', 'stocks-data.json')
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, 'logs', 'bloko-scroller.log')

parent = os.path.dirname(PROJECT_ROOT)
sys.path.append(parent)
from samplebase import SampleBase

# Setup logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class Ticker:
    id: str
    name: str
    pos: int = 0
    width: int = 0

class DisplayConfig:
    def __init__(self):
        self.base_color = graphics.Color(255, 255, 255)
        self.up_color = graphics.Color(0, 255, 0)
        self.down_color = graphics.Color(255, 0, 0)
        self.interrupt_color = graphics.Color(255, 0, 0)

class ResourceManager:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.fonts: Dict[str, graphics.Font] = {}
        self.images: Dict[str, Image.Image] = {}
        
    def load_font(self, name: str, path: str) -> graphics.Font:
        font = graphics.Font()
        full_path = os.path.join(self.project_root, "fonts", path)
        font.LoadFont(full_path)
        self.fonts[name] = font
        return font

    def load_image(self, name: str, path: str) -> Image.Image:
        full_path = os.path.join(self.project_root, "images", path)
        image = Image.open(full_path).convert('RGB')
        self.images[name] = image
        return image

    def load_ticker_images(self, tickers: List[dict]) -> Dict[str, Image.Image]:
        return {
            t["name"]: self.load_image(
                t["name"],
                os.path.join("tickers", t["image_path"])
            )
            for t in tickers
        }

class StockDataManager:
    def __init__(self, data_file_path: str):
        self.data_file_path = data_file_path
        self.stock_data: Optional[Dict] = None

    def load_stocks(self) -> bool:
        try:
            with open(self.data_file_path) as json_file:
                json_data = json.load(json_file)
                self.stock_data = parse_stocks_data(json_data)
                logging.info("Updated stock data successfully")
                return True
        except Exception as e:
            logging.error(f"Error loading stocks data: {e}")
            self.stock_data = None
            return False

    def get_ticker_data(self, ticker_name: str) -> Tuple[str, str, float]:
        """Returns (price, change_str, change_raw)"""
        if not self.stock_data:
            return ("loading", "loading", 0.0)

        try:
            ticker_data = self.stock_data[ticker_name]
            price = str(round(ticker_data["current_price"], 2))
            change_raw = round(ticker_data["regular_market_change_percent"], 2)
            change_str = str(change_raw)
            return price, change_str, change_raw
        except Exception as e:
            logging.error(f"Error getting ticker data for {ticker_name}: {e}")
            return ("error", "error", 0.0)

class Scroller(SampleBase):
    def __init__(self):
        super(Scroller, self).__init__()
        self.project_root = PROJECT_ROOT
        self.resources = ResourceManager(PROJECT_ROOT)
        self.stock_data = StockDataManager(DATA_FILE_PATH)
        self.display_config = DisplayConfig()
        self.active_tickers: List[Ticker] = []
        self.t_index = 0

    def initialize(self) -> bool:
        try:
            self.frame_buffer = self.matrix.CreateFrameCanvas()
            self.tickers = TickerData().tickers
            
            self.resources.load_font("main", "7x13.bdf")
            self.resources.load_image("arrow_up", "symbols/arrow_green.ppm")
            self.resources.load_image("arrow_down", "symbols/arrow_red.ppm")
            self.ticker_images = self.resources.load_ticker_images(self.tickers)

            self.active_tickers = [self.new_ticker(0)]
            self.stock_data.load_stocks()
            
            return True
        except Exception as e:
            logging.error(f"Initialization failed: {e}")
            return False

    def new_ticker(self, index: int) -> Ticker:
        return Ticker(
            id=str(uuid.uuid1()),
            name=self.tickers[index]["name"],
            pos=self.frame_buffer.width
        )

    def run(self):
        if not self.initialize():
            logging.error("Failed to initialize scroller")
            return

        while True:
            self.update_tickers()
            self.usleep(8500)

    def update_tickers(self):
        self.frame_buffer.Clear()
        for ticker in self.active_tickers:
            self.draw_ticker(ticker)
            self.update_ticker_position(ticker)
        
        self.frame_buffer = self.matrix.SwapOnVSync(self.frame_buffer)

    def draw_ticker(self, ticker):
        main_font = self.resources.fonts["main"]
        """Draws a single ticker with its image, price, and change data"""
        # Get image and position
        t_image = self.resources.images[ticker.name]
        img_w, _ = t_image.size
        self.frame_buffer.SetImage(t_image, ticker.pos)
        
        # Get price data and determine arrow/color
        price, change, change_raw = self.stock_data.get_ticker_data(ticker.name)
        arrow = self.resources.images["arrow_up"] if change_raw > 0 else self.resources.images["arrow_down"]
        change_color = self.display_config.up_color if change_raw > 0 else self.display_config.down_color
        
        # Calculate positions and draw elements
        text_base_pos = ticker.pos + img_w + 4
        title_w = graphics.DrawText(self.frame_buffer, main_font, text_base_pos, 15, self.display_config.base_color, ticker.name)
        
        price_w = graphics.DrawText(self.frame_buffer, main_font, text_base_pos, 26, self.display_config.up_color, price)
        
        arrow_pos = text_base_pos + 4 + price_w
        self.frame_buffer.SetImage(arrow, arrow_pos, 21)
        
        change_pos = arrow_pos + arrow.size[0] + 4
        change_w = graphics.DrawText(self.frame_buffer, main_font, change_pos, 26, change_color, change)
        
        # Calculate total width
        line_top_w = title_w
        line_bottom_w = price_w + 4 + arrow.size[0] + 4 + change_w
        ticker.width = img_w + max(line_top_w, line_bottom_w) + 12

    def update_ticker_position(self, ticker):
        """Updates ticker position and manages active tickers list"""
        # Remove ticker when it moves offscreen
        if ticker.pos + 500 + ticker.width == 0:
            self.active_tickers.remove(ticker)
            return
        
        # Add new ticker when current one is fully visible
        if ticker.pos == self.frame_buffer.width - ticker.width:
            self.t_index += 1
            index_next = self.t_index % len(self.tickers)
            self.active_tickers.append(self.new_ticker(index_next))
        
        ticker.pos -= 1