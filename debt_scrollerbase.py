import sys
import os
import time
from dataclasses import dataclass
from datetime import datetime
import math
import uuid
import json
from PIL import Image

from tickers import TickerData
from countries import CountryData
from rgbmatrix import graphics
# Import samplebase from parent directory 'samples'
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from samplebase import SampleBase

@dataclass
class Ticker:
    id: str # used internally of each active ticker
    name: str
    code: str
    pos: str = 40
    width: int = 0

class DebtScroller(SampleBase):
    def __init__(self):
        super(DebtScroller, self).__init__()
        self.int_flag = False
        self.debt_preds_data = read_forecast_file()
        self.gdp_data = read_gdp_file()
        self.dates_in_data = self.debt_preds_data.keys()
        # self.load_stocks()

    def init_fonts(self):
        self.font = graphics.Font()
        self.interrupt_font = graphics.Font()
        self.font.LoadFont("../../../../fonts/7x13.bdf")
        self.interrupt_font.LoadFont("./fonts/helvB18.bdf")

    def filter_countries(self,countries):
        # get available countries in dataset
        # assumes dataset items have been sorted beforehand
        latest_item = list(self.debt_preds_data.keys())[0]
        avail_countries = list(self.debt_preds_data[latest_item].keys())
        filtered = []
        for c in countries:
            if c["name"] in avail_countries:
                filtered.append(c)
        return filtered

    def run(self):
        self.frame_buffer = self.matrix.CreateFrameCanvas()
        self.tickers = CountryData().countries
        # filter to make sure countries in tickers are available in dataset
        self.tickers = self.filter_countries(self.tickers)
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
            print("reps:", reps, "text width:",txt_w, "screen width:", self.matrix.width)
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
        while space_avail > (txt_w + min_margin):
            reps += 1
            space_avail = space_avail - (txt_w + min_margin)
        return reps
    
    def print_reps(self, reps, txt_w):
        #space_avail = self.matrix.width - txt_w
        increment = math.floor(self.matrix.width / (reps + 1))
        anchor = increment
        print("increment", increment)
        for rep in range(0, reps):
            print("printing rep:", rep, "at anchor:", anchor)
            graphics.DrawText(self.frame_buffer, self.interrupt_font, anchor, 24, self.interrupt_color, self.int_text)
            anchor += increment

    def sleep_once(self, t):
        if self.sleep_once_flag:
            time.sleep(t)
            self.sleep_once_flag = False

    def load_imgs(self):
        img_dict = {}
        for t in self.tickers:
            image = Image.open(t["image_path"]).convert('RGB')
            t_name = t["name"] # should use country code here
            img_dict[t_name] = image
        return img_dict

    def new_ticker(self, index):
        # get a ticker from tickers and add to active tickers
        return Ticker(id=uuid.uuid1(), name=self.tickers[index]["name"], pos=0, code=self.tickers[index]["code"] )

    def interrupt(self, text):
        self.int_text = text
        self.max_brightness = self.matrix.brightness
        self.int_flag = True
        self.sleep_once_flag = True
        self.clear_buffer_flag = True

    def get_country_debt_and_gdp(self, country_name):
        now = math.floor(time.time()*1000) # epoch
        min_date, max_date = get_date_range(now, self.dates_in_data)

        if min_date and max_date:
            min_date_debt = self.debt_preds_data[str(min_date)][country_name]
            max_date_debt = self.debt_preds_data[str(max_date)][country_name]
            
            # get debt for current time and gdp
            debt_now = interpolate_vals(now, min_date, min_date_debt, max_date, max_date_debt)    
            gdp = get_gdp(country_name, self.gdp_data)
            
            return (debt_now, gdp)
        else:
            print("No data available in debt_predictions.json that matches the current time.")

    def update_tickers(self):
        self.frame_buffer.Clear()
        for ticker in self.active_tickers:
            # get data
            t_name = ticker.name
            t_code = ticker.code
            t_pos = ticker.pos
            t_image = self.images[t_name]
            img_w, img_h = t_image.size

            ########### MAKE THIS A FUNCTION
    
            # get proyected debt and gdp for current country in the scroller
            debt, gdp = self.get_country_debt_and_gdp(t_name)
            gdp_perc = (debt/gdp)*100
            
            # format strings
            debt_str = "${:,.2f}".format(debt)
            gdp_str = "%" + str(truncate(gdp_perc))
            
            # resize fix
            #t_image = t_image.resize((46,30))
            #self.frame_buffer.SetImage(t_image, t_pos,1)
            # compose frame
            self.frame_buffer.SetImage(t_image, t_pos)
            base_margin = 4
            first_line_h = 15
            second_line_h = 26
            left_margin = 4
            right_margin = 12
            text_base_pos = t_pos + img_w + left_margin
            title_w = graphics.DrawText(self.frame_buffer, self.font, text_base_pos, first_line_h, self.base_color, t_code)
            debt_pos = text_base_pos
            debt_w = graphics.DrawText(self.frame_buffer, self.font, debt_pos, second_line_h, self.up_color, debt_str)
            gdp_pos = text_base_pos + base_margin + title_w + base_margin 
            gdp_w = graphics.DrawText(self.frame_buffer, self.font, gdp_pos, first_line_h, self.down_color, gdp_str)
            line_top_w = title_w
            line_bottom_w = debt_w + base_margin + base_margin + gdp_w
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
            #ticker.pos -= 1

        # update screen
        self.frame_buffer = self.matrix.SwapOnVSync(self.frame_buffer)


# country, debt-related functions

def truncate(num):
    return int(num * 10) / 10

def datetime_dict(data):
    dt_data = {}
    for key in data.keys():
        dt = datetime.fromtimestamp(int(key)/1000)
        dt_data[dt] = data[key]
    return dt_data

def epoch_to_datetime(epoch):
    return datetime.fromtimestamp(int(epoch)/1000)

def interpolate_vals(x, x1, y1, x2, y2):
    out = y1 + (x - x1) * ((y2 - y1) / (x2 - x1))
    return out

def read_forecast_file():
    f = open('debt_predictions.json')
    debt_preds_data = json.load(f)
    f.close()
    return debt_preds_data

def read_gdp_file():
    f = open('gdp.json')
    #print(f.read())
    gdp_data = json.load(f)
    gdp_data = json.loads(gdp_data)
    f.close()
    return gdp_data

def get_country_list(debt_preds_data):
    # assumes items have been sorted beforehand
    latest_item = list(debt_preds_data.keys())[0]
    return list(debt_preds_data[latest_item].keys())

def get_date_range(now, dates_in_data):
    """Returns the date range within the provided date ranges('dates_in_data') with respect to 'now '
    For instance: if now: 2022-6-2 then ranges should be min_date: 2022-1-1, max_date: 2023-1-1. As long as these dates can be found in the data."""
    before = []
    after = []
    for d in dates_in_data:
        current_date = int(d)
        if current_date > now:
            after.append(current_date)
        if current_date < now:
            before.append(current_date)

    if after:
        max_date = min(after)
    else:
        max_date = None

    if before:
        min_date = max(before)
    else: 
        min_date = None

    return (min_date, max_date)

def get_gdp(country_name,gdp_data):
    time_key = list(gdp_data.keys())[0]
    return gdp_data[time_key][country_name]

if __name__ == "__main__":
    scroller = DebtScroller()
    if (not scroller.process()):
        scroller.print_help()
