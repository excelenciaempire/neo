# Burp Suite AI — "Custom AI Agent" (six2dez) · integración condicional

**Único** de los 3 repos de Burp AI que Neo puede **invocar** de verdad: es una extensión de Burp
(Kotlin/Montoya) que **embebe un servidor MCP** (SSE `http://127.0.0.1:9876/sse`, hasta **59 tools**
de Burp) + trae una skill `burp-scan` pensada para que un CLI de IA (como Neo/Claude Code) sea el
motor de razonamiento sobre Burp. Repo: https://github.com/six2dez/burp-ai-agent (MIT).

> **Condicional**: el MCP solo existe mientras **tú** tengas **Burp Suite abierto** con la extensión
> cargada y el MCP activado. Neo **no** puede levantar Burp ni por `execute_command`. Si no está,
> `web-exploit` degrada limpiamente a hexstrike/kali-mcp (sin inventar resultados).

## Requisitos
- **Burp Suite** (Community o Pro 2023.12+) instalado en el host. Node.js 18+ (para el puente MCP).
- Scanner pasivo/activo y algunas tools `[pro]` requieren **Burp Professional**; el análisis manual
  y la mayoría de tools MCP funcionan en **Community**.

## Instalar la extensión en tu Burp
- **BApp Store**: Extensions → BApp Store → busca **"Custom AI Agent"** → Install. (build 'store', 8 tools)
- **o .jar completo** (59 tools): descarga el `.jar` de *Releases* del repo (o `./gradlew clean shadowJar`
  con JAVA_HOME=jdk-21) → Extensions → Installed → Add → Java → selecciona el `.jar`.

## Activar el MCP y conectarlo a Neo
1. En Burp: **Settings → MCP Server → Enable** (SSE en `127.0.0.1:9876`). Si activas *External Access*,
   se genera un token (header `Authorization: Bearer <token>`).
2. En Neo, añade el servidor MCP **cuando vayas a usar Burp** (no está en `.mcp.json` por defecto para
   no dar errores en máquinas sin Burp):
   ```bash
   claude mcp add --transport sse burp http://127.0.0.1:9876/sse
   ```
   o añade a `.mcp.json`:
   ```json
   "burp": { "type": "sse", "url": "http://127.0.0.1:9876/sse" }
   ```
   (con External Access, añade el header Authorization con tu token).
3. Reinicia Claude Code para que cargue el MCP `burp`.

## Tools clave (vía el MCP `burp`)
Navegación/estado: `status`, `scope_check`, `proxy_history`, `site_map`.
Envío: `http1_request` / `http2_request`, `send_to_repeater`, `intruder_*`.
OOB: `collaborator_*`. Hallazgos: `issue_create`. (Las `[unsafe]`/`[pro]` mutan estado o requieren Pro.)

## Cómo lo usa `web-exploit`
1. **Preflight**: llama `status`/`scope_check`. Si el MCP no responde → avisa "Burp no está corriendo
   con el MCP" y sigue con hexstrike/kali-mcp. **Nunca** inventes resultados.
2. Protocolo: **pasivo** (proxy_history, site_map, passive) → **activo** (http requests, intruder) →
   **OOB** (collaborator) → **report** (issue_create / VulnForce).
3. **Autorización**: las tools mutantes/`[unsafe]` (http1_request, intruder, collaborator) solo tras
   confirmar alcance (`AUTHORIZATION.md`). Confina el MCP a hosts **in-scope** (Scoped MCP Access).

> La skill original `burp-scan` está en el repo (`skills/burp-scan/SKILL.md`); puedes copiarla a
> `.claude/skills/` si quieres su protocolo completo.
