# image-recon — OSINT por imagen (arsenal de Neo)

Herramienta **propia** de Neo (no un clon de terceros). Versión **ética y ligera** de un
"reverse image / similarity" al estilo Lenso, **sin** reconocimiento facial contra internet.

> ⚠️ Solo sobre imágenes propias, con consentimiento, o dentro de un engagement autorizado
> (`AUTHORIZATION.md`). El matching es **solo contra un corpus que tú aportas** — no contra
> "todo internet". La búsqueda inversa/facial de personas requiere autorización explícita.

## Qué hace
| Comando | Función |
|---|---|
| `meta <img>` | EXIF/GPS (exiftool) + `phash`/`dhash`; si hay GPS, devuelve `maps_url`. |
| `hash <img>` | `phash` / `dhash` / `ahash` (hashing perceptual). |
| `search <url-img>` | Genera URLs de **búsqueda inversa** (Yandex / TinEye / Google Lens / Bing) para abrir con `browser-harness`. |
| `index <dir> -o idx.json` | Construye índice pHash de un **corpus propio/autorizado**. |
| `match <img> idx.json` | Casi-duplicados en el corpus por **distancia Hamming** (`-t` umbral, `-l` límite). |

## Instalación (en el contenedor kali-mcp)
```bash
docker exec kali-mcp bash -lc 'mkdir -p /opt/image-recon'
docker cp tools/image-recon/image_recon.py kali-mcp:/opt/image-recon/image_recon.py
docker exec kali-mcp pip3 install --break-system-packages pillow imagehash
```

## Uso (vía la tool MCP `execute_command`)
```bash
python3 /opt/image-recon/image_recon.py meta   /ruta/foto.jpg
python3 /opt/image-recon/image_recon.py search https://sitio/foto.jpg
python3 /opt/image-recon/image_recon.py index  /casos/set-autorizado -o /tmp/idx.json
python3 /opt/image-recon/image_recon.py match  /ruta/query.jpg /tmp/idx.json -t 8
```

## Roadmap (opcional, no incluido por peso)
- Similitud **semántica** con embeddings **CLIP** + índice **FAISS** (requiere torch, ~2 GB).
- Detección de rostros local (recorte/alineado) para acotar el pHash a la cara — siempre
  sobre corpus propio, nunca indexando a terceros.
