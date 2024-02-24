# This web page to manage chronically sick people. 
A sick person suffers from hypertension and/or diabetes. 
This system helps to improve the monitoring of sick people, and manage their 
- attentions,
- electrocardiograms in hypertensive people,
- foot cheek in diabetic people,
- references to a major hospital,
- Mosare,

- This web page was done using Django, python3, and SQLite

# Deploy on Apache2 in Ubuntu 20.04
## Steps
1. Install Apapche2
2. List out the project's folder and file's path.
3. Collect static files.
4. Migrate the database.
5. Change the permission and ownership of the database files and other folders.
6. Make changes in the Apache config file.
7. Enable the site.
8. Install WSGI mod in Apache2.
9. Restart the Apache Server.

## Step 1: Install Apache2
the folowing are the commands to install Apache2 on Ubuntu 20.04
```
sudo apt update
sudo apt install apache2
```
## Step 2: List out the project's folder/file path: 
It is important to list the following paths: 

> Directories

```
Folder name - /home/ubuntu/hospital/

Project name - cronicos
Project path - /home/ubuntu/hospital/cronicos

Application name - usuarios
Application path - /home/ubuntu/hospital/cronicos/usuarios/

Enviorment folder path - /home/ubuntu/hospita/hospital_env
Wsgi File Path - /home/ubuntu/hospital/cronicos/cronicos/wsgi.py
```
## Step 3: Collect Static Files
Django provides a mechanism for collecting static files into one place so that they can be served easily. 

Open the file Setting.py located in /hospital/cronicos/cronicos/settings.py:
```
# add the following code

import os 
STATIC_URL = '/static/' 
STATIC_ROOT = os.path.join(BASE_DIR, "static/") 
STATICFILES=[STATIC_ROOT]

```
Activate the source and collect the statics files using the following commands

```
source hospita/hospital_env/bin/activate
python3 hospital/cronicos/manage.py collectstatic
```

## Step 4: Migrate the database
Migrate the database using the MakeMigration and Migrate command:
```
python3 hospital/cronicos/manage.py makemigrations
python3 hospital/cronicos/manage.py migrate
```
## Step 5: Change permission and ownership
If you are using a SQLite database, then change the permissions of the SQLite file. Also, change the ownership of the Django project folders.

The following commands will change the permission and ownership of the files and folders.
```
chmod 664 /hospital/cronicos/cronicos/db.sqlite3
sudo chown :www-data /hospital/cronicos/db.sqlite3
sudo chown :www-data /hospital/cronicos/
sudo chown :www-data /hospital/cronicos/cronicos
```
## Step 6: Changes in Apache2 config file
We need to make a few changes in the 000-default.conf file. Before that, though, make backup of the file. The following are the commands to open the file and create backup of the file.

```
# Go to the location - 
cd /etc/apache2/sites-available

# Take a backup of file
sudo cp 000-default.conf 000-default.conf_backup

# Open conf file using Vi
sudo vi 000-default.conf

```
Add the below code to the file
```
Alias /static /home/ubuntu/hospital/cronicos/cronicos/static
        <Directory /home/ubuntu/hospital/cronicos/cronicos/static>
            Require all granted
        </Directory>
        <Directory /home/ubuntu/hospital/cronicos/cronicos/cronicos>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>
        WSGIPassAuthorization On
        WSGIDaemonProcess DemoProject python-path=/home/ubuntu/hospital/cronicos/cronicos python-home=/home/ubuntu/hospital/hospital_env
        WSGIProcessGroup DemoProject
        WSGIScriptAlias / /home/ubuntu/hospital/cronicos/cronicos/cronicos/wsgi.py
```
After adding the above snippet, the config fiel will look like this: 
```
<VirtualHost *:80>
	# The ServerName directive sets the request scheme, hostname and port that
	# the server uses to identify itself. This is used when creating
	# redirection URLs. In the context of virtual hosts, the ServerName
	# specifies what hostname must appear in the request's Host: header to
	# match this virtual host. For the default virtual host (this file) this
	# value is not decisive as it is used as a last resort host regardless.
	# However, you must set it for any further virtual host explicitly.
	#ServerName www.example.com

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
	# error, crit, alert, emerg.
	# It is also possible to configure the loglevel for particular
	# modules, e.g.
	#LogLevel info ssl:warn

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	# For most configuration files from conf-available/, which are
	# enabled or disabled at a global level, it is possible to
	# include a line for only one particular virtual host. For example the
	# following line enables the CGI configuration for this host only
	# after it has been globally disabled with "a2disconf".
	#Include conf-available/serve-cgi-bin.conf
	
	Alias /static /home/ubuntu/hospital/cronicos/cronicos/static
        <Directory /home/ubuntu/hospital/cronicos/cronicos/static>
            Require all granted
        </Directory>
        <Directory /home/ubuntu/hospital/cronicos/cronicos/cronicos>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>
        WSGIPassAuthorization On
        WSGIDaemonProcess DemoProject python-path=/home/ubuntu/hospital/cronicos/cronicos python-home=/home/ubuntu/hospital/hospital_env
        WSGIProcessGroup DemoProject
        WSGIScriptAlias / /home/ubuntu/hospital/cronicos/cronicos/cronicos/wsgi.py
</VirtualHost>
```

## Step 7: Enable the site
Now enable the above conf file using the a2ensite command.
```
cd /etc/apache2/sites-available/
sudo a2ensite 000-default.conf
```
## Step 8: Install WSGI mod in Apache2
Install the WSGI mod library for the Apache 2 server using the following command. After installation, enable the WSGI.
```
sudo apt-get install libapache2-mod-wsgi-py3
sudo a2enmod wsgi
```
## Step 9: Restart the Apache server
Restart the Apache server using the following command:
```
sudo service apache2 restart
```
And the webpage is done! :tada:

# Deploy on pythonanywhere.com

## Steps
1. steps on Consoles' tab
2. steps on Web App's tab
3. Database setup

## Steps on Consoles' tab
- First, we create a new console, and on it,
```
# Download the git project
git clone https://github.com/reynaldocv/cronicos.git
# Create a environment
mkvirtualenv hospital_env --python=/usr/bin/python3.8
# Install Django
pip install django
```
## Steps on Web App's tab
Create a Web app with Manual Config
Head over to the Web tab and create a new web app, choosing the "Manual Configuration" option and the right version of Python (the same one you used to create your virtualenv).
<p align="center">
  <img src="/imgs/django.png">
</p>

Configuring the environment part:

<p align="center">
  <img src="/imgs/env.png">
</p>

Configuring the code part:

<p align="center">
  <img src="/imgs/code.png">
</p>

Configuring the wsgi.py file. 

<p align="center">
  <img src="/imgs/wsgi.png">
</p>

Configuring the static file part:

<p align="center">
  <img src="/imgs/static.png">
</p>

## Database setup 

Go back to console and we execute the following commands: 

```
source .virtualenvs/hospital_env/bin/activate
cd cronicos/cronicos/

# Generate database
python3 manage.py migrate

# Generate the statics files
python3 manage.py collectstatic

```
> [!IMPORTANT]
> 
Modify the parameter ALLOWED HOST to add our URL, in settings.py file: 
```
ALLOWED_HOSTS = ['192.168.1.12', "localhost", "127.0.0.1","**reynaldocv.pythonanywhere.com**"]
```

Now, you are done! :tada:
