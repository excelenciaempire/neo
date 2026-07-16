
# Seeker y Ngrok

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a realizar ataques de phishing para conseguir datos sensibles como la ubicación de una persona, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Seeker</mark>

El concepto detrás de **Seeker** es simple: así como alojamos páginas de phishing para obtener credenciales, Seeker crea una página falsa que solicita la ubicación del usuario, como lo hacen muchos sitios web populares basados en ubicación.

{% embed url="<https://github.com/thewhiteh4t/seeker?tab=readme-ov-file#usage>" %}

<figure><img src="/files/bHOec5zlJC1j7VG655as" alt=""><figcaption></figcaption></figure>

**Seeker** aloja una página web falsa que solicita permiso para acceder a la ubicación del objetivo. Si el objetivo concede los permisos, podemos obtener la siguiente información:

#### Información de Ubicación

* **Longitud**
* **Latitud**
* **Precisión**
* **Altitud** (no siempre disponible)
* **Dirección** (solo disponible si el usuario está en movimiento)
* **Velocidad** (solo disponible si el usuario está en movimiento)

#### Información del Dispositivo (sin necesidad de permisos)

Además de la información de ubicación, **Seeker** también recopila información del dispositivo sin necesidad de permisos adicionales:

* **ID único**
* **Modelo del dispositivo**
* **Información del GPU**
* **Nombre y versión del navegador**
* **Dirección IP pública**
* **Dirección IP local**
* **Puerto local**
* **Etc...**

### Instalación en Kali Linux

```bash
git clone https://github.com/thewhiteh4t/seeker.git
cd seeker/
chmod +x install.sh
./install.sh
```

```bash
python3 seeker.py
```

## <mark style="color:purple;">Ngrok</mark>

Ngrok es un servicio que nos permitirá crear un forwarding de nuestra página corriendo en localhost y generar un link que podemos compartir con cualquier persona:

### Instalación en Kali Linux

```bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
sudo mv ngrok /usr/local/bin/
ngrok --version
```

### Configurar Authtoken

Deberás crear una cuenta en [su sitio oficial](https://ngrok.com/) para acceder al authtoken, y una vez que lo tenemos podemos configurarlo con el siguiente comando:

```bash
ngrok config add-authtoken $YOUR_AUTHTOKEN
```

<figure><img src="/files/MXicYYk9UQoVn3LHDwXV" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Configuración del ataque</mark>

En este ejemplo utilizaremos el servicio de Google Drive para que la víctima nos comparta algún archivo y saber su ubicación en tiempo real.&#x20;

1. Para ello seleccionamos la opción 1 y pegamos un link a nuestro Google Drive:

<figure><img src="/files/bHOec5zlJC1j7VG655as" alt=""><figcaption></figcaption></figure>

2. Ahora arrancamos ngrok por el puerto 8080 (que es el que utiliza Seeker por defecto):

```bash
ngrok http 8080
```

<figure><img src="/files/n3STH8aiTixw1sQ3UQt8" alt=""><figcaption></figcaption></figure>

Esto nos genera un link que podemos compartir con cualquier persona, incluso fuera de nuestra red local. Podemos camuflar este link para que no parezca de phising con Maskphish

Una vez que el objetivo abre el enlace (y acepta los permisos de ubicación), conseguimos datos relevantes sobre el objetivo y su ubicación exacta:

<figure><img src="/files/rkWaLdW13IVcjNpTgFTt" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/NXD57O0rJjNcES0q0TDh" alt=""><figcaption></figcaption></figure>
