
# Password Attacks

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir contraseñas de un usuario y acceder a sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo o en un entorno controlado.
{% endhint %}

## <mark style="color:purple;">Autenticación</mark>

La autenticación, en esencia, es la validación de la identidad presentando una combinación de tres factores principales a un mecanismo de validación:

1. Algo que sabes (una contraseña, código de acceso, pin, etc.).
2. Algo que tienes (una tarjeta de identificación, una clave de seguridad u otras herramientas MFA).
3. Algo que eres (tu yo físico, nombre de usuario, dirección de correo electrónico u otros identificadores).

***

## <mark style="color:purple;">Almacenamiento de credenciales</mark>

Cada aplicación que admite mecanismos de autenticación compara las entradas/credenciales proporcionadas con bases de datos locales o remotas. En el caso de bases de datos locales, estas credenciales se almacenan localmente en el sistema. Las aplicaciones web suelen ser vulnerables a las inyecciones de SQL, lo que puede llevar al peor de los casos a que los atacantes vean la totalidad de los datos de una organización en texto sin formato.

Hay muchas listas de palabras diferentes que contienen las contraseñas más utilizadas. Un ejemplo de una de estas listas es `rockyou.txt`. Esta lista incluye alrededor de 14 millones de contraseñas únicas y se creó después de una violación de datos de la empresa RockYou, que contenía un total de 32 millones de cuentas de usuario. La empresa RockYou almacenó todas las credenciales en texto plano en su base de datos, que los atacantes podían ver después de un ataque exitoso de inyección SQL.

También sabemos que todos los sistemas operativos admiten este tipo de mecanismos de autenticación. Por tanto, las credenciales almacenadas se almacenan localmente. Veamos con más detalle cómo se crean, almacenan y administran los sistemas basados ​​en Windows y Linux.

***

## <mark style="color:purple;">Linux</mark>

Como ya sabemos, los sistemas basados ​​en Linux manejan todo en forma de archivo. En consecuencia, las contraseñas también se almacenan cifradas en un archivo. Este archivo se llama `shadow` y se encuentra `/etc/shadow` y forma parte del sistema de gestión de usuarios de Linux. Además, estas contraseñas suelen almacenarse en formato `hashes`. Un ejemplo puede verse así:

### **Archivo etc/shadow**

```shell-session
root@kali:~# cat /etc/shadow

...SNIP...
htb-student:$y$j9T$3QSBB6CbHEu...SNIP...f8Ms:18955:0:99999:7:::
```

El archivo `/etc/shadow` tiene un formato único en el que las entradas se ingresan y guardan cuando se crean nuevos usuarios.

<table><thead><tr><th width="163"></th><th width="314"></th><th width="161"></th><th></th><th></th><th width="135"></th><th width="162"></th><th width="139"></th><th></th></tr></thead><tbody><tr><td>htb-student:</td><td>$y$j9T$3QSBB6CbHEu...SNIP...f8Ms:</td><td>18955:</td><td>0:</td><td>99999:</td><td>7:</td><td>:</td><td>:</td><td>:</td></tr><tr><td><code>&#x3C;username></code>:</td><td><code>&#x3C;Contraseña encriptada></code>:</td><td><code>&#x3C;Último día de cambio></code>:</td><td><code>&#x3C;min age></code>:</td><td><code>&#x3C;max age></code>:</td><td><code>&#x3C;tiempo de aviso></code>:</td><td><code>&#x3C;periodo inactividad></code>:</td><td><code>&#x3C;fecha de expiración></code>:</td><td><code>&#x3C;campo reservado></code></td></tr></tbody></table>

El cifrado de la contraseña en este archivo tiene el siguiente formato:

<table><thead><tr><th width="140"></th><th width="139"></th><th></th></tr></thead><tbody><tr><td><code>$ &#x3C;id></code></td><td><code>$ &#x3C;salt></code></td><td><code>$ &#x3C;hashed></code></td></tr><tr><td><code>$ y</code></td><td><code>$ j9T</code></td><td><code>$ 3QSBB6CbHEu...SNIP...f8Ms</code></td></tr></tbody></table>

El tipo (`id`) es el método hash criptográfico utilizado para cifrar la contraseña. En el pasado se utilizaron muchos métodos hash criptográficos diferentes y algunos sistemas todavía los utilizan en la actualidad.

