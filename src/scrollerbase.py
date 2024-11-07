import sys
import os
import logging
from time import sleep
from dataclasses import dataclass
import math
import uuid
import json
from PIL import Image
from json_parser import parse_stocks_data

from tickers import TickerData
from rgbmatrix import graphics

# Import samplebase from parent directory 'samples'
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent = os.path.dirname(PROJECT_ROOT)
sys.path.append(parent)
from samplebase import SampleBase

# # Project paths setup
DATA_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', 'stocks-data.json')
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, 'logs', 'bloko-scroller.log')

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
    pos: str = 0
    width: int = 0

data_directory = './data/'

class Scroller(SampleBase):
    def __init__(self):
        logging.info("Initializing Scroller...")
        super(Scroller, self).__init__()
        self.load_stocks()

    def init_fonts(self):
        self.font = graphics.Font()
        self.interrupt_font = graphics.Font()
        self.font.LoadFont(os.path.join(PROJECT_ROOT, "fonts", "7x13.bdf"))
        self.interrupt_font.LoadFont(os.path.join(PROJECT_ROOT, "fonts", "helvB18.bdf"))

    def run(self):
        self.frame_buffer = self.matrix.CreateFrameCanvas()
        self.tickers = TickerData().tickers
        self.images = self.load_imgs()
        self.arrow_up = Image.open(os.path.join(PROJECT_ROOT,"images","symbols", "arrow_green.ppm")).convert('RGB')
        self.arrow_down = Image.open(os.path.join(PROJECT_ROOT,"images","symbols", "arrow_red.ppm")).convert('RGB')
        self.active_tickers = [self.new_ticker(0)]
        self.init_fonts()
        self.init_colors()
        self.t_index = 0

        # Main scroller loop
        while True:
            self.update_tickers()

    def init_colors(self):
        self.base_color = graphics.Color(255, 255, 255)
        self.up_color = graphics.Color(0, 255, 0)
        self.down_color = graphics.Color(255, 0, 0)
        self.interrupt_color = graphics.Color(255,0, 0)

    def sleep_once(self, t):
        if self.sleep_once_flag:
            sleep(t)
            self.sleep_once_flag = False

    def load_imgs(self):
        img_dict = {}
        for t in self.tickers:
            img_path = os.path.join(PROJECT_ROOT, "images", "tickers", t["image_path"])
            image = Image.open(img_path).convert('RGB')
            t_name = t["name"]
            img_dict[t_name] = image
        return img_dict

    def new_ticker(self, index):
        return Ticker(id=uuid.uuid1(), name=self.tickers[index]["name"], pos=self.frame_buffer.width)

    def load_stocks(self):
            logging.info("Reading updated stocks data from file...")
            try:
                with open(DATA_FILE_PATH) as json_file:
                    json_data = json.load(json_file)
                    self.stock_data = parse_stocks_data(json_data)
                    logging.info("Updated stock data OK!")
            except Exception as e:
                logging.error("Error loading stocks data")
                self.stock_data = None

    def get_ticker_fields_from_data(self, name):
        temp_text = "loading"
        price = temp_text
        change = temp_text
        change_raw = 0
        if self.stock_data is not None:
            try:
                ticker_data = self.stock_data[name]
                price = str(round(ticker_data["current_price"], 2))
                change = str(round(ticker_data["regular_market_change_percent"], 2))
                change_raw = round(ticker_data["regular_market_change_percent"], 2)
            except Exception as e:
                logging.error("Error at scrollerbase get_ticker_fields_from_data()")
        else:
            logging.info("No ticker data yet. Stocks may still file is loading..")
        return [price, change, change_raw]

    def update_tickers(self):
        self.frame_buffer.Clear()
        for ticker in self.active_tickers:
            # get data
            t_name = ticker.name
            t_pos = ticker.pos
            t_image = self.images[t_name]
            img_w, img_h = t_image.size

            ########### MAKE THIS A FUNCTION
            # here we fetch values from cached api calls
            # and draw the arrows
    
            price, change, change_raw = self.get_ticker_fields_from_data(ticker.name)

            # compose frame
            self.frame_buffer.SetImage(t_image, t_pos)
            if change_raw > 0:
                arrow = self.arrow_up
                change_color = self.up_color
            else:
                arrow = self.arrow_down
                change_color = self.down_color

            arrow_w, arrow_h = arrow.size
            base_margin = 4
            first_line_h = 15
            second_line_h = 26
            arrow_pos_h = 21
            left_margin = 4
            right_margin = 12
            text_base_pos = t_pos + img_w + left_margin
            title_w = graphics.DrawText(self.frame_buffer, self.font, text_base_pos, first_line_h, self.base_color, t_name)
            price_pos = text_base_pos
            price_w = graphics.DrawText(self.frame_buffer, self.font, price_pos, second_line_h, self.up_color, price)
            arrow_pos = price_pos + base_margin + price_w
            self.frame_buffer.SetImage(arrow, arrow_pos, arrow_pos_h)
            change_pos = arrow_pos + arrow_w + base_margin
            change_w = graphics.DrawText(self.frame_buffer, self.font, change_pos, second_line_h, change_color, change)
            line_top_w = title_w
            line_bottom_w = price_w + base_margin + arrow_w + base_margin + change_w
            if line_top_w > line_bottom_w:
                txt_w = line_top_w + right_margin
            else:
                txt_w = line_bottom_w + right_margin
            ###########

            # update ticker
            # removes ticker when it has moved offscreen
            offscreen_margin = 500
            if t_pos + offscreen_margin + ticker.width == 0:
                self.active_tickers.remove(ticker)
            
           
            ticker.width = img_w + txt_w
            # Adds a new ticker to active_tickers when right-most ticker is completely visible
            # if the ticker right edge touches the canvas edges
            if t_pos == self.frame_buffer.width - ticker.width:
                # fetch next ticker from ticker_list
                self.t_index += 1
                # find equivalent index in ticker_list
                index_next = self.t_index % len(self.tickers)
                self.active_tickers.append(self.new_ticker(index_next))
            ticker.pos -= 1

        # update screen
        self.frame_buffer = self.matrix.SwapOnVSync(self.frame_buffer)


if __name__ == "__main__":
    scroller = Scroller()
    # if (not scroller.process()):
    #     scroller.print_help()
