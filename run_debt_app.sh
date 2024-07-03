#!/bin/bash
source /home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/yfinance_env/bin/activate
exec python /home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/app.py --led-cols=768 --led-slowdown=5 --led-gpio-mapping=regular --led-rows=32 --led-chain=1 --led-pixel-mapper=V-mapper  --led-parallel=2 --led-brightness=70
