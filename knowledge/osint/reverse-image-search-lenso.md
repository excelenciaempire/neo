# Image-OSINT: Reverse Image & Face Search (Lenso.ai)

Cubre el hueco de **OSINT por imagen** que Neo no tenía (el resto del stack opera sobre
username/email/dominio; `exiftool` solo lee EXIF). Destilado del repo de ejemplos
**lenso-ai/reverse-image-search-api** — que es un **SaaS de pago** (no hay código self-hostable).

> ⚠️ **Doble uso.** La búsqueda **facial** (localizar a una persona en la web desde una foto)
> es OSINT legítimo (verificación de identidad, catfish/suplantación, fraude, personas
> desaparecidas, periodismo) **pero** permite de-anonimizar y perfilar. Úsala **solo** con
> autorización/consentimiento y dentro del alcance de `AUTHORIZATION.md`. Documenta el objetivo
> de cada búsqueda facial. Nada de perfilado masivo ni no consentido.

## API (requiere token Bearer de pago de Lenso.ai)

| Acción | Método / Endpoint |
|---|---|
| **Face search** (persona por foto) | `POST https://api.eyematch.ai/search` |
| **Category search** | `POST https://api.lenso.ai/search` con `category` ∈ `{duplicates, landmarks, similar, related}` |
| **Consumo / cuota** | `GET https://api.lenso.ai/usage` |

**Auth**: header `Authorization: Bearer <token>`.
**Body** (JSON): `image` (imagen en **base64**), `sortType` (p. ej. `QUALITY_DESCENDING`),
`page`/`multiPage`, `domainsToInclude` / `domainsToExclude`, `fromDate` / `toDate`.
**Respuesta**: `urlList` (URLs de imagen/fuente), `confidenceScore` (0-100), `availablePages`, fecha de indexado.

Ejemplo (Python, del repo):
```python
import base64, requests
img = base64.b64encode(open("cara.jpg","rb").read()).decode()
r = requests.post("https://api.eyematch.ai/search",
    json={"image": img, "sortType": "QUALITY_DESCENDING", "page": 1},
    headers={"Authorization": "Bearer <TOKEN>"})
print(r.json())   # urlList + confidenceScore
```

## Metodología (cuándo usarla)
- **Verificar un perfil**: ¿la foto de perfil aparece en otros sitios/otra identidad? → catfish/suplantación.
- **Correlacionar imágenes**: misma foto reutilizada en varias cuentas → vincula identidades.
- **Contexto de una imagen**: landmarks (dónde), duplicados, similares.

## Alternativas pasivas/gratuitas (no depender de una sola API de pago)
- **Google Lens**, **Yandex Images** (muy fuerte en caras), **TinEye** (reutilización/primera aparición),
  **PimEyes** (facial). Ejecutables a mano vía `browser-harness`.

> Uso desde `recon-osint`: paso **opcional** de image-OSINT. Requiere clave Lenso.ai (o usar las
> alternativas por navegador) y **consentimiento/autorización explícita** para búsqueda facial de personas.
