# Bloko's ticker scroller display

Version yFinance para obra Pedro Engel. Runs in two separate services, one for yfinance and the other for the scroller app.py

## Install scroller service

- Find sample file in `/samples/bloko.service`
- Copy and paste the file to: `/lib/systemd/system/`

## Install data service

- Find sample file in `/samples/bloko-data.service`
- Copy and paste the file to: `/lib/systemd/system/`

### Handy commands

- Check service status: `$ systemctl status bloko.service`
- Reload daemons: `$ sudo systemctl daemon-reload`
- Restart service `$ sudo systemctl restart bloko.service`
- Stop: `$ service bloko stop`
- Enable service on boot: `$ sudo systemctl enable bloko.service`

- Check service status: `$ systemctl status bloko-data.service`
- Reload daemons: `$ sudo systemctl daemon-reload`
- Restart service `$ sudo systemctl restart bloko-data.service`
- Stop: `$ service bloko stop`
- Enable service on boot: `$ sudo systemctl enable bloko-data.service`
