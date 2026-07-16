
# OSINT a Usernames

## <mark style="color:purple;">Sherlock</mark>

**Sherlock** es una herramienta de OSINT diseñada para buscar nombres de usuario en una amplia variedad de plataformas en línea, como redes sociales, foros, servicios de correo y otros sitios web. Es especialmente útil para investigar la presencia digital de una persona o entidad, recopilando rápidamente información pública basada en nombres de usuario específicos.

{% embed url="<https://github.com/sherlock-project/sherlock>" %}

<figure><img src="/files/Pz7DZlV3urseVns6dLMg" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">GoSearch</mark>

GoSearch es una herramienta escrita en Go que nos permite recopilar una gran cantidad de información sobre un nombre de usuario, extrayendo hasta filtraciones de contraseñas, emails relacionados, etc...

Está inspirado en [Sherlock](https://github.com/sherlock-project/sherlock) , sin embargo, `GoSearch` lo mejora al corregir varias de sus principales limitaciones:

1. Sherlock está basado en Python, lo que lo hace más lento en comparación con Go.
2. Sherlock está desactualizado y carece de actualizaciones.
3. Sherlock a veces informa falsos positivos como resultados válidos.
4. Sherlock frecuentemente pasa por alto nombres de usuario reales, lo que genera falsos negativos.
5. Sherlock no busca en la base de datos de inteligencia de delitos cibernéticos cómo HudsonRock
6. Sherlock no busca en la base de datos de ProxyNova o BreachDirectory

{% embed url="<https://github.com/ibnaleem/gosearch.git>" %}

<figure><img src="/files/humpXrBfilue21avswHz" alt=""><figcaption></figcaption></figure>

#### Instalación

```bash
sudo apt update && sudo apt install golang -y
go install github.com/ibnaleem/gosearch@latest
export PATH=$PATH:$(go env GOPATH)/bin
source ~/.zshrc   # o ~/.bashrc

gosearch -u [USERNAME] --no-false-positives
```

#### Si no tienes un nombre de usuario

Puedes utilizar Username Anarchy para generar un listado de posibles nombres de usuario a partir de un nombre y apellido:

```bash
git clone https://github.com/urbanadventurer/username-anarchy
cd username-anarchy
./username-anarchy firstname lastname
```

***

## <mark style="color:purple;">Maigret</mark>

Maigret es una herramienta de OSINT que se utiliza para recopilar información sobre perfiles en redes sociales. La herramienta Maigret analiza perfiles en redes sociales como Instagram, Twitter, LinkedIn y otros, para encontrar información asociada a un nombre de usuario específico. Puede proporcionar detalles sobre la actividad en línea de una persona, como sus publicaciones, fotos, seguidores, etc.

{% embed url="<https://github.com/soxoj/maigret>" %}

<figure><img src="/files/20fqhzMg3erjteYoMq4T" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">User Recon</mark>

**UserRecon** es una herramienta de **OSINT** diseñada para buscar la presencia de un nombre de usuario en múltiples plataformas en línea. Es particularmente útil en investigaciones para identificar si un nombre de usuario está asociado a cuentas en redes sociales, foros, servicios web y más.

{% embed url="<https://github.com/wishihab/userrecon>" %}

<figure><img src="/files/SIRWK1OigVvlbJ3uPhPV" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">DetectDee</mark>

**DetectDee** es una herramienta de **OSINT** desarrollada para identificar la presencia de nombres de usuario en diversas plataformas en línea. Al ejecutar comandos a través de su interfaz de terminal, DetectDee automatiza la búsqueda y proporciona enlaces directos a las cuentas encontradas, facilitando así el reconocimiento de la actividad en línea de un usuario específico.

{% embed url="<https://github.com/piaolin/DetectDee>" %}

```shell-session
./detectdee detect -n therock
                                                                           
██████╗ ███████╗████████╗███████╗ ██████╗████████╗██████╗ ███████╗███████╗
██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝
██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║  ██║█████╗  █████╗  
██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║  ██║██╔══╝  ██╔══╝  
██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ██████╔╝███████╗███████╗
╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚══════╝
INFO   [2025-05-13 12:31:35] Detect for [therock]                         
INFO   [2025-05-13 12:31:36] [+] therock         mastodon-social: https://mastodon.social/@therock 
INFO   [2025-05-13 12:31:36] [+] therock         tryhackme      : https://tryhackme.com/p/therock 
INFO   [2025-05-13 12:31:36] [+] therock         ultimate-guitar: https://ultimate-guitar.com/u/therock 
INFO   [2025-05-13 12:31:36] [+] therock         hackerone      : https://hackerone.com/therock?type=user 
INFO   [2025-05-13 12:31:36] [+] therock         steamgroup     : https://steamcommunity.com/groups/therock 
INFO   [2025-05-13 12:31:36] [+] therock         slack          : https://therock.slack.com 
INFO   [2025-05-13 12:31:36] [+] therock         wordpress      : https://therock.wordpress.com/ 
INFO   [2025-05-13 12:31:36] [+] therock         thehackerworld : https://www.thehackerworld.com/profile/therock/  
INFO   [2025-05-13 12:31:36] [+] therock         dockerhub      : https://hub.docker.com/u/therock/ 
INFO   [2025-05-13 12:31:36] [+] therock         flickr         : https://www.flickr.com/people/therock 
INFO   [2025-05-13 12:31:36] [+] therock         osu!           : https://osu.ppy.sh/users/therock 
INFO   [2025-05-13 12:31:37] [+] therock         gitbook        : https://therock.gitbook.io/ 
INFO   [2025-05-13 12:31:37] [+] therock         npm            : https://www.npmjs.com/~therock 
INFO   [2025-05-13 12:31:37] [+] therock         academia-edu   : https://independent.academia.edu/therock 
INFO   [2025-05-13 12:31:38] [+] therock         twitter        : https://twitter.com/therock 
INFO   [2025-05-13 12:31:39] [+] therock         instagram      : https://www.instagram.com/therock/
INFO   [2025-05-13 12:31:56] [+] therock         reddit         : https://www.reddit.com/user/therock 
INFO   [2025-05-13 12:31:57] [+] therock         icq            : https://icq.im/therock/en 
<---SNIP--->
INFO   [2025-05-13 12:32:05] [+] therock Registrant Country: [{US 80} {RU 13} {CN 12} {GB 10} {DE 8} {IS 5} {CZ 4} {CA 4} {AU 4} {ES 3} {PL 3} {FR 3} {KY 1} {SE 1} {NL 1} {BR 1} {AT 1} {UK 1} {EE 1}] 
INFO   [2025-05-13 12:32:05] [+] Detect completed, save to result.txt  
```

Eso nos genera un archivo `results.txt` con todas las redes sociales identificadas del objetivo. Ahora indicándole el parámetro `screenshot` automáticamente nos guardará una captura de pantalla de cada una de las redes sociales, lo que nos permite visualizar rápidamente cuales son las fuentes verdaderas y cuales falsos positivos.

{% hint style="success" %}
El parámetro `screenshot` recoge los datos del archivo `results.txt` automáticamente
{% endhint %}

```
./detectdee screenshot
                                                                           
██████╗ ███████╗████████╗███████╗ ██████╗████████╗██████╗ ███████╗███████╗
██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝
██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║  ██║█████╗  █████╗  
██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║  ██║██╔══╝  ██╔══╝  
██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ██████╔╝███████╗███████╗
╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚══════╝
INFO   [2025-05-13 12:31:35] Detect for [therock] 
INFO   [2025-05-13 12:44:51] [+] screenshot success https://community.eintracht.de/fans/therock 
INFO   [2025-05-13 12:44:52] [+] screenshot success https://www.bandcamp.com/therock 
INFO   [2025-05-13 12:44:52] [+] screenshot success https://www.goodreads.com/therock 
INFO   [2025-05-13 12:44:54] [+] screenshot success https://www.reddit.com/user/therock
<---SNIP--->
```

Eso nos genera la carpeta screenshots con todas las capturas de pantalla:

<figure><img src="/files/Rx4F3zJSEtdxiApgUcfI" alt=""><figcaption></figcaption></figure>

#### Instalación

```bash
wget https://github.com/piaolin/DetectDee/releases/download/v1.4.719/DetectDee_linux_amd64.zip
unzip DetectDee_linux_amd64.zip
chmod +x DetectDee 
sudo ./DetectDee -h
```

***

## <mark style="color:purple;">Linkook</mark>

Linkook es una herramienta de OSINT que automatiza el descubrimiento de redes sociales vinculadas a un usuario, encontrando los emails asociados a ese usuario y contraseñas filtradas a través de la API de Have I Been Pwned.

{% embed url="<https://github.com/JackJuly/linkook>" %}

```bash
pipx install linkook
linkook {username}
```

<figure><img src="/files/Vp9CI6tA4KFc6rf9qkuh" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Whats My Name</mark>

Whats My Name es un servicio online gratuito que nos permite analizar todas las cuentas de redes sociales y toda la presencia digital vinculada a un username.

{% embed url="<https://whatsmyname.app>" %}

<figure><img src="/files/QGljd5oYsiz4QeHMXS6g" alt=""><figcaption></figcaption></figure>
