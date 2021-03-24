# QartNLP - Web Service
<p align="center">
  <img 
        width="460"
        src="https://i.ibb.co/x55NgfZ/logo.png"
    >


<br/>
<img alt="Unilab" src="https://img.shields.io/badge/Unilab-2021-orange?style=for-the-badge"/>
<img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>
<img alt="Flask" src="https://img.shields.io/badge/flask%20-%23000.svg?&style=for-the-badge&logo=flask&logoColor=white"/>
<br/>
<img alt="contributors" src="https://img.shields.io/github/contributors/temurchichua/QartNLPWebService?style=for-the-badge"/>
<img alt="commits" src="https://img.shields.io/github/commit-activity/w/temurchichua/QartNLPWebService?style=for-the-badge"/>
</p>

## Branch Structure

main branches: `deploy` | `development` 

temporary branches: `front` | `back` [ from `development`]

- `deploy` - stable branch
- `development` - working branch
- `front` - workspace for front-end division
- `back` - workspace for back-end division

### pull request
All the pull requests are sent to your `division` branch.  
When creating new branch, always use the structure of the branch anatomy.

branch anatomy: `division`/`type`/`title`

divisions: `front` | `back`

`division` branch is synced to the `development` branch once a week.

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