
# OSINT a Dominios

## <mark style="color:purple;">Argus</mark>

**ARGUS** es una herramienta de **OSINT y recopilación de información** diseñada para automatizar la recopilación y análisis de información pública. Su enfoque principal está en simplificar la búsqueda y organización de datos relevantes sobre un objetivo, como direcciones IP, dominios, correos electrónicos, perfiles de redes sociales y más. Es especialmente útil para investigadores de ciberseguridad, hackers éticos y analistas forenses.

{% embed url="<https://github.com/jasonxtn/Argus>" %}

```bash
git clone https://github.com/jasonxtn/argus.git && cd argus
pip install -r requirements.txt
python argus.py
```

<figure><img src="/files/hSdM1dKIIK0T6HVjR00o" alt=""><figcaption></figcaption></figure>

{% embed url="<https://youtu.be/sh7lmlmBsW0?si=kdmlqxhsV9fniI2o>" %}

## <mark style="color:purple;">Bbot</mark>

**Bbot** es una herramienta de **OSINT** que se centra en la recolección automatizada de información. Desarrollada por Black Lantern Security, Bbot puede rastrear datos provenientes de diversas fuentes en línea, brindando a los usuarios una forma efectiva de reunir información pública de manera estructurada.

{% embed url="<https://github.com/blacklanternsecurity/bbot>" %}

```bash
pipx install bbot

bbot -h                               
  ______  _____   ____ _______
 |  ___ \|  __ \ / __ \__   __|
 | |___) | |__) | |  | | | |
 |  ___ <|  __ <| |  | | | |
 | |___) | |__) | |__| | | |
 |______/|_____/ \____/  |_|
 BIGHUGE BLS OSINT TOOL v2.4.2

www.blacklanternsecurity.com/bbot

usage: bbot [-h] [-t TARGET [TARGET ...]] [-w WHITELIST [WHITELIST ...]] [-b BLACKLIST [BLACKLIST ...]] [--strict-scope] [-p [PRESET ...]] [-c [CONFIG ...]] [-lp]
            [-m MODULE [MODULE ...]] [-l] [-lmo] [-em MODULE [MODULE ...]] [-f FLAG [FLAG ...]] [-lf] [-rf FLAG [FLAG ...]] [-ef FLAG [FLAG ...]] [--allow-deadly] [-n SCAN_NAME] [-v]
            [-d] [-s] [--force] [-y] [--fast-mode] [--dry-run] [--current-preset] [--current-preset-full] [-mh MODULE] [-o DIR] [-om MODULE [MODULE ...]] [-lo] [--json] [--brief]
            [--event-types EVENT_TYPES [EVENT_TYPES ...]] [--exclude-cdn] [--no-deps | --force-deps | --retry-deps | --ignore-failed-deps | --install-all-deps] [--version]
            [--proxy HTTP_PROXY] [-H CUSTOM_HEADERS [CUSTOM_HEADERS ...]] [--custom-yara-rules CUSTOM_YARA_RULES] [--user-agent USER_AGENT]
```

```bash
Ejemplos

# Escaneo de Subdominios
bbot -t evilcorp.com -p subdomain-enum

# Subdominios (pasivo)
bbot -t evilcorp.com -p subdomain-enum -rf passive

# Extracción de emails
bbot -t evilcorp.com -p email-enum

# Subdominios + Puertos + Capturas de pantalla
bbot -t evilcorp.com -p subdomain-enum -m portscan gowitness -n my_scan -o .

# Subdominios + Escaneo Web Básico
bbot -t evilcorp.com -p subdomain-enum web-basic

# Web Spider
bbot -t www.evilcorp.com -p spider -c web.spider_distance=2 web.spider_depth=2

# Escaneo completo
bbot -t evilcorp.com -p kitchen-sink --allow-deadly
```

Una de las funciones más útiles es la de extraer emails de un dominio:

```
bbot -t hackthissite.org -p email-enum
  ______  _____   ____ _______
 |  ___ \|  __ \ / __ \__   __|
 | |___) | |__) | |  | | | |
 |  ___ <|  __ <| |  | | | |
 | |___) | |__) | |__| | | |
 |______/|_____/ \____/  |_|
 BIGHUGE BLS OSINT TOOL v2.4.2

www.blacklanternsecurity.com/bbot

[INFO] Scan seeded with 1 targets (1 in whitelist)
[INFO] Loaded 8/8 scan modules (dehashed,dnscaa,dnstlsrpt,emailformat,hunterio,pgp,skymem,sslcert)
[INFO] Loaded 6/6 internal modules (aggregate,cloudcheck,dnsresolve,excavate,speculate,unarchive)
[INFO] Loaded 6/6 output modules, (csv,emails,json,python,stdout,txt)
[INFO] internal.speculate: No portscanner enabled. Assuming open ports: 80, 443
[INFO] Setup soft-failed for dehashed: No username / API key set
[INFO] Setup soft-failed for hunterio: No API key set
[SUCC] Setup succeeded for 20/22 modules.
[SUCC] Scan ready. Press enter to execute diabolical_lori

[SUCC] Starting scan diabolical_lori
[SCAN]              	diabolical_lori (SCAN:bcdf7ad9b7620d70207f568fa673be24a4c6e915)	TARGET
[DNS_NAME]          	hackthissite.org	TARGET	(a-record, domain, in-scope, mx-record, ns-record, soa-record, target, txt-record)
[ORG_STUB]          	hackthissite	speculate
[EMAIL_ADDRESS]     	admin@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	scram@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	irc@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	manonmission@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	no-reply@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	staff@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	apply@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	anarkakari@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	monica@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	sam@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	store@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	dotty@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	h@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	ircuser@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	weekend@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	mshred@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	advertising@hackthissite.org	skymem	(in-scope)
[EMAIL_ADDRESS]     	donate@hackthissite.org	skymem	(in-scope)
<---SNIP--->
[INFO] output.csv: Saved CSV output to /home/kali/.bbot/scans/diabolical_lori/output.csv
[INFO] output.emails: Saved 20 email addresses to /home/kali/.bbot/scans/diabolical_lori/emails.txt
[INFO] output.json: Saved JSON output to /home/kali/.bbot/scans/diabolical_lori/output.json
[INFO] output.txt: Saved TXT output to /home/kali/.bbot/scans/diabolical_lori/output.txt
[SUCC] Scan diabolical_lori completed in 22 seconds with status FINISHED
```

