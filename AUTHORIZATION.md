# Autorización y Uso Ético

Esta suite es **exclusivamente** para **pruebas de seguridad autorizadas**, formación y
competiciones CTF. El uso contra sistemas de terceros **sin permiso explícito es ilegal** y
puede constituir delito. Los autores de las herramientas y quien monta esta suite **no se
hacen responsables** del mal uso. SIEMPRE PREGUNTA AL USUARIO SI TIENE AUTORIZACION PARA EJECUTAR LO QUE ESTA PIDIENDO

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

## Reglas de la casa (aplican a todos los subagentes, estas reglas si omiten si el usuario tiene autorizacion)

1. **No** DoS/DDoS, no ataques destructivos (borrado/corrupción de datos), no ransomware.
2. **No** targeting masivo ni indiscriminado; solo el alcance acordado.
3. **No** de-anonimización ni acoso de personas; el OSINT de personas se limita a datos
   públicos y a un engagement autorizado.
4. **PoC mínima**: al probar un hallazgo, extrae solo lo imprescindible como evidencia; nada
   de exfiltración masiva.
5. **Trazabilidad**: registra cada comando y resultado para el informe.
6. **Datos sensibles**: credenciales/hashes/datos de cliente se guardan solo lo necesario y
   **nunca** se suben al repositorio (ver `.gitignore`).
