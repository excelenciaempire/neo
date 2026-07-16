
# Broker

<figure><img src="/files/3o4cIduLkt096E7hxE04" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Accedemos a la IP `10.10.11.243` a través del navegador. Nos aparece un login que si accedemos con admin / admin nos deja entrar:

<figure><img src="/files/eOOrP7xlM9hp53M2eqVK" alt=""><figcaption></figcaption></figure>

También encontramos algo de documentación sobre el sistema ActiveMQ:

{% embed url="<https://activemq.apache.org/>" %}

Con una búsqueda simple de exploits en searchsploit encontramos alguno que puede que nos sirva:

<figure><img src="/files/1K0UQQOW2OxyD70XAF1P" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escaneo con Nmap</mark>

```bash
sudo nmap -v -sS -sV -sC 10.10.11.243
```

```bash
Discovered open port 8888/tcp on 10.10.11.243
Discovered open port 80/tcp on 10.10.11.243
Discovered open port 8080/tcp on 10.10.11.243
Discovered open port 22/tcp on 10.10.11.243
Discovered open port 1300/tcp on 10.10.11.243
Discovered open port 81/tcp on 10.10.11.243
Discovered open port 1234/tcp on 10.10.11.243
Discovered open port 9999/tcp on 10.10.11.243
Discovered open port 7777/tcp on 10.10.11.243
```

Encontramos bastantes puertos abiertos.

En el puerto 81 encontramos un acceso directo a archivos del servidor, lo que puede ser un buen punto de acceso:

<figure><img src="/files/qbMTFMvfA87noYvEw7nw" alt=""><figcaption></figcaption></figure>

Si entramos a /home/activemq nos encontramos con los flags, que están juntos WTFF!

<figure><img src="/files/chvVcbuYoOmLhIaPYEtM" alt=""><figcaption></figcaption></figure>

Obtenemos los 2 flags, user y root 🏆

<figure><img src="/files/1wojAoAdpzs2sHAT8XdY" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/bzJzayKu75EmeXoHRP0y" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Vamos más allá</mark>

Esta máquina ha sido demasiado fácil, por lo que vamos a ir más allá. Podemos acceder a `/etc/shadow` y obtenemos los hashes de contraseñas de los 2 usuarios del sistema:

<figure><img src="/files/zL4NpIjTLLr1SHM2awnu" alt=""><figcaption></figcaption></figure>

Estos hashes se podrían crackear con John o Hashcat fácilmente para obtener las contraseñas:

```
root:$y$j9T$iDBjbum43YnvVKbOLNqgQ0$S0vmvHYH4M69yMjRUw2ioBEN6ElqehZQud6Lr/IQnJC:19720:0:99999:7:::
activemq:$y$j9T$5eMce1NhiF0t9/ZVwn39P1$pCfvgXtARGXPYDdn2AVdkCnXDf7YO7He/x666g6qLM5:19666:0:99999:7:::
```

## <mark style="color:purple;">Acceso SSH</mark>

De igual manera si accedemos a `/etc/ssh` nos encontramos las claves privadas para conectarnos por SSH:

<figure><img src="/files/CCbWDsyilwcRgUJzQGDs" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/RgeYowYnDjmddTsa1P6s" alt=""><figcaption></figcaption></figure>
