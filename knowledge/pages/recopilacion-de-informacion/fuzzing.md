
# Fuzzing

{% hint style="danger" %}
**Nota:** Este tipo de búsquedas son muy invasivas, ya que hacen muchas peticiones al servidor del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Seclists</mark>

{% embed url="<https://github.com/danielmiessler/SecLists>" %}

Las seclists son colecciones de listas de palabras clave que se utilizan con herramientas de enumeración y fuzzing, como Nmap, Dirb, Gobuster, ffuf, etc., para descubrir vulnerabilidades en sistemas y aplicaciones. Vienen instaladas por defecto en Kali linux.

### Instalación

```bash
sudo apt install seclists -y
```

```bash
cd /usr/share/seclists
```

<figure><img src="/files/DEiHJvlQbuZ5eHqLHc0o" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Crear un diccionario de números</mark>

```bash
afsh4ck@kali$ for i in $(seq 1 1000); do echo $i >> ids.txt; done
```

```bash
cat ids.txt
1
2
3
# <-- SNIP -->
999
1000
```

## <mark style="color:purple;">Dirsearch</mark>

{% embed url="<https://github.com/maurosoria/dirsearch>" %}

Su principal función es realizar búsquedas y enumeraciones en servidores web en busca de directorios y archivos ocultos o sensibles que podrían representar una posible vulnerabilidad de seguridad. Estos directorios y archivos a menudo contienen información confidencial o son puntos de entrada potenciales para atacantes.

{% code title="Instalación y uso" %}

```bash
sudo apt-get install dirsearch
dirsearch -u http://target.com
dirsearch -u http://target.com -x 404,403,302 # Excluir páginas con status negativo
```

{% endcode %}

<figure><img src="/files/TTuj09q0Ne1K7iq7RrFl" alt=""><figcaption><p>Dirsearch</p></figcaption></figure>

Lo veremos más en detalle en la sección:

{% content-ref url="/pages/ssWzJQImYDA2caGm23aV" %}
[Dirsearch](/ethical-hacking-cheatsheet/recopilacion-de-informacion/fuzzing/dirsearch.md)
{% endcontent-ref %}

## <mark style="color:purple;">Radamsa (Fuzzing para DdoS)</mark>

{% embed url="<https://gitlab.com/akihe/radamsa>" %}

Radamsa es una herramienta de generación de mutaciones de entradas utilizada para pruebas de penetración y pruebas de seguridad. Esta herramienta es de código abierto y se utiliza para generar entradas aleatorias y mutadas para aplicaciones y sistemas de software.

#### Empleo

{% code overflow="wrap" %}

```bash
cd /radamsa/bin
echo “hola” > texto.txt
ffuf -request /home/kali/Escritorio/request-bwap --input-cmd 'radamsa texto.txt' -input-num 10000000000
```

{% endcode %}

## <mark style="color:purple;">Dirbuster</mark>

DirBuster es una herramienta de código abierto utilizada para realizar pruebas de penetración en aplicaciones web. La herramienta está escrita en Java y se ejecuta en sistemas operativos Linux, Unix y Windows.

DirBuster se usa para encontrar y enumerar los directorios y archivos ocultos en una aplicación web. La herramienta utiliza una lista de directorios y archivos comunes para realizar estas pruebas.

{% hint style="danger" %}
Técnica de reconocimiento activo, no utilizar sin autorización del objetivo.
{% endhint %}

```bash
dirbuster -u TARGET
```

* En la GUI seleccionar la wordlist a utilizar

### A continuación veremos algunas de las técnicas y herramientas más utilizadas para fuzzing:

{% content-ref url="/pages/ssAmyHO0V9t3GsljYTTG" %}
[Crawling](/ethical-hacking-cheatsheet/recopilacion-de-informacion/crawling.md)
{% endcontent-ref %}

{% content-ref url="/pages/BCt1x9j4Sf2NG3MCMhZJ" %}
[Gobuster](/ethical-hacking-cheatsheet/recopilacion-de-informacion/fuzzing/gobuster.md)
{% endcontent-ref %}

{% content-ref url="/pages/27SGdsmGYGBRQvxKhO4z" %}
[Ffuf](/ethical-hacking-cheatsheet/recopilacion-de-informacion/fuzzing/ffuf.md)
{% endcontent-ref %}
