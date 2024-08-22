# yfinance fix

Acuerdate que la branch donde está el fix de yfinance se llama yfinancefix

Para cambiarte a esa branch tienes q poner:

`git fetch`

`git switch yfinancefix`

`git pull`

## Para instalar yfinance en la raspi

- Update system packages: `sudo apt-get update`
- Install OpenBLAS and other dependencies: `sudo apt-get install libopenblas-dev libatlas-base-dev`
- Install virtual env: `pip3 install virtualenv`
- Go to project directory `/bloko` and create a virtual environment: `python3 -m venv yfinance_env`
- Activate the virtual environment: `source yfinance_env/bin/activate`
- Reinstall numpy: `pip install --no-cache-dir --force-reinstall numpy`
