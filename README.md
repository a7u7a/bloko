**Development branch for the international debt project**

- Notes: in order for this to work both `debt_predictions.json` and `gdp.json` must be compatible by having the same countries and matching dates. Both `.json` files were generated using [this](https://github.com/a7u7a/blokis-intl-debt)
- Debt scroller app is run with: `sudo python debt_app.py --led-cols=64`


# Bloko's ticker scroller display

- This software was developed for my friend Ignacio Gatica's art project called "Stones Above Diamonds"
- It's job is to control an LED display, similar to the ones seen on financial districts. Here is a picture of it in action at [Hessel Museum of Art](https://ccs.bard.edu/museum):
![Stones Above Diamonds by Ignacio Gatica](expo.jpeg)


### Install
- This software is meant to run on a Raspberry Pi running Raspberry Pi OS. Tested on Raspberry Pi OS Lite Kernel version: 5.10, Debian version: 11 (bullseye)
- Requires Python version 3.7 at least, tested on 3.9
- Requires internet connection in order to update ticker values
- Connects to Yahoo Finance web API. No `yfinance` module required
- For the ticker display: 
  - You must first install this: https://github.com/hzeller/rpi-rgb-led-matrix
  - Make sure Python 3 bindings are correctly installed by running some samples 
  - Then clone this repo inside `bindings/python/samples` folder
  - Only then you should try to run the ticker
- For the swiper:
  - Simply clone this repo inside the home directory
  - You will need a card reader that is compatible with the keyboard module: https://pypi.org/project/keyboard/


### Setup
- Run `chmod -R 777 ./` to give folder privileges and avoid permission errors using while using `sudo`.

### Test the ticker 
- Most basic command to test ticker on a 1x2 arrangement of 32x32 pixel: `sudo python app.py --led-cols=64`

### Start ticker scroller
- Run using sudo (required by `rpi-rgb-led-matrix` python bindings)
```
sudo python app.py app.py --led-cols=768 --led-slowdown-gpio=5 --led-gpio-mapping=regular  --led-rows=32 --led-chain=1 --led-pixel-mapper=V-mapper  --led-parallel=2 --led-brightness=70
```

### Start card swiper kiosk
- Also needs to run with sudo, required by the `keyboard` module: `sudo python kiosk.py`

### Test card interruption without kiosk
- Run `python interrupt_test.py`

### Autostart setup: Scroller Ticker display
- Shh into the pi: `$ ssh pi@raspberrypi.local`
- Create unit file: `$ sudo nano /lib/systemd/system/bloko.service`
- Add this to the file: 
```
[Unit]
Description=Bloko ticker display daemon
After=multi-user.target

[Service]
WorkingDirectory=/home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/
ExecStart=/usr/bin/python3 /home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/app.py --led-cols=768 --led-slowdown-gpio=5 --led-gpio-mapping=regular  --led-rows=32 --led-chain=1 --led-pixel-mapper=V-mapper  --led-parallel=2 --led-brightness=70

[Install]
WantedBy=multi-user.target
```
- Reload daemons: `$ sudo systemctl daemon-reload`
- Enable service on boot: `$ sudo systemctl enable bloko.service`
- Reboot: `$ sudo reboot`

### Autostart setup: Swiper Kiosk
- Shh into the pi: `$ ssh pi@raspberrypi.local`
- Create unit file: `$ sudo nano /lib/systemd/system/bloko_swiper.service`
- Add this to the file: 
```
[Unit]
Description=Bloko ticker display daemon
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/bloko/kiosk.py

[Install]
WantedBy=multi-user.target
```
- Reload daemons: `$ sudo systemctl daemon-reload`
- Enable service on boot: `$ sudo systemctl enable bloko_swiper.service`
- Reboot: `$ sudo reboot`


### Check that daemon is running: 
- Run: `$ systemctl status bloko.service`
- Output should be like: 
```
pi@raspberrypi:~ $ systemctl status bloko.service
● bloko.service - Bloko ticker display daemon
     Loaded: loaded (/lib/systemd/system/bloko.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2022-03-05 00:13:22 GMT; 10min ago
   Main PID: 955 (python3)
      Tasks: 7 (limit: 1597)
        CPU: 8min 32.862s
     CGroup: /system.slice/bloko.service
             └─955 /usr/bin/python3 /home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/app.py --led-cols=768...

Mar 05 00:13:22 raspberrypi systemd[1]: Started Bloko ticker display daemon.
Mar 05 00:13:24 raspberrypi python3[955]: Suggestion: to slightly improve display update, add
Mar 05 00:13:24 raspberrypi python3[955]:         isolcpus=3
Mar 05 00:13:24 raspberrypi python3[955]: at the end of /boot/cmdline.txt and reboot (see README.md)
```
### Stop daemon
- Run `$ service bloko stop`
