
# Nmap: Análisis

<figure><img src="/files/abQVqN9v7ULefRF5xoBm" alt=""><figcaption><p>Análisis de vulnerabilidades con Nmap</p></figcaption></figure>

### Detección de vulnerabilidades

```bash
nmap -v --script vuln TARGET
```

### Escaneo completo con detección de vulnerabilidades

```bash
sudo nmap -v -A -sCV -T5 --script=vuln TARGET
```

### Exportar informe de vulnerabilidades

```bash
sudo nmap -v -sS -sC -sV -T5 --script=vuln -oX vulns.xml --webxml TARGET
```

```
firefox vulns.xml
```

<figure><img src="/files/nhHwYWPZLV928lrfWEoG" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Comandos completos de Nmap</mark>

{% content-ref url="/pages/hbs35mOjMMP01gN0RuPl" %}
[Nmap](/ethical-hacking-cheatsheet/recopilacion-de-informacion/recopilacion-de-informacion/recopilacion-activa/nmap.md)
{% endcontent-ref %}
