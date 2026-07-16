
# Ataques Híbridos

Muchas organizaciones implementan políticas que exigen a los usuarios cambiar sus contraseñas periódicamente para mejorar la seguridad. Sin embargo, estas políticas pueden generar, sin querer, patrones de contraseña predecibles si los usuarios no reciben la formación adecuada sobre la higiene de contraseñas.

![Diagrama que muestra la contraseña original 'Summer2023' modificada a 'Summer2023!' y 'Summer2024'.](https://academy.hackthebox.com/storage/modules/57/2n.png)

Lamentablemente, una práctica generalizada e insegura entre los usuarios es realizar pequeñas modificaciones en sus contraseñas cuando se ven obligados a cambiarlas. Esto suele manifestarse añadiendo un número o un carácter especial al final de la contraseña actual. Por ejemplo, un usuario podría tener una contraseña inicial como "`Summer2023`" y luego, cuando se le solicite actualizarla, cambiarla a "`¡Summer2023!`" o "`Summer2024`".

Este comportamiento predecible crea una vulnerabilidad que los ataques híbridos pueden explotar sin piedad. Los atacantes aprovechan esta tendencia humana empleando técnicas sofisticadas que combinan las ventajas de los ataques de diccionario y de fuerza bruta, lo que aumenta drásticamente la probabilidad de vulnerar contraseñas.

## <mark style="color:purple;">Ataques híbridos en acción</mark>

Ilustremos esto con un ejemplo práctico. Imaginemos un atacante que ataca a una organización conocida por exigir cambios de contraseñas regulares.

![Diagrama de flujo que muestra el proceso de ataque de contraseña: la organización objetivo utiliza contraseñas comunes y términos de la industria; el atacante realiza reconocimiento, ataque de diccionario y fuerza bruta contra las cuentas de usuario.](https://academy.hackthebox.com/storage/modules/57/3n.png)

El atacante comienza lanzando un ataque de diccionario, utilizando una lista de palabras seleccionada con contraseñas comunes, términos específicos del sector y, posiblemente, información personal relacionada con la organización o sus empleados. Esta fase intenta identificar rápidamente cualquier objetivo fácil: cuentas protegidas por contraseñas débiles o fáciles de adivinar.

Sin embargo, si el ataque de diccionario no tiene éxito, el ataque híbrido pasa sin problemas a un modo de fuerza bruta. En lugar de generar combinaciones de contraseñas aleatorias, modifica estratégicamente las palabras de la lista original, añadiendo números, caracteres especiales o incluso incrementando los años, como en nuestro ejemplo "Summer 2023".

Este enfoque de fuerza bruta dirigido reduce drásticamente el espacio de búsqueda en comparación con un ataque de fuerza bruta tradicional y al mismo tiempo cubre muchas variaciones potenciales de contraseña que los usuarios podrían emplear para cumplir con la política de cambio de contraseña.

## <mark style="color:purple;">El poder de los ataques híbridos</mark>

La eficacia de los ataques híbridos reside en su adaptabilidad y eficiencia. Aprovechan las ventajas de las técnicas de diccionario y fuerza bruta, maximizando las posibilidades de descifrar contraseñas, especialmente en escenarios donde los usuarios siguen patrones predecibles.

Es importante tener en cuenta que los ataques híbridos no se limitan al escenario de cambio de contraseña descrito anteriormente. Pueden adaptarse para explotar cualquier patrón de contraseña observado o sospechoso dentro de la organización objetivo. Consideremos un escenario en el que se tiene acceso a una lista de palabras de contraseñas comunes y se ataca a una organización con la siguiente política de contraseñas:

* Longitud mínima: 8 caracteres
* Debe incluir:
  * Al menos una letra mayúscula
  * Al menos una letra minúscula
  * Al menos un número

### Adaptar una wordlist a políticas de contraseñas

Para extraer únicamente las contraseñas que cumplen con esta política, podemos aprovechar las potentes herramientas de línea de comandos disponibles por defecto en la mayoría de los sistemas Linux/Unix, específicamente `grep` en combinación con expresiones regulares. Para ello, usaremos la lista de contraseñas [darkweb2017-top10000.txt.](https://github.com/danielmiessler/SecLists/blob/master/Passwords/darkweb2017-top10000.txt) Primero, descargue la lista de palabras.

```shell-session
afsh4ck@kali$ wget https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/darkweb2017-top10000.txt
```

A continuación, debemos comenzar a hacer coincidir esa lista de palabras con la política de contraseñas.

```shell-session
afsh4ck@kali$ grep -E '^.{8,}$' darkweb2017-top10000.txt > darkweb2017-minlength.txt
```

Este comando inicial `grep` cumple con el requisito principal de la política: una contraseña con una longitud mínima de 8 caracteres. La expresión regular `^.{8,}$` actúa como filtro, garantizando que solo las contraseñas con al menos 8 caracteres se filtren y se guarden en un archivo temporal llamado `darkweb2017-minlength.txt`.

```shell-session
afsh4ck@kali$ grep -E '[A-Z]' darkweb2017-minlength.txt > darkweb2017-uppercase.txt
```

Basándose en el filtro anterior, este comando `grep` aplica la exigencia de la política de incluir al menos una letra mayúscula. La expresión regular `[A-Z]` garantiza que cualquier contraseña que no contenga una letra mayúscula se descarte, refinando aún más la lista guardada en `darkweb2017-uppercase.txt`.

```shell-session
afsh4ck@kali$ grep -E '[a-z]' darkweb2017-uppercase.txt > darkweb2017-lowercase.txt
```

Este comando, que mantiene la cadena de filtrado con `grep`, garantiza el cumplimiento del requisito de la política de incluir al menos una letra minúscula. La expresión regular `[a-z]` actúa como filtro, conservando únicamente las contraseñas que incluyen al menos una letra minúscula y almacenándolas en `darkweb2017-lowercase.txt`.

```shell-session
afsh4ck@kali$ grep -E '[0-9]' darkweb2017-lowercase.txt > darkweb2017-number.txt
```

Este último comando `grep` cumple con el requisito numérico de la política. La expresión regular `[0-9]`actúa como filtro, garantizando que las contraseñas que contengan al menos un dígito numérico se conserven en `darkweb2017-number.txt`.

```shell-session
afsh4ck@kali$ wc -l darkweb2017-number.txt

89 darkweb2017-number.txt
```

Como se muestra en el resultado anterior, el filtrado meticuloso de la extensa lista de 10 000 contraseñas con la política de contraseñas ha reducido drásticamente nuestras posibles contraseñas a 89. Esta drástica reducción del espacio de búsqueda representa una mejora significativa en la eficiencia para cualquier intento posterior de descifrado de contraseñas. Una lista más pequeña y específica se traduce en un ataque más rápido y focalizado, optimizando el uso de recursos computacionales y aumentando la probabilidad de una vulneración exitosa.

## <mark style="color:purple;">Robo de credenciales</mark>

### Aprovechar datos robados para obtener acceso no autorizado

![Diagrama de flujo que muestra fuentes de credenciales, como violaciones de datos y phishing, que conducen a acciones de los atacantes como la adquisición de credenciales y acceso no autorizado, lo que resulta en el robo de datos y fraude de identidad.](https://academy.hackthebox.com/storage/modules/57/5n.png)

Los ataques de robo de credenciales se aprovechan de la desafortunada realidad de que muchos usuarios reutilizan sus contraseñas en varias cuentas en línea. Esta práctica generalizada, a menudo impulsada por la comodidad y la dificultad de gestionar numerosas credenciales únicas, crea un terreno fértil para que los atacantes la exploten.

Se trata de un proceso de varias etapas que comienza con la obtención por parte de los atacantes de listas de nombres de usuario y contraseñas comprometidos. Estas listas pueden provenir de filtraciones de datos a gran escala o compilarse mediante estafas de phishing y malware. Cabe destacar que las listas de palabras disponibles públicamente, como `rockyou`las que se encuentran en \[nombre `seclists`del usuario], también pueden servir como punto de partida, ofreciendo a los atacantes un conjunto de contraseñas de uso común.

Una vez armados con estas credenciales, los atacantes identifican objetivos potenciales: servicios en línea probablemente utilizados por las personas cuya información poseen. Las redes sociales, los proveedores de correo electrónico, la banca en línea y los sitios de comercio electrónico son objetivos prioritarios debido a la información confidencial que suelen contener.

El ataque pasa entonces a una fase automatizada. Los atacantes utilizan herramientas o scripts para probar sistemáticamente las credenciales robadas con los objetivos seleccionados, a menudo imitando el comportamiento normal del usuario para evitar ser detectados. Esto les permite probar rápidamente un gran número de credenciales, aumentando sus posibilidades de encontrar una coincidencia.

Una coincidencia exitosa otorga acceso no autorizado, lo que facilita diversas actividades maliciosas, desde robo de datos y fraude de identidad hasta delitos financieros. La cuenta comprometida puede ser una plataforma para nuevos ataques, la propagación de malware o la infiltración en los sistemas conectados.

### El problema de la reutilización de contraseñas

El problema principal que impulsa el éxito del robo de credenciales es la práctica generalizada de reutilizar contraseñas. Cuando los usuarios usan la misma contraseña o contraseñas similares para varias cuentas, una brecha en una plataforma puede tener un efecto dominó, comprometiendo muchas otras cuentas. Esto pone de relieve la urgente necesidad de contraseñas sólidas y únicas para cada servicio en línea, junto con medidas de seguridad proactivas como la autenticación multifactor.
