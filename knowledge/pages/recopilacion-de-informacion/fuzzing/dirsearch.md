
# Dirsearch

Dirsearch es una herramienta escrita en Python para realizar **fuerza bruta de directorios y archivos** en aplicaciones web. Es similar a Gobuster, pero ofrece más flexibilidad y opciones avanzadas, como soporte para proxies, múltiples métodos HTTP y personalización de encabezados.

Dirsearch incluye su propio diccionario por defecto con 11460 palabras, que en la mayoría de ocasiones será más que de sobra para encontrar directorios y archivos ocultos.

<figure><img src="/files/3ZznIIccbjGy6BWu7OKd" alt=""><figcaption></figcaption></figure>

Lo podemos instalar en Kali Linux con el siguiente comando:

```bash
sudo apt install dirsearch
```

## <mark style="color:purple;">Fuzzing con Dirsearch</mark>

### **Uso básico**

```bash
dirsearch -u <URL> -e <EXTENSIONES> -w <WORDLIST>
```

* **`-u`**: Especifica la URL objetivo.
* **`-e`**: Extensiones de archivos (por ejemplo: `php,html,txt`).
* **`-w`**: Ruta de la wordlist.

***

### **Ejemplos prácticos**

#### **Fuzzing básico con lista por defecto**

```bash
dirsearch -u https://example.com
```

#### **Enumerar directorios básicos:**

```bash
dirsearch -u https://example.com -w /usr/share/wordlists/dirb/common.txt
```

#### **Buscar archivos `.php` y `.html`:**

```bash
dirsearch -u https://example.com -e php,html -w /usr/share/wordlists/dirb/common.txt
```

#### **Usar múltiples hilos para acelerar la búsqueda:**

```bash
dirsearch -u https://example.com -w /usr/share/wordlists/dirb/common.txt -t 50
```

#### **Filtrar resultados negativos**

```bash
dirsearch -u https://example.com -x 400,401,402,403
```

#### **Personalizar el encabezado `User-Agent`:**

```bash
dirsearch -u https://example.com -w /usr/share/wordlists/dirb/common.txt --user-agent "Mozilla/5.0"
```

#### **Usar un proxy:**

```bash
dirsearch -u https://example.com -w /usr/share/wordlists/dirb/common.txt --proxy http://127.0.0.1:8080
```

***

### **Opciones adicionales útiles**

* **`-r`**: Seguir redirecciones.
* **`--random-agents`**: Usar un User-Agent aleatorio para cada petición.
* **`--exclude-status`**: Excluir ciertos códigos de estado (por ejemplo, 403).

***

### Desactivar Python Warnings

Hay ocasiones en las que esta herramienta muestra unos warnings de python. Los podemos desactivar con la siguiente variable de entorno para que no nos molesten:

```bash
export PYTHONWARNINGS="ignore"
```
