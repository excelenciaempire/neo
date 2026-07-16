
# Herramientas Genéricas

## <mark style="color:purple;">OSINT UI</mark>

OSINT UI es una plataforma propia que he desarrollado, y se trata de un entorno de escritorio virtual que proporciona un conjunto de herramientas integradas en una interfaz de estilo "hacker" para facilitar la recopilación y el análisis de información de fuentes públicas.

{% embed url="<https://osint-ui.com>" %}

<figure><img src="/files/jYlpLimsgQTjBzGat9vE" alt=""><figcaption></figcaption></figure>

#### Video completo de la plataforma

{% embed url="<https://youtu.be/kSbXRrbr29o>" %}

## <mark style="color:purple;">OSINT Framework</mark>

OSINT Framework es una herramienta de código abierto y gratuita que proporciona una lista organizada de herramientas y recursos de OSINT (Inteligencia de Fuentes Abiertas) en una sola interfaz fácil de usar.

Esta herramienta es muy útil para los profesionales de la seguridad y los investigadores que necesitan recopilar información de fuentes abiertas.

{% embed url="<https://osintframework.com/>" %}

<figure><img src="/files/4MEcX33rL9Fl7w6rDez1" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Shodan</mark>

Shodan es un motor de búsqueda especializado en identificar dispositivos conectados a Internet. A diferencia de otros motores de búsqueda que indexan páginas web, Shodan explora los dispositivos y servicios conectados, como servidores, routers, cámaras de vigilancia, bases de datos, y muchos otros. Es muy utilizado en la comunidad de seguridad informática y hacking ético para realizar investigaciones sobre infraestructura, monitoreo de vulnerabilidades y auditorías de seguridad.

<figure><img src="/files/gHB1sg77hV1IupUxJ2UC" alt=""><figcaption></figcaption></figure>

{% embed url="<https://www.shodan.io>" %}

#### Video completo usando Shodan

{% embed url="<https://youtu.be/dF3Cm_QSTGw?si=QAEpWz79hIjCSkP8>" %}

#### Shodan Querys

Repositorio con un montón de Querys de búsqueda para Shodan.

{% embed url="<https://github.com/jakejarvis/awesome-shodan-queries>" %}

{% hint style="info" %}
Es necesario estar logueado para utilizar querys de búsqueda
{% endhint %}

<table data-header-hidden><thead><tr><th width="68"></th><th width="280"></th><th></th></tr></thead><tbody><tr><td><strong>Nº</strong></td><td><strong>Query</strong></td><td><strong>Descripción</strong></td></tr><tr><td>1</td><td><code>port:22</code></td><td>Busca dispositivos con el puerto SSH (22) abierto.</td></tr><tr><td>2</td><td><code>port:21 "230 Login successful"</code></td><td>Dispositivos FTP con acceso anónimo permitido.</td></tr><tr><td>3</td><td><code>port:3389</code></td><td>Encuentra servicios de Escritorio Remoto (RDP).</td></tr><tr><td>4</td><td><code>port:3306</code></td><td>Bases de datos MySQL accesibles en Internet.</td></tr><tr><td>5</td><td><code>port:1433</code></td><td>Bases de datos Microsoft SQL Server expuestas.</td></tr><tr><td>6</td><td><code>port:5900 "authentication disabled"</code></td><td>VNC con autenticación deshabilitada.</td></tr><tr><td>7</td><td><code>port:23</code></td><td>Servicios Telnet expuestos.</td></tr><tr><td>8</td><td><code>port:9200</code></td><td>Instancias de Elasticsearch accesibles.</td></tr><tr><td>9</td><td><code>port:27017</code></td><td>MongoDB sin autenticación habilitada.</td></tr><tr><td>10</td><td><code>ssl:"github.com"</code></td><td>Certificados SSL que mencionan GitHub (posible filtración de datos o servidores internos).</td></tr><tr><td>11</td><td><code>http.title:"phpMyAdmin"</code></td><td>Detecta servidores con phpMyAdmin accesible públicamente.</td></tr><tr><td>12</td><td><code>http.title:"Apache2 Ubuntu Default Page"</code></td><td>Encuentra servidores web que usan la página por defecto de Apache en Ubuntu.</td></tr><tr><td>13</td><td><code>product:"Apache Tomcat"</code></td><td>Servidores con Apache Tomcat.</td></tr><tr><td>14</td><td><code>http.title:"DVR Login"</code></td><td>Cámaras de vigilancia y sistemas de videograbación (DVR) con páginas de login abiertas.</td></tr><tr><td>15</td><td><code>port:8545</code></td><td>NodOS de Ethereum expuestos que podrían permitir transacciones sin autorización.</td></tr><tr><td>16</td><td><code>port:445</code></td><td>Dispositivos con el puerto SMB abierto (vulnerable a ataques como EternalBlue).</td></tr><tr><td>17</td><td><code>product:"Cisco ASA"</code></td><td>Dispositivos de seguridad Cisco ASA.</td></tr><tr><td>18</td><td><code>product:"OpenSSH"</code></td><td>Sistemas que ejecutan OpenSSH.</td></tr><tr><td>19</td><td><code>port:8000,8001</code></td><td>Puertos abiertos comúnmente usados para servidores de administración o desarrollo.</td></tr><tr><td>20</td><td><code>port:6379 "Redis"</code></td><td>Instancias Redis sin protección (sin autenticación).</td></tr><tr><td>21</td><td><code>port:389</code></td><td>Servicios LDAP expuestos.</td></tr><tr><td>22</td><td><code>"Server: MikroTik"</code></td><td>Dispositivos MikroTik, conocidos por vulnerabilidades en versiones antiguas.</td></tr><tr><td>23</td><td><code>product:"Microsoft IIS"</code></td><td>Servidores web con Microsoft IIS.</td></tr><tr><td>24</td><td><code>"default password"</code></td><td>Dispositivos que usan contraseñas por defecto (potencialmente vulnerables).</td></tr><tr><td>25</td><td><code>port:8080 http.title:"Index of /"</code></td><td>Servidores web con directorios listados (índice visible).</td></tr></tbody></table>

