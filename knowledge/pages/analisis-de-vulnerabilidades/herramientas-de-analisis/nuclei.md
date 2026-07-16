
# Nuclei

Nuclei es una herramienta de código abierto utilizada para realizar pruebas de seguridad automatizadas en aplicaciones web. La herramienta está escrita en Go y se ejecuta en sistemas operativos Linux, Unix y Windows.

{% embed url="<https://github.com/projectdiscovery/nuclei>" %}

<figure><img src="/files/cquYKIsn5WA2M3FhuZBg" alt=""><figcaption></figcaption></figure>

Nuclei utiliza plantillas (templates) predefinidas para realizar pruebas de seguridad en diferentes aplicaciones y tecnologías web. Estas plantillas se pueden personalizar o crear desde cero para adaptarse a las necesidades específicas de la evaluación de seguridad.

```bash
sudo apt install nuclei
nuclei --update-templates
```

## <mark style="color:purple;">Escaneos con Nuclei</mark>

#### **1. Escaneo básico de un sitio web:**

```bash
nuclei -u http://example.com
```

#### **2. Escaneo usando templates específicas:**

```bash
nuclei -u http://example.com -t cves/
```

#### **3. Escaneo de múltiples URLs desde un archivo:**

```bash
nuclei -l urls.txt
```

**4. Guardar resultados en un archivo:**

```bash
nuclei -u http://example.com -o resultados.txt
```

#### 5. Escaneo completo buscando vulnerabilidades críticas

```bash
nuclei -u http://example.com -severity critical -json -o criticas.json
```

## <mark style="color:purple;">Opciones avanzadas de Nuclei</mark>

<table data-header-hidden><thead><tr><th width="162"></th><th width="275"></th><th></th></tr></thead><tbody><tr><td><strong>Opción</strong></td><td><strong>Descripción</strong></td><td><strong>Ejemplo</strong></td></tr><tr><td><code>-silent</code></td><td>Muestra solo resultados sin mensajes adicionales.</td><td><code>nuclei -u http://example.com -silent</code></td></tr><tr><td><code>-json</code></td><td>Salida en formato JSON.</td><td><code>nuclei -u http://example.com -json</code></td></tr><tr><td><code>-rate-limit</code></td><td>Limita la cantidad de solicitudes por segundo.</td><td><code>nuclei -u http://example.com -rate-limit 50</code></td></tr><tr><td><code>-tags</code></td><td>Escanea usando plantillas etiquetadas.</td><td><code>nuclei -u http://example.com -tags xss</code></td></tr><tr><td><code>-H</code></td><td>Añade cabeceras personalizadas a las solicitudes.</td><td><code>nuclei -u http://example.com -H "Authorization: Bearer TOKEN"</code></td></tr></tbody></table>

## <mark style="color:purple;">Nuclei Templates</mark>

Las siguientes plantillas son las que tenemos disponibles en el momento de la publicación de este post. Recomiendo ver las últimas plantillas disponibles en su repositorio o hacer un `--update-templates` para tener las últimas actualizaciones.

<table><thead><tr><th width="158">Template</th><th width="286">Descripción</th><th>Ejemplo de Uso</th></tr></thead><tbody><tr><td><code>cloud</code></td><td>Plantillas relacionadas con servicios en la nube.</td><td><code>nuclei -u https://example.com -t cloud/</code></td></tr><tr><td><code>code</code></td><td>Plantillas para análisis de código y entornos.</td><td><code>nuclei -u https://example.com -t code/</code></td></tr><tr><td><code>cves</code></td><td>Plantillas para analizar distintos CVEs en el objetivo</td><td><code>clei -u https://example.com -t cves/</code></td></tr><tr><td><code>dast</code></td><td>Plantillas para Dynamic Application Security Testing.</td><td><code>nuclei -u https://example.com -t dast/</code></td></tr><tr><td><code>dns</code></td><td>Plantillas para pruebas relacionadas con DNS.</td><td><code>nuclei -u example.com -t dns/</code></td></tr><tr><td><code>file</code></td><td>Plantillas orientadas a análisis de archivos.</td><td><code>nuclei -u https://example.com -t file/</code></td></tr><tr><td><code>headless</code></td><td>Pruebas que interactúan sin interfaz gráfica.</td><td><code>nuclei -u https://example.com -t headless/</code></td></tr><tr><td><code>helpers</code></td><td>Recursos auxiliares utilizados por otras plantillas.</td><td><code>nuclei -u https://example.com -t helpers/</code></td></tr><tr><td><code>http</code></td><td>Plantillas relacionadas con el protocolo HTTP.</td><td><code>nuclei -u https://example.com -t http/</code></td></tr><tr><td><code>javascript</code></td><td>Templates para análisis de JavaScript.</td><td><code>nuclei -u https://example.com -t javascript/</code></td></tr><tr><td><code>network</code></td><td>Pruebas relacionadas con redes.</td><td><code>nuclei -u example.com -t network/</code></td></tr><tr><td><code>passive</code></td><td>Plantillas para análisis pasivo.</td><td><code>nuclei -u https://example.com -t passive/</code></td></tr><tr><td><code>profiles</code></td><td>Perfiles personalizados para escaneos.</td><td><code>nuclei -u https://example.com -t profiles/</code></td></tr><tr><td><code>ssl</code></td><td>Plantillas para certificados SSL/TLS.</td><td><code>nuclei -u example.com -t ssl/</code></td></tr><tr><td><code>workflows</code></td><td>Flujos de trabajo automatizados.</td><td><code>nuclei -u https://example.com -t workflows/</code></td></tr></tbody></table>
