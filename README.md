# Bloko's ticker display

### Install
- This software is meant to run on a Raspberry Pi running Raspberry Pi OS. Tested on Raspberry Pi OS Lite Kernel version: 5.10, Debian version: 11 (bullseye)
- Requires Python 3.7
- For the ticker display: 
  - You must first install this: https://github.com/hzeller/rpi-rgb-led-matrix
  - Make sure Python 3 bindings are correctly installed by running some samples 
  - Then clone this repo inside bindings/python/samples folder
  - Only then you should attempt running the ticker
- For the swiper:
  - Simply clone this repo inside the home directory
  - You will need a card reader that is compatible with the keyboard module: https://pypi.org/project/keyboard/


### Setup
- Run `chmod -R 777 ./` to give folder privileges and avoid permission errors using while using `sudo`.

### Start ticker scroller
- Run with sudo `sudo python app.py --led-cols=64`

### Start card swiper kiosk
- Run `sudo python kiosk.py`

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
WorkingDirectory=/home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/
ExecStart=/usr/bin/python3 /home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/kiosk.py

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
