
# Análisis de Memoria

Nuestro objetivo es rastrear los pasos del atacante en la máquina comprometida y determinar cómo logró eludir el Sistema de Detección de Intrusos de Red (NIDS). La investigación identificará la familia de malware específica empleada en el ataque y sus características. Además, nuestra tarea consiste en identificar y mitigar cualquier rastro o huella dejado por el atacante.

{% embed url="<https://cyberdefenders.org/blueteam-ctf-challenges/redline/>" %}

## <mark style="color:purple;">¿Que es un Redline?</mark>

RedLine, también conocido como RedLine Stealer y RecordStealer, es un *malware* de tipo *stealer* que se distribuye a través de una plataforma de *malware* como servicio (MaaS) y está diseñado para recolectar y robar información de los dispositivos infectados. Además, puede proporcionar una puerta trasera a los atacantes que permite incluir los dispositivos como parte de una *botnet* para realizar otras actividades maliciosas.

{% embed url="<https://www.incibe.es/servicio-antibotnet/info/RedLine>" %}

***

## <mark style="color:purple;">Archivo de memoria</mark>

Nos descargamos el archivo en Kali Linux y lo extraemos:

```bash
unzip -P cyberdefenders.org c86-REDSTEALER.zip
```

```shell-session
afsh4ck@kali$ ls
MemoryDump.mem

afsh4ck@kali$ file MemoryDump.mem                                                                      
MemoryDump.mem: Windows Event Trace Log
```

***

## <mark style="color:purple;">Pregunta 1</mark>

> ¿Cómo se llama el proceso sospechoso?

Vamos a descarganos Volatility para analizar este archivo:

{% embed url="<https://github.com/volatilityfoundation/volatility3.git>" %}

```bash
git clone https://github.com/volatilityfoundation/volatility3.git
cd volatility3
pip install --user -e ".[full]"

vol -h
```

#### Buscar procesos sospechosos

Primero, buscaremos código o DLLs ocultas o inyectadas en la memoria con el complemento "**`malfind`**", lo que puede ayudar a encontrar rápidamente procesos sospechosos en algunos casos con el siguiente comando:

```bash
vol -f MemoryDump.mem windows.malfind

Volatility 3 Framework 2.26.2
/home/kali/Escritorio/machines/ciberdefenders/redline/volatility3/volatility3/framework/deprecation.py:28: FutureWarning: This API (volatility3.plugins.windows.malware.malfind.Malfind.run) will be removed in the first release after 2026-06-07. This plugin has been renamed, please call volatility3.plugins.windows.malware.malfind.Malfind rather than volatility3.plugins.windows.malfind.Malfind.
  warnings.warn(

PID	Process	Start VPN	End VPN	Tag	Protection	CommitCharge	PrivateMemory	File output	Notes	Hexdump	Disasm
/home/kali/Escritorio/machines/ciberdefenders/redline/volatility3/volatility3/framework/deprecation.py:105: FutureWarning: This plugin (volatility3.plugins.windows.malfind.Malfind) has been renamed and will be removed in the first release after 2026-06-07. Please ensure all method calls to this plugin are replaced with calls to volatility3.plugins.windows.malware.malfind.Malfind
  warnings.warn(
WARNING  volatility3.plugins.windows.malware.malfind: [proc_id 5704] Found suspicious DIRTY + PAGE_EXECUTE_READ page at 0x21ddbca0000

5704	RuntimeBroker.	0x21ddbca0000	0x21ddbcaffff	VadS	PAGE_EXECUTE_READ	16	1	Disabled	N/A	
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................	
0x21ddbca0000:	add	byte ptr [rax], al
0x21ddbca0002:	add	byte ptr [rax], al
0x21ddbca0004:	add	byte ptr [rax], al
0x21ddbca0006:	add	byte ptr [rax], al
0x21ddbca0008:	add	byte ptr [rax], al
0x21ddbca000a:	add	byte ptr [rax], al
0x21ddbca000c:	add	byte ptr [rax], al
<---SNIP--->
5896	oneetx.exe	0x400000	0x437fff	VadS	PAGE_EXECUTE_READWRITE	56	1	Disabled	MZ header	
4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00 MZ..............
b8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00 ........@.......
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 ................	
0x400000:	dec	ebp
0x400001:	pop	edx
0x400002:	nop	
0x400003:	add	byte ptr [ebx], al
0x400005:	add	byte ptr [eax], al
0x400007:	add	byte ptr [eax + eax], al
0x40000a:	add	byte ptr [eax], al
7540	smartscreen.ex	0x2505c140000	0x2505c15ffff	VadS	PAGE_EXECUTE_READWRITE	1	1	Disabled	N/A	
48 89 54 24 10 48 89 4c 24 08 4c 89 44 24 18 4c H.T$.H.L$.L.D$.L
89 4c 24 20 48 8b 41 28 48 8b 48 08 48 8b 51 50 .L$ H.A(H.H.H.QP
48 83 e2 f8 48 8b ca 48 b8 60 00 14 5c 50 02 00 H...H..H.`..\P..
00 48 2b c8 48 81 f9 70 0f 00 00 76 09 48 c7 c1 .H+.H..p...v.H..	
0x2505c140000:	mov	qword ptr [rsp + 0x10], rdx
0x2505c140005:	mov	qword ptr [rsp + 8], rcx
0x2505c14000a:	mov	qword ptr [rsp + 0x18], r8
0x2505c14000f:	mov	qword ptr [rsp + 0x20], r9
0x2505c140014:	mov	rax, qword ptr [rcx + 0x28]
0x2505c140018:	mov	rcx, qword ptr [rax + 8]
0x2505c14001c:	mov	rdx, qword ptr [rcx + 0x50]
0x2505c140020:	and	rdx, 0xfffffffffffffff8
<---SNIP--->
```

De igual manera podríamos sacar todo el árbol de procesos con el comando:

```bash
vol -f MemoryDump.mem windows.pstree
```

Encontramos 3 procesos sospechosos:

```q
5704	RuntimeBroker.exe
5896	oneetx.exe
7540	smartscreen.exe
```

#### Análisis de procesos sospechosos

Luego investigamos los procesos sospechosos a partir de los IDs de proceso obtenidos usando el complemento “**`pslist`**” y el siguiente comando:

```bash
vol -f MemoryDump.mem windows.pslist | grep -E "5704|5896|7540" 

5704	824	RuntimeBroker.	0xad8185962080	5	-	1	False	2023-05-21 22:32:44.000000 UTC	N/A	Disabled
5896	8844	oneetx.exe	0xad8189b41080	5	-	1	True	2023-05-21 22:30:56.000000 UTC	N/A	Disabled
7732	5896	rundll32.exe	0xad818d1912c0	1	-	1	True	2023-05-21 22:31:53.000000 UTC	N/A	Disabled
7540	824	smartscreen.ex	0xad818e893080	14	-	1	False	2023-05-21 23:02:26.000000 UTC	N/A	Disabled
```

El proceso que más nos llama la atención es el `5896 oneetx.exe`, marcado en True:

<table><thead><tr><th width="98.5390625">Valor</th><th>Significado</th></tr></thead><tbody><tr><td><code>True</code></td><td>El proceso <strong>está presente activamente</strong> en la tabla de procesos (<code>EPROCESS list</code>) al momento del volcado de memoria.</td></tr><tr><td><code>False</code></td><td>El proceso <strong>fue terminado (killed)</strong> antes del volcado, pero sus estructuras aún permanecen en la memoria y pueden ser recuperadas.</td></tr></tbody></table>

Así que dumpeamos el proceso para analizarlo con VirusTotal:

```bash
vol -f MemoryDump.mem windows.dumpfile --pid 5896
                                                    
Volatility 3 Framework 2.26.2
Progress:  100.00		PDB scanning finished                        
Cache	FileObject	FileName	Result

ImageSectionObject	0xad818e37b8e0	AcLayers.dll	file.0xad818e37b8e0.0xad818ea09d00.ImageSectionObject.AcLayers.dll.img
ImageSectionObject	0xad818da36c30	oneetx.exe	file.0xad818da36c30.0xad818ca48660.ImageSectionObject.oneetx.exe.img
<---SNIP--->
```

Tenemos el archivo malicioso:

```
file.0xad818da36c30.0xad818ca48660.ImageSectionObject.oneetx.exe.img
```

#### Extraemos el hash del malware

```bash
md5sum file.0xad818da36c30.0xad818ca48660.ImageSectionObject.oneetx.exe.img

