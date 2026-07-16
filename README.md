# Neo — Suite de Hacking Ético, Ciberseguridad y OSINT

Suite de **agentes de IA (Claude Code)** para pentesting ético, ciberseguridad ofensiva y OSINT.
Combina **5 subagentes especializados**, una **base de conocimiento offline** (mirror del 100% de
la *Ethical Hacking Cheatsheet* de afsh4ck — 767 páginas), **OSINT en vivo** por navegador y
**dos backends de ejecución real** de herramientas (kali-mcp + HexStrike AI, 200+ tools).

> ⚠️ **Solo para pruebas autorizadas, formación y CTF.** Lee **[AUTHORIZATION.md](AUTHORIZATION.md)**.
> El uso contra sistemas de terceros sin permiso explícito es ilegal.

---

## Qué puede hacer

**Sin instalar nada (Nivel 1 — conocimiento + OSINT):**
- Guiar cualquier técnica con metodología real, citando las **767 páginas** de conocimiento
  (recon, explotación, Active Directory, evasión, post-explotación, informes, CPTS/eCPPT/eWPTX).
- **OSINT en vivo** por navegador: huella de dominios/empresas/personas, subdominios, Shodan,
  dorking, `crt.sh`, GitHub leaks, Wayback, redes sociales.
- Planificar engagements por fases y **redactar informes** (severidad, CVSS, remediación).

**Con Docker (Nivel 2 — ejecución real de 200+ herramientas):**
- **recon** — nmap, masscan, amass, subfinder, theHarvester, dnsrecon, whatweb.
- **web/API** — nuclei, sqlmap, wpscan, gobuster/ffuf, nikto, arjun, commix (OWASP WSTG).
- **redes / Active Directory** — enum4linux, crackmapexec, impacket (Kerberoast/AS-REP/DCSync),
  hydra, responder, smbclient.
- **cloud / contenedores** (vía HexStrike) — prowler, trivy, scout-suite, kube-hunter/bench,
  checkov, terrascan.
- **soporte** — generación de payloads, cracking (john/hashcat), forense (binwalk/steghide/exiftool).

Pídele cosas como: *"pentest completo a esta máquina de mi lab"*, *"audita esta web mía por OWASP
Top 10"*, *"kerberoast este dominio AD de laboratorio"*, *"OSINT de mi empresa"*.

---

## Arquitectura

```
┌── Claude Code (abre la carpeta Neo/) ───────────────────────────────┐
│  5 subagentes (.claude/agents/) + knowledge/ (767 págs)             │
│                                                                     │
│  Nivel 1: browser-harness (OSINT en vivo) ─── funciona sin Docker   │
│  Nivel 2: MCP  ─┬─ kali      → contenedor Kali  (localhost:666)  50+ │
│                 └─ hexstrike → HexStrike server (:8888, en Kali) 150+│
└─────────────────────────────────────────────────────────────────────┘
```

### La suite (`.claude/agents/`)
| Agente | Rol |
|--------|-----|
| **pentest-orchestrator** | Punto de entrada. Coordina el engagement por fases y delega (en paralelo). |
| **recon-osint** | Recon pasivo/activo + OSINT (Shodan, subdominios, DNS, correos, personas). |
| **web-exploit** | Web/API OWASP WSTG (SQLi, XSS, uploads, SSRF, IDOR, WordPress). |
| **network-ad** | Redes + Active Directory (SMB/LDAP/Kerberos, MITM, WiFi, pivoting). |
| **reporting** | Informe profesional: severidad, CVSS, evidencia, remediación. |

Cada agente aplica la **puerta de autorización** (objetivo + base legítima + nivel de
intrusividad) antes de cualquier acción activa.

### Base de conocimiento (`knowledge/`)
Mirror fiel de **[afsh4ck.gitbook.io/ethical-hacking-cheatsheet](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet)**:
`00-index.md` (índice de 767 páginas) · `cheatsheet-full.md` (~27k líneas) ·
`pages/**` (cada apartado, jerarquía original) · `osint/shodan-queries.md`.

---

## Instalación desde cero

```bash
git clone https://github.com/excelenciaempire/neo.git
cd neo
pwsh resources/setup.ps1          # clona las herramientas de terceros en resources/
```

- **Nivel 1** funciona ya: abre Claude Code en `neo/` → los 5 agentes + conocimiento + OSINT.
- **Nivel 2** (ejecución real) — sigue [`execution/SETUP.md`](execution/SETUP.md):
  1. Instalar Docker Desktop (+ WSL2 en Windows).
  2. `bash resources/kali-mcp/init.sh` → backend **kali-mcp** en `localhost:666`.
  3. `bash execution/setup-hexstrike.sh` → backend **HexStrike** en el contenedor.
  4. Reiniciar Claude Code en `neo/` para cargar los MCP `kali` y `hexstrike`.

---

## Uso

```
> usa pentest-orchestrator para auditar 10.10.10.5 (mi lab de HackTheBox)
> recon-osint: OSINT de mi-dominio.com
> web-exploit: audita https://miapp-autorizada.com
> network-ad: kerberoast en mi DC de lab
```

---

## Ética y alcance
- Solo objetivos **autorizados** (permiso escrito, lab/CTF, o de tu propiedad). Ver [`AUTHORIZATION.md`](AUTHORIZATION.md).
- **No** DoS, ni ataques destructivos, ni targeting masivo, ni exfiltración masiva (solo PoC mínima).
- OSINT de personas: solo datos públicos y con fin autorizado; sin acoso ni de-anonimización.
- Se **excluyó** deliberadamente `elder-plinius/G0DM0D3` (jailbreaks de LLM): no es tooling de
  seguridad ofensiva y queda fuera del propósito ético de la suite.

## Estructura
```
Neo/
├── README.md · AUTHORIZATION.md · CLAUDE.md · .mcp.json · .gitignore
├── .claude/agents/       # orchestrator + recon-osint + web-exploit + network-ad + reporting
├── knowledge/            # mirror 100% de la cheatsheet + índice + consolidado + shodan
├── resources/            # herramientas de terceros (gitignored; re-clonar con setup.ps1)
└── execution/            # SETUP.md + setup-hexstrike.sh (Docker + kali-mcp + HexStrike)
```

## Créditos
Ethical Hacking Cheatsheet — [afsh4ck](https://afsh4ck.gitbook.io/ethical-hacking-cheatsheet) ·
WSTG-Scan — [afsh4ck](https://github.com/afsh4ck/WSTG-Scan) ·
awesome-shodan-queries — [jakejarvis](https://github.com/jakejarvis/awesome-shodan-queries) ·
kali-mcp — [pabpereza](https://github.com/pabpereza/kali-mcp) ·
hexstrike-ai — [0x4m4](https://github.com/0x4m4/hexstrike-ai).
Cada herramienta conserva su licencia y autoría (ver `resources/README.md`).
