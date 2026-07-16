# Backend de ejecución — Docker + kali-mcp (+ hexstrike opcional)

Los subagentes **razonan y guían** sin instalar nada, y hacen **OSINT en vivo** con
`browser-harness`. Para **ejecutar herramientas Kali reales** (nmap, sqlmap, hydra, nuclei,
crackmapexec, impacket…) necesitas levantar el backend de ejecución en este equipo Windows.

## 0. Requisitos (verificados en este equipo)
- Windows 11 (build 26200). Virtualización de firmware: **activada** ✅.
- **Sin Docker / sin WSL** todavía → los instala el paso 1–2.
- Se requieren **permisos de administrador (UAC)** y **al menos un reinicio**.

## 1. WSL2 (backend de Docker Desktop)
En **PowerShell como Administrador**:
```powershell
wsl --install --no-distribution
```
Esto instala el kernel WSL2. **Reinicia** si lo pide.

## 2. Docker Desktop (sin winget → descarga directa)
En PowerShell (Administrador):
```powershell
$u = 'https://desktop.docker.com/win/main/amd64/Docker Desktop Installer.exe'
$o = "$env:TEMP\DockerDesktopInstaller.exe"
Invoke-WebRequest -Uri $u -OutFile $o
Start-Process -Wait $o -ArgumentList 'install','--quiet','--accept-license','--backend=wsl-2'
```
Al terminar, **reinicia** e inicia **Docker Desktop**. Espera a que el motor esté "running":
```powershell
docker version
docker ps
```

## 3. Levantar kali-mcp
kali-mcp construye un contenedor Kali y expone el MCP en `http://localhost:666/mcp`.
En **Git Bash** (con el `docker` de Docker Desktop en el PATH):
```bash
cd resources/kali-mcp
./init.sh          # docker compose up -d --build; espera a que el MCP esté sano
```
La primera build tarda varios minutos (descarga Kali + 50+ herramientas).

El proyecto ya trae [`../.mcp.json`](../.mcp.json) apuntando a `http://localhost:666/mcp`, así
que al abrir Claude Code en `Neo/` se detecta el servidor MCP `kali` automáticamente.

## 4. Verificación (objetivo autorizado)
`scanme.nmap.org` es el host que **Nmap ofrece explícitamente para pruebas**:
```bash
curl -s http://localhost:666/mcp   # el endpoint responde
```
Y desde el agente (tool MCP `kali` → `nmap_scan`):
```
nmap_scan  target=scanme.nmap.org  options="-sV -T4 --top-ports 100"
```
Debe devolver puertos/servicios. A partir de aquí, los subagentes pueden usar las tools MCP.

## 5. hexstrike-ai — segundo backend (150+ tools) DENTRO del contenedor Kali

hexstrike-ai corre **dentro del contenedor kali-mcp** (reutiliza sus herramientas y su Python),
y su MCP se conecta vía `docker exec` — así **no necesitas Python en Windows**. Ya viene
configurado en [`../.mcp.json`](../.mcp.json) como servidor MCP `hexstrike`.

**Instalar/restaurar** (idempotente):
```bash
bash execution/setup-hexstrike.sh   # copia hexstrike al contenedor + instala deps (flask, fastmcp, selenium, mitmproxy...)
```
El script instala pip vía `get-pip.py` (esquiva mirrors de Kali) y solo las dependencias
necesarias (se omiten `angr`/`pwntools`, pesados y de uso lazy).

**Cómo se conecta**: el bridge `hexstrike` de `.mcp.json` arranca el server `:8888` **bajo
demanda** (`docker exec -i kali-mcp ... hexstrike_mcp.py`). No hace falta arrancarlo a mano.

> ⚠️ **NO uses `docker commit`** para persistir hexstrike: en esta imagen de ~15 GB corrompió
> el snapshot de containerd y dejó el contenedor en crash-loop. hexstrike vive en la capa de
> escritura del contenedor (sobrevive a reinicios); si **recreas** el contenedor (`init.sh`
> rebuild / `docker rm`), vuelve a ejecutar `setup-hexstrike.sh`.

> El MCP `hexstrike` requiere `docker` en el PATH del sistema (Docker Desktop lo añade tras
> instalar) y el contenedor `kali-mcp` corriendo.

## 6. VulnForce — motor de informes (servicio Docker + MCP)

