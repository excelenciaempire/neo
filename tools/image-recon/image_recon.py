#!/usr/bin/env python3
"""
image-recon - OSINT por imagen (etico, scoped). Parte del arsenal de Neo.

Hace:
  - meta    : metadatos EXIF/GPS (exiftool) + hash perceptual de una imagen.
  - hash    : pHash/dHash/aHash de una imagen.
  - search  : dada la URL de una imagen, genera las URLs de busqueda inversa
              (Yandex / TinEye / Google Lens / Bing) para abrir con browser-harness.
  - index   : construye un indice pHash de un CORPUS PROPIO/autorizado (-> JSON).
  - match   : busca casi-duplicados de una imagen contra ese indice (distancia Hamming).

NO hace reconocimiento facial contra internet (eso seria vigilancia biometrica de
terceros no consentida). El matching es SOLO contra un corpus que tu aportas.

Uso etico: imagenes propias, con consentimiento, o dentro de un engagement autorizado
(ver AUTHORIZATION.md). La busqueda inversa/facial de personas solo con autorizacion.
"""
import argparse
import json
import os
import sys
import subprocess
import urllib.parse

BANNER = "[image-recon] uso solo sobre imagenes propias/autorizadas (ver AUTHORIZATION.md)"


def _need(mod):
    try:
        return __import__(mod)
    except ImportError:
        sys.exit(f"ERROR: falta el paquete '{mod}'. Instala: pip3 install pillow imagehash")


def _phash(path, kind="phash"):
    imagehash = _need("imagehash")
    Image = _need("PIL").Image
    img = Image.open(path)
    fn = {"phash": imagehash.phash, "dhash": imagehash.dhash, "ahash": imagehash.average_hash}[kind]
    return str(fn(img))


def _exif(path):
    """EXIF/GPS via exiftool (JSON). Devuelve dict o {}."""
    try:
        out = subprocess.run(["exiftool", "-json", "-n", path],
                             capture_output=True, text=True, timeout=60)
        data = json.loads(out.stdout or "[]")
        return data[0] if data else {}
    except Exception as e:
        return {"_exiftool_error": str(e)}


def cmd_meta(args):
    if not os.path.isfile(args.image):
        sys.exit(f"no existe: {args.image}")
    ex = _exif(args.image)
    gps = {}
    for k in ("GPSLatitude", "GPSLongitude", "GPSPosition", "GPSAltitude", "GPSDateTime"):
        if k in ex:
            gps[k] = ex[k]
    result = {
        "file": args.image,
        "phash": _phash(args.image, "phash"),
        "dhash": _phash(args.image, "dhash"),
        "camera": {k: ex.get(k) for k in ("Make", "Model", "LensModel", "Software") if ex.get(k)},
        "timestamps": {k: ex.get(k) for k in ("DateTimeOriginal", "CreateDate", "ModifyDate") if ex.get(k)},
        "gps": gps,
    }
    if gps.get("GPSLatitude") and gps.get("GPSLongitude"):
        result["gps"]["maps_url"] = f"https://www.google.com/maps?q={gps['GPSLatitude']},{gps['GPSLongitude']}"
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_hash(args):
    print(json.dumps({
        "file": args.image,
        "phash": _phash(args.image, "phash"),
        "dhash": _phash(args.image, "dhash"),
        "ahash": _phash(args.image, "ahash"),
    }, indent=2))


def cmd_search(args):
    """Genera URLs de busqueda inversa a partir de la URL publica de una imagen."""
    u = urllib.parse.quote(args.url, safe="")
    engines = {
        "yandex":       f"https://yandex.com/images/search?rpt=imageview&url={u}",
        "tineye":       f"https://tineye.com/search?url={u}",
        "google_lens":  f"https://lens.google.com/uploadbyurl?url={u}",
        "bing_visual":  f"https://www.bing.com/images/searchbyimage?cbir=sbi&imgurl={u}",
    }
    print(json.dumps({
        "note": "Abre estas URLs con browser-harness (Google Lens/Bing pueden requerir sesion).",
        "image_url": args.url,
        "reverse_search": engines,
    }, indent=2, ensure_ascii=False))


def _iter_images(root):
    exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}
    for dp, _, files in os.walk(root):
        for f in files:
            if os.path.splitext(f)[1].lower() in exts:
                yield os.path.join(dp, f)


def cmd_index(args):
    if not os.path.isdir(args.corpus):
        sys.exit(f"no es un directorio: {args.corpus}")
    idx = {}
    n = 0
    for p in _iter_images(args.corpus):
        try:
            idx[p] = _phash(p, "phash")
            n += 1
        except Exception as e:
            print(f"skip {p}: {e}", file=sys.stderr)
    with open(args.out, "w") as fh:
        json.dump({"kind": "phash", "corpus": os.path.abspath(args.corpus), "entries": idx}, fh)
    print(f"[+] indexadas {n} imagenes -> {args.out}")


def cmd_match(args):
    imagehash = _need("imagehash")
    with open(args.index) as fh:
        data = json.load(fh)
    qh = imagehash.hex_to_hash(_phash(args.image, "phash"))
    results = []
    for path, hexh in data.get("entries", {}).items():
        try:
            d = qh - imagehash.hex_to_hash(hexh)
            if d <= args.threshold:
                results.append({"match": path, "hamming": int(d)})
        except Exception:
            continue
    results.sort(key=lambda r: r["hamming"])
    print(json.dumps({
        "query": args.image,
        "threshold": args.threshold,
        "matches": results[: args.limit],
        "total_matches": len(results),
    }, indent=2, ensure_ascii=False))


def main():
    print(BANNER, file=sys.stderr)
    p = argparse.ArgumentParser(prog="image-recon", description="OSINT por imagen (etico, scoped).")
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("meta", help="EXIF/GPS + hash de una imagen"); m.add_argument("image"); m.set_defaults(fn=cmd_meta)
    h = sub.add_parser("hash", help="pHash/dHash/aHash"); h.add_argument("image"); h.set_defaults(fn=cmd_hash)
    s = sub.add_parser("search", help="URLs de busqueda inversa desde una URL de imagen"); s.add_argument("url"); s.set_defaults(fn=cmd_search)
    i = sub.add_parser("index", help="indexa un corpus propio (pHash)")
    i.add_argument("corpus"); i.add_argument("-o", "--out", default="corpus_index.json"); i.set_defaults(fn=cmd_index)
    mt = sub.add_parser("match", help="busca casi-duplicados en el corpus")
    mt.add_argument("image"); mt.add_argument("index")
    mt.add_argument("-t", "--threshold", type=int, default=10); mt.add_argument("-l", "--limit", type=int, default=20)
    mt.set_defaults(fn=cmd_match)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
