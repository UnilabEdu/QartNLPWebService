# QartNLP - Web Service
![](https://img.shields.io/github/v/release/temurchichua/QartNLPWebService)
![](https://img.shields.io/github/pipenv/locked/python-version/temurchichua/QartNLPWebService)


## Setup & Run
To make the project run on your device you need have [Python 3.x installed](https://realpython.com/installing-python/).

### virtualenv
It's highly recommended to use virtual environments while working on the project. 
To set up the environment we will be using [venv](https://realpython.com/python-virtual-environments-a-primer/) module.

#### set up
Setting up virtual environment is a one time process. To set up the environment use the following command:
```bash
python -m venv env
```
It will create the virtual environment in your computer named `env` at the `env` directory.

#### activate
Before you can start installing or using packages in your virtual environment you’ll need to activate it
On macOS and Linux:
```bash
source env/bin/activate
```

On Windows:

```bash
.\env\Scripts\activate
```
#### deactivate
If you want to switch projects or otherwise leave your virtual environment, simply run:
```bash
deactivate
```

### Installing the Requirements
Project is built using Python web framework - Flask.
Flask and all the other dependency modules can be installed from the commandline using `pip` manager:

```bash
pip install -r requirements.txt
```

### Run 
activate the environment and run the following command:
```bash
python app.py
```

## used modules
-   [Flask](http://flask.pocoo.org/) & [Werkzeug](Werkzeug) — base for everything.