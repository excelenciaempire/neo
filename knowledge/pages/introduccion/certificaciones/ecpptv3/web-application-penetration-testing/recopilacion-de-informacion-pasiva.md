
# Recopilación de información pasiva

#### Relacionado

{% content-ref url="/pages/Cr8VUHF50vhiuVlAeAWi" %}
[Recopilación Pasiva](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-pasiva.md)
{% endcontent-ref %}

### OWASP Web Security Testing Guide

{% embed url="<https://owasp.org/www-project-web-security-testing-guide/>" %}

El OWASP WSTG es una guía completa para evaluar la seguridad de aplicaciones y servicios web. Creado gracias a la colaboración de profesionales de la ciberseguridad y voluntarios dedicados, el WSTG proporciona un framework utilizado por pentesters y organizaciones de todo el mundo.

#### Checklist

Tenemos este checklist XSL super útil para ir marcando cada sección como hecho:

{% embed url="<https://github.com/tanprathan/OWASP-Testing-Checklist>" %}

<figure><img src="/files/VQiAlNL6VxRRGa8ZGXfA" alt=""><figcaption></figcaption></figure>

### WHOIS

El **protocolo WHOIS** es un **servicio de consulta** que permite obtener información pública sobre **dominios de Internet, direcciones IP y sistemas autónomos (ASN)**.

En pocas palabras: **sirve para saber “quién está detrás” de un dominio o una IP**.

#### ¿Qué tipo de información muestra?

Depende del dominio o IP, pero normalmente incluye:

* **Propietario / registrante** del dominio
* **Organización o empresa**
* **Correo de contacto** (técnico y administrativo)
* **Fechas importantes**:
  * Creación
  * Última actualización
  * Expiración
* **Servidor DNS**
* **Proveedor de Internet (ISP)** para IPs
* **ASN** (Autonomous System Number)

```bash
whois tesla.com
                                                                                 
   Domain Name: TESLA.COM
   Registry Domain ID: 187902_DOMAIN_COM-VRSN
   Registrar WHOIS Server: whois.markmonitor.com
   Registrar URL: http://www.markmonitor.com
   Updated Date: 2024-10-02T10:15:20Z
   Creation Date: 1992-11-04T05:00:00Z
   Registry Expiry Date: 2026-11-03T05:00:00Z
   Registrar: MarkMonitor Inc.
   Registrar IANA ID: 292
   Registrar Abuse Contact Email: abusecomplaints@markmonitor.com
   Registrar Abuse Contact Phone: +1.2086851750
   Domain Status: clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited
   Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited
   Domain Status: clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited
   Domain Status: serverDeleteProhibited https://icann.org/epp#serverDeleteProhibited
   Domain Status: serverTransferProhibited https://icann.org/epp#serverTransferProhibited
   Domain Status: serverUpdateProhibited https://icann.org/epp#serverUpdateProhibited
   Name Server: A1-12.AKAM.NET
   Name Server: A10-67.AKAM.NET
   Name Server: A12-64.AKAM.NET
   Name Server: A28-65.AKAM.NET
   Name Server: A7-66.AKAM.NET
   Name Server: A9-67.AKAM.NET
<SNIP>
```

También tenemos esta utilidad web súper útil:

{% embed url="<https://whois.domaintools.com/>" %}

### Host

Nos permite descubrir rápidamente distintas IPs asociadas a un dominio:

```bash
host tesla.com
                                                           
tesla.com has address 2.18.53.207
tesla.com has address 2.18.55.207
tesla.com has address 2.18.49.207
tesla.com has address 2.18.48.207
tesla.com has address 2.18.50.207
tesla.com has address 2.18.51.207
tesla.com has address 2.18.52.207
tesla.com has address 2.18.54.207
tesla.com has address 23.40.100.207
tesla.com has address 23.7.244.207
tesla.com mail is handled by 10 tesla-com.mail.protection.outlook.com.
```

### Enumeración DNS Pasiva

#### DNS Recon

**dnsrecon** es una **herramienta de reconocimiento DNS** usada en **ciberseguridad y pentesting** para **recolectar información sobre un dominio** a partir de su infraestructura DNS.

Dicho simple: **sirve para descubrir qué hay detrás de un dominio usando DNS**.

```bash
dnsrecon -d hackthissite.org -D /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -t brt
```

<figure><img src="/files/l8BQRpiUGd78pgcTlQBY" alt=""><figcaption></figcaption></figure>

#### DNSDumspter

**DNSDumpster** es una **herramienta OSINT de reconocimiento DNS** que se usa para **descubrir información sobre la infraestructura de un dominio**, de forma **pasiva** y muy visual.

Dicho sencillo: **sirve para ver subdominios, servidores y relaciones DNS de un dominio**.

{% embed url="<https://dnsdumpster.com/>" %}

<figure><img src="/files/BoYY3eyZwCsUozHdZ2pw" alt=""><figcaption></figcaption></figure>

#### Webserver Metafiles

**robots.txt** es un **archivo de texto** que se usa para **indicar a los motores de búsqueda (robots o crawlers)** qué partes de un sitio web **pueden o no pueden rastrear**.

Dicho simple: **le dice a los “bots” qué páginas deben ignorar**.

```
https://example.com/robots.txt
```

### Enumeración pasiva de tecnologías web

En la siguiente sección tengo recogidas multitud de técnicas para identificar tecnologías web:

{% content-ref url="/pages/8W5bpzLqbddEEBoh7uEA" %}
[Identificar Tecnologías](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-pasiva/identificar-tecnologias.md)
{% endcontent-ref %}
