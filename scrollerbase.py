
from rgbmatrix import graphics
from tickers import TickerData
from PIL import Image
from time import sleep
from dataclasses import dataclass
import uuid
import math
import sys
import os
  
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
  
# now we can import the module in the parent
# directory.
from samplebase import SampleBase

@dataclass
class Ticker:
    id: str
    name: str
    pos: str = 0
    width: int = 0

class Scroller(SampleBase):
    def __init__(self):
        super(Scroller, self).__init__()
        self.int_flag = False

    def init_fonts(self):
        self.font = graphics.Font()
        self.font.LoadFont("../../../../fonts/7x13.bdf")

    def init_colors(self):
        self.base_color = graphics.Color(255, 255, 255)
        self.up_color = graphics.Color(0, 255, 0)
        self.down_color = graphics.Color(255, 0, 0)

    def run(self):
        self.frame_buffer = self.matrix.CreateFrameCanvas()
        self.tickers = TickerData().tickers
        self.images = self.load_imgs()
        self.active_tickers = [self.new_ticker(0)]
        self.init_fonts()
        self.init_colors()
        self.t_index = 0
        
        # main scroller loop
        while True:
            if not self.int_flag:
                self.update_tickers()
            else:
                self.update_interruption()
            self.usleep(10000)

    def update_interruption(self):
        self.clear_buffer_on_interruption()
        graphics.DrawText(self.frame_buffer, self.font, self.interrupt_text_pos, 23, self.down_color, self.int_text)
        self.frame_buffer = self.matrix.SwapOnVSync(self.frame_buffer)
        self.sleep_once(1)
        if self.matrix.brightness > 0:
            self.matrix.brightness -= 1
            self.usleep(10000)
        else:
            self.int_flag = False
            self.matrix.brightness = self.max_brightness

    def clear_buffer_on_interruption(self):
        if self.clear_buffer_flag:
            self.frame_buffer.Clear()
            self.matrix.Fill(0,0,0)
            self.clear_buffer_flag = False

    def sleep_once(self, t):
        if self.sleep_once_flag:
            sleep(t)
            self.sleep_once_flag = False

    def load_imgs(self):
        img_dict = {}
        for t in self.tickers:
            image = Image.open(t["image_path"]).convert('RGB')
            image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
            t_name = t["name"]
            img_dict[t_name] = image
        return img_dict

    def new_ticker(self, index):
        return Ticker(id=uuid.uuid1(), name=self.tickers[index]["name"], pos=self.frame_buffer.width)

    def interrupt(self, text):
        print("interrupted")
        self.int_text = text
        self.max_brightness = self.matrix.brightness
        self.interrupt_text_pos = math.floor(self.matrix.width / 2)
        self.int_flag = True
        self.sleep_once_flag = True
        self.clear_buffer_flag = True

    def update_tickers(self):
        self.frame_buffer.Clear()
        for ticker in self.active_tickers:
            # get data
            t_name = ticker.name
            t_pos = ticker.pos
            t_image = self.images[t_name]
            img_w, img_h = t_image.size

            # here we fetch values from cached api calls
            # and draw the arrows

            # compose frame
            self.frame_buffer.SetImage(t_image, t_pos)
            title_w = graphics.DrawText(self.frame_buffer, self.font, t_pos + img_w, 10, self.base_color, t_name)
            graphics.DrawText(self.frame_buffer, self.font, t_pos + img_w, 23, self.up_color, "+10")
            graphics.DrawText(self.frame_buffer, self.font, t_pos + img_w + 25, 23, self.down_color, "-5")

            # update ticker
            # removes ticker when it has moved offscreen
            margin = 500
            if t_pos + margin + ticker.width == 0:
                self.active_tickers.remove(ticker)
            txt_w = title_w + 20
            ticker.width = img_w + txt_w 
            # Adds a new ticker to active_tickers when right-most ticker is completely visible
            # if the ticker right edge touches the canvas edges
            if t_pos == self.frame_buffer.width - ticker.width:
                # fetch next ticker from ticker_list
                self.t_index += 1
                index_next = self.t_index % len(self.tickers) # find equivalent index in ticker_list 
                self.active_tickers.append(self.new_ticker(index_next))
            ticker.pos -= 1
            
        # update screen
        self.frame_buffer = self.matrix.SwapOnVSync(self.frame_buffer)

if __name__ == "__main__":
    scroller = Scroller()
    if (not scroller.process()):
        scroller.print_help()