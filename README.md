# Bloko's ticker scroller display

Version yFinance para obra Pedro Engel. Runs in two separate services, one for yfinance and the other for the scroller app.py

## Install scroller service

- Create unit file: `$ sudo nano /lib/systemd/system/bloko.service`
- Add this to the file:

```bash
[Unit]
Description=Bloko ticker scroller daemon
After=multi-user.target

[Service]
WorkingDirectory=/home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/
ExecStart=/home/pi/rpi-rgb-led-matrix/bindings/python/samples/bloko/run_scroller_app.sh

[Install]
WantedBy=multi-user.target
```

### Handy commands

- Check service status: `$ systemctl status bloko.service`
- Reload daemons: `$ sudo systemctl daemon-reload`
- Restart service `$ sudo systemctl restart bloko.service`
- Stop: `$ service bloko stop`
- Enable service on boot: `$ sudo systemctl enable bloko.service`

## Install yfinance service

### yfinance requires a virtual env to run

- Create a new env: `python3 -m venv yfinance_env`
- Activate env: `source yfinance_env/bin/activate`
- Install yfinance: `pip install yfinance`
- Test: `python async_finance.py`

### Autostart

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

### Handy commands

- Check service status: `$ systemctl status yfinance.service`
- Reload daemons: `$ sudo systemctl daemon-reload`
- Restart service `$ sudo systemctl restart yfinance.service`
- Stop: `$ service yfinance stop`
- Enable service on boot: `$ sudo systemctl enable yfinance.service`
