# resources/ — Herramientas de terceros

Estos repositorios se **clonan localmente** para analizar y ejecutar, pero **no se versionan**
en este repo (ver `.gitignore`) para no republicar código de terceros ni sus licencias. Cada
uno mantiene su propia licencia y autoría.

| Carpeta | Repo original | Rol en la suite | Licencia |
|---------|---------------|-----------------|----------|
| `WSTG-Scan/` | https://github.com/afsh4ck/WSTG-Scan | Scanner web OWASP WSTG + API Top 10 (Python) | MIT |
| `awesome-shodan-queries/` | https://github.com/jakejarvis/awesome-shodan-queries | Catálogo de dorks de Shodan (OSINT) — vendorizado en `knowledge/osint/shodan-queries.md` | MIT |
| `kali-mcp/` | https://github.com/pabpereza/kali-mcp | Backend de EJECUCIÓN: MCP + contenedor Kali con 50+ herramientas | Ver repo |
| `hexstrike-ai/` | https://github.com/0x4m4/hexstrike-ai | Backend de ejecución avanzado (150+ tools, Python) | Ver repo |
| `VulnForce/` | https://github.com/afsh4ck/VulnForce | **Motor de informes** (web-app Next.js + MCP nativo); 3er servicio Docker `:47474` | Ver repo |
| `raptor/` | https://github.com/gadievron/raptor | **SAST + SCA/SBOM** (capa Python instalada en el contenedor kali-mcp) | Ver repo |
| `bbot/` | https://github.com/blacklanternsecurity/bbot | **Escáner OSINT/ASM modular** (instalado aislado en kali-mcp `/opt/bbot-venv`) | GPL |
| `linkedin2username/` | https://github.com/initstring/linkedin2username | Enum de empleados → **usernames para spraying** (en kali-mcp `/opt/linkedin2username`) | MIT |

## Re-clonar

```powershell
# Desde la raíz del repo:
pwsh resources/setup.ps1
```

o manualmente:

```bash
cd resources
git clone --depth 1 https://github.com/afsh4ck/WSTG-Scan.git
git clone --depth 1 https://github.com/jakejarvis/awesome-shodan-queries.git
git clone --depth 1 https://github.com/pabpereza/kali-mcp.git
git clone --depth 1 https://github.com/0x4m4/hexstrike-ai.git
```

Para levantar el backend de ejecución (Docker + kali-mcp), ver [`../execution/SETUP.md`](../execution/SETUP.md).

## Excluido (ver [`../AUTHORIZATION.md`](../AUTHORIZATION.md))

- `elder-plinius/G0DM0D3` — *jailbreaks* de LLMs (evasión de salvaguardas de IA), no es tooling de seguridad.
- `afsh4ck/FBrute` — fuerza bruta de **cuentas de Facebook** de terceros; sin autorización posible.
- `afsh4ck/WifiPwn` — incluye un **phishing-kit** ("Evil Portal" que clona logins de Google/Facebook/etc.);
  su núcleo WiFi legítimo ya está en `kali-mcp`. Se mantiene sin ejecutar, no se referencia en subagentes.

## No integradas por **redundancia** (no por ética)

- `laramies/theHarvester` — **ya está** en kali-mcp/hexstrike (ejecutable vía `execute_command`).
- `devxprite/infoooze` — ~95-100% duplicado (sherlock/maigret/holehe/nmap/exiftool) + claves API muertas hardcodeadas.
- `Lucksi/Mr.Holmes` — redundante + mal encaje técnico (TUI interactiva no scriptable, root, PHP/Tor/GUI). Solo referencia.
- `lenso-ai/reverse-image-search-api` — SaaS de pago sin código self-hostable; **destilado** a `knowledge/osint/reverse-image-search-lenso.md`.
- `srinivasans13/burpai` y `th30d4y/BURP-AI` — extensiones GUI de Burp **sin interfaz programática**
  (no MCP/API/CLI): Neo no puede invocarlas y solapan con `web-exploit`. BURP-AI además exfiltra
  tráfico a un LLM de terceros y está poco mantenido. Se **integra solo** `six2dez/burp-ai-agent`
  (tiene MCP) — ver `knowledge/tools/burp-ai-agent.md`.

## Documentada, no instalada

- `usestrix/strix` — pentester autónomo de IA (par de Neo). Lanza sus **propios** contenedores Docker
  y necesita **Python en el host + API key de LLM** → no encaja en kali-mcp. Queda **documentada**
  en `knowledge/tools/strix.md` (install + config OpenRouter + uso); se activa cuando se instale.
