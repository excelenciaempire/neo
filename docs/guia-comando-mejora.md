# Guía: crear el slash command `/mejora` en Neo

Crea un comando `/mejora` **a nivel de proyecto** (vive en `Neo/.claude/commands/`, solo aplica
cuando trabajas en Neo) que **reescribe tu prompt aplicando las técnicas de tu repositorio de
prompting** y luego lo ejecuta con el subagente adecuado de la suite.

---

## 1. Cómo funcionan los slash commands (lo esencial)

- Son archivos **Markdown** en `.claude/commands/`. El **nombre del archivo = el comando**:
  `mejora.md` → `/mejora`.
- **Ámbito**:
  - `Neo/.claude/commands/` → solo dentro de Neo (lo que queremos aquí).
  - `~/.claude/commands/` → en todos tus proyectos.
- **Variables** que puedes usar dentro del archivo:
  - `$ARGUMENTS` → todo lo que escribas tras el comando. `$1`, `$2` → argumentos por posición.
  - `@ruta/archivo` → **inserta el contenido** de ese archivo en el prompt.
  - `` !`comando` `` → **ejecuta bash** y mete su salida (requiere `allowed-tools: Bash(...)`).
- **Frontmatter** opcional: `description`, `argument-hint`, `allowed-tools`, `model`.

---

## 2. Mete las técnicas de tu repo dentro de Neo

El comando necesita leer tus técnicas **offline**. Clónalas como subcarpeta:

```bash
cd c:/Users/river/Desktop/Neo
git clone https://github.com/TU-USUARIO/TU-REPO-PROMPTS.git prompt-techniques
```

- Si **no** quieres versionar esas técnicas en el repo de Neo, añade `prompt-techniques/` a `.gitignore`.
- Alternativa: déjalas fuera y apunta a la ruta absoluta en el comando con `@C:/ruta/...`.

Identifica su **formato** (elige tu caso en el paso 3):
- **🅐 Documentos** `.md` / `.txt` con técnicas → el comando los lee.
- **🅑 Un script / CLI** (`improve.py`, etc.) → el comando lo ejecuta.

---

## 3. Crea el comando `Neo/.claude/commands/mejora.md`

### Caso 🅐 — tus técnicas son documentos (lo más común)

```markdown
---
description: Reescribe mi prompt aplicando las tecnicas de mi repo, y lo ejecuta con Neo
argument-hint: <el prompt / la tarea a mejorar>
allowed-tools: Read, Grep, Glob, Task
---
Eres un ingeniero de prompts experto trabajando dentro de la suite Neo (pentest/OSINT).

## 1. Carga mis tecnicas
Lee mi guia principal de prompting:
@prompt-techniques/README.md

Explora el resto de la carpeta segun el tipo de tarea:
- Usa `Glob` sobre `prompt-techniques/**/*.md` para ver que hay.
- Usa `Grep` para encontrar la tecnica relevante (few-shot, rol, chain-of-thought,
  formato de salida, restricciones, etc.).

## 2. Prompt del usuario
$ARGUMENTS

## 3. Que hacer
1. Detecta la intencion y el dominio del prompt.
2. Reescribelo APLICANDO mis tecnicas (estructura, contexto, rol, restricciones, formato de salida).
3. Muestrame el **prompt mejorado** en un bloque de codigo (antes/despues, breve).
4. Luego **ejecutalo**: delega en el subagente de Neo adecuado
   (pentest-orchestrator / recon-osint / web-exploit / network-ad / reporting),
   respetando siempre la puerta de autorizacion.
```

### Caso 🅑 — tus técnicas son un script / CLI

```markdown
---
description: Mejora mi prompt con mi herramienta y lo ejecuta con Neo
argument-hint: <el prompt a mejorar>
allowed-tools: Bash(python:*), Task
---
Prompt mejorado por mi herramienta de prompting:

!`python prompt-techniques/improve.py "$ARGUMENTS"`

Toma EXACTAMENTE ese prompt mejorado de arriba y ejecutalo con el subagente de Neo
adecuado (pentest-orchestrator / recon-osint / ...), aplicando la puerta de autorizacion.
```

---

## 4. Úsalo

Los comandos de proyecto se **detectan solos** (si ya tenías Claude Code abierto, reinícialo o
escribe `/` para refrescar la lista). Luego:

```
/mejora haz osint de mi-dominio.com y dame la superficie expuesta
```

→ Claude carga tus técnicas, reescribe ese prompt y lo ejecuta con `recon-osint`.

Verifica que aparece: escribe `/` y busca **mejora** en la lista (con tu `description`).

---

## 5. Afinar (opcional)

- **Solo mejorar, sin ejecutar**: quita el punto 4 / la última línea del template → te devuelve
  el prompt y para ahí.
- **Namespacing**: `Neo/.claude/commands/neo/mejora.md` → el comando pasa a ser `/neo:mejora`.
- **Argumentos por posición**: `$1` para el prompt, `$2` para (p. ej.) el subagente objetivo.
- **100% automático (sin escribir `/mejora`)**: eso ya no es un slash command sino un **hook
  `UserPromptSubmit`** en `settings.json` — mismo motor, pero se dispara en **cada** prompt.

---

## 6. Troubleshooting

| Problema | Causa / arreglo |
|---|---|
| El comando no aparece | ¿Está en `Neo/.claude/commands/*.md`? Reinicia Claude Code. |
| `@prompt-techniques/...` no carga | La ruta es relativa a la **raíz del proyecto**; confirma que la carpeta existe ahí. |
| El `` !`...` `` no ejecuta | Falta `allowed-tools: Bash(...)` en el frontmatter, o el binario no está en el PATH. |
| No respeta la ética | El template ya invoca la puerta de autorización; mantén esa línea. |

---

> **Referencia oficial de slash commands:** https://docs.claude.com/en/docs/claude-code/slash-commands