| **ID**   | **Cryptographic Hash Algorithm**                                      |
| -------- | --------------------------------------------------------------------- |
| `$1$`    | [MD5](https://en.wikipedia.org/wiki/MD5)                              |
| `$2a$`   | [Blowfish](https://en.wikipedia.org/wiki/Blowfish_\(cipher\))         |
| `$5$`    | [SHA-256](https://en.wikipedia.org/wiki/SHA-2)                        |
| `$6$`    | [SHA-512](https://en.wikipedia.org/wiki/SHA-2)                        |
| `$sha1$` | [SHA1crypt](https://en.wikipedia.org/wiki/SHA-1)                      |
| `$y$`    | [Yescrypt](https://github.com/openwall/yescrypt)                      |
| `$gy$`   | [Gost-yescrypt](https://www.openwall.com/lists/yescrypt/2019/06/30/1) |
| `$7$`    | [Scrypt](https://en.wikipedia.org/wiki/Scrypt)                        |

Sin embargo, algunos archivos más pertenecen al sistema de gestión de usuarios de Linux. Los otros dos archivos son `/etc/passwd` y `/etc/group`. En el pasado, la contraseña cifrada se almacenaba junto con el nombre de usuario en el archivo `/etc/passwd`, pero esto se reconocía cada vez más como un problema de seguridad porque todos los usuarios del sistema pueden ver el archivo y debe ser legible. El archivo `/etc/shadow` sólo puede ser leído por el usuario `root`.

### **Archivo etc/passwd**

```shell-session
afsh4ck@kali$ cat /etc/passwd

...SNIP...
htb-student:x:1000:1000:,,,:/home/htb-student:/bin/bash
```

<table><thead><tr><th width="163"></th><th width="151"></th><th></th><th></th><th width="140"></th><th width="143"></th><th width="202"></th></tr></thead><tbody><tr><td><code>htb-student:</code></td><td><code>x:</code></td><td><code>1000:</code></td><td><code>1000:</code></td><td><code>,,,:</code></td><td><code>/home/htb-student:</code></td><td><code>/bin/bash</code></td></tr><tr><td><code>&#x3C;username>:</code></td><td><code>&#x3C;password>:</code></td><td><code>&#x3C;uid>:</code></td><td><code>&#x3C;gid>:</code></td><td><code>&#x3C;comment>:</code></td><td><code>&#x3C;home directory>:</code></td><td><code>&#x3C;cmd executed after logging in></code></td></tr></tbody></table>

El campo `x` de contraseña indica que la contraseña cifrada está en el archivo `/etc/shadow`. Sin embargo, la redirección al archivo `/etc/shadow` no hace que los usuarios del sistema sean invulnerables porque si los derechos de este archivo se configuran incorrectamente, el archivo puede manipularse de modo que el usuario `root` no necesite escribir una contraseña para iniciar sesión. El campo vacío significa que podemos iniciar sesión con el nombre de usuario sin ingresar una contraseña.

* [Autenticación de usuario de Linux](https://tldp.org/HOWTO/pdf/User-Authentication-HOWTO.pdf)

***

## <mark style="color:purple;">Windows</mark>

El [proceso de autenticación de clientes de Windows](https://docs.microsoft.com/en-us/windows-server/security/windows-authentication/credentials-processes-in-windows-authentication) a menudo puede ser más complicado que con los sistemas Linux y consta de muchos módulos diferentes que realizan todos los procesos de inicio de sesión, recuperación y verificación. Además, existen muchos procedimientos de autenticación diferentes y complejos en sistemas Windows, como la autenticación Kerberos. La [Autoridad de Seguridad Local](https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/configuring-additional-lsa-protection) (`LSA`) es un subsistema protegido que autentica a los usuarios y los registra en la computadora local. Además, la LSA mantiene información sobre todos los aspectos de la seguridad local en una computadora. También proporciona varios servicios para traducir entre nombres e identificaciones de seguridad ( `SIDs`).

El subsistema de seguridad realiza un seguimiento de las políticas y cuentas de seguridad que residen en un sistema informático. En el caso de un Controlador de Dominio, estas políticas y cuentas se aplican al dominio donde se encuentra el Controlador de Dominio. Estas políticas y cuentas se almacenan en Active Directory. Además, el subsistema LSA proporciona servicios para verificar el acceso a objetos, verificar los permisos de los usuarios y generar mensajes de monitoreo.

### **Diagrama del proceso de autenticación de Windows**

![](https://academy.hackthebox.com/storage/modules/147/Auth_process1.png)

El inicio de sesión interactivo local se realiza mediante la interacción entre el proceso de inicio de sesión ( [WinLogon](https://www.microsoftpressstore.com/articles/article.aspx?p=2228450\&seqNum=8) ), el proceso de interfaz de usuario de inicio de sesión (`LogonUI`), los proveedores de credenciales, `LSASS`, uno o más `paquetes de autenticación` y `SAM` o `Active Directory`. Los paquetes de autenticación, en este caso, son las bibliotecas de vínculos dinámicos (`DLL`) que realizan comprobaciones de autenticación. Por ejemplo, para inicios de sesión interactivos y no unidos a un dominio, se utiliza el paquete de autenticación `Msv1_0.dll`

`Winlogon` es un proceso confiable responsable de gestionar las interacciones de los usuarios relacionadas con la seguridad. Éstas incluyen:

* Iniciar LogonUI para ingresar contraseñas al iniciar sesión
* Cambiar contraseñas
* Bloquear y desbloquear la estación de trabajo

Depende de los proveedores de credenciales instalados en el sistema para obtener el nombre de cuenta o la contraseña de un usuario. Los proveedores de credenciales son objetos `COM` que se encuentran en archivos DLL.

Winlogon es el único proceso que intercepta las solicitudes de inicio de sesión desde el teclado enviadas mediante un mensaje RPC desde Win32k.sys. Winlogon inicia inmediatamente la aplicación LogonUI al iniciar sesión para mostrar la interfaz de usuario para iniciar sesión. Después de que Winlogon obtiene un nombre de usuario y una contraseña de los proveedores de credenciales, llama a LSASS para autenticar al usuario que intenta iniciar sesión.

### **LSASS**

[Local Security Authority Subsystem Service](https://en.wikipedia.org/wiki/Local_Security_Authority_Subsystem_Service) (`LSASS`) es una colección de muchos módulos y tiene acceso a todos los procesos de autenticación que se pueden encontrar en `%SystemRoot%\System32\Lsass.exe`. Este servicio es responsable de la política de seguridad del sistema local, la autenticación de usuarios y el envío de registros de auditoría de seguridad al archivo `Event log`. En otras palabras, es la bóveda para los sistemas operativos basados ​​en Windows, y podemos encontrar una ilustración más detallada de la arquitectura LSASS [aquí](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-2000-server/cc961760\(v=technet.10\)?redirectedfrom=MSDN) .

<table data-header-hidden><thead><tr><th width="175"></th><th></th></tr></thead><tbody><tr><td><strong>Paquetes de autenticación</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>Lsasrv.dll</code></td><td>El servicio LSA Server aplica políticas de seguridad y actúa como administrador de paquetes de seguridad para LSA. El LSA contiene la función Negociar, que selecciona el protocolo NTLM o Kerberos después de determinar qué protocolo tendrá éxito.</td></tr><tr><td><code>Msv1_0.dll</code></td><td>Paquete de autenticación para inicios de sesión en máquinas locales que no requieren autenticación personalizada.</td></tr><tr><td><code>Samsrv.dll</code></td><td>El Administrador de cuentas de seguridad (SAM) almacena cuentas de seguridad locales, aplica políticas almacenadas localmente y admite API.</td></tr><tr><td><code>Kerberos.dll</code></td><td>Paquete de seguridad cargado por LSA para la autenticación basada en Kerberos en una máquina.</td></tr><tr><td><code>Netlogon.dll</code></td><td>Servicio de inicio de sesión basado en red.</td></tr><tr><td><code>Ntdsa.dll</code></td><td>Esta biblioteca se utiliza para crear nuevos registros y carpetas en el registro de Windows.</td></tr></tbody></table>

Fuente: [Documentos de Microsoft](https://docs.microsoft.com/en-us/windows-server/security/windows-authentication/credentials-processes-in-windows-authentication) .

Cada sesión de inicio de sesión interactiva crea una instancia separada del servicio Winlogon. La arquitectura [de identificación y autenticación gráfica](https://docs.microsoft.com/en-us/windows/win32/secauthn/gina) ( `GINA`) se carga en el área de proceso utilizada por Winlogon, recibe y procesa las credenciales e invoca las interfaces de autenticación a través de la función [LSALogonUser](https://docs.microsoft.com/en-us/windows/win32/api/ntsecapi/nf-ntsecapi-lsalogonuser) .

### **Base de datos SAM**

El [Security Account Manager](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc756748\(v=ws.10\)?redirectedfrom=MSDN) (`SAM`) es un archivo de base de datos en los sistemas operativos Windows que almacena las contraseñas de los usuarios. Se puede utilizar para autenticar usuarios locales y remotos. SAM utiliza medidas criptográficas para evitar que usuarios no autenticados accedan al sistema. Las contraseñas de usuario se almacenan en formato hash en una estructura de registro como `LM`hash o `NTLM`hash. Este archivo se encuentra en la ruta `%SystemRoot%/system32/config/SAM` y está montado en HKLM/SAM. Se requieren permisos a nivel de SISTEMA para verlo.

Los sistemas Windows se pueden asignar a un grupo de trabajo o a un dominio durante la instalación. Si el sistema ha sido asignado a un grupo de trabajo, maneja la base de datos SAM localmente y almacena a todos los usuarios existentes localmente en esta base de datos. Sin embargo, si el sistema se ha unido a un dominio, el Controlador de Dominio ( `DC`) debe validar las credenciales de la base de datos de Active Directory ( `ntds.dit`), que está almacenada en `%SystemRoot%\ntds.dit`.

Microsoft introdujo una característica de seguridad en Windows NT 4.0 para ayudar a mejorar la seguridad de la base de datos SAM contra el pirateo de software fuera de línea. Esta es la característica `SYSKEY`( `syskey.exe`), que, cuando está habilitada, cifra parcialmente la copia del disco duro del archivo SAM para que los valores hash de contraseña para todas las cuentas locales almacenadas en el SAM se cifren con una clave.

### **Administrador de Credenciales**

![](https://academy.hackthebox.com/storage/modules/147/authn_credman_credprov.png)

Fuente: [Documentos de Microsoft](https://docs.microsoft.com/en-us/windows-server/security/windows-authentication/credentials-processes-in-windows-authentication) .

Credential Manager es una función integrada en todos los sistemas operativos Windows que permite a los usuarios guardar las credenciales que utilizan para acceder a diversos recursos de red y sitios web. Las credenciales guardadas se almacenan según los perfiles de usuario en el archivo `Credential Locker`. Las credenciales se cifran y almacenan en la siguiente ubicación:

```powershell
PS C:\Users\[Username]\AppData\Local\Microsoft\[Vault/Credentials]\
```

Existen varios métodos para descifrar las credenciales guardadas con Credential Manager. Practicaremos con algunos de estos métodos en este módulo.

### **NTDS**

Es muy común encontrarnos con entornos de red donde los sistemas Windows están unidos a un dominio de Windows. Esto es común porque facilita a los administradores la gestión de todos los sistemas propiedad de sus respectivas organizaciones (administración centralizada). En estos casos, los sistemas Windows enviarán todas las solicitudes de inicio de sesión a controladores de dominio que pertenecen al mismo bosque de Active Directory. Cada controlador de dominio aloja un archivo llamado `NTDS.dit` que se mantiene sincronizado en todos los controladores de dominio con la excepción de [los controladores de dominio de solo lectura](https://docs.microsoft.com/en-us/windows/win32/ad/rodc-and-active-directory-schema) . NTDS.dit es un archivo de base de datos que almacena los datos en Active Directory, que incluye, entre otros:

* Cuentas de usuario (hash de nombre de usuario y contraseña)
* Cuentas grupales
* cuentas de computadora
* Objetos de política de grupo

Practicaremos métodos que nos permitan extraer credenciales del archivo NTDS.dit más adelante en este módulo.

Ahora que hemos repasado los conceptos de almacenamiento de credenciales, estudiemos los diversos ataques que podemos realizar para extraer credenciales y ampliar nuestro acceso durante las evaluaciones.
