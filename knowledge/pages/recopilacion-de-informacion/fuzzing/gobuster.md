
# Gobuster

{% hint style="danger" %}
**Nota:** Este tipo de búsquedas son muy invasivas, ya que hacen muchas peticiones al servidor del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

<figure><img src="/files/zwTYxHZiBukmZPga1bIx" alt=""><figcaption></figcaption></figure>

Gobuster utiliza una lista de palabras clave o diccionario para buscar archivos y directorios que no están visibles a simple vista en un sitio web.

## <mark style="color:purple;">Fuzzing con Gobuster</mark>

### Fuzzing de directorios ocultos en una IP

{% hint style="info" %}
Podemos ignorar los códigos de estado usando el parámetro `-b`
{% endhint %}

```bash
gobuster dir -u https://hackthissite.org -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -b 301

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     https://hackthissite.org
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
[+] Negative Status codes:   301
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/security             (Status: 200) [Size: 361]
/robots               (Status: 200) [Size: 66]
/article_20000419     (Status: 200) [Size: 0]
/article_20000306     (Status: 200) [Size: 0]
/CHANGELOG            (Status: 403) [Size: 199]
/flag-de              (Status: 302) [Size: 272] [--> http://www.google.com/translate_c?hl=de&sl=en&u=http://www.hackthissite.org/flag]
<----SNIP---->
```

### Pantallas ocultas: (des, login..)

```bash
gobuster vhost dir -u example.com -w /usr/share/dirb/wordlists/common.txt -t 50
```

### Enumeración de subdominios

```bash
# Añadir un DNS Server como 1.1.1.1 en /etc/resolv.conf

gobuster dns -d kali.org -w /usr/share/seclists/Discovery/DNS/namelist.txt 
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Domain:     kali.org
[+] Threads:    10
[+] Timeout:    1s
[+] Wordlist:   /usr/share/seclists/Discovery/DNS/namelist.txt
===============================================================
Starting gobuster in DNS enumeration mode
===============================================================
Found: aphrodite.kali.org
Found: arm.kali.org
Found: atlas.kali.org
Found: atropos.kali.org
Found: backup.kali.org
Found: bugs.kali.org
<----SNIP---->
```

### Devolver solo peticiones con status positivo

{% code overflow="wrap" %}

```bash
gobuster dir -u example.com -w /usr/share/dirb/wordlists/directory-list-2.3-medium.txt -f -e
```

{% endcode %}
