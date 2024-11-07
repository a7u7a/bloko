# Bloko's ticker scroller display

- This software was developed for my friend Ignacio Gatica's art project called "Stones Above Diamonds"
- It's job is to control an LED display, similar to the ones seen on financial districts. Here is a picture of it in action at [Hessel Museum of Art](https://ccs.bard.edu/museum):
![Stones Above Diamonds by Ignacio Gatica](expo.jpeg)

### Install
- This software is meant to run on a Raspberry Pi running Raspberry Pi OS. Tested on Raspberry Pi OS Lite Kernel version: 5.10, Debian version: 11 (bullseye)
- Requires Python version 3.7 at least, tested on 3.9
- Requires internet connection in order to update ticker values
- For the ticker display: 
  - You must first install this: https://github.com/hzeller/rpi-rgb-led-matrix
  - Make sure Python 3 bindings are correctly installed by running some samples 
  - Then clone this repo inside `bindings/python/samples` folder
  - Only then you should try to run the ticker

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
- Enable service on boot: `$ sudo systemctl enable bloko.service