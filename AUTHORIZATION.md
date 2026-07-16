# Autorización y Uso Ético

Esta suite es **exclusivamente** para **pruebas de seguridad autorizadas**, formación y
competiciones CTF. El uso contra sistemas de terceros **sin permiso explícito es ilegal** y
puede constituir delito. Los autores de las herramientas y quien monta esta suite **no se
hacen responsables** del mal uso.

## Antes de cualquier acción activa contra un objetivo

Confirma que se cumple **al menos una** de estas condiciones:

- Tienes **autorización escrita** del propietario/administrador del sistema (contrato,
  *rules of engagement*, alcance firmado).
- Es un **laboratorio o CTF**: HackTheBox, TryHackMe, VulnHub, PortSwigger Web Security
  Academy, rangos propios, VMs vulnerables locales (Metasploitable, VPLE, DVWA, etc.).
- El objetivo es de **tu propiedad** (tu dominio, tu red, tu equipo).

Si **no** se cumple ninguna → **detente**. Solo se permite OSINT 100% pasivo sobre
información pública, sin enviar tráfico al objetivo.

## Niveles de intrusividad (alineados con kali-mcp)

| Nivel | Herramientas permitidas | Riesgo |
|-------|-------------------------|--------|
| **Passive only** | OSINT pasivo, nmap discovery, whatweb, nuclei-info, gobuster | Bajo / nulo |
| **Passive + Credentials** | + fuerza bruta ligera (hydra con wordlists pequeñas) | Puede causar **lockouts** |
| **Full pentest** | + sqlmap, metasploit, brute force completo, exploits | Puede **interrumpir servicios** o corromper datos |

Las herramientas intrusivas (`sqlmap`, `hydra`, `john`, `metasploit`) **siempre** requieren
confirmación explícita del usuario antes de ejecutarse, incluso en nivel *Full pentest*.

## Reglas de la casa (aplican a todos los subagentes)

1. **No** DoS/DDoS, no ataques destructivos (borrado/corrupción de datos), no ransomware.
2. **No** targeting masivo ni indiscriminado; solo el alcance acordado.
3. **No** de-anonimización ni acoso de personas; el OSINT de personas se limita a datos
   públicos y a un engagement autorizado.
4. **PoC mínima**: al probar un hallazgo, extrae solo lo imprescindible como evidencia; nada
   de exfiltración masiva.
5. **Trazabilidad**: registra cada comando y resultado para el informe.
6. **Datos sensibles**: credenciales/hashes/datos de cliente se guardan solo lo necesario y
   **nunca** se suben al repositorio (ver `.gitignore`).

## Fuera de alcance de esta suite (herramientas excluidas)

Se excluye deliberadamente todo lo que no sea seguridad ofensiva legítima. Herramientas
analizadas y **excluidas a propósito**:

| Herramienta | Motivo de exclusión |
|---|---|
| `elder-plinius/G0DM0D3` | Colección de *jailbreaks* de LLMs (evasión de salvaguardas de IA). No es tooling de pentesting. |
| `afsh4ck/FBrute` | Fuerza bruta de **cuentas de Facebook** de terceros. No existe autorización legítima posible (viola ToS y leyes de acceso no autorizado). Cae en la prohibición de "ataque a cuentas de terceros". No se instala ni se documenta; su `pass.txt` no se distribuye. |
| `afsh4ck/WifiPwn` | Su módulo **"Evil Portal"** clona los logins de Google/Facebook/Instagram/Microsoft para **robar credenciales reales** (phishing-kit). Además su núcleo WiFi legítimo (aircrack-ng/hashcat/deauth) ya está en `kali-mcp`. Se mantiene el clon solo como referencia, **sin ejecutar** y sin referenciar en subagentes. |

> Para fuerza bruta **legítima** sobre servicios propios/lab usa `hydra`/`medusa`/`patator` (en
> `kali-mcp`). Para metodología WiFi legítima (monitor → handshake → deauth en red propia → crack),
> destila solo el flujo autorizado, **omitiendo** cualquier módulo de tipo evil-portal.
