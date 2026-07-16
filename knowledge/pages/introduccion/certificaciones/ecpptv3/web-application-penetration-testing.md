
# Web Application Penetration Testing

## <mark style="color:$primary;">Cheatsheet</mark>

### **Nikto | Web Server Vulnerability Scanning**

{% content-ref url="/pages/VPSl5TXmq4XV3PrKyeFJ" %}
[Análisis de vulnerabilidades](/ethical-hacking-cheatsheet/analisis-de-vulnerabilidades/analisis-de-vulnerabilidades.md)
{% endcontent-ref %}

| Comando                                      | Qué hace                                           |
| -------------------------------------------- | -------------------------------------------------- |
| `nikto -h TARGET`                            | Realiza un escaneo general de vulnerabilidades web |
| `nikto -h TARGET -o nikto.html -Format html` | Exporta los resultados del escaneo en formato HTML |

***

### **GoBuster | File & Directory Enumeration**

{% content-ref url="/pages/zIAtmEU0cp7fFcQmTGan" %}
[Fuzzing](/ethical-hacking-cheatsheet/recopilacion-de-informacion/fuzzing.md)
{% endcontent-ref %}

{% content-ref url="/pages/BCt1x9j4Sf2NG3MCMhZJ" %}
[Gobuster](/ethical-hacking-cheatsheet/recopilacion-de-informacion/fuzzing/gobuster.md)
{% endcontent-ref %}

| Comando                                           | Qué hace                                          |
| ------------------------------------------------- | ------------------------------------------------- |
| `gobuster dir -u TARGET -w wordlist`              | Enumeración de archivos y directorios             |
| `gobuster dir -u TARGET -w wordlist -b 403,404`   | Filtra resultados por códigos HTTP (ej. 403, 404) |
| `gobuster dir -u TARGET -w wordlist -x .php,.txt` | Filtra por extensiones de archivos                |
| `gobuster dir -u TARGET -w wordlist -r`           | Sigue redirecciones HTTP automáticamente          |

***

### **OWASP Amass | Automated Recon**

| Comando                                                      | Qué hace                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------- |
| `amass enum -d TARGET`                                       | Enumeración de subdominios                                    |
| `amass enum -passive -d TARGET`                              | Enumeración pasiva de subdominios                             |
| `amass enum -passive -d TARGET -src -dir PathToOutputFolder` | Muestra fuentes de datos y guarda resultados en un directorio |

***

### **Wordpress**

{% content-ref url="/pages/N3Dg6Gd8W9TwD1JQNYEI" %}
[Wordpress - Enumeración](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-a-aplicaciones-web/ataques-a-cms/wordpress-enumeracion.md)
{% endcontent-ref %}

{% content-ref url="/pages/PEWsAHu0BFRMpR9FBnC6" %}
[Wordpress - Ataques](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/ataques-a-aplicaciones-web/ataques-a-cms/wordpress-ataques.md)
{% endcontent-ref %}

| Comando                                                                               | Qué hace                                               |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `wpscan --url TARGET`                                                                 | Enumeración básica                                     |
| `wpscan --url TARGET --enumerate p --plugins-detection aggressive`                    | Enumeración de plugins                                 |
| `wpscan --url TARGET --enumerate p --plugins-detection aggressive --api-token APIKEY` | Enumeración de plugins + detección de vulnerabilidades |

***

### **OWASP ZAP | SQLi**

{% content-ref url="/pages/ztuMrmFRs2u0HYX8NFjb" %}
[Zap Fuzzer](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/web-proxies/zap-fuzzer.md)
{% endcontent-ref %}

| Comando / Pasos                                          | Qué hace                                |
| -------------------------------------------------------- | --------------------------------------- |
| Abrir OWASP ZAP y hacer clic en el icono del navegador   | Inicia el proxy con navegador integrado |
| Cargar el sitio objetivo en el navegador                 | Permite interceptar peticiones          |
| En “Sites”, clic derecho → `Attack` → `Fuzz`             | Prepara ataque de fuzzing               |
| Editar → eliminar valor del parámetro → guardar          | Define punto de inyección               |
| Seleccionar espacio del parámetro → `Add`                | Añade punto de fuzz                     |
| File Fuzzers → `jbrofuzz` → SQL Injection → Start Fuzzer | Ejecuta fuzzing SQLi automatizado       |
| Revisar “`Reflected`” en Fuzzer                          | Detecta posibles vulnerabilidades       |

***

### **SQLMap**

{% content-ref url="/pages/Vmwan4ozoYs6b29MDC10" %}
[SQLMap](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-web/sql-injection/sqlmap.md)
{% endcontent-ref %}

| Comando                                                                              | Qué hace                                             |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| `sqlmap -u TARGETURL --data "PARAMETERNAME" -p PARAMETERNAME --method POST/GET`      | Intenta detectar SQLi                                |
| `sqlmap -r REQUESTFILE -p PARAMETERNAME --technique=E`                               | Usa petición capturada (Burp) con técnica específica |
| `sqlmap -r REQUESTFILE -p PARAMETERNAME --technique=E --current-db`                  | Muestra la base de datos actual                      |
| `sqlmap -r REQUESTFILE -p PARAMETERNAME --technique=E -D DBNAME --tables`            | Lista tablas de la base de datos                     |
| `sqlmap -r REQUESTFILE -p PARAMETERNAME --technique=E -D DBNAME -T TABLENAME --dump` | Extrae datos de una tabla                            |
| `sqlmap -r REQUESTFILE -p PARAMETERNAME --technique=E --current-user`                | Muestra el usuario actual de la BD                   |

## <mark style="color:$primary;">Secciones</mark>

{% content-ref url="/pages/w7sv9DJZA3xUzmYUsSYa" %}
[Recopilación de información pasiva](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/web-application-penetration-testing/recopilacion-de-informacion-pasiva.md)
{% endcontent-ref %}

{% content-ref url="/pages/oSrRZuVPFXTWvg8QBBpW" %}
[Recopilación de información activa](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/web-application-penetration-testing/recopilacion-de-informacion-activa.md)
{% endcontent-ref %}

{% content-ref url="/pages/hyPEXKdMF9eRxCHam3Gb" %}
[Vulnerabilidades Web](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/web-application-penetration-testing/vulnerabilidades-web.md)
{% endcontent-ref %}

{% content-ref url="/pages/2YZtSUbjozC9Cy31Sv8u" %}
[Web Application Penetration Testing CTF 2](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/web-application-penetration-testing/web-application-penetration-testing-ctf-2.md)
{% endcontent-ref %}
