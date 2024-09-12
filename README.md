# Bloko's ticker scroller display

Version yFinance para obra Pedro Engel

## Autostart setup: Ticker Scroller display

- Shh into the pi: `$ ssh pi@raspberrypi.local`
- Create unit file: `$ sudo nano /lib/systemd/system/bloko.service`
- Add this to the file:

```bash
[Unit]
Description=Bloko ticker scroller daemon
After=multi-user.target

[Service]
WorkingDirectory=/home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/
ExecStart=/usr/bin/python3 /home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/app.py --led-cols=640 --led-slowdown=2 --led-gpio-mapping=adafruit-hat

[Install]
WantedBy=multi-user.target
```

- Reload daemons: `$ sudo systemctl daemon-reload`
- Enable service on boot: `$ sudo systemctl enable bloko.service`
- Reboot: `$ sudo reboot`

## Autostart setup: Async-yfinance

- Shh into the pi: `$ ssh pi@raspberrypi.local`
- Create unit file: `$ sudo nano /lib/systemd/system/yfinance.service`
- Add this to the file:

```bash
[Unit]
Description=Bloko ticker yfinance daemon
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/
ExecStart=/usr/bin/python3 /home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/async-finance.py

[Install]
WantedBy=multi-user.target
```

- Reload daemons: `$ sudo systemctl daemon-reload`
- Enable service on boot: `$ sudo systemctl enable bloko.service`
- Reboot: `$ sudo reboot`

## Check that daemon is running

- Run: `$ systemctl status bloko.service`
