
# Ataques a aplicaciones que se conectan a servicios

Las aplicaciones que están conectadas a servicios a menudo incluyen cadenas de conexión que pueden filtrarse si no están suficientemente protegidas. En los siguientes párrafos, repasaremos el proceso de enumeración y explotación de aplicaciones que están conectadas a otros servicios para ampliar su funcionalidad. Esto puede ayudarnos a recopilar información y a movernos lateralmente o escalar nuestros privilegios durante las pruebas de penetración.

***

## <mark style="color:purple;">Examen de ejecutable ELF</mark>

El binario `octopus_checker` se encuentra en una máquina remota durante la prueba. Al ejecutar la aplicación localmente, se revela que se conecta a instancias de bases de datos para verificar que estén disponibles.

```shell-session
afsh4ck@kali$ ./octopus_checker 

Program had started..
Attempting Connection 
Connecting ... 

The driver reported the following diagnostics whilst running SQLDriverConnect

01000:1:0:[unixODBC][Driver Manager]Can't open lib 'ODBC Driver 17 for SQL Server' : file not found
connected
```

El binario probablemente se conecta usando una cadena de conexión SQL que contiene credenciales. Usando herramientas como [PEDA](https://github.com/longld/peda) (Python Exploit Development Assistance for GDB) podemos examinar más a fondo el archivo. Esta es una extensión del depurador GNU estándar (GDB), que se usa para depurar programas C y C++. GDB es una herramienta de línea de comandos que le permite recorrer el código, establecer puntos de interrupción y examinar y cambiar variables. Al ejecutar el siguiente comando podemos ejecutar el binario a través de él.

```shell-session
afsh4ck@kali$ gdb ./octopus_checker

GNU gdb (Debian 9.2-1) 9.2
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./octopus_checker...
(No debugging symbols found in ./octopus_checker)
```

Una vez cargado el binario, establecemos el estilo de visualización del código `disassembly-flavor` y procedemos a desensamblar la función principal del programa.

```wasm
gdb-peda$ set disassembly-flavor intel
gdb-peda$ disas main

Dump of assembler code for function main:
   0x0000555555555456 <+0>:	endbr64 
   0x000055555555545a <+4>:	push   rbp
   0x000055555555545b <+5>:	mov    rbp,rsp
 
 <SNIP>
 
   0x0000555555555625 <+463>:	call   0x5555555551a0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x000055555555562a <+468>:	mov    rdx,rax
   0x000055555555562d <+471>:	mov    rax,QWORD PTR [rip+0x299c]        # 0x555555557fd0
   0x0000555555555634 <+478>:	mov    rsi,rax
   0x0000555555555637 <+481>:	mov    rdi,rdx
   0x000055555555563a <+484>:	call   0x5555555551c0 <_ZNSolsEPFRSoS_E@plt>
   0x000055555555563f <+489>:	mov    rbx,QWORD PTR [rbp-0x4a8]
   0x0000555555555646 <+496>:	lea    rax,[rbp-0x4b7]
   0x000055555555564d <+503>:	mov    rdi,rax
   0x0000555555555650 <+506>:	call   0x555555555220 <_ZNSaIcEC1Ev@plt>
   0x0000555555555655 <+511>:	lea    rdx,[rbp-0x4b7]
   0x000055555555565c <+518>:	lea    rax,[rbp-0x4a0]
   0x0000555555555663 <+525>:	lea    rsi,[rip+0xa34]        # 0x55555555609e
   0x000055555555566a <+532>:	mov    rdi,rax
   0x000055555555566d <+535>:	call   0x5555555551f0 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1EPKcRKS3_@plt>
   0x0000555555555672 <+540>:	lea    rax,[rbp-0x4a0]
   0x0000555555555679 <+547>:	mov    edx,0x2
   0x000055555555567e <+552>:	mov    rsi,rbx
   0x0000555555555681 <+555>:	mov    rdi,rax
   0x0000555555555684 <+558>:	call   0x555555555329 <_Z13extract_errorNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEPvs>
   0x0000555555555689 <+563>:	lea    rax,[rbp-0x4a0]
   0x0000555555555690 <+570>:	mov    rdi,rax
   0x0000555555555693 <+573>:	call   0x555555555160 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev@plt>
   0x0000555555555698 <+578>:	lea    rax,[rbp-0x4b7]
   0x000055555555569f <+585>:	mov    rdi,rax
   0x00005555555556a2 <+588>:	call   0x5555555551d0 <_ZNSaIcED1Ev@plt>
   0x00005555555556a7 <+593>:	cmp    WORD PTR [rbp-0x4b2],0x0

<SNIP>

   0x0000555555555761 <+779>:	mov    rbx,QWORD PTR [rbp-0x8]
   0x0000555555555765 <+783>:	leave  
   0x0000555555555766 <+784>:	ret    
End of assembler dump.
```

Esto revela varias instrucciones de llamada que apuntan a direcciones que contienen cadenas. Parecen ser secciones de una cadena de conexión SQL, pero las secciones no están en orden y el orden de bytes implica que el texto de la cadena está invertido. El orden de bytes define el orden en que se leen los bytes en diferentes arquitecturas. Más abajo en la función, vemos una llamada a SQLDriverConnect.

```wasm
   0x00005555555555ff <+425>:	mov    esi,0x0
   0x0000555555555604 <+430>:	mov    rdi,rax
   0x0000555555555607 <+433>:	call   0x5555555551b0 <SQLDriverConnect@plt>
   0x000055555555560c <+438>:	add    rsp,0x10
   0x0000555555555610 <+442>:	mov    WORD PTR [rbp-0x4b4],ax
```

Al agregar un breakpoint en esta dirección y ejecutar el programa una vez más, se revela una cadena de conexión SQL en la dirección del registro RDX, que contiene las credenciales para una instancia de base de datos local.

```wasm
gdb-peda$ b *0x5555555551b0

Breakpoint 1 at 0x5555555551b0

gdb-peda$ run

Starting program: /htb/rollout/octopus_checker 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Program had started..
Attempting Connection 
[----------------------------------registers-----------------------------------]
RAX: 0x55555556c4f0 --> 0x4b5a ('ZK')
RBX: 0x0 
RCX: 0xfffffffd 
RDX: 0x7fffffffda70 ("DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost, 1401;UID=username;PWD=password;")
RSI: 0x0 
RDI: 0x55555556c4f0 --> 0x4b5a ('ZK')

<SNIP>
```

Además de intentar conectarse al servicio MS SQL, los evaluadores de penetración también pueden verificar si la contraseña puede ser reutilizada por usuarios de la misma red.

***

## <mark style="color:purple;">Examen de archivos DLL</mark>

Un archivo DLL (`Dynamically Linked Library`) es un código que se ejecuta desde otros programas. El binario `MultimasterAPI.dll` se encuentra en una máquina remota durante el proceso de enumeración. El análisis del archivo revela que se trata de un ensamblado .Net.

```powershell
C:\> Get-FileMetaData .\MultimasterAPI.dll

<SNIP>
M .NETFramework,Version=v4.6.1 TFrameworkDisplayName.NET Framework 4.6.1    api/getColleagues        ! htt
p://localhost:8081*POST         Ò^         øJ  ø,  RSDSœ»¡ÍuqœK£"Y¿bˆ   C:\Users\Hazard\Desktop\Stuff\Multimast
<SNIP>
```

Mediante el depurador y editor de ensamblados .NET [dnSpy](https://github.com/0xd4d/dnSpy) , podemos ver el código fuente directamente. Esta herramienta permite leer, editar y depurar el código fuente de un ensamblado .NET (C# y Visual Basic). La inspección de `MultimasterAPI.Controllers`-> `ColleagueController` revela una cadena de conexión a la base de datos que contiene la contraseña.

![dnspy\_oculto](https://academy.hackthebox.com/storage/modules/113/apps_conn_to_services/dnspy_hidden.png)

Además de intentar conectarse al servicio MS SQL, también se pueden utilizar ataques como el Password Spraying para probar la seguridad de otros servicios.

***

## <mark style="color:purple;">Caso práctico</mark>&#x20;

```
Objetivo: 10.129.205.20

SSH a 10.129.205.20 (ACADEMY-ACA-ROLLOUT)
Usuario "htb-student"
Contraseña "HTB_@cademy_stdnt!"
```

> ¿Qué credenciales se encontraron para la instancia de base de datos local al depurar el binario `octopus_checker`?

Nos conectamos por ssh y encontramos el binario ELF a analizar:

```bash
htb-student@htb:~$ ls
octopus_checker
```

Al ejecutarlo vemos que intenta conectarse a un SQL Server:

```
htb-student@htb:~$ ./octopus_checker 
Program had started..
Attempting Connection 

Connecting ... 

The driver reported the following diagnostics whilst running SQLDriverConnect

01000:1:5701:[Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Changed database context to 'master'.
01000:2:5703:[Microsoft][ODBC Driver 17 for SQL Server][SQL Server]Changed language setting to us_english.
connected
```

El binario probablemente se conecta usando una cadena de conexión SQL que contiene credenciales.&#x20;

Vamos a analizarlo con gba:

```shell-session
htb-student@htb:~$ gdb ./octopus_checker 
GNU gdb (Ubuntu 9.2-0ubuntu1~20.04.1) 9.2
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./octopus_checker...
(No debugging symbols found in ./octopus_checker)
gdb-peda$
```

```wasm
gdb-peda$ start
gdb-peda$ disas main
Dump of assembler code for function main:
=> 0x0000555555555456 <+0>:	endbr64 
   0x000055555555545a <+4>:	push   rbp
   0x000055555555545b <+5>:	mov    rbp,rsp
   0x000055555555545e <+8>:	push   rbx
   0x000055555555545f <+9>:	sub    rsp,0x4b8
   0x0000555555555466 <+16>:	mov    rax,QWORD PTR fs:0x28
   0x000055555555546f <+25>:	mov    QWORD PTR [rbp-0x18],rax
   0x0000555555555473 <+29>:	xor    eax,eax
   0x0000555555555475 <+31>:	lea    rsi,[rip+0xbe5]        # 0x555555556061
   0x000055555555547c <+38>:	lea    rdi,[rip+0x2bbd]        # 0x555555558040 <_ZSt4cout@@GLIBCXX_3.4>
   0x0000555555555483 <+45>:	call   0x5555555551a0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x0000555555555488 <+50>:	mov    rdx,rax
   0x000055555555548b <+53>:	mov    rax,QWORD PTR [rip+0x2b3e]        # 0x555555557fd0
   0x0000555555555492 <+60>:	mov    rsi,rax
   0x0000555555555495 <+63>:	mov    rdi,rdx
   0x0000555555555498 <+66>:	call   0x5555555551c0 <_ZNSolsEPFRSoS_E@plt>
   0x000055555555549d <+71>:	lea    rax,[rbp-0x4b0]
   0x00005555555554a4 <+78>:	mov    rdx,rax
   0x00005555555554a7 <+81>:	mov    esi,0x0
   0x00005555555554ac <+86>:	mov    edi,0x1
   0x00005555555554b1 <+91>:	call   0x555555555170 <SQLAllocHandle@plt>
   0x00005555555554b6 <+96>:	mov    rax,QWORD PTR [rbp-0x4b0]
   0x00005555555554bd <+103>:	mov    ecx,0x0
   0x00005555555554c2 <+108>:	mov    edx,0x3
   0x00005555555554c7 <+113>:	mov    esi,0xc8
   0x00005555555554cc <+118>:	mov    rdi,rax
   0x00005555555554cf <+121>:	call   0x555555555230 <SQLSetEnvAttr@plt>
   0x00005555555554d4 <+126>:	mov    rax,QWORD PTR [rbp-0x4b0]
   0x00005555555554db <+133>:	lea    rdx,[rbp-0x4a8]
   0x00005555555554e2 <+140>:	mov    rsi,rax
   0x00005555555554e5 <+143>:	mov    edi,0x2
   0x00005555555554ea <+148>:	call   0x555555555170 <SQLAllocHandle@plt>
   0x00005555555554ef <+153>:	lea    rsi,[rip+0xb81]        # 0x555555556077
   0x00005555555554f6 <+160>:	lea    rdi,[rip+0x2b43]        # 0x555555558040 <_ZSt4cout@@GLIBCXX_3.4>
   0x00005555555554fd <+167>:	call   0x5555555551a0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x0000555555555502 <+172>:	mov    rdx,rax
   0x0000555555555505 <+175>:	mov    rax,QWORD PTR [rip+0x2ac4]        # 0x555555557fd0
   0x000055555555550c <+182>:	mov    rsi,rax
   0x000055555555550f <+185>:	mov    rdi,rdx
   0x0000555555555512 <+188>:	call   0x5555555551c0 <_ZNSolsEPFRSoS_E@plt>
   0x0000555555555517 <+193>:	movabs rax,0x7b3d524556495244
   0x0000555555555521 <+203>:	movabs rdx,0x697244204342444f
   0x000055555555552b <+213>:	mov    QWORD PTR [rbp-0x480],rax
   0x0000555555555532 <+220>:	mov    QWORD PTR [rbp-0x478],rdx
   0x0000555555555539 <+227>:	movabs rax,0x6620373120726576
   0x0000555555555543 <+237>:	movabs rdx,0x53204c515320726f
   0x000055555555554d <+247>:	mov    QWORD PTR [rbp-0x470],rax
   0x0000555555555554 <+254>:	mov    QWORD PTR [rbp-0x468],rdx
   0x000055555555555b <+261>:	movabs rax,0x533b7d7265767265
   0x0000555555555565 <+271>:	movabs rdx,0x6f6c3d5245565245
   0x000055555555556f <+281>:	mov    QWORD PTR [rbp-0x460],rax
   0x0000555555555576 <+288>:	mov    QWORD PTR [rbp-0x458],rdx
   0x000055555555557d <+295>:	movabs rax,0x2c74736f686c6163
   0x0000555555555587 <+305>:	movabs rdx,0x49553b3130343120
   0x0000555555555591 <+315>:	mov    QWORD PTR [rbp-0x450],rax
   0x0000555555555598 <+322>:	mov    QWORD PTR [rbp-0x448],rdx
   0x000055555555559f <+329>:	movabs rax,0x4457503b41533d44
   0x00005555555555a9 <+339>:	movabs rdx,0x7263335374304e3d
   0x00005555555555b3 <+349>:	mov    QWORD PTR [rbp-0x440],rax
   0x00005555555555ba <+356>:	mov    QWORD PTR [rbp-0x438],rdx
   0x00005555555555c1 <+363>:	mov    DWORD PTR [rbp-0x430],0x3b217433
   0x00005555555555cb <+373>:	mov    BYTE PTR [rbp-0x42c],0x0
   0x00005555555555d2 <+380>:	mov    rax,QWORD PTR [rbp-0x4a8]
   0x00005555555555d9 <+387>:	lea    rsi,[rbp-0x420]
   0x00005555555555e0 <+394>:	lea    rdx,[rbp-0x480]
   0x00005555555555e7 <+401>:	push   0x0
   0x00005555555555e9 <+403>:	lea    rcx,[rbp-0x4b6]
   0x00005555555555f0 <+410>:	push   rcx
   0x00005555555555f1 <+411>:	mov    r9d,0x400
   0x00005555555555f7 <+417>:	mov    r8,rsi
   0x00005555555555fa <+420>:	mov    ecx,0xfffffffd
   0x00005555555555ff <+425>:	mov    esi,0x0
   0x0000555555555604 <+430>:	mov    rdi,rax
   0x0000555555555607 <+433>:	call   0x5555555551b0 <SQLDriverConnect@plt>
   0x000055555555560c <+438>:	add    rsp,0x10
   0x0000555555555610 <+442>:	mov    WORD PTR [rbp-0x4b4],ax
   0x0000555555555617 <+449>:	lea    rsi,[rip+0xa70]        # 0x55555555608e
   0x000055555555561e <+456>:	lea    rdi,[rip+0x2a1b]        # 0x555555558040 <_ZSt4cout@@GLIBCXX_3.4>
   0x0000555555555625 <+463>:	call   0x5555555551a0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x000055555555562a <+468>:	mov    rdx,rax
   0x000055555555562d <+471>:	mov    rax,QWORD PTR [rip+0x299c]        # 0x555555557fd0
   0x0000555555555634 <+478>:	mov    rsi,rax
   0x0000555555555637 <+481>:	mov    rdi,rdx
   0x000055555555563a <+484>:	call   0x5555555551c0 <_ZNSolsEPFRSoS_E@plt>
   0x000055555555563f <+489>:	mov    rbx,QWORD PTR [rbp-0x4a8]
   0x0000555555555646 <+496>:	lea    rax,[rbp-0x4b7]
   0x000055555555564d <+503>:	mov    rdi,rax
   0x0000555555555650 <+506>:	call   0x555555555220 <_ZNSaIcEC1Ev@plt>
   0x0000555555555655 <+511>:	lea    rdx,[rbp-0x4b7]
   0x000055555555565c <+518>:	lea    rax,[rbp-0x4a0]
   0x0000555555555663 <+525>:	lea    rsi,[rip+0xa34]        # 0x55555555609e
   0x000055555555566a <+532>:	mov    rdi,rax
   0x000055555555566d <+535>:	call   0x5555555551f0 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1EPKcRKS3_@plt>
   0x0000555555555672 <+540>:	lea    rax,[rbp-0x4a0]
   0x0000555555555679 <+547>:	mov    edx,0x2
   0x000055555555567e <+552>:	mov    rsi,rbx
   0x0000555555555681 <+555>:	mov    rdi,rax
   0x0000555555555684 <+558>:	call   0x555555555329 <_Z13extract_errorNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEEPvs>
   0x0000555555555689 <+563>:	lea    rax,[rbp-0x4a0]
   0x0000555555555690 <+570>:	mov    rdi,rax
   0x0000555555555693 <+573>:	call   0x555555555160 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev@plt>
   0x0000555555555698 <+578>:	lea    rax,[rbp-0x4b7]
   0x000055555555569f <+585>:	mov    rdi,rax
   0x00005555555556a2 <+588>:	call   0x5555555551d0 <_ZNSaIcED1Ev@plt>
   0x00005555555556a7 <+593>:	cmp    WORD PTR [rbp-0x4b2],0x0
   0x00005555555556af <+601>:	je     0x5555555556e5 <main+655>
   0x00005555555556b1 <+603>:	cmp    WORD PTR [rbp-0x4b2],0x1
   0x00005555555556b9 <+611>:	je     0x5555555556e5 <main+655>
   0x00005555555556bb <+613>:	lea    rsi,[rip+0x9ed]        # 0x5555555560af
   0x00005555555556c2 <+620>:	lea    rdi,[rip+0x2977]        # 0x555555558040 <_ZSt4cout@@GLIBCXX_3.4>
   0x00005555555556c9 <+627>:	call   0x5555555551a0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x00005555555556ce <+632>:	mov    rdx,rax
   0x00005555555556d1 <+635>:	mov    rax,QWORD PTR [rip+0x28f8]        # 0x555555557fd0
   0x00005555555556d8 <+642>:	mov    rsi,rax
   0x00005555555556db <+645>:	mov    rdi,rdx
   0x00005555555556de <+648>:	call   0x5555555551c0 <_ZNSolsEPFRSoS_E@plt>
   0x00005555555556e3 <+653>:	jmp    0x55555555570d <main+695>
   0x00005555555556e5 <+655>:	lea    rsi,[rip+0x9d3]        # 0x5555555560bf
   0x00005555555556ec <+662>:	lea    rdi,[rip+0x294d]        # 0x555555558040 <_ZSt4cout@@GLIBCXX_3.4>
   0x00005555555556f3 <+669>:	call   0x5555555551a0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
   0x00005555555556f8 <+674>:	mov    rdx,rax
   0x00005555555556fb <+677>:	mov    rax,QWORD PTR [rip+0x28ce]        # 0x555555557fd0
   0x0000555555555702 <+684>:	mov    rsi,rax
   0x0000555555555705 <+687>:	mov    rdi,rdx
   0x0000555555555708 <+690>:	call   0x5555555551c0 <_ZNSolsEPFRSoS_E@plt>
   0x000055555555570d <+695>:	mov    eax,0x0
   0x0000555555555712 <+700>:	mov    rcx,QWORD PTR [rbp-0x18]
   0x0000555555555716 <+704>:	xor    rcx,QWORD PTR fs:0x28
   0x000055555555571f <+713>:	je     0x555555555761 <main+779>
   0x0000555555555721 <+715>:	jmp    0x55555555575c <main+774>
   0x0000555555555723 <+717>:	endbr64 
   0x0000555555555727 <+721>:	mov    rbx,rax
   0x000055555555572a <+724>:	lea    rax,[rbp-0x4a0]
   0x0000555555555731 <+731>:	mov    rdi,rax
   0x0000555555555734 <+734>:	call   0x555555555160 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEED1Ev@plt>
   0x0000555555555739 <+739>:	jmp    0x555555555742 <main+748>
   0x000055555555573b <+741>:	endbr64 
   0x000055555555573f <+745>:	mov    rbx,rax
   0x0000555555555742 <+748>:	lea    rax,[rbp-0x4b7]
   0x0000555555555749 <+755>:	mov    rdi,rax
   0x000055555555574c <+758>:	call   0x5555555551d0 <_ZNSaIcED1Ev@plt>
   0x0000555555555751 <+763>:	mov    rax,rbx
   0x0000555555555754 <+766>:	mov    rdi,rax
   0x0000555555555757 <+769>:	call   0x555555555210 <_Unwind_Resume@plt>
   0x000055555555575c <+774>:	call   0x5555555551e0 <__stack_chk_fail@plt>
   0x0000555555555761 <+779>:	mov    rbx,QWORD PTR [rbp-0x8]
   0x0000555555555765 <+783>:	leave  
   0x0000555555555766 <+784>:	ret    
End of assembler dump.
```

Observamos una llamada a `SQLDriverConnect`:

```wasm
   0x00005555555555ff <+425>:	mov    esi,0x0
   0x0000555555555604 <+430>:	mov    rdi,rax
   0x0000555555555607 <+433>:	call   0x5555555551b0 <SQLDriverConnect@plt>
   0x000055555555560c <+438>:	add    rsp,0x10
   0x0000555555555610 <+442>:	mov    WORD PTR [rbp-0x4b4],ax
```

Creamos un breakpoint en su dirección de memoria y ejecutamos de nuevo la aplicación:

```wasm
gdb-peda$ b *0x5555555551b0
Breakpoint 2 at 0x5555555551b0
gdb-peda$ run
Starting program: /home/htb-student/octopus_checker 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Program had started..
Attempting Connection 
[----------------------------------registers-----------------------------------]
RAX: 0x55555556c4f0 --> 0x4b5a ('ZK')
RBX: 0x5555555557d0 (<__libc_csu_init>:	endbr64)
RCX: 0xfffffffd 
RDX: 0x7fffffffdf30 ("DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost, 1401;UID=SA;PWD=N0tS3cr3t!;")
RSI: 0x0 
RDI: 0x55555556c4f0 --> 0x4b5a ('ZK')
RBP: 0x7fffffffe3b0 --> 0x0 
RSP: 0x7fffffffded8 --> 0x55555555560c (<main+438>:	add    rsp,0x10)
RIP: 0x5555555551b0 (<SQLDriverConnect@plt>:	endbr64)
R8 : 0x7fffffffdf90 --> 0x0 
R9 : 0x400 
R10: 0xfffffffffffff8ff 
R11: 0x246 
R12: 0x555555555240 (<_start>:	endbr64)
R13: 0x7fffffffe4a0 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x213 (CARRY parity ADJUST zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x5555555551a0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>:	endbr64 
   0x5555555551a4 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt+4>:	
    bnd jmp QWORD PTR [rip+0x2dcd]        # 0x555555557f78 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@got.plt>
   0x5555555551ab <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt+11>:	nop    DWORD PTR [rax+rax*1+0x0]
=> 0x5555555551b0 <SQLDriverConnect@plt>:	endbr64 
   0x5555555551b4 <SQLDriverConnect@plt+4>:	bnd jmp QWORD PTR [rip+0x2dc5]        # 0x555555557f80 <SQLDriverConnect@got.plt>
   0x5555555551bb <SQLDriverConnect@plt+11>:	nop    DWORD PTR [rax+rax*1+0x0]
   0x5555555551c0 <_ZNSolsEPFRSoS_E@plt>:	endbr64 
   0x5555555551c4 <_ZNSolsEPFRSoS_E@plt+4>:	bnd jmp QWORD PTR [rip+0x2dbd]        # 0x555555557f88 <_ZNSolsEPFRSoS_E@got.plt>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffded8 --> 0x55555555560c (<main+438>:	add    rsp,0x10)
0008| 0x7fffffffdee0 --> 0x7fffffffdefa --> 0xb3b000007ffff7fe 
0016| 0x7fffffffdee8 --> 0x0 
0024| 0x7fffffffdef0 --> 0x7fffffffe2b0 --> 0x7ffff7d4cf74 --> 0x2 
0032| 0x7fffffffdef8 --> 0x7ffff7fe7c3e (<_dl_runtime_resolve_xsavec+126>:	mov    r11,rax)
0040| 0x7fffffffdf00 --> 0x55555556b3b0 --> 0x4b59 ('YK')
0048| 0x7fffffffdf08 --> 0x55555556c4f0 --> 0x4b5a ('ZK')
0056| 0x7fffffffdf10 --> 0x7ffff7d4c000 --> 0x7ffff7d46280 --> 0x7ffff7cb2cb0 (<_ZNSt7num_getIwSt19istreambuf_iteratorIwSt11char_traitsIwEEED2Ev>:	endbr64)
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 2, 0x00005555555551b0 in SQLDriverConnect@plt ()
```

Vemos que en la parte de `registers` obtenemos las credenciales en plano del SQL Server:

```wasm
[----------------------------------registers-----------------------------------]
RAX: 0x55555556c4f0 --> 0x4b5a ('ZK')
RBX: 0x5555555557d0 (<__libc_csu_init>:	endbr64)
RCX: 0xfffffffd 
RDX: 0x7fffffffdf30 ("DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost, 1401;UID=SA;PWD=N0tS3cr3t!;")
```

```
SA:N0tS3cr3t!
```
