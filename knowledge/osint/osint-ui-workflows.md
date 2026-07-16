# OSINT Workflows por entidad (destilado de osint-ui)

Checklist OSINT accionable, organizado por **tipo de entidad**, con la herramienta que Neo ya
ejecuta para cada paso. Destilado de la metodología de **osint-ui** (afsh4ck) — que es un SaaS
cerrado; aquí queda solo la **metodología** mapeada a los binarios de `kali-mcp`/`hexstrike`.

> Alcance: OSINT pasivo sobre información pública (excepción permitida por `AUTHORIZATION.md`).
> El Port Scanner y cualquier consulta activa requieren objetivo autorizado.

## 1. Username → perfiles multi-plataforma
- **Neo**: `sherlock <user>` · `maigret <user>` (hexstrike / kali). Enumera cuentas por plataforma.
- Correlaciona: mismo alias en GitHub, Reddit, X, IG, TikTok → pivote a email/nombre real.

## 2. Email → validez, cuentas y reputación
- **Validez / cuentas**: `holehe <email>` (dónde está registrado), `theHarvester` (correos de un dominio).
- **Higiene DNS del dominio**: `dig MX`, registros **SPF/DMARC** (`dig TXT dominio`, `_dmarc.dominio`).
- **Brechas**: Have I Been Pwned (web/API).
- **Enriquecedor de osint-ui**: clasificación/reputación de email vía **API Dymo** (validez, desechable, rol).
- **Dorks**: `"email@dominio"` en Google/Bing.

## 3. Phone → línea, país y mensajería
- **Neo**: `phoneinfoga scan -n <e164>` (tipo de línea, operador, país, formato).
- Enlaces directos WhatsApp/Telegram (`wa.me/<num>`, `t.me/+<num>`) para confirmar existencia.

## 4. Domain → WHOIS, DNS y subdominios
- **Neo**: `whois <dominio>` · `dnsrecon -d <dominio>` · `subfinder -d <dominio>` / `amass enum -passive`.
- Histórico: WHOIS histórico, `crt.sh` (certificados → subdominios), Wayback.

## 5. Puertos / superficie (activo — requiere autorización)
- **Neo**: `nmap -sV --top-ports 1000 <host>` (o `--top-ports 100` rápido) · `masscan` para rangos.
- Correlaciona con **Shodan** (`knowledge/osint/shodan-queries.md`) para la vista pasiva.

## 6. Reputación (IP / dominio)
- **Neo / CTI**: VirusTotal, AbuseIPDB, GreyNoise (web/API). Clasifica malicioso/limpio y categorías.

## 7. Metadatos de imágenes → geolocalización
- **Neo**: `exiftool <img>` → extrae **EXIF/GPS**. Si hay coords: pásalas a Maps.
- Sin GPS: reverse image (Yandex/Google Lens/TinEye) + chronolocation (sombras/hora) + objetos de fondo.

## 8. Hash → identificar y (si autorizado) crackear
- **Identificar**: `hashid <hash>` / `hash-identifier`.
- **Lookup** de hashes ya obtenidos: **CrackStation** (web) — rápido para hashes comunes.
- **Crackear** (sobre material propio/autorizado): `hashcat -m <modo> hash.txt rockyou.txt` / `john`.

---

## Extras de osint-ui a recordar
- **Google Dorks por entidad**: plantillas listas (`site:`, `filetype:`, `intext:"..."`) por dominio/usuario/email.
- **Export a JSON**: guarda cada resultado estructurado para el dossier (lo hace `reporting`).
- **Referencia manual opcional**: la UI vive en `https://osint-ui.com` (SaaS de terceros) — usable a mano
  vía `browser-harness`, nunca como dependencia. Precaución PII / alcance.

Flujo típico del subagente `recon-osint`: parte de un selector → corre 1-4 en paralelo → correlaciona
en un grafo → pasa a `reporting`. Empieza siempre **pasivo**.
