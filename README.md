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
ExecStart=/home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/run_debt_app.sh

[Install]
WantedBy=multi-user.target
```

- Reload daemons: `$ sudo systemctl daemon-reload`
- Enable service on boot: `$ sudo systemctl enable bloko.service`
- Reboot: `$ sudo reboot`

## Autostart setup: Async-yfinance

- Create a new env: `python3 -m venv yfinance_env`
- Activate env: `source yfinance_env/bin/activate`

- Install yfinance and make sure it runs: 
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
ExecStart=/home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/run_yfinance_app.sh

[Install]
WantedBy=multi-user.target
```

- Reload daemons: `$ sudo systemctl daemon-reload`
- Enable service on boot: `$ sudo systemctl enable yfinance.service`
- Reboot: `$ sudo reboot`

## Check that daemon is running

- Run: `$ systemctl status yfinance.service`
