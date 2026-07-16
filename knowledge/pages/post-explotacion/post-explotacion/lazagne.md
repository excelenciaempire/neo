
# LaZagne

{% embed url="<https://github.com/AlessandroZ/LaZagne>" %}

{% hint style="danger" %}
**Nota:**  Esta herramienta se debe utilizar de manera ética y legal, ya que el acceso no autorizado a contraseñas o datos puede ser ilegal y está en contra de las políticas y leyes de muchos lugares.
{% endhint %}

<figure><img src="/files/qWPHd07Ua6bKw8Cmnp28" alt=""><figcaption></figcaption></figure>

## Opciones

```bash
❯ python3 laZagne.py
usage: laZagne.py [-h] [--version]
                  {all,chats,sysadmin,databases,mails,memory,wifi,browsers,wallet,git,unused}
                  ...

|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|

positional arguments:
  {all,chats,sysadmin,databases,mails,memory,wifi,browsers,wallet,git,unused}
                        Choose a main command
    all                 Run all modules
    chats               Run chats module
    sysadmin            Run sysadmin module
    databases           Run databases module
    mails               Run mails module
    memory              Run memory module
    wifi                Run wifi module
    browsers            Run browsers module
    wallet              Run wallet module
    git                 Run git module
    unused              Run unused module

options:
  -h, --help            show this help message and exit
  --version             laZagne version

```

## Uso

<table><thead><tr><th width="323">Comando</th><th>Descripción</th></tr></thead><tbody><tr><td><code>python laZagne.py all</code></td><td>Ejecutar todos los módulos disponibles para recuperar contraseñas</td></tr><tr><td><code>python laZagne.py all -vv</code></td><td>Modo verbose</td></tr><tr><td><code>python laZagne.py browsers</code></td><td>Recuperar contraseñas almacenadas en navegadores web</td></tr><tr><td><code>python laZagne.py ftp</code></td><td>Recuperar contraseñas de clientes FTP</td></tr><tr><td><code>python laZagne.py ssh</code></td><td>Recuperar contraseñas SSH almacenadas</td></tr><tr><td><code>python laZagne.py windows</code></td><td>Recuperar contraseñas de cuentas de usuario de Windows</td></tr><tr><td><code>python laZagne.py wifi</code></td><td>Recuperar contraseñas de redes Wi-Fi almacenadas</td></tr><tr><td><code>python laZagne.py all -oN output.txt</code></td><td>Guardar la salida en un archivo específico</td></tr><tr><td><p><code>python laZagne.py all</code> </p><p><code>-password UserPassw0rd</code></p></td><td>Para descifrar las credenciales del dominio, se puede hacer especificando la contraseña de Windows del usuario</td></tr><tr><td><code>python laZagne.py all -i</code></td><td>Modo interactivo</td></tr><tr><td><code>python laZagne.py all -quiet -oA</code></td><td>Modo silencioso (no se imprimirá nada en la salida estándar)</td></tr></tbody></table>
