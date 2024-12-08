# Sociale Sportschool

This repository contains the source code of
https://www.socialesportschool.nl/, provided here under the
[GPLv3](LICENSE) license as part of our free and open source
philosophy.

A former version of this website has been archived on
https://socialesportschool.created.today/

## Installation

Install Python and run the following commands:

    pip install -r requirements.txt
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver

## Usage

Visit https://localhost:8000/admin/bootcamps/bootcamp/ to start adding
bootcamps.