Nos guarda todos los resultados en la ruta que nos genera, en formato `csv`, `json` y `txt`.

```bash
cat /home/kali/.bbot/scans/diabolical_lori/emails.txt                
───────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: /home/kali/.bbot/scans/diabolical_lori/emails.txt
───────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ admin@hackthissite.org
   2   │ scram@hackthissite.org
   3   │ irc@hackthissite.org
   4   │ manonmission@hackthissite.org
   5   │ no-reply@hackthissite.org
   6   │ staff@hackthissite.org
   7   │ apply@hackthissite.org
   8   │ anarkakari@hackthissite.org
   9   │ monica@hackthissite.org
  10   │ sam@hackthissite.org
  11   │ store@hackthissite.org
  12   │ dotty@hackthissite.org
  13   │ h@hackthissite.org
  14   │ ircuser@hackthissite.org
  15   │ weekend@hackthissite.org
  16   │ mshred@hackthissite.org
  17   │ advertising@hackthissite.org
  18   │ donate@hackthissite.org
  19   │ spaux@hackthissite.org
  20   │ kage@hackthissite.org
```

***

## <mark style="color:purple;">OSINT Dashboard</mark>

OSINT Dashboard es una herramienta online que centraliza multitud de herramientas para analizar dominios, IPs o hashes. Solamente escribimos el dominio o IP y luego ejecutamos cada una de las herramientas para hacer una búsqueda dirigida al dominio que hemos seleccionado.

{% embed url="<https://ekky19.github.io/osint/>" %}

<figure><img src="/files/N0EbuBKqHLEYcUQJs26A" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Metagoofill</mark>

**Metagoofil** es una herramienta de recolección de información (OSINT) incluida en Kali Linux, usada principalmente para **extraer metadatos** de documentos públicos que están disponibles en internet.

{% embed url="<https://www.kali.org/tools/metagoofil/>" %}

```bash
sudo apt update
sudo apt install metagoofil
```

Metagoofil busca y descarga documentos públicos como: `.pdf .doc/.docx .xls/.xlsx .ppt o .odt`, entre otros desde un dominio objetivo, y luego **extrae metadatos** como:

* Nombres de usuarios.
* Nombres de máquinas.
* Software utilizado.
* Versiones de programas.
* Caminos locales en los documentos.
* Posible estructura interna de la organización.

```shell-session
root@kali:~# metagoofil -d kali.org -t pdf -l 100 -n 25 -o kalipdf -f kalipdf.html

******************************************************
*     /\/\   ___| |_ __ _  __ _  ___   ___  / _(_) | *
*    /    \ / _ \ __/ _` |/ _` |/ _ \ / _ \| |_| | | *
*   / /\/\ \  __/ || (_| | (_| | (_) | (_) |  _| | | *
*   \/    \/\___|\__\__,_|\__, |\___/ \___/|_| |_|_| *
*                         |___/                      *
* Metagoofil Ver 2.2                                 *
* Christian Martorella                               *
* Edge-Security.com                                  *
* cmartorella_at_edge-security.com                   *
******************************************************
['pdf']

[-] Starting online search...

[-] Searching for pdf files, with a limit of 100
        Searching 100 results...
Results: 21 files found
Starting to download 25 of them:
```

<table><thead><tr><th width="73.6796875">Opción</th><th width="142.34375">Valor</th><th>Descripción</th></tr></thead><tbody><tr><td><code>-d</code></td><td><code>kali.org</code></td><td>Dominio objetivo del que se buscarán documentos.</td></tr><tr><td><code>-t</code></td><td><code>pdf</code></td><td>Tipo(s) de archivo a buscar (en este caso, solo PDF).</td></tr><tr><td><code>-l</code></td><td><code>100</code></td><td>Límite de resultados de búsqueda (hasta 100 enlaces desde Google).</td></tr><tr><td><code>-n</code></td><td><code>25</code></td><td>Número máximo de archivos a descargar (de los encontrados).</td></tr><tr><td><code>-o</code></td><td><code>kalipdf</code></td><td>Carpeta de salida donde se guardarán los documentos descargados.</td></tr><tr><td><code>-f</code></td><td><code>kalipdf.html</code></td><td>Nombre del archivo HTML donde se generará el reporte con los metadatos.</td></tr></tbody></table>

***

## <mark style="color:purple;">Leak IX</mark>

LeakIX es una plataforma online que nos permite extraer información relevante de un dominio cómo diferentes IPs asociadas, hostnames, leaks, CVEs, reds y países, mostrándonos la información de manera muy visual en un gráfico.

{% embed url="<https://leakix.net>" %}

<figure><img src="/files/y5g9iVWtPXkV6lEa3xKH" alt=""><figcaption></figcaption></figure>
