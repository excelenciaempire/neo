
# Batea

{% embed url="<https://github.com/delvelabs/batea>" %}

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a hacer muchas peticiones al servidor del objetivo, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## Instalación

```bash
git clone git@github.com:delvelabs/batea.git
cd batea
python3 setup.py sdist
pip3 install -r requirements.txt
pip3 install -e .
```

## Uso

Necesitamos un informe de nmap en formato xml para pasárselo a Batea:

```bash
# Información completa
sudo nmap -v -A 192.168.0.0/16 -oX output.xml

# Información parcial
sudo nmap -v -O -sV 192.168.0.0/16 -oX output.xml

batea -v output.xml
```

## Ejemplos de uso

```bash
# uso simple (muestra los 5 principales hallazgos con el formato por defecto)
batea nmap_report.xml

# mostrar los top 3
batea -n 3 nmap_report.xml

# mostrar todos los activos
batea -A nmap_report.xml

# usando varios archivos de hosts
batea -A nmap_report1.xml nmap_report2.xml

# usando comodines (XSL por defecto)
batea ./nmap*.xml
batea -f csv ./assets*.csv

# Puedes usar batea con modelos preentrenados y exportar modelos entrenados.

# Entrenamiento, salida y volcado del modelo para persistencia
batea -D mymodel.batea nmap_report.xml

# usando modelo preentrenado
batea -L mymodel.batea nmap_report.xml

# usando CSV preformateado junto con archivos XML
batea -x nmap_report.xml -c portscan_data.csv

# ajustar verbosidad
batea -vv nmap_report.xml
```
