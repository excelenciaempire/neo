# resources/ — Herramientas de terceros

Estos repositorios se **clonan localmente** para analizar y ejecutar, pero **no se versionan**
en este repo (ver `.gitignore`) para no republicar código de terceros ni sus licencias. Cada
uno mantiene su propia licencia y autoría.

| Carpeta | Repo original | Rol en la suite | Licencia |
|---------|---------------|-----------------|----------|
| `WSTG-Scan/` | https://github.com/afsh4ck/WSTG-Scan | Scanner web OWASP WSTG + API Top 10 (Python) | MIT |
| `awesome-shodan-queries/` | https://github.com/jakejarvis/awesome-shodan-queries | Catálogo de dorks de Shodan (OSINT) — vendorizado en `knowledge/osint/shodan-queries.md` | MIT |
| `kali-mcp/` | https://github.com/pabpereza/kali-mcp | Backend de EJECUCIÓN: MCP + contenedor Kali con 50+ herramientas | Ver repo |
| `hexstrike-ai/` | https://github.com/0x4m4/hexstrike-ai | Backend de ejecución avanzado (150+ tools, Python) — opcional | Ver repo |

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

## Excluido

`elder-plinius/G0DM0D3` **no** se incluye: es una colección de *jailbreaks* de LLMs (evasión de
salvaguardas de IA), no una herramienta de seguridad ofensiva. Queda fuera del propósito ético
de esta suite (ver [`../AUTHORIZATION.md`](../AUTHORIZATION.md)).
