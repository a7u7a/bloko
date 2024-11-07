#!/bin/bash
exec python3 /home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/src/ticker_scroller.py --led-cols=64 #devkit
#exec python3 /home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/src/ticker_scroller.py --led-cols=768 --led-slowdown=5 --led-gpio-mapping=regular --led-rows=32 --led-chain=1 --led-pixel-mapper=V-mapper  --led-parallel=2 --led-brightness=70