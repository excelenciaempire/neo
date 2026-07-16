#!/usr/bin/env python3
"""
image-recon - OSINT por imagen (etico, scoped). Parte del arsenal de Neo.

Comandos ligeros (system python: pillow + imagehash):
  - meta    : metadatos EXIF/GPS (exiftool) + hash perceptual de una imagen.
  - hash    : pHash/dHash/aHash de una imagen.
  - search  : dada la URL de una imagen, genera URLs de busqueda inversa
              (Yandex / TinEye / Google Lens / Bing) para abrir con browser-harness.
  - index   : indice pHash de un CORPUS PROPIO/autorizado (-> JSON).
  - match   : casi-duplicados de una imagen contra ese indice (distancia Hamming).

Comandos semanticos (requieren el venv CLIP: /opt/image-recon-venv/bin/python):
  - embed   : embedding CLIP de una imagen (dim + norma).
  - cindex  : indice FAISS de embeddings CLIP de un corpus propio.
  - csearch : busqueda semantica en el corpus. Query = imagen (img->img) o --text "..."
              (texto->imagen, ej. "a person wearing a red jacket").

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


def _need(mod, hint=None):
    try:
        return __import__(mod)
    except ImportError:
        sys.exit(f"ERROR: falta '{mod}'. {hint or 'Instala la dependencia.'}")


def _pil_image():
    try:
        from PIL import Image
        return Image
    except ImportError:
        sys.exit("ERROR: falta 'pillow'. pip3 install pillow")


# ---------- ligero (pillow + imagehash) ----------

def _phash(path, kind="phash"):
    imagehash = _need("imagehash", "pip3 install pillow imagehash")
    Image = _pil_image()
    img = Image.open(path)
    fn = {"phash": imagehash.phash, "dhash": imagehash.dhash, "ahash": imagehash.average_hash}[kind]
    return str(fn(img))


def _exif(path):
    try:
        out = subprocess.run(["exiftool", "-json", "-n", path],
                             capture_output=True, text=True, timeout=60)
        data = json.loads(out.stdout or "[]")
        return data[0] if data else {}
    except Exception as e:
        return {"_exiftool_error": str(e)}


def _iter_images(root):
    exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}
    for dp, _, files in os.walk(root):
        for f in files:
            if os.path.splitext(f)[1].lower() in exts:
                yield os.path.join(dp, f)


def cmd_meta(args):
    if not os.path.isfile(args.image):
        sys.exit(f"no existe: {args.image}")
    ex = _exif(args.image)
    gps = {k: ex[k] for k in ("GPSLatitude", "GPSLongitude", "GPSPosition", "GPSAltitude", "GPSDateTime") if k in ex}
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
    print(json.dumps({"file": args.image, "phash": _phash(args.image, "phash"),
                      "dhash": _phash(args.image, "dhash"), "ahash": _phash(args.image, "ahash")}, indent=2))


def cmd_search(args):
    u = urllib.parse.quote(args.url, safe="")
    engines = {
        "yandex":      f"https://yandex.com/images/search?rpt=imageview&url={u}",
        "tineye":      f"https://tineye.com/search?url={u}",
        "google_lens": f"https://lens.google.com/uploadbyurl?url={u}",
        "bing_visual": f"https://www.bing.com/images/searchbyimage?cbir=sbi&imgurl={u}",
    }
    print(json.dumps({"note": "Abre con browser-harness (Lens/Bing pueden requerir sesion).",
                      "image_url": args.url, "reverse_search": engines}, indent=2, ensure_ascii=False))


def cmd_index(args):
    if not os.path.isdir(args.corpus):
        sys.exit(f"no es un directorio: {args.corpus}")
    idx, n = {}, 0
    for p in _iter_images(args.corpus):
        try:
            idx[p] = _phash(p, "phash"); n += 1
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
    print(json.dumps({"query": args.image, "threshold": args.threshold,
                      "matches": results[: args.limit], "total_matches": len(results)}, indent=2, ensure_ascii=False))


# ---------- semantico (CLIP + FAISS, venv aislado) ----------

_MODEL = None


def _clip():
    """Carga perezosa del modelo CLIP (cacheado)."""
    global _MODEL
    if _MODEL is None:
        st = _need("sentence_transformers",
                   "usa el venv CLIP: /opt/image-recon-venv/bin/python ... (o pip install sentence-transformers torch faiss-cpu)")
        model_name = os.environ.get("IMAGE_RECON_CLIP", "clip-ViT-B-32")
        _MODEL = st.SentenceTransformer(model_name)
    return _MODEL


def _embed_images(paths):
    np = _need("numpy")
    Image = _pil_image()
    model = _clip()
    imgs, ok = [], []
    for p in paths:
        try:
            imgs.append(Image.open(p).convert("RGB")); ok.append(p)
        except Exception as e:
            print(f"skip {p}: {e}", file=sys.stderr)
    if not imgs:
        return ok, np.zeros((0, 512), dtype="float32")
    emb = model.encode(imgs, normalize_embeddings=True, convert_to_numpy=True)
    return ok, emb.astype("float32")


def cmd_embed(args):
    _, emb = _embed_images([args.image])
    if len(emb) == 0:
        sys.exit("no se pudo procesar la imagen")
    print(json.dumps({"file": args.image, "dim": int(emb.shape[1]),
                      "l2norm": float((emb[0] ** 2).sum() ** 0.5)}, indent=2))


def cmd_cindex(args):
    faiss = _need("faiss", "pip install faiss-cpu (en el venv CLIP)")
    paths = list(_iter_images(args.corpus))
    ok, emb = _embed_images(paths)
    if len(emb) == 0:
        sys.exit("corpus sin imagenes procesables")
    index = faiss.IndexFlatIP(emb.shape[1])   # cosine (embeddings normalizados)
    index.add(emb)
    faiss.write_index(index, args.out + ".faiss")
    with open(args.out + ".paths.json", "w") as fh:
        json.dump({"model": os.environ.get("IMAGE_RECON_CLIP", "clip-ViT-B-32"),
                   "corpus": os.path.abspath(args.corpus), "paths": ok}, fh)
    print(f"[+] indice CLIP con {len(ok)} imagenes -> {args.out}.faiss (+ .paths.json)")


def cmd_csearch(args):
    faiss = _need("faiss"); np = _need("numpy")
    index = faiss.read_index(args.index + ".faiss")
    with open(args.index + ".paths.json") as fh:
        meta = json.load(fh)
    paths = meta["paths"]
    model = _clip()
    if args.text:
        q = model.encode([args.query], normalize_embeddings=True, convert_to_numpy=True).astype("float32")
    else:
        _, q = _embed_images([args.query])
        if len(q) == 0:
            sys.exit("no se pudo procesar la imagen de consulta")
    k = min(args.limit, len(paths))
    D, I = index.search(q, k)
    matches = [{"match": paths[i], "similarity": round(float(s), 4)}
               for s, i in zip(D[0], I[0]) if i >= 0 and s >= args.min_sim]
    print(json.dumps({"query": args.query, "mode": "text->image" if args.text else "image->image",
                      "matches": matches}, indent=2, ensure_ascii=False))


def main():
    print(BANNER, file=sys.stderr)
    p = argparse.ArgumentParser(prog="image-recon", description="OSINT por imagen (etico, scoped).")
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("meta"); m.add_argument("image"); m.set_defaults(fn=cmd_meta)
    h = sub.add_parser("hash"); h.add_argument("image"); h.set_defaults(fn=cmd_hash)
    s = sub.add_parser("search"); s.add_argument("url"); s.set_defaults(fn=cmd_search)
    i = sub.add_parser("index"); i.add_argument("corpus"); i.add_argument("-o", "--out", default="corpus_index.json"); i.set_defaults(fn=cmd_index)
    mt = sub.add_parser("match"); mt.add_argument("image"); mt.add_argument("index")
    mt.add_argument("-t", "--threshold", type=int, default=10); mt.add_argument("-l", "--limit", type=int, default=20); mt.set_defaults(fn=cmd_match)
    # semanticos (CLIP)
    e = sub.add_parser("embed"); e.add_argument("image"); e.set_defaults(fn=cmd_embed)
    ci = sub.add_parser("cindex"); ci.add_argument("corpus"); ci.add_argument("-o", "--out", default="clip_index"); ci.set_defaults(fn=cmd_cindex)
    cs = sub.add_parser("csearch"); cs.add_argument("query"); cs.add_argument("index")
    cs.add_argument("--text", action="store_true", help="query es texto (texto->imagen)")
    cs.add_argument("-l", "--limit", type=int, default=10)
    cs.add_argument("--min-sim", type=float, default=0.0, help="similitud minima [0-1]")
    cs.set_defaults(fn=cmd_csearch)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
