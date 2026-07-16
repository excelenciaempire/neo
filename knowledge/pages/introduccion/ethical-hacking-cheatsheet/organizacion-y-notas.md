
# Organización y Notas

## <mark style="color:purple;">Estructura de carpetas</mark>

Ejemplo de estructura de carpetas para una auditoría:

```shell-session
afshack@kali$ tree .
.
└── Penetration-Testing
    │
    ├── Host 1
    │   ├── Reconocimiento
    │   │   └── ...
    │   ├── Vulnerabilidades
    │   │   └── ...
    │   ├── Explotación
    │   │   └── ...
    │   ├── Post-Exploitation
    │   │   └── ...
    │   └── Movimientos-Laterales
    │       └── ...
    ├── Host 2
    │   ├── Reconocimiento
    │   │   └── ...
    │   ├── Vulnerabilidades
    │   │   └── ...
    │   ├── Explotación
    │   │   └── ...
    │   ├── Post-Exploitation
    │   │   └── ...
    │   └── Movimientos-Laterales
    │       └── ...
    ├── Reportes
    │   └── ...
	└── Resultados
	    └── ...
```

Ejemplo de estructura de organización de scripts:

```shell-session
afshack@kali$ tree .
.
└── hack-tools
    |
    ├── AD
    │   ├── script-1
    │   ├── script-2
    │   └── ...
    ├── BOMB
    │   ├── script-1
    │   ├── script-2
    │   └── ...
    ├── CMS
    │   ├── script-1
    │   ├── script-2
    │   └── ...
    ├── EXPLOIT
    │   ├── script-1
    │   ├── script-2
    │   └── ...
    ├── FUZZING
    │   ├── script-1
    │   ├── script-2
    │   └── ...
    ├── MULTI
    │   ├── script-1
    │   ├── script-2
    │   └── ...
    ├── OSINT
    └── ...
```

## <mark style="color:purple;">Organización para auditorías</mark>

```python
afshack@kali$ tree Projects/

Projects/    # ---> Carpeta general
└── Company  # ---> Nombre de la empresa
    ├── EPT  # ---> External Penetration Test
    │   ├── evidence
    │   │   ├── credentials
    │   │   ├── data
    │   │   └── screenshots
    │   ├── logs
    │   ├── scans
    │   ├── scope
    │   └── tools
    └── IPT  # ---> Internal Penetration Test
        ├── evidence
        │   ├── credentials
        │   ├── data
        │   └── screenshots
        ├── logs
        ├── scans
        ├── scope
        └── tools
```

## <mark style="color:purple;">Tomar nota</mark>

***

Tomar notas es otra parte esencial de nuestras pruebas de penetración porque acumulamos mucha información, resultados e ideas diferentes que son difíciles de recordar todos a la vez. Hay cinco tipos principales diferentes de información que es necesario anotar:

1. Información recién descubierta
2. Ideas para pruebas y procesamiento adicionales
3. Resultados del escaneo
4. Inicio sesión
5. Capturas de pantalla

## <mark style="color:purple;">Herramientas</mark>

Hay muchos recursos disponibles para la documentación, aquí dejo alguno de los mejores:

{% embed url="<https://www.notion.so/>" %}
Documentación online estilo Markdown
{% endembed %}

{% embed url="<https://xmind.app/>" %}
Mapas mentales y relación de ideas
{% endembed %}

{% embed url="<https://obsidian.md/>" %}
Documentación online estilo Markdown
{% endembed %}

{% embed url="<https://www.gitbook.com/>" %}
Documentación online estilo Markdown
{% endembed %}

## <mark style="color:purple;">Ejemplo de estructura de reporte</mark>

Un ejemplo de estructura para un reporte profesional podría ser algo así:

`External Penetration Test - <Nombre del cliente>`

* `Scope` (incluidas las direcciones/rangos de IP dentro del alcance, las URL, cualquier host frágil, los plazos de prueba y cualquier limitación u otra información relativa que necesitemos tener a mano)
* `Puntos de contacto del cliente`
* `Credenciales`
* `Discovery / Enumeración`
  * `Escaneos`
  * `Live hosts`
* `Application Discovery`
  * `Escaneos`
  * `Hosts Interesantes / Notables`
* `Explotación`
  * `<Hostname o IP>`
  * `<Hostname o IP>`
* `Post-Exploitation`
  * `<Hostname o IP>`
  * `<<Hostname o IP>`

## <mark style="color:purple;">Capturas de pantalla</mark>

Es fundamental conseguir claridad, y una imagen vale más que mil palabras. Para ello podemos utilizar una herramienta llamada `FlameShot` que nos facilita realizar capturas de pantalla y editarlas directamente.

{% embed url="<https://flameshot.org/>" %}

{% embed url="<https://apps.microsoft.com/detail/9p22whgtqlg5?hl=es-ES&gl=CL>" %}

## <mark style="color:purple;">Diagramas</mark>

En algunos ejercicios de hacking ético, como técnicas de pivoting, tener un diagrama de la red en la que nos estamos moviendo puede resultar de gran ayuda.&#x20;

### Draw\.io

Para esto yo recomiendo la web de `draw.io` donde podemos crear distintos diagramas fácilmente:

{% embed url="<https://app.diagrams.net/>" %}

<figure><img src="/files/zJV6l7LSZ0kHNDq8FcMW" alt=""><figcaption></figcaption></figure>

### FlossFlow

También es muy útil la aplicación de FlossFlow, que nos permite crear diagramas isométricos super visuales directamente desde una interfaz web muy fácil de usar:

{% embed url="<https://github.com/stan-smith/FossFLOW>" %}

<figure><img src="/files/EotixP9IHVMHDV34Gnro" alt=""><figcaption></figcaption></figure>
