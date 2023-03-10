# 2023_Scouter
Repo for 2023 Charged Up Scouting Application

Application is written in Python with Django as the ORM back end.

Requires installing the latest release of Django, Python3, and their relevant dependencies.

1. Install a virtual environment -- pip install venv
1. Create a virtual environment directory on your system -- python3 -m venv .venv
1. Activate your virtual environment -- source ./.venv/bin/activate
1. Install the scouting app dependencies -- pip install -r requirements.txt
1. Get to work!


# Configuring your local environment once you have the code checked out

1. Create the database migrationss, this sets up the database structure -- python3 scouter/manage.py makemigrations
1. Apply the new database schema -- python3 scouter/manage.py migrate
1. Create the database admin user -- python scouter/manage.py createsuperuser
1. Enter the admin username, give some email address, and type the password