f40168cc10f8cb6fe05322fc391e6947  file.0xad818da36c30.0xad818ca48660.ImageSectionObject.oneetx.exe.img
```

#### Análisis con VirusTotal

Al importar el hash en VirusTotal vemos que varios proveedores han informado sobre el archivo y lo han identificado como un troyano.

<figure><img src="/files/OCC6oycSPlYJrfFuTdZB" alt=""><figcaption></figcaption></figure>

#### Identificar la familia del malware

Con strings y el tipo de malware "redline" descubrimos que concretamente se trata de un Stealer:

```bash
strings MemoryDump.mem | grep -i "redline"                    

!Redline.YUQ!
!RedLineStealer
Redline.N
!RedLineStealer.
!Redline.GDL
RedLineStealer
<---SNIP--->
```

***

## <mark style="color:purple;">Pregunta 2</mark>

> ¿Cuál es el nombre del proceso secundario del proceso sospechoso?

Tras detectar el proceso sospechoso `5896 oneetx.exe`, podemos encontrar el proceso secundario asociado usando el complemento "`pslist`".

```bash
vol -f MemoryDump.mem windows.pslist | grep -E "5896" 

5896	8844	oneetx.exe	0xad8189b41080	5	-	1	True	2023-05-21 22:30:56.000000 UTC	N/A	Disabled
7732	5896	rundll32.exe	0xad818d1912c0	1	-	1	True	2023-05-21 22:31:53.000000 UTC	N/A	Disabled
```

Encontramos el proceso secundario:

```bash
7732	rundll32.exe
```

***

## <mark style="color:purple;">Pregunta 3</mark> <a href="#id-114c" id="id-114c"></a>

> ¿Cuál es la protección de memoria que se aplica a la región de memoria del proceso sospechoso?

Como resultado, al utilizar el complemento “`malfind`**”** en la [pregunta 1](#pregunta-1), encontramos el método de protección de memoria en la sección `VadS Protection`.

```bash
vol -f MemoryDump.mem windows.malfind

