#!/usr/bin/env bash
# Instala hexstrike-ai DENTRO del contenedor kali-mcp (idempotente).
# Requisitos: contenedor `kali-mcp` corriendo (resources/kali-mcp/init.sh) y `docker` en PATH.
# Uso:  bash execution/setup-hexstrike.sh
set -uo pipefail
DOCKER="${DOCKER:-docker}"
CT=kali-mcp
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HEX_SRC="$REPO_ROOT/resources/hexstrike-ai"

echo "[*] Verificando contenedor $CT..."
"$DOCKER" ps --filter name=$CT --format '{{.Names}}' | grep -q "$CT" || {
  echo "ERROR: el contenedor $CT no esta corriendo. Ejecuta primero: bash resources/kali-mcp/init.sh"; exit 1; }

if [ ! -f "$HEX_SRC/hexstrike_server.py" ]; then
  echo "[*] hexstrike-ai no esta en resources/, clonando..."
  git clone --depth 1 https://github.com/0x4m4/hexstrike-ai.git "$HEX_SRC"
fi

echo "[*] Copiando hexstrike al contenedor (si falta)..."
"$DOCKER" exec "$CT" bash -lc 'test -f /opt/hexstrike-ai/hexstrike_server.py' 2>/dev/null \
  || "$DOCKER" cp "$HEX_SRC" "$CT:/opt/hexstrike-ai"

echo "[*] Bootstrap pip + dependencias (idempotente)..."
"$DOCKER" exec "$CT" bash -lc '
set -e
python3 -m pip --version >/dev/null 2>&1 || {
  curl -fsSL https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
  python3 /tmp/get-pip.py --break-system-packages
}
for p in psutil flask aiohttp beautifulsoup4 fastmcp selenium webdriver-manager mitmproxy; do
  mod=$(echo "$p" | sed "s/beautifulsoup4/bs4/; s/webdriver-manager/webdriver_manager/")
  if python3 -c "import $mod" 2>/dev/null; then echo "  ok  $p"; continue; fi
  echo "  instalando $p ..."
  pip3 install --break-system-packages --ignore-installed --root-user-action=ignore \
       --retries 10 --timeout 90 "$p" >/dev/null 2>&1 || echo "  WARN fallo $p (reintenta)"
done
python3 -c "import flask,psutil,requests,aiohttp,bs4,selenium,mitmproxy,fastmcp,webdriver_manager" \
  && echo "[+] Dependencias OK"
'
echo "[+] hexstrike listo. El servidor :8888 se arranca bajo demanda desde el MCP bridge (.mcp.json)."
echo "    Nota: NO uses 'docker commit' para persistir (corrompe la imagen de 15GB); si recreas"
echo "    el contenedor (rebuild/rm), vuelve a ejecutar este script."
