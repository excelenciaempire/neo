
# Instalar qFlipper en Kali Linux

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-mU-xci-ZON3mhTIBwe9Ta-20241025-132049.png?format=webp" alt=""><figcaption></figcaption></figure>

## <mark style="color:orange;">Instalación de qFlipper</mark> <a href="#xf0g4" id="xf0g4"></a>

Para instalar **qFlipper** en **Kali Linux** y poder ejecutarlo globalmente desde cualquier terminal, sigue estos pasos:

***

### **1. Descargar qFlipper**

Vamos a descargar qFlipper desde su web oficial:

{% embed url="<https://flipperzero.one/downloads>" %}

Seleccionamos Download for Linux:

<figure><img src="/files/Nu4ThGr6DH36OHmpy1wl" alt=""><figcaption></figcaption></figure>

En la carpeta de Descargas tendremos el ejecutable:

```
qFlipper-x86_64-1.3.3.AppImage
```

Instalar dependencias necesarias para ejecutar archivos `.AppImage`:

```bash
sudo apt install libfuse2 -y
```

***

### **2. Dar permisos de ejecución**

Una vez descargado, otorga permisos de ejecución al archivo:

```bash
chmod +x *.AppImage
```

***

### **3. Moverlo a `/usr/local/bin/` para usarlo globalmente**

Para poder ejecutar **qFlipper** desde cualquier terminal sin necesidad de moverte a su directorio, muévelo a **`/usr/local/bin/`**:

```bash
sudo mv qFlipper-x86_64-1.3.3.AppImage /usr/local/bin/qflipper
```

Ahora puedes abrirlo con el siguiente comando desde cualquier terminal:

```bash
sudo qflipper
```

***

### **4. Crear un acceso directo en el menú de aplicaciones (Opcional)**

Si quieres agregar **qFlipper** al menú de aplicaciones en Kali Linux, crea un archivo `.desktop`:

```bash
sudo nano /usr/share/applications/qflipper.desktop
```

Añade lo siguiente:

```ini
[Desktop Entry]
Name=qFlipper
Exec=/usr/local/bin/qflipper
Icon=qflipper
Type=Application
Categories=Utility;
Terminal=false
```

Guarda el archivo con `CTRL + X`, luego `Y` y `ENTER`.

Para actualizar el menú:

```bash
update-desktop-database ~/.local/share/applications
```