Web-app de reporting de pentest con **MCP nativo**. Corre como **3er servicio** del stack (junto a
kali-mcp:666 y hexstrike:8888). Build + run en Windows/Docker:
```bash
docker build -t vulnforce:latest resources/VulnForce
docker run -d --name vulnforce --restart unless-stopped --user 0 -p 47474:3000 \
  -v "C:/Users/river/Desktop/Neo/execution/vulnforce-data:/app/data" vulnforce:latest
```
- **UI**: http://localhost:47474 · **MCP**: `http://localhost:47474/api/mcp` (ya en
  [`../.mcp.json`](../.mcp.json) como server `vulnforce`).
- Verificar: `curl -s -o /dev/null -w "%{http_code}" http://localhost:47474/` → **200**;
  el MCP responde a `initialize` (serverInfo `vulnforce`).
- Datos en `execution/vulnforce-data/` (**gitignored** — informes = sensibles). Expón solo en localhost/VPN.
- Tools MCP: `list_projects`, `create_report`, `create_finding` (severidad+CVSS), `append_to_report`
  (marcador `{{findings.table}}`), `list_findings`… El subagente `reporting` las usa; export a PDF/HTML/MD desde la UI.

## 7. raptor — SAST / SCA dentro de kali-mcp

Instala (idempotente) la **capa Python headless** de raptor en el contenedor kali-mcp:
```bash
docker exec kali-mcp bash -lc 'git clone --depth 1 https://github.com/gadievron/raptor.git /opt/raptor; \
  cd /opt/raptor && pip3 install --break-system-packages --root-user-action=ignore -r requirements.txt && \
  pip3 install --break-system-packages --root-user-action=ignore semgrep'
```
Uso vía la tool MCP `execute_command` (**solo código propio/autorizado**; los PoCs no se versionan):
```
python3 /opt/raptor/raptor.py scan --repo <ruta> --policy-groups owasp,secrets   # SAST (Semgrep) -> SARIF/JSON
python3 /opt/raptor/raptor.py sca  --repo <ruta>                                  # SCA / SBOM + CVEs de dependencias
```
Los modos `analyze`/`validate` (validación de explotabilidad con LLM) requieren API key. **No** se
integra la capa de orquestación Claude Code de raptor (sería redundante con Neo).

## Notas de esta instalación en Windows (gotchas ya resueltos)

Al montar esto en Windows 11 aparecieron 2 problemas; si **re-clonas** kali-mcp, aplícalos
antes de `./init.sh`:

1. **`entrypoint.sh` con finales de línea CRLF** → el contenedor entra en crash-loop con
   `exec /entrypoint.sh: no such file or directory` (Linux interpreta el shebang como
   `/bin/bash\r`). Arréglalo a LF:
   ```bash
   sed -i 's/\r$//' resources/kali-mcp/docker/entrypoint.sh
   ```
   (Recomendado además: `git config --global core.autocrlf input` para no reintroducirlo.)

2. **`searchsploit -u` descarga `exploitdb-papers` (~2.5 GB)** desde un mirror lento y cuelga
   el build. Ya se editó `docker/Dockerfile` para quitarlo (searchsploit sigue funcionando con
   el paquete `exploitdb`). Si re-clonas, elimina `searchsploit -u ||true &&` de esa línea `RUN`.

## Cargar las tools MCP en Claude Code

El MCP `kali` se detecta al **arrancar** Claude Code. Si abriste Claude Code en `Neo/` **antes**
de que el contenedor estuviera arriba, **reinicia Claude Code** (o `/mcp`) para que cargue las
tools `mcp__kali__*` (nmap_scan, sqlmap_scan, etc.). Verifica el servidor con:
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:666/mcp   # 405 = vivo (espera POST)
```

## Verificación realizada (referencia)
- Contenedor `kali-mcp` `Up (healthy)`, MCP `kali_mcp v1.22.0`, tools expuestas OK.
- Scan real autorizado: `nmap -Pn -sV --top-ports 50 scanme.nmap.org` → 1 host up, puertos
  detectados en ~192 s. `scanme.nmap.org` es el objetivo que el proyecto Nmap ofrece para pruebas.

## Troubleshooting (kali-mcp)
- `init.sh` colgado en "Waiting for MCP server" → `docker ps`, `docker logs kali-mcp` (revisa CRLF).
- Puerto 666 ocupado → cambia el mapeo en `docker/compose.yml` y en `../.mcp.json`.
- Build falla → reintenta (repos de Kali a veces caídos), verifica salida a Internet.

> Toda ejecución queda sujeta a [`../AUTHORIZATION.md`](../AUTHORIZATION.md). Herramientas
> intrusivas (sqlmap/hydra/john/metasploit) requieren confirmación explícita.
