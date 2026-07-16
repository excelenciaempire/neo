
# CeWL

{% embed url="<https://github.com/digininja/CeWL>" %}

## <mark style="color:purple;">**1. Diccionario básico**</mark>

```bash
cewl http://example.com -w pass.txt
```

Este comando generará un diccionario utilizando las palabras clave encontradas en el sitio web `http://example.com` y lo guardará en un archivo llamado `pass.txt`.

## <mark style="color:purple;">**2. Profundidad de búsqueda**</mark>

```bash
cewl http://example.com -w pass.txt -d 2
```

Utiliza la opción `-d` para especificar la profundidad de búsqueda. En este caso, se buscarán palabras clave hasta una profundidad de 2 niveles desde la página principal.

## <mark style="color:purple;">**3. Limitar la longitud de las palabras**</mark>

```bash
cewl http://example.com -w pass.txt -m 4
```

Con la opción `-m`, puedes limitar la longitud mínima de las palabras incluidas en el diccionario.

## <mark style="color:purple;">**4. Excluir palabras comunes**</mark>

```bash
cewl http://example.com -w pass.txt -x
```

La opción `-x` excluye palabras comunes del diccionario, como "the", "and", etc.

## <mark style="color:purple;">**5. Número máximo de palabras**</mark>

```bash
cewl http://example.com -w pass.txt -n 1000
```

Utiliza la opción `-n` para especificar el número máximo de palabras en el diccionario.

## <mark style="color:purple;">**6. Palabras en minúsculas**</mark>

```bash
cewl http://example.com -w pass.txt --lowercase
```

La opción `--lowercase` genera palabras en minúsculas en el diccionario.

## <mark style="color:purple;">**7. Palabras en mayúsculas**</mark>

```bash
cewl http://example.com -w pass.txt --uppercase
```

La opción `--uppercase` genera palabras en mayúsculas en el diccionario.

## <mark style="color:purple;">**8. Palabras encontradas en las URL**</mark>

```bash
cewl http://example.com -w pass.txt --with-url
```

La opción `--with-url` incluirá palabras encontradas en las URL en el diccionario.

Recuerda ajustar los comandos según tus necesidades y el sitio web que estás analizando.
