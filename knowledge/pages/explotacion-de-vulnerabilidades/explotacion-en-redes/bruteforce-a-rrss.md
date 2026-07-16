
# Bruteforce a RRSS

{% hint style="danger" %}
**Nota:** Vamos a realizar fuerza bruta a redes sociales para conseguir datos sensibles como contraseñas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo.
{% endhint %}

## <mark style="color:purple;">Bruteforce a Instagram y Facebook</mark>

{% hint style="info" %}
Muchas de estas técnicas puede que no funcionen correctamente con las últimas actualizaciones de seguridad de las distintas aplicaciones.
{% endhint %}

### Yphish

{% embed url="<https://github.com/thiagous06/YPhish>" %}

<figure><img src="/files/u6wsQ9Q8jfP8qwJGfIWQ" alt=""><figcaption></figcaption></figure>

Es una herramienta muy sencilla en Python que nos permite hacer varias acciones, entre las que tiene fuerza bruta a varios servicios como redes sociales.

### Instashell

{% embed url="<https://github.com/maxrooted/instashell>" %}

<figure><img src="/files/DuMRZL4EFYyF6IJst11B" alt=""><figcaption></figcaption></figure>

Instashell es una herramienta de bruteforce a Instagram, que además lo realiza a traves de TOR, siendo completamente anónimo. El diccionario por defecto contiene 39330 palabras, pero podemos utilizar el diccionario que queramos.

#### Empleo

```
git clone https://github.com/thelinuxchoice/instashell
cd instashell
chmod +x instashell.sh
service tor start
sudo ./instashell.sh
```

## Facebook-BruteForce

{% embed url="<https://github.com/IAmBlackHacker/Facebook-BruteForce>" %}

<figure><img src="/files/zi9Kdh5SE5rzcX1gr9c6" alt=""><figcaption></figcaption></figure>

Herramienta que nos permite hacer bruteforce a Facebook de manera muy simple. Tenemos que colocar el diccionario que queramos dentro de la carpeta con el nombre passwords.txt

#### Empleo

```
git clone https://github.com/IAmBlackHacker/Facebook-BruteForce
cd Facebook-BruteForce
python3 -m pip install requests bs4
python3 -m pip install mechanize
python3 fb.py
```
