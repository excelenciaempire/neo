# Neo — Suite de Hacking Ético, Ciberseguridad y OSINT

Suite de **subagentes de Claude Code** para pentesting ético, ciberseguridad ofensiva y OSINT,
con una **base de conocimiento offline** (mirror del 100% de la *Ethical Hacking Cheatsheet* de
afsh4ck), **OSINT en vivo** por navegador y un **backend de ejecución** de herramientas Kali.

> ⚠️ **Solo para pruebas autorizadas, formación y CTF.** Lee **[AUTHORIZATION.md](AUTHORIZATION.md)**
> antes de usarla. El uso no autorizado es ilegal.

## Qué incluye

- **La suite de agentes** (`.claude/agents/`): un orquestador + 4 especialistas.
- **Base de conocimiento** (`knowledge/`): 767 páginas de la cheatsheet en Markdown + índice +
  consolidado + catálogo de dorks de Shodan.
- **Herramientas** (`resources/`): WSTG-Scan, kali-mcp, hexstrike-ai, awesome-shodan-queries.
- **Ejecución real** (`execution/`): guía para levantar Docker + kali-mcp (MCP con 50+ tools).

## La suite (`.claude/agents/`)

| Agente | Rol | Ejemplo de invocación |
|--------|-----|-----------------------|
| **pentest-orchestrator** | Coordina el engagement por fases y delega. Punto de entrada. | *"haz un pentest a 10.10.10.5 (es mi lab)"* |
| **recon-osint** | Recon pasivo/activo + OSINT (Shodan, subdominios, DNS, correos). | *"OSINT de mi-dominio.com"* |
| **web-exploit** | Web/API OWASP WSTG (SQLi, XSS, uploads, SSRF, IDOR, WordPress). | *"audita https://miapp-autorizada.com"* |
| **network-ad** | Redes + Active Directory (SMB/LDAP/Kerberos, MITM, WiFi, pivoting). | *"kerberoast en mi DC de lab"* |
| **reporting** | Informe profesional: severidad, CVSS, evidencia, remediación. | *"genera el informe del engagement"* |

Al abrir Claude Code en esta carpeta, los agentes se detectan solos. Invócalos por nombre o deja
que **pentest-orchestrator** decida y delegue. Cada agente aplica la **puerta de autorización**
antes de cualquier acción activa.

## Base de conocimiento (`knowledge/`)

Mirror fiel (Markdown) de **[afsh4ck.gitbook.io/ethical-hacking-cheatsheet](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet)**:

- `00-index.md` — índice maestro de las **767 páginas** con enlaces.
- `cheatsheet-full.md` — **todo** el contenido consolidado en un archivo (~27k líneas).
- `pages/**` — cada apartado como archivo `.md`, con la **misma jerarquía** del sitio
  (recon, análisis de vulns, explotación web/host/red, evasión, post-explotación, Active
  Directory, enterprise, anonimato, informes, etc.).
- `osint/shodan-queries.md` — catálogo de dorks de Shodan (vendorizado).

Los agentes buscan aquí (`Grep`/`Glob`) el comando o técnica exacta antes de improvisar.

## OSINT en vivo (sin instalar nada)

`recon-osint` usa la skill **browser-harness** (control de navegador) para Shodan, dorking,
`crt.sh`, redes sociales, GitHub, Wayback, etc. Funciona hoy, sin Docker.

## Ejecución de herramientas Kali (opcional, requiere Docker)

Para lanzar nmap/sqlmap/hydra/nuclei/crackmapexec/impacket **de verdad**, levanta el backend
**kali-mcp** (contenedor Kali + MCP en `localhost:666`). Guía paso a paso en
**[execution/SETUP.md](execution/SETUP.md)**. El [`.mcp.json`](.mcp.json) ya está listo.

## Estructura

```
Neo/
├── README.md · AUTHORIZATION.md · .mcp.json · .gitignore
├── .claude/agents/       # la suite: orchestrator + recon-osint + web-exploit + network-ad + reporting
├── knowledge/            # mirror 100% de la cheatsheet + índice + consolidado + shodan
│   ├── 00-index.md · cheatsheet-full.md
│   ├── pages/**          # 767 páginas .md (jerarquía original)
│   └── osint/shodan-queries.md
├── resources/            # herramientas de terceros (gitignored; re-clonar con setup.ps1)
└── execution/SETUP.md    # Docker + kali-mcp (+ hexstrike opcional)
```

## Créditos

- **Ethical Hacking Cheatsheet** — Alex Fernández Santos ([afsh4ck](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet)).
- **WSTG-Scan** — [afsh4ck](https://github.com/afsh4ck/WSTG-Scan).
- **awesome-shodan-queries** — [jakejarvis](https://github.com/jakejarvis/awesome-shodan-queries).
- **kali-mcp** — [pabpereza](https://github.com/pabpereza/kali-mcp).
- **hexstrike-ai** — [0x4m4](https://github.com/0x4m4/hexstrike-ai).

Cada herramienta conserva su licencia y autoría (ver `resources/README.md`).

## Nota de alcance

Se **excluyó** deliberadamente `elder-plinius/G0DM0D3`: es una colección de *jailbreaks* de
LLMs (evasión de salvaguardas de IA), no tooling de seguridad ofensiva, y queda fuera del
propósito ético de esta suite.