#### Queries Específicas para Cámaras Web Expuestas

<table data-header-hidden><thead><tr><th width="68"></th><th width="283"></th><th></th></tr></thead><tbody><tr><td><strong>Nº</strong></td><td><strong>Query</strong></td><td><strong>Descripción</strong></td></tr><tr><td>26</td><td><code>port:554 has_screenshot:true</code></td><td>Cámaras que transmiten vía RTSP (Real-Time Streaming Protocol).</td></tr><tr><td>27</td><td><code>port:81 "GoAhead"</code></td><td>Cámaras web que usan el servidor web "GoAhead".</td></tr><tr><td>28</td><td><code>port:80 "AVTech"</code></td><td>Cámaras de seguridad AVTech accesibles.</td></tr><tr><td>29</td><td><code>port:80 "webcamXP"</code></td><td>Cámaras web que usan el software webcamXP.</td></tr><tr><td>30</td><td><code>port:80 "Netwave IP Camera"</code></td><td>Cámaras Netwave IP expuestas.</td></tr><tr><td>31</td><td><code>title:"Live View / - AXIS"</code></td><td>Cámaras AXIS con la interfaz de "Live View" visible.</td></tr><tr><td>32</td><td><code>port:8080 "IP Camera"</code></td><td>Cámaras IP expuestas en el puerto 8080.</td></tr><tr><td>33</td><td><code>port:80 "Sony Network Camera"</code></td><td>Cámaras Sony con interfaces accesibles públicamente.</td></tr><tr><td>34</td><td><code>port:80 "Panasonic Network Camera"</code></td><td>Cámaras Panasonic con interfaces accesibles.</td></tr><tr><td>35</td><td><code>port:80 "Hikvision" "200 OK"</code></td><td>Cámaras de vigilancia Hikvision con acceso público.</td></tr></tbody></table>

## <mark style="color:purple;">The Harvester</mark>

The Harvester es una herramienta de búsqueda de información que se utiliza en pruebas de penetración y en hacking ético para recopilar información sobre un objetivo. The Harvester puede buscar información en una variedad de fuentes, incluyendo motores de búsqueda, redes sociales, sitios web públicos y más. Viene instalado por defecto en Kali Linux.

{% embed url="<https://github.com/laramies/theHarvester>" %}

```bash
theHarvester -h
```

