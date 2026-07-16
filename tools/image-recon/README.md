# image-recon — OSINT por imagen (arsenal de Neo)

Herramienta **propia** de Neo (no un clon de terceros). Versión **ética y ligera** de un
"reverse image / similarity" al estilo Lenso, **sin** reconocimiento facial contra internet.

> ⚠️ Solo sobre imágenes propias, con consentimiento, o dentro de un engagement autorizado
> (`AUTHORIZATION.md`). El matching es **solo contra un corpus que tú aportas** — no contra
> "todo internet". La búsqueda inversa/facial de personas requiere autorización explícita.

## Qué hace

**Ligero** (system python: `pillow` + `imagehash`):
| Comando | Función |
|---|---|
| `meta <img>` | EXIF/GPS (exiftool) + `phash`/`dhash`; si hay GPS, devuelve `maps_url`. |
| `hash <img>` | `phash` / `dhash` / `ahash` (hashing perceptual). |
| `search <url-img>` | Genera URLs de **búsqueda inversa** (Yandex / TinEye / Google Lens / Bing) para abrir con `browser-harness`. |
| `index <dir> -o idx.json` | Índice pHash de un **corpus propio/autorizado**. |
| `match <img> idx.json` | Casi-duplicados en el corpus por **distancia Hamming** (`-t` umbral, `-l` límite). |

**Semántico** (venv CLIP: `/opt/image-recon-venv/bin/python`, con `torch`+`sentence-transformers`+`faiss`):
| Comando | Función |
|---|---|
| `embed <img>` | Embedding CLIP (dim + norma). |
| `cindex <dir> -o clip` | Índice **FAISS** de embeddings CLIP de un corpus propio → `clip.faiss` + `clip.paths.json`. |
| `csearch <img> clip` | Búsqueda **imagen→imagen** (semántica, no solo duplicados). |
| `csearch "texto" clip --text` | Búsqueda **texto→imagen** (ej. `"a person wearing a red jacket"`). `--min-sim` filtra. |

> El pHash encuentra **casi-duplicados**; CLIP encuentra **similitud semántica** (misma escena/objeto
> aunque la imagen sea distinta) y permite consultar por **texto**. Ambos, solo sobre tu corpus.

## Instalación (en el contenedor kali-mcp)
```bash
docker exec kali-mcp bash -lc 'mkdir -p /opt/image-recon'
docker cp tools/image-recon/image_recon.py kali-mcp:/opt/image-recon/image_recon.py
# ligero:
docker exec kali-mcp pip3 install --break-system-packages pillow imagehash
# semantico (venv aislado; torch CPU + CLIP + FAISS):
docker exec kali-mcp bash -lc 'python3 -m virtualenv /opt/image-recon-venv && \
  /opt/image-recon-venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu && \
  /opt/image-recon-venv/bin/pip install sentence-transformers faiss-cpu pillow numpy'
```

## Uso (vía la tool MCP `execute_command`)
```bash
# ligero (system python)
python3 /opt/image-recon/image_recon.py meta   /ruta/foto.jpg
python3 /opt/image-recon/image_recon.py search https://sitio/foto.jpg
python3 /opt/image-recon/image_recon.py index  /casos/set-autorizado -o /tmp/idx.json
python3 /opt/image-recon/image_recon.py match  /ruta/query.jpg /tmp/idx.json -t 8

# semantico (venv CLIP)
V=/opt/image-recon-venv/bin/python
$V /opt/image-recon/image_recon.py cindex  /casos/set-autorizado -o /tmp/clip
$V /opt/image-recon/image_recon.py csearch /ruta/query.jpg /tmp/clip          # imagen->imagen
$V /opt/image-recon/image_recon.py csearch "a red car at night" /tmp/clip --text --min-sim 0.2
```
Modelo por defecto `clip-ViT-B-32` (override con `IMAGE_RECON_CLIP`). El primer `cindex` descarga el modelo (~600 MB).

## Roadmap (opcional)
- Detección de rostros local (recorte/alineado) para acotar el embedding a la cara — siempre
  sobre corpus propio, nunca indexando a terceros.
- Modelos CLIP mayores (ViT-L) o multilingües para consultas de texto en español.