Volatility 3 Framework 2.26.2
/home/kali/Escritorio/machines/ciberdefenders/redline/volatility3/volatility3/framework/deprecation.py:28: FutureWarning: This API (volatility3.plugins.windows.malware.malfind.Malfind.run) will be removed in the first release after 2026-06-07. This plugin has been renamed, please call volatility3.plugins.windows.malware.malfind.Malfind rather than volatility3.plugins.windows.malfind.Malfind.
  warnings.warn(

PID	Process	Start VPN	End VPN	Tag	Protection	CommitCharge	PrivateMemory	File output	Notes	Hexdump	Disasm
/home/kali/Escritorio/machines/ciberdefenders/redline/volatility3/volatility3/framework/deprecation.py:105: FutureWarning: This plugin (volatility3.plugins.windows.malfind.Malfind) has been renamed and will be removed in the first release after 2026-06-07. Please ensure all method calls to this plugin are replaced with calls to volatility3.plugins.windows.malware.malfind.Malfind
  warnings.warn(
WARNING  volatility3.plugins.windows.malware.malfind: [proc_id 5704] Found suspicious DIRTY + PAGE_EXECUTE_READ page at 0x21ddbca0000

5896	oneetx.exe	0x400000	0x437fff	VadS	PAGE_EXECUTE_READWRITE	56	1	Disabled	MZ header	
4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00 MZ..............
b8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00 ........@.......
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 ................	
0x400000:	dec	ebp
0x400001:	pop	edx
0x400002:	nop	
0x400003:	add	byte ptr [ebx], al
0x400005:	add	byte ptr [eax], al
0x400007:	add	byte ptr [eax + eax], al
0x40000a:	add	byte ptr [eax], al
```

Concretamente el método de protección de memoria es:

```
PAGE_EXECUTE_READWRITE
```

***

## <mark style="color:purple;">Pregunta 4</mark>

> ¿Cuál es el nombre del proceso responsable de la conexión VPN?

Analicemos los procesos interesantes que podrían ser procesos VPN y luego analicemos los procesos relativos usando el siguiente comando:

```bash
vol -f MemoryDump.mem windows.pstree

Volatility 3 Framework 2.26.2
Progress:  100.00		PDB scanning finished                        
PID	PPID	ImageFileName	Offset(V)	Threads	Handles	SessionId	Wow64	CreateTime	ExitTime	Audit	Cmd	Path

4	0	System	0xad8185883180	157	-	N/A	False	2023-05-21 22:27:10.000000 UTC	N/A	-	-	-
* 1280	4	MemCompression	0xad8187835080	62	-	N/A	False	2023-05-21 22:27:49.000000 UTC	N/A	MemCompression	-	-
* 108	4	Registry	0xad81858f2080	4	-	N/A	False	2023-05-21 22:26:54.000000 UTC	N/A	Registry	-	-
* 332	4	smss.exe	0xad81860dc040	2	-	N/A	False	2023-05-21 22:27:10.000000 UTC	N/A	\Device\HarddiskVolume3\Windows\System32\smss.exe	-	-
452	444	csrss.exe	0xad81861cd080	12	-	0	False	2023-05-21 22:27:22.000000 UTC	N/A	\Device\HarddiskVolume3\Windows\System32\csrss.exe	-	-
528	520	csrss.exe	0xad8186f1b140	14	-	1	False	2023-05-21 22:27:25.000000 UTC	N/A	\Device\HarddiskVolume3\Windows\System32\csrss.exe		
552	444	wininit.exe	0xad8186f2b080	1	-	0	False	2023-05-21 22:27:25.000000 UTC	N/A	\Device\HarddiskVolume3\Windows\System32\wininit.exe	-	-
* 696	552	lsass.exe	0xad8186fc6080	10	-	0	False	2023-05-21 22:27:29.000000 UTC	N/A	\Device\HarddiskVolume3\Windows\System32\lsass.exe	C:\Windows\system32\lsass.exe	C:\Windows\system32\lsass.exe
<---SNIP--->
*** 6724	3580	Outline.exe	0xad818e578080	0	-	1	True	2023-05-21 22:36:09.000000 UTC	2023-05-21 23:01:24.000000 UTC	\Device\HarddiskVolume3\Program Files (x86)\Outline\Outline.exe	-	-
**** 4224	6724	Outline.exe	0xad818e88b080	0	-	1	True	2023-05-21 22:36:23.000000 UTC	2023-05-21 23:01:24.000000 UTC	\Device\HarddiskVolume3\Program Files (x86)\Outline\Outline.exe	-	-
**** 4628	6724	tun2socks.exe	0xad818de82340	0	-	1	True	2023-05-21 22:40:10.000000 UTC	2023-05-21 23:01:24.000000 UTC	\Device\HarddiskVolume3\Program Files (x86)\Outline\resources\app.asar.unpacked\third_party\outline-go-tun2socks\win32\tun2socks.exe	-	-
```

Después de analizar el proceso y buscar información, se encontró que el proceso **tun2socks.exe** probablemente está relacionado con VPN y el proceso responsable de la conexión VPN es el proceso con ID **`6724`** , que es el proceso padre del proceso **`tun2socks.exe`** .

Lo podemos verificar con el siguiente comando:

```bash
vol -f MemoryDump.mem windows.pstree | grep -E "6724"

*** 6724	3580	Outline.exe	0xad818e578080	0	-	1	True	2023-05-21 22:36:09.000000 UTC	2023-05-21 23:01:24.000000 UTC	\Device\HarddiskVolume3\Program Files (x86)\Outline\Outline.exe	-	-
**** 4224	6724	Outline.exe	0xad818e88b080	0	-	1	True	2023-05-21 22:36:23.000000 UTC	2023-05-21 23:01:24.000000 UTC	\Device\HarddiskVolume3\Program Files (x86)\Outline\Outline.exe	-	-
**** 4628	6724	tun2socks.exe	0xad818de82340	0	-	1	True	2023-05-21 22:40:10.000000 UTC	2023-05-21 23:01:24.000000 UTC	\Device\HarddiskVolume3\Program Files (x86)\Outline\resources\app.asar.unpacked\third_party\outline-go-tun2socks\win32\tun2socks.exe	-	-
```

***

## <mark style="color:purple;">Pregunta 5</mark>

> ¿Cuál es la dirección IP del atacante?

Echamos un vistazo a las conexiones de red y buscamos los procesos sospechosos encontrados en la [pregunta 1](#pregunta-1) para ver si alguna conexión de red se dirige a otros destinos.&#x20;

Teníamos estos procesos sospechosos:

```q
5704	RuntimeBroker.exe
5896	oneetx.exe
7540	smartscreen.exe
```

Utilizamos el siguiente comando para analizar las conexiones de red de los ejecutables:

```bash
vol -f MemoryDump.mem windows.netscan | grep "oneetx.exe"

0xad818de4aa20.0TCPv4	10.0.85.2DB scan55462fin77.91.124.20	80	CLOSED	5896	oneetx.exe	2023-05-21 23:01:22.000000 UTC
0xad818e4a6900	UDPv4	0.0.0.0	0	*	0		5480	oneetx.exe	2023-05-21 22:39:47.000000 UTC
0xad818e4a6900	UDPv6	::	0	*	0		5480	oneetx.exe	2023-05-21 22:39:47.000000 UTC
0xad818e4a9650	UDPv4	0.0.0.0	0	*	0		5480	oneetx.exe	2023-05-21 22:39:47.000000 UTC
```

Encontramos que el proceso sospechoso `5896 oneetx.exe` tiene una conexión a la dirección IP `77.91.124.20` en el puerto 80, por lo que verificaremos la dirección IP con VirusTotal.

<figure><img src="/files/8NtGVgGDBxnC8YlZ0Iqw" alt=""><figcaption></figcaption></figure>

Concretamente es una IP de Alemania.

También podríamos analizar esta IP con la herramienta de C2 Tracker de ViriBack:

{% embed url="<https://tracker.viriback.com/>" %}

<figure><img src="/files/bkCLSprCqpw5JNfUGKMs" alt=""><figcaption></figcaption></figure>

El proveedor de ViriBlack informó que la dirección IP sospechosa era malware y, en el contexto de crowdsourcing, la información de ViriBlack se identificó en el Panel relacionada con el malware Amadey.

***

## <mark style="color:purple;">Pregunta 7</mark>

> ¿Cuál es la URL completa del archivo PHP que visitó el atacante?

Tenemos indicios de que abrió un archivo PHP tal y como muestra C2 Tracker, pero vamos a corroborarlo. Para ello vamos a extraer todas las strings que contengan la dirección IP del atacante:

```bash
strings MemoryDump.mem | grep -iE "http(|s):\/\/77.91.124.20\/"

http://77.91.124.20/ E
http://77.91.124.20/store/gamel
http://77.91.124.20/ E
http://77.91.124.20/DSC01491/
http://77.91.124.20/DSC01491/
http://77.91.124.20/store/games/index.php
http://77.91.124.20/store/games/index.php
http://77.91.124.20/store/games/index.php
```

Vemos que la ruta completa que visitó el atacante es:

```http
http://77.91.124.20/store/games/index.php
```

***

## <mark style="color:purple;">Pregunta 8</mark>

> ¿Cuál es la ruta completa del ejecutable malicioso?

Para obtener la ruta completa del ejecutable malicioso, se puede utilizar el complemento “`filescan`” para escanear archivos en la memoria utilizando los nombres de procesos o ejecutables maliciosos en la búsqueda. Para ello utilizamos el siguiente comando:

```bash
vol -f MemoryDump.mem windows.filescan | grep "oneetx.exe"

0xad818d436c70  \Users\Tammam\AppData\Local\Temp\c3912af058\oneetx.exe
0xad818da36c30	\Users\Tammam\AppData\Local\Temp\c3912af058\oneetx.exe
0xad818ef1a0b0	\Users\Tammam\AppData\Local\Temp\c3912af058\oneetx.exe
```

Encontramos la ruta completa del ejecutable malicioso:

```
C:\Users\Tammam\AppData\Local\Temp\c3912af058\oneetx.exe
```
