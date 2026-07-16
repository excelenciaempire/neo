# Neo — Suite de Hacking Ético / Ciberseguridad / OSINT

Este proyecto es una suite de **pentesting ético, ciberseguridad ofensiva y OSINT**.
Trabaja SIEMPRE dentro de un alcance autorizado. Lee `AUTHORIZATION.md`.

## Puerta de autorización (obligatoria antes de acciones activas)
Antes de cualquier escaneo/enumeración/explotación que envíe tráfico a un objetivo, confirma:
objetivo exacto, autorización (permiso escrito, lab/CTF, o propiedad del usuario) y nivel de
intrusividad (Passive / Passive+Credentials / Full). Si no hay autorización y no es lab/propio,
**detente y pregunta**. El OSINT 100% pasivo sobre información pública es la única excepción.

## Cómo trabajar aquí
- Para engagements completos o multi-fase, usa el subagente **pentest-orchestrator**, que delega
  en **recon-osint**, **web-exploit**, **network-ad** y **reporting** (`.claude/agents/`).
- **Base de conocimiento** (busca con `Grep`/`Glob` antes de improvisar):
  - `knowledge/00-index.md` — índice de las 767 páginas.
  - `knowledge/cheatsheet-full.md` — referencia completa consolidada.
  - `knowledge/pages/**` — cada técnica/herramienta como `.md`.
  - `knowledge/osint/shodan-queries.md` — dorks de Shodan.
- **OSINT en vivo**: skill `browser-harness` vía `Bash`.
- **Ejecución de herramientas Kali**: MCP `kali` (`http://localhost:666/mcp`), si está levantado
  (ver `execution/SETUP.md`). Herramientas intrusivas (sqlmap/hydra/john/metasploit) requieren
  confirmación explícita en cada uso.

## Reglas
- No DoS, no ataques destructivos, no targeting masivo, no exfiltración masiva (solo PoC mínima).
- Si una tool/MCP no está disponible, dilo; nunca inventes resultados.
- Registra cada comando y resultado para el informe. Datos sensibles nunca se versionan.
- Responde en el idioma del usuario (español por defecto).
