
# Herramientas de Análisis

## <mark style="color:purple;">Nessus</mark>

Es una de las herramientas más completas y ampliamente utilizada en organizaciones para encontrar vulnerabilidades en sistemas. Hay una sección dedicada solamente a este herramienta:

{% content-ref url="/pages/iQvceuPmt2Gjt0rLb5gv" %}
[Nessus](/ethical-hacking-cheatsheet/analisis-de-vulnerabilidades/herramientas-de-analisis/nessus.md)
{% endcontent-ref %}

## <mark style="color:purple;">OpenVAS</mark>

Es otra de las herramientas de análisis de vulnerabilidades más utilizadas. También hay una sección en detalle sobre esta herramienta:

{% content-ref url="/pages/1ODr9a4cQXwhi2nZIlRB" %}
[OpenVAS](/ethical-hacking-cheatsheet/analisis-de-vulnerabilidades/herramientas-de-analisis/openvas.md)
{% endcontent-ref %}

## <mark style="color:purple;">Nikto</mark>

Nikto es capaz de realizar pruebas de seguridad automatizadas en servidores web y aplicaciones web, incluyendo pruebas de vulnerabilidades comunes como inyecciones SQL, cross-site scripting (XSS), Local File Inclusion y otros.

{% hint style="success" %}
Viene instalado en Kali Linux por defecto
{% endhint %}

{% embed url="<https://github.com/sullo/nikto>" %}

```bash
nikto -h
nikto -host TARGET -o report.html -Format html
```

## <mark style="color:purple;">Skipfish</mark>

Skipfish es capaz de realizar pruebas automatizadas de seguridad en aplicaciones web, incluyendo pruebas de vulnerabilidades comunes como inyecciones SQL, cross-site scripting (XSS), Local File Inclusion y otros. La herramienta también puede realizar pruebas de directorios y archivos, escaneo de puertos y seguimiento de cookies y encabezados.

Además, Skipfish tiene la capacidad de generar informes detallados sobre las vulnerabilidades de seguridad encontradas en la aplicación web evaluada.

{% hint style="success" %}
Viene instalado en Kali Linux por defecto
{% endhint %}

```bash
skipfish -h
skipfish -o vuln-scan http://example.com
```

```shell-session
afsh4ck@kali$ skipfish -o vuln-scan http://hackthissite.org

skipfish version 2.10b by lcamtuf@google.com

  - hackthissite.org -

Scan statistics:

      Scan time : 0:00:16.186
  HTTP requests : 1 (0.1/s), 0 kB in, 0 kB out (0.0 kB/s)  
    Compression : 0 kB in, 0 kB out (0.0% gain)    
    HTTP faults : 1 net errors, 0 proto errors, 0 retried, 0 drops
 TCP handshakes : 1 total (1.0 req/conn)  
     TCP faults : 0 failures, 1 timeouts, 0 purged
 External links : 0 skipped
   Reqs pending : 0        

Database statistics:

         Pivots : 2 total, 2 done (100.00%)    
    In progress : 0 pending, 0 init, 0 attacks, 0 dict    
  Missing nodes : 0 spotted
     Node types : 1 serv, 1 dir, 0 file, 0 pinfo, 0 unkn, 0 par, 0 val
   Issues found : 0 info, 1 warn, 0 low, 0 medium, 0 high impact
      Dict size : 2 words (2 new), 1 extensions, 0 candidates
     Signatures : 77 total
        
[+] Copying static resources...
[+] Sorting and annotating crawl nodes: 2
[+] Looking for duplicate entries: 2
[+] Counting unique nodes: 2
[+] Saving pivot data for third-party tools...
[+] Writing scan description...
[+] Writing crawl tree: 2
[+] Generating summary views...
[+] Report saved to 'vuln-scan/index.html' [0x8be97479].
[+] This was a great day for science!
```

## <mark style="color:purple;">Nuclei</mark>

Nuclei es una herramienta de código abierto utilizada para realizar pruebas de seguridad automatizadas en aplicaciones web. La herramienta está escrita en Go y se ejecuta en sistemas operativos Linux, Unix y Windows.

Hay una sección dedicada solamente a esta herramienta en detalle:

{% content-ref url="/pages/CQo0eLoSd6q4Gj4dEm2v" %}
[Nuclei](/ethical-hacking-cheatsheet/analisis-de-vulnerabilidades/herramientas-de-analisis/nuclei.md)
{% endcontent-ref %}
