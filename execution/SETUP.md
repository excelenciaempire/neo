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

## 5. (Opcional) hexstrike-ai — backend avanzado (150+ tools)
Requiere Python 3 y muchas herramientas Linux → **córrelo dentro del contenedor Kali** (o en
una VM Kali con acceso a la red objetivo), no en el host Windows.
```bash
# dentro de Kali:
git clone https://github.com/0x4m4/hexstrike-ai.git && cd hexstrike-ai
python3 -m venv hexstrike-env && source hexstrike-env/bin/activate
pip3 install -r requirements.txt
python3 hexstrike_server.py         # server en :8888
```
Añade su MCP (edita `../.mcp.json`), apuntando `--server` a la IP/puerto donde corra:
```json
"hexstrike-ai": {
  "command": "python3",
  "args": ["/ruta/hexstrike-ai/hexstrike_mcp.py", "--server", "http://127.0.0.1:8888"],
  "timeout": 300,
  "alwaysAllow": []
}
```
Mantén `alwaysAllow: []` para exigir confirmación en cada ejecución autónoma.

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
