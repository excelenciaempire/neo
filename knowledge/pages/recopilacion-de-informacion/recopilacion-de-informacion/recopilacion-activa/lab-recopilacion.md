
# Lab - Recopilación

## <mark style="color:purple;">Introducción</mark>

Acabas de decidir unirte al programa de [Bug Bounty](https://bounty.github.com/) de GitHub después de que un amigo tuyo recibiera un gran pago por descubrir una falla crítica de RCE. Después de leer las reglas detenidamente, comienza con la recopilación y enumeración de información pasiva y activa para intentar descubrir un objetivo interesante. Después de revisar el [alcance](https://bounty.github.com/#scope) , decide apuntar al dominio `githubapp.com`.

La descripción de este dominio dice lo siguiente:

```shell-session
githubapp.com

This is our domain for hosting employee-facing services. 

All subdomains under githubapp.com are in-scope except:

- atom-io.githubapp.com
- atom-io-staging.githubapp.com
- email.enterprise-staging.githubapp.com
- email.haystack.githubapp.com
- reply.githubapp.com
```

Realiza una recopilación de información pasiva y activa en este dominio y responda las preguntas a continuación para completar la evaluación de habilidades y finalizar este módulo.

***

## <mark style="color:purple;">Pregunta 1</mark>

¿Cuál es el `Registrar IANA ID` del registrador del dominio githubapp.com?

```shell-session
afsh4ck@kali$ whois githubapp.com                       
   Domain Name: GITHUBAPP.COM
   Registry Domain ID: 1671607560_DOMAIN_COM-VRSN
   Registrar WHOIS Server: whois.markmonitor.com
   Registrar URL: http://www.markmonitor.com
   Updated Date: 2023-07-10T09:15:13Z
   Creation Date: 2011-08-11T23:30:52Z
   Registry Expiry Date: 2025-08-11T23:30:52Z
   Registrar: MarkMonitor Inc.
   Registrar IANA ID: 292
   Registrar Abuse Contact Email: abusecomplaints@markmonitor.com
   Registrar Abuse Contact Phone: +1.2086851750
   Domain Status: clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited
   Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited
   Domain Status: clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited
   Name Server: DNS1.P08.NSONE.NET
   Name Server: DNS2.P08.NSONE.NET
   Name Server: DNS3.P08.NSONE.NET
   Name Server: DNS4.P08.NSONE.NET
   Name Server: NS-1059.AWSDNS-04.ORG
   Name Server: NS-1805.AWSDNS-33.CO.UK
   Name Server: NS-496.AWSDNS-62.COM
   Name Server: NS-713.AWSDNS-25.NET
   DNSSEC: unsigned
   URL of the ICANN Whois Inaccuracy Complaint Form: https://www.icann.org/wicf/
>>> Last update of whois database: 2024-02-27T15:03:16Z <<<
```

Respuesta: `Registrar IANA ID: 292`

***

## <mark style="color:purple;">Pregunta 2</mark>

¿Cuál es el último servidor de correo devuelto al consultar los `registros MX` de `githubapp.com`?

```shell-session
afsh4ck@kali$ dnsenum githubapp.com

dnsenum VERSION:1.2.6

-----   githubapp.com   -----

Host's addresses:
__________________

githubapp.com.                           535      IN    A        140.82.112.30
githubapp.com.                           535      IN    A        140.82.114.30
githubapp.com.                           535      IN    A        140.82.113.30
githubapp.com.                           535      IN    A        140.82.114.29
githubapp.com.                           535      IN    A        140.82.112.29
githubapp.com.                           535      IN    A        140.82.113.29

Name Servers:
______________

dns1.p08.nsone.net.                      44       IN    A        198.51.44.8
dns2.p08.nsone.net.                      44       IN    A        198.51.45.8
dns3.p08.nsone.net.                      80       IN    A        198.51.44.72
dns4.p08.nsone.net.                      107      IN    A        198.51.45.72
ns-496.awsdns-62.com.                    1854     IN    A        205.251.193.240
ns-713.awsdns-25.net.                    189      IN    A        205.251.194.201
ns-1059.awsdns-04.org.                   522      IN    A        205.251.196.35
ns-1805.awsdns-33.co.uk.                 176      IN    A        205.251.199.13

Mail (MX) Servers:
___________________

aspmx.l.google.com.                      198      IN    A        64.233.166.27
alt1.aspmx.l.google.com.                 218      IN    A        142.250.153.26
alt2.aspmx.l.google.com.                 93       IN    A        142.251.9.27
aspmx2.googlemail.com.                   133      IN    A        142.250.153.27
aspmx3.googlemail.com.                   53       IN    A        142.251.9.26
aspmx4.googlemail.com.                   293      IN    A        142.250.150.27
aspmx5.googlemail.com.                   278      IN    A        74.125.200.27
```

Respuesta: `aspmx5.googlemail.com`

***

## <mark style="color:purple;">Pregunta 3</mark>

Realiza una identificación de infraestructura activa contra el host `https://i.imgur.com`. ¿Qué nombre de servidor se devuelve para el host?

{% code overflow="wrap" %}

```shell-session
afsh4ck@kali$ whatweb -a3 https://i.imgur.com -v   
  
WhatWeb report for https://i.imgur.com
Status    : 302 Found
Title     : <None>
IP        : 151.101.132.193
Country   : UNITED STATES, US

Summary   : Access-Control-Allow-Methods[GET, OPTIONS], HTTPServer[cat factory 1.0], RedirectLocation[https://imgur.com/], Strict-Transport-Security[max-age=300], UncommonHeaders[retry-after,x-served-by,x-cache-hits,x-timer,access-control-allow-methods,access-control-allow-origin]

Detected Plugins:
[ Access-Control-Allow-Methods ]
	Specifies the method or methods allowed when accessing a 
	resource 
.....
```

{% endcode %}

Respuesta: `cat factory 1.0`

***

## <mark style="color:purple;">Pregunta 4</mark>

Realiza una enumeración de subdominios en el host `githubapp.com`. ¿Qué subdominio tiene la palabra "`triage`" en el nombre?

```shell-session
afsh4ck@kali$ subfinder -d githubapp.com | grep triage

               __    _____           __         
   _______  __/ /_  / __(_)___  ____/ /__  _____
  / ___/ / / / __ \/ /_/ / __ \/ __  / _ \/ ___/
 (__  ) /_/ / /_/ / __/ / / / / /_/ /  __/ /    
/____/\__,_/_.___/_/ /_/_/ /_/\__,_/\___/_/

		projectdiscovery.io

[INF] Current subfinder version v2.6.0 (outdated)
[INF] Loading provider config from /home/kali/.config/subfinder/provider-config.yaml
[INF] Enumerating subdomains for githubapp.com
[INF] Found 149 subdomains for githubapp.com in 15 seconds 367 milliseconds

data-triage-reports.githubapp.com
```

Respuesta: `data-triage-reports.githubapp.com`
