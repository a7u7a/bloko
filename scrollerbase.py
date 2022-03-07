from email.mime import base
import sys
import os
from time import sleep
from dataclasses import dataclass
import math
import uuid
import json
from PIL import Image

from tickers import TickerData
from rgbmatrix import graphics
# Import samplebase from parent directory 'samples'
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
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
        self.load_stocks()

    def init_fonts(self):
        self.font = graphics.Font()
        self.interrupt_font = graphics.Font()
        self.font.LoadFont("../../../../fonts/7x13.bdf")
        self.interrupt_font.LoadFont("./fonts/helvB18.bdf")

    def run(self):
        self.frame_buffer = self.matrix.CreateFrameCanvas()
        self.tickers = TickerData().tickers
        self.images = self.load_imgs()
        self.arrow_up = Image.open("./images/arrow_green.ppm").convert('RGB')
        self.arrow_down = Image.open("./images/arrow_red.ppm").convert('RGB')
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

    def init_colors(self):
        self.base_color = graphics.Color(255, 255, 255)
        self.up_color = graphics.Color(0, 255, 0)
        self.down_color = graphics.Color(255, 0, 0)
        self.interrupt_color = graphics.Color(255,0, 0)

    def update_interruption(self):
        self.clear_buffer_on_interruption()
        self.int_flag = False

    def clear_buffer_on_interruption(self):
        if self.clear_buffer_flag:
            self.frame_buffer.Clear()
            self.matrix.Fill(0, 0, 0)
            # draw init text
            txt_w = graphics.DrawText(self.frame_buffer, self.interrupt_font, 0, 24, self.interrupt_color, self.int_text)
            reps = self.get_reps(txt_w)
            print("reps", reps)
            if reps > 1:
                self.print_reps(reps, txt_w)
            else:
                self.frame_buffer.Clear()
                anchor=(self.matrix.width/2) - (txt_w/2)
                graphics.DrawText(self.frame_buffer, self.interrupt_font, anchor, 24, self.interrupt_color, self.int_text)
            self.frame_buffer = self.matrix.SwapOnVSync(self.frame_buffer)
            self.sleep_once(20)
            self.clear_buffer_flag = False

    def get_reps(self, txt_w):
        space_avail = self.matrix.width - txt_w 
        min_margin = 10
        reps = 0
        while (space_avail - min_margin) > txt_w:
            reps += 1
            space_avail = space_avail/2
        return reps

    def print_reps(self, reps, txt_w):
        space_avail = self.matrix.width - txt_w
        increment = (space_avail/reps) + txt_w
        anchor = increment
        for rep in range(0,reps):
            print("rep", rep)
            graphics.DrawText(self.frame_buffer, self.interrupt_font, anchor, 24, self.interrupt_color, self.int_text)
            anchor += increment

    # how many copies
    def get_repetition_count(self, txt_width):
        count = 0
        min_total_margin = 500
        total_text_width = txt_width * count
        total_margin = self.matrix.width - total_text_width
        while total_margin > min_total_margin:
            total_text_width = txt_width * count
            total_margin = self.matrix.width - total_text_width
            count += 1

        # serve at least one
        if count == 0:
            count = 1

        return {count: count, total_margin: total_margin}

    def sleep_once(self, t):
        if self.sleep_once_flag:
            sleep(t)
            self.sleep_once_flag = False

    def load_imgs(self):
        img_dict = {}
        for t in self.tickers:
            image = Image.open(t["image_path"]).convert('RGB')
            t_name = t["name"]
            img_dict[t_name] = image
        return img_dict

    def new_ticker(self, index):
        return Ticker(id=uuid.uuid1(), name=self.tickers[index]["name"], pos=self.frame_buffer.width)

    def interrupt(self, text):
        self.int_text = text
        self.max_brightness = self.matrix.brightness
        self.int_flag = True
        self.sleep_once_flag = True
        self.clear_buffer_flag = True

    def load_stocks(self):
            try:
                with open('stock_data.json') as json_file:
                    self.stock_data = json.load(json_file)
                    print("Updated stock data OK")
            except Exception as e: 
                print(e)
                print("Error updating stock data")
                self.stock_data = None

    def get_ticker_fields_from_data(self, name):
        temp_text = "wait"
        try:
            ticker_data = self.stock_data[name]
            volume = str(ticker_data["regularMarketVolume"]["fmt"])
            price = str(ticker_data["regularMarketPrice"]["fmt"])
            change = str(ticker_data["regularMarketChangePercent"]["fmt"])
            change_raw = float(ticker_data["regularMarketChangePercent"]["raw"])  
        except Exception as e: 
            print(e)
            volume = temp_text
            price = temp_text
            change = temp_text
            change_raw = 0
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
            # print("change_raw",change_raw)
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
            # if change_raw != 0: # no arrow when change is zero
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
    if (not scroller.process()):
        scroller.print_help()
