
# Rainbow Table

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Que es Rainbow Table</mark>

Las contraseñas de un sistema informático no se almacenan como texto sin formato, sino como valores con hash (valores numéricos que identifican datos de forma única). Un rainbow table es un gran diccionario de valores hash precalculados y las contraseñas a partir de las cuales se calcularon.

A diferencia de un ataque de fuerza bruta que tiene que calcular cada hash, un ataque de arco iris compara el hash de una contraseña con los almacenados en la tabla rainbow. Cuando un atacante encuentra una coincidencia, identifica la contraseña utilizada para crear el hash.

Este ataque se basa en comparar los hashes que equivalen a las contraseñas, que siempre tienen un formato alfanumérico, lo que aumenta la velocidad de crackeo.

```
PASS + ESSID AP = PMK
```

El PMK va a ser comparado con el handshake y si es válido es la contraseña correcta.

<table><thead><tr><th width="209">Contraseña</th><th>Hash</th></tr></thead><tbody><tr><td>password123</td><td>5f4dcc3b5aa765d61d8327deb882cf99</td></tr><tr><td>123456</td><td>e10adc3949ba59abbe56e057f20f883e</td></tr><tr><td>qwerty</td><td>d8578edf8458ce06fbc5bb76a58c5ca4</td></tr><tr><td>abc123</td><td>e99a18c428cb38d5f260853678922e03</td></tr><tr><td>letmein</td><td>0d107d09f5bbe40cade3de5c71e9e9b7</td></tr><tr><td>admin</td><td>21232f297a57a5a743894a0e4a801fc3</td></tr></tbody></table>

## <mark style="color:purple;">1. Crear base de datos con la wordlist</mark>

```bash
airolib-ng wpa-bd --import passwd <WORDLIST>
airolib-ng wpa-bd --import essid <NOMBRE-TARGET>
```

## <mark style="color:purple;">2. Crear diccionario PMK</mark>

```bash
airolib-ng wpa-bd --batch
```

## <mark style="color:purple;">3. Cracking con aircrack</mark>

```
aircrack-ng -r wpa-bd handshake.cap
```
