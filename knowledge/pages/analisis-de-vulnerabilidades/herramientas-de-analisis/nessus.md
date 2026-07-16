
# Nessus

**Nessus** es una herramienta ampliamente utilizada para el análisis de vulnerabilidades en sistemas informáticos. Fue creada por Tenable Inc. y se encuentra entre las herramientas más populares y fiables en el ámbito de la ciberseguridad. Nessus permite identificar, evaluar y gestionar vulnerabilidades en redes, sistemas operativos, aplicaciones y dispositivos conectados.

{% hint style="warning" %}
Es de pago, pero la versión free (Essentials) tiene un límite de 6 IPs, por lo que podemos utilizarlo en nuestras pruebas con fines no comerciales.
{% endhint %}

<figure><img src="/files/RfEC22Ugg0ZLaG8aldGW" alt=""><figcaption><p>Nessus Dashboard</p></figcaption></figure>

## <mark style="color:purple;">Instalación</mark>

Para utilizar Nessus en Kali Linux, sigue los siguientes pasos:

1. Descarga Nessus Essentials [<mark style="color:purple;">desde su sitio web</mark>](https://www.tenable.com/downloads/nessus?_gl=1*1kvy08y*_ga*MTgxMjY2ODQ0LjE3MzI2MDg5ODY.*_ga_HSJ1XWV6ND*MTczMjYwODk4NS4xLjAuMTczMjYwODk4NS42MC4xLjM0NTk5NDA3Mw..\&loginAttempted=true)<mark style="color:purple;">.</mark>
2. Descomprime el archivo tar.gz descargado utilizando el siguiente comando:

```bash
sudo dpkg -i Nessus-10.8.3-ubuntu1604_amd64.deb

[sudo] contraseña para kali: 
Seleccionando el paquete nessus previamente no seleccionado.
(Leyendo la base de datos ... 428847 ficheros o directorios instalados actualmente.)
Preparando para desempaquetar Nessus-10.8.3-ubuntu1604_amd64.deb ...
Desempaquetando nessus (10.8.3) ...
Configurando nessus (10.8.3) ...
HMAC : (Module_Integrity) : Pass
SHA1 : (KAT_Digest) : Pass
SHA2 : (KAT_Digest) : Pass
SHA3 : (KAT_Digest) : Pass
TDES : (KAT_Cipher) : Pass
AES_GCM : (KAT_Cipher) : Pass
<----SNIP---->
INSTALL PASSED
Unpacking Nessus Scanner Core Components...

 - You can start Nessus Scanner by typing /bin/systemctl start nessusd.service
 - Then go to https://kali:8834/ to configure your scanner
```

3. Inicia Nessus utilizando el siguiente comando:

```bash
/bin/systemctl start nessusd.service

==== AUTHENTICATING FOR org.freedesktop.systemd1.manage-units ====
Necesita autenticarse para iniciar «nessusd.service».
Authenticating as: kali,,, (kali)
Password: 
==== AUTHENTICATION COMPLETE ====
```

6. Abre un navegador web e ingresa la dirección "[https://localhost:8834](https://localhost:8834/)" para acceder a la interfaz web de Nessus.
7. Crea una cuenta de usuario y sigue las instrucciones para configurar Nessus.

<figure><img src="/files/ZdTAcrRzVv1sCpuRkOHR" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/KWQ0RILjvesfUsF7Oskt" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escaneo con Nessus</mark>

<figure><img src="/files/inldc7Hs5wuKkh2ZuoBK" alt=""><figcaption><p>Scan Templates</p></figcaption></figure>

* Elegimos el tipo de escaneo
* Definimos el target
* Configuramos las opciones
* Elegimos si queremos que se autentique contra servicios usando un `login:password`&#x20;

<figure><img src="/files/Nz8yjNAFTtYyjlLkVw5n" alt=""><figcaption><p>Listado de hosts</p></figcaption></figure>

<figure><img src="/files/CyDhmhBDyTxBwQmr2GlG" alt=""><figcaption><p>Vulnerabilidades encontradas</p></figcaption></figure>

## <mark style="color:purple;">Exportar escaneos de Nessus</mark>

Se pueden utilizar scripts como `nessus-report-downloader` para descargar rápidamente los resultados del análisis en todos los formatos disponibles desde la CLI mediante la API REST de Nessus:

{% embed url="<https://raw.githubusercontent.com/eelsivart/nessus-report-downloader/master/nessus6-report-downloader.rb>" %}

```shell-session
afsh4ck@kali$ ./nessus_downloader.rb 

Nessus 6 Report Downloader 1.0

Enter the Nessus Server IP: 127.0.0.1
Enter the Nessus Server Port [8834]: 8834
Enter your Nessus Username: admin
Enter your Nessus Password (will not echo): 

Getting report list...
Scan ID Name                                               Last Modified                  Status         
------- ----                                               -------------                  ------         
1     Windows_basic                                Aug 22, 2020 22:07 +00:00      completed      
         
Enter the report(s) your want to download (comma separate list) or 'all': 1

Choose File Type(s) to Download: 
[0] Nessus (No chapter selection)
[1] HTML
[2] PDF
[3] CSV (No chapter selection)
[4] DB (No chapter selection)
Enter the file type(s) you want to download (comma separate list) or 'all': 3

Path to save reports to (without trailing slash): /assessment_data/inlanefreight/scans/nessus

Downloading report(s). Please wait...

[+] Exporting scan report, scan id: 1, type: csv
[+] Checking export status...
[+] Report ready for download...
[+] Downloading report to: /assessment_data/inlanefreight/scans/nessus/inlanefreight_basic_5y3hxp.csv

Report Download Completed!
```

### Impacto de la red

También es esencial tener en cuenta el impacto potencial del escaneo de vulnerabilidades en una red, especialmente en anchos de banda bajos o enlaces congestionados. Esto se puede medir usando [vnstat](https://humdi.net/vnstat/) :

```shell-session
afsh4ck@kali$ sudo apt install vnstat
```

Supervisemos el adaptador de red `eth0` antes de ejecutar un análisis de Nessus:

```shell-session
afsh4ck@kali$ sudo vnstat -l -i eth0

Monitoring eth0...    (press CTRL-C to stop)

   rx:       332 bit/s     0 p/s          tx:       332 bit/s     0 p/s

   rx:         0 bit/s     0 p/s          tx:         0 bit/s     0 p/s
   rx:         0 bit/s     0 p/s          tx:         0 bit/s     0 p/s^C

 eth0  /  traffic statistics

                           rx         |       tx
--------------------------------------+------------------
  bytes                        572 B  |           392 B
--------------------------------------+------------------
          max              480 bit/s  |       332 bit/s
      average              114 bit/s  |        78 bit/s
          min                0 bit/s  |         0 bit/s
--------------------------------------+------------------
  packets                          8  |               5
--------------------------------------+------------------
          max                  1 p/s  |           0 p/s
      average                  0 p/s  |           0 p/s
          min                  0 p/s  |           0 p/s
--------------------------------------+------------------
  time                    40 seconds
```

Podemos comparar este resultado con el resultado que obtenemos al monitorear la misma interfaz durante un análisis de Nessus en un solo host:

```shell-session
afsh4ck@kali$ sudo vnstat -l -i eth0

Monitoring eth0...    (press CTRL-C to stop)

   rx:   307.92 kbit/s   641 p/s          tx:   380.41 kbit/s   767 p/s^C

 eth0  /  traffic statistics

                           rx         |       tx
--------------------------------------+------------------
  bytes                     1.04 MiB  |        1.34 MiB
--------------------------------------+------------------
          max          414.81 kbit/s  |   480.59 kbit/s
      average          230.57 kbit/s  |   296.72 kbit/s
          min                0 bit/s  |         0 bit/s
--------------------------------------+------------------
  packets                      18252  |           22733
--------------------------------------+------------------
          max                864 p/s  |         969 p/s
      average                480 p/s  |         598 p/s
          min                  0 p/s  |           0 p/s
--------------------------------------+------------------
  time                    38 seconds


real  0m38.588s
user  0m0.002s
sys 0m0.016s
```

Al comparar los resultados, podemos ver que la cantidad de bytes y paquetes transferidos durante un análisis de vulnerabilidad es bastante significativo y puede afectar gravemente a una red si no se ajusta adecuadamente o no se realiza en dispositivos frágiles/sensibles.
