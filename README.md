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
sourde hospita/hospital_env/bin/activate
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
And the webpage is done!






# Deploy on pythonanywhere.com










- [x] #739
- [ ] https://github.com/octo-org/octo-repo/issues/740
- [ ] Add delight to the experience when all tasks are complete :tada:

- Visão geral do projeto: 

    O projeto consiste em saber se tem vagas (ou não) num estacionamento. 

    A projeto a discutir, pode ajudar às pessoas a saber onde eles podem estacionar seu veiculo (no momento), e
fazer uma estimativa a futuro se no estacionamento.


<p align="center">
  <img height="200" src="/img/img_car.jpeg">    
   
</p>


# Descrição técnica
  
- RASPBERRY PI 3 MODEL B: É um computador de baixo custo e que tem o tamanho de um cartão de crédito desenvolvido no Reino Unido pela Fundação Raspberry Pi. Para usá-lo, basta plugar um teclado e um mouse padrão a ele e conectar tudo isso a um monitor ou a uma televisão. Os modelos custam entre US$ 25 e US$ 35.

<p align="center">
  <img src="/img/Raspberry.png">
</p>


      - Especificações:      
        - A 1.2GHz 64-bit quad-core ARMv8 CPU
        - 802.11n Wireless LAN
        - Bluetooth 4.1 & Bluetooth Low Energy (BLE)
        - BCM2837, 1.2GHz 64-bit quad-core ARM Cortex-A53
        - 1GB RAM
        - 10/100 Ethernet port
        - 802.11n WiFi NIC
        - Bluetooth 4.1 & Bluetooth Low Energy (BLE)
        - HDMI port
        - USB 2.0 interface x 4
        - Micro SD card slot
        - Combined 3.5mm audio jack and composite video
        - 40-pin GPIO interface
        - Camera interface (CSI)
        - Display interface (DSI)
        - Upgraded power management
        - supports more peripherals (requires a 2.5A - 3.0A power supply)Tensão de Alimentação:  4-30V;
        
 - 2 Câmeras: Usamos dois tipos: uma de um celular e outra com conexão USB  

        - Camera Multilaser WC040
  <p align="center">
  <img height="200" src="/IoT project - slides/img/slide_cam1.jpeg">  
  </p>
    
        - Celular LG G3
    
  <p align="center">  
  <img height="200" src="/IoT project - slides/img/slide_cam2.jpg">
  </p>      
        
## Open-design (extra)


<p align="center">
   <img height="500" src="/IoT project - slides/img/estrutura.jpeg">
</p>

# Instalação
- Em um dos celulares:
    
    - Instalamos o aplicativo IP Webcam e executamos. O aplicativo dá um IP (que pode ser acessado numa LAN) onde nós podemos monitorar usando qualquer navegador web (veja a seguiente pagina web https://pplware.sapo.pt/smartphones-tablets/android/ip-webcam-como-usar-o-seu-android-como-uma-webcam/ para mais dados).

- No Raspberry (deve estar na misma LAN do celular com o IP Webcam) o simplesmente conetados a uma câmera USB:
    
    - Executamos o seguinte [código em python](cod_raspberry/cam.py) que tira a fotoe que é subida num host (nesse caso foi https://www.ime.usp.br/~reynaldo/phd/internet_coisas/ e o processo acontece cada 60 seg.) além disso faz uma análise da imagem com o Computer Vision API - Azure, a informação gerada e salvada num json e num dataset do pythonanywhere. 
    
- No https://www.pythonanywhere.com/:
    
    - Criamos os seguintes APIs executando o seguinte [código em python](cod_pythonanywhere/app_flask.py) que tem comandos para fazer consultas na "API de Pesquisa de Visual Computational" (Veja as seguintes paginas web https://techtutorialsx.com/2016/12/27/python-anywhere-deploying-a-flask-server-on-the-cloud/ e https://azure.microsoft.com/pt-br/services/cognitive-services/computer-vision/ para mais dados). Os servicios criados foram:
        
        - http://reynaldocv.pythonanywhere.com/add/{text1}
        - http://reynaldocv.pythonanywhere.com/dataset/
        - http://reynaldocv.pythonanywhere.com/futuro/{dia}/{hora}/{minutos}
        
- No outro celular:

    - Instalamos o [Android APP](/cod_android/app_debug.apk) que foi fieto en Android Studio (java) usando as bibliotecas Picasso (mostrar imagens da web) e Retrofit (consumo de API services) (http://square.github.io/picasso/ e http://blog.matheuscastiglioni.com.br/consumindo-web-service-no-android-com-retrofit). O código do app está localizado em 
    [cod_android](/cod_android/).


# Descrição da arquitetura

O raspberry tira as imagens de um dos celulares que tem instalado do IP Webcam o pela câmera USB e joga na internet, faz 
uma análise da imagem com o Computer Vision API, e a informação gerada e salvada num json e num dataset do pythonanywhere. 

Com o outro celular, fazemos uso de um API service https://reynaldocv.pythonanywhere.com. esse servicio pega a imagem da internet e faz um análise con o API de Pesquisa em Visual Computational para saber a descricao da imagem. e no celular é so mostrar.

# Exemplo 1

 <p align="center">
     <img height="460" src="/IoT project - slides/img/app_foto_2.png">    
     <img height="460" src="/IoT project - slides/img/app_foto_1.png"> 
     <img height="460" src="/IoT project - slides/img/futuro_1.png"> 
    
 
</p>

# Exemplo com carrinhos
 <p align="center">
     <img height="460" src="/IoT project - slides/img/carrinho_1.png">    
     <img height="460" src="/IoT project - slides/img/carrinho_2.png"> 
     <img height="460" src="/IoT project - slides/img/carrinho_6.png"> 
    
 
</p>




