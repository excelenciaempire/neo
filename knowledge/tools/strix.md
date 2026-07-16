# Strix — pentester autónomo de IA (herramienta externa, par de Neo)

**Strix** (usestrix/strix, Apache-2.0) son **agentes autónomos de IA de pentesting**: ejecutan tu
código dinámicamente en **sandboxes Docker**, encuentran vulnerabilidades y las **validan con PoCs
reales** (no falsos positivos), generan parches y reportes. https://github.com/usestrix/strix

> **No** se instala dentro de `kali-mcp` (lanza sus **propios** contenedores Docker → sería
> Docker-en-Docker). Corre como **herramienta aparte** en el host. Se **solapa** con Neo: no es una
> tool que Neo llame por comando, sino un **par** al que le entregas un objetivo para validación
> autónoma profunda, y cuyos resultados (SARIF/report) puede consumir `reporting`/VulnForce.

## Requisitos
- **Docker** corriendo (✓). Primer run descarga la imagen sandbox.
- **Python 3 + pipx** en el host (el Windows de Neo hoy no tiene Python → instalar si se va a usar).
- **API key de LLM** (obligatoria — es un agente LLM). Aquí: **OpenRouter**.

## Instalación
```bash
pipx install strix-agent          # o: uvx strix-agent
```

## Configuración con OpenRouter
```bash
# modelo via OpenRouter (formato litellm openrouter/<vendor>/<model>)
export STRIX_LLM="openrouter/anthropic/claude-sonnet-4.6"   # o openrouter/openai/gpt-5.4, etc.
export LLM_API_KEY="<tu-api-key-de-openrouter>"
# opcionales:
export PERPLEXITY_API_KEY="..."        # capacidad de busqueda
export STRIX_REASONING_EFFORT="high"   # high (default) | medium (quick scan)
```
Elige el modelo en https://openrouter.ai/models. Sin `LLM_API_KEY` strix no arranca.

## Uso
```bash
strix --target ./ruta-codigo                                  # carpeta local
strix --target https://github.com/org/repo                    # repo
strix --target https://tu-app-autorizada.com                  # web en vivo
strix -t api.tu-app.com --instruction "IDOR y logica de negocio"
strix --target ./ --scan-mode quick --scope-mode diff --diff-base origin/main   # CI: solo el diff
strix -n --target ./ --scan-mode quick                        # -n = no interactivo (CI)
```
Resultados en `strix_runs/<run-name>/` (incluye SARIF y reporte).

## Cómo encaja en Neo
- `pentest-orchestrator`: para una **validación autónoma profunda** de un objetivo autorizado
  (código propio, repo, o URL con permiso), delega en **strix** como par externo y luego pasa su
  SARIF/reporte a `reporting`/VulnForce. Para recon/servicios/AD sigue usando kali-mcp/hexstrike.
- `web-exploit`: útil cuando quieres PoCs validados automáticamente sobre una app, no solo hallazgos.

## Ética
- **Solo objetivos autorizados** (`AUTHORIZATION.md`): strix **ejecuta código y explota** de forma
  autónoma. Úsalo sobre código propio, lab, o con permiso escrito. Los PoCs/parches generados no se
  versionan en Neo.

## Estado en Neo
- **Documentado, no instalado** (decisión del usuario). Para activarlo: instalar Python+pipx en el
  host, `pipx install strix-agent`, exportar la config de OpenRouter y correr `strix --target ...`.