```bash
theHarvester -d facebook.com -l 400 -b all

Created default proxies.yaml at /home/kali/.theHarvester/proxies.yaml
*******************************************************************
*  _   _                                            _             *
* | |_| |__   ___    /\  /\__ _ _ ____   _____  ___| |_ ___ _ __  *
* | __|  _ \ / _ \  / /_/ / _` | '__\ \ / / _ \/ __| __/ _ \ '__| *
* | |_| | | |  __/ / __  / (_| | |   \ V /  __/\__ \ ||  __/ |    *
*  \__|_| |_|\___| \/ /_/ \__,_|_|    \_/ \___||___/\__\___|_|    *
*                                                                 *
* theHarvester 4.5.1                                              *
* Coded by Christian Martorella                                   *
* Edge-Security Research                                          *
* cmartorella@edge-security.com                                   *
*                                                                 *
*******************************************************************

[*] Target: facebook.com 

Created default api-keys.yaml at /home/kali/.theHarvester/api-keys.yaml

[!] Missing API key for bevigil. 
Read api-keys.yaml from /home/kali/.theHarvester/api-keys.yaml

[*] IPs found: 202                                                                                                
-------------------                                                                                               
10.110.143.20                                                                                                     
10.110.199.18                                                                                                     
129.134.25.123                                                                                                      
...

[*] Hosts found: 22819                                                                                            
---------------------                                                                                             
*.facebook.com                                                                                                    
*.m.facebook.com                                                                                                  
0-125.channel.facebook.com  
...
```

Podemos añadir APIs de todos los servicios que tiene vinculados para aumentar la cantidad de información que nos devuelve. El archivo de APIs está en la siguiente ruta:

```bash
/home/kali/.theHarvester/api-keys.yaml
# o
/root/.theHarvester/api-keys.yaml
```

```bash
sudo nano /home/kali/.theHarvester/api-keys.yaml

apikeys:
  bevigil:
    key: # Añadir clave aquí

  binaryedge:
    key: # Añadir clave aquí

  bing:
    key: # Añadir clave aquí

  bufferoverun:
    key: # Añadir clave aquí

  censys:
    id:
    secret: # Añadir clave aquí

  criminalip:
    key: # Añadir clave aquí

  fullhunt:
    key: # Añadir clave aquí
```

## <mark style="color:purple;">Infooze</mark>

Infoooze es una herramienta OSINT (Inteligencia de código abierto) potente y fácil de usar que permite recopilar información rápida y fácilmente sobre un objetivo específico. Con Infoooze, puede buscar fácilmente información sobre sitios web, direcciones IP, nombres de usuario, direcciones de email y más, desde una sencilla interfaz de línea de comandos. También tiene la capacidad de guardar automáticamente los resultados de sus búsquedas en un archivo de texto.&#x20;

{% embed url="<https://github.com/devXprite/infoooze>" %}

<figure><img src="/files/o3jLcHsPBGIwouKWVUEg" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Mr.Holmes</mark>

Mr.Holmes es una herramienta de recopilación de información (OSINT). El objetivo principal es obtener información sobre dominios, nombres de usuario y números de teléfono con la ayuda de fuentes públicas disponibles en Internet y también utiliza Google Dorks para investigaciones específicas. También utiliza servidores proxy para que sus solicitudes sean completamente anónimas y una API WhoIS para obtener más información sobre un dominio.

{% embed url="<https://github.com/Lucksi/Mr.Holmes>" %}

<figure><img src="/files/r3z9HWnnduRl53cwZY21" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">The Spy's Job</mark>

Esta herramienta está enfocada al OSINT de casi todos los ámbitos (Personas, Nicknames, Redes Sociales, Emails, Números de Teléfono, Páginas Webs, IPs Públicas e Imágenes) Recopila y automatiza todas las técnicas de OSINT más avanzadas posibles en una sola herramienta para trabajar de la forma más cómoda y rápida posible, ya que solo tenemos que dar un par de clics y él solo se pondrá a recopilar y mostrar de forma ordenada y clasificada toda la Información.

{% embed url="<https://github.com/XDeadHackerX/The_spy_job>" %}

<figure><img src="/files/dXJqrOEVFm7y8KD1AHAv" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">IntelX</mark>

IntelX (Intelligence X) es una plataforma avanzada de OSINT diseñada para buscar y analizar información pública y privada en Internet, incluidas fuentes como: Web superficial, Deep web, archivos filtrados, bases de datos públicas, documentos en caché y filtraciones de contraseñas.

IntelX destaca por ofrecer búsquedas en profundidad y acceso a datos que no siempre están indexados por motores de búsqueda convencionales, siendo ideal para investigaciones relacionadas con ciberseguridad y hacking ético.

{% embed url="<https://intelx.io/>" %}

<figure><img src="/files/a0AL76sTf6INsf8zZkHo" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Maltego</mark>

**Maltego** es una poderosa herramienta de OSINT utilizada para recopilar, analizar y visualizar información pública de forma gráfica. Es especialmente útil en investigaciones relacionadas con ciberseguridad, análisis de redes sociales, análisis forense digital y reconocimiento durante pruebas de penetración. Tiene una interfaz visual donde podemos ver los resultados de forma gráfica y ejecutar distintos transformadores mediante APIs. Viene instalado por defecto en Kali Linux.

{% embed url="<https://www.maltego.com/>" %}

<figure><img src="/files/kbPbkLvfMRD1xuQnZUnK" alt=""><figcaption></figcaption></figure>
