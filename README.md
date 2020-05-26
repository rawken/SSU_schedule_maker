# SSU scheduler

This script makes schedule of specified SSU faculty and group and sends it to your Google Calendar

## Installation

### Linux

First of all, install [pip3](https://pip.pypa.io/en/stable/).

```
sudo apt update
sudo apt install python3-pip
```

Next, install [virtualenv](https://virtualenv.pypa.io/en/latest/) using pip. virtualenv is a tool to
create isolated Python environments.

```
pip3 install virtualenv
```

Then, create virtual environment in your working directory using virtualenv:

```
virtualenv ssu_scheduler
source ./ssu_scheduler/bin/activate
```

After activating your virtualenv, install all required Google libraries, using requirements.txt:

```
pip3 install -r /path/to/requirements.txt
```

### Windows

Go to https://www.python.org/downloads/release/ and select any stable python 3 release (for example https://www.python.org/downloads/release/python-383/). Download it and install it on your computer.

Then open cmd with same user as user that you use installer for. Type:
```
pip3 install -r C:\path\to\requirements.xtx
```

After that, you're ready to use script.

## Usage

### Linux

To run script use next template:

```
python3 ssu_scheduler.py -f <faculty_name> -g <group_number>
```

Full list of proper faculty names will be available soon.

### Windows

To run script use next template:

```
py ssu_scheduler.py -f <faculty_name> -g <group_number>
```

## Example

```
python3 ssu_scheduler.py -f knt -g 321
```
