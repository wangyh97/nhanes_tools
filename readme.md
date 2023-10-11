## Directory
- [Features](#features)
- [Requirements](#requirements) 
- [Installation](#installation)
- [Usage](#usage)

## Features
- automatic download all xpt files in NHANES project from 1999-2018
## Requirements
List requirements for using the project
- requests==2.31.0
- beautifulsoup4==4.12.2
## Installation
```
git clone git@github.com:wangyh97/nhanes_tools.git
```

## Usage
make sure you have already installed the requirements properly in your venv, run
```
python download_data.py
```
downloaded file will be arranged as following:

- [*root]
  - [data]  
    - [1999-2000]
        - [Demographics data]
            - [DEMO.XPT]
        - [Dietary data]
            - [DRXFMT.XPT]
            - [DRXST.XPT]
            - [...]
    - [2001-2002]
    - [2003-2004]
    - [...]
  - [download_data.py]
  - [README.md]
