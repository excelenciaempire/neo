
# Ingeniería Social

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a realizar ataques de phishing para conseguir datos sensibles como usuarios y contraseñas, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Social Engineering Toolkit</mark>

<figure><img src="/files/DPgeTr8cvu4erb6Nj4Ok" alt=""><figcaption><p>Social Engineering Toolkit Interface</p></figcaption></figure>

SET automatiza los ataques de ingeniería social, lo que permite a los usuarios realizar pruebas de seguridad en sistemas y redes utilizando técnicas de ingeniería social. Viene instalado por defecto en Kali Linux

Para utilizar SET en Kali Linux, se deben seguir los siguientes pasos:

1. Abrir una terminal en Kali Linux.
2. Descargar e instalar SET mediante el siguiente comando: `sudo apt-get install set`.
3. Iniciar SET con el siguiente comando: `sudo setoolkit`.
4. Seleccionar la opción de ataque deseada del menú principal de SET.
5. Seguir las instrucciones proporcionadas por SET para configurar y lanzar el ataque.

Vemos esta herramienta en detalle en la sección:

{% content-ref url="/pages/echTeeBwDFlyDcrbvQ5L" %}
[Social Engineering Toolkit](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/phising/social-engineering-toolkit.md)
{% endcontent-ref %}

### Clonar web para conseguir datos de usuario

{% hint style="info" %}
Para que funcione la técnica que veremos a continuación es necesario haber realizado previamente un ARP Spoofing. Ver sección [Man in the Middle](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/man-in-the-middle.md)
{% endhint %}

{% code title="En Kali Linux" %}

```bash
sudo setoolkit
```

{% endcode %}

```bash
Social Engineering attacks 
Website attack vectors 
Web jacking attack
Custom import

1. En el navegador buscar la página a suplantar y darle a “save page as” y abajo elegir HTML only
2. Elegir el nombre index.html 
3. Establecer la ruta a la pagina de destino: /home/kali/Escritorio/index.html/
4. Introducir la URL del sitio clonado: facebook.es
5. Quieres desactivar apache? -> Y
6. Elegir la ip de atacante (dejar por defecto)
```

Esto nos suplanta nuestra página de localhost en nuestra máquina de atacante, y cuando la víctima vaya a facebook.es y meta sus credenciales las capturaremos en tiempo real.

## <mark style="color:purple;">Deep Fake</mark>

Consiste en cambiar nuestra cara en una videollamada en directo por ejemplo por la de un alto cargo directivo de una organización.

<figure><img src="/files/lozadfBPDjdoRa3xhe41" alt=""><figcaption><p>Deep Fake con face-2-face</p></figcaption></figure>

{% embed url="<https://github.com/datitran/face2face-demo>" %}

### **1. Preparar el entorno**

```bash
# Clonar repositorio
git clone git@github.com:datitran/face2face-demo.git

# Crear entorno conda a partir de archivo
conda env create -f environment.yml
```

### **2. Generar Train Data**

Para entrenar al modelo necesitamos un vídeo de la persona a suplantar

```bash
python generate_train_data.py --file angela_merkel_speech.mp4 --num 400 --landmark-model shape_predictor_68_face_landmarks.dat
```

Input:

* `file` es el nombre del archivo de vídeo a partir del cual desea crear el conjunto de datos.
* `num` es el número de datos de tren que se van a crear.
* `landmark-model` es el modelo de referencia facial que se utiliza para detectar las referencias. Se proporciona un modelo de referencia facial preentrenado.

### **3. Correr la demo**

```bash
python run_webcam.py --source 0 --show 0 --landmark-model shape_predictor_68_face_landmarks.dat --tf-model face2face-reduced-model/frozen_model.pb
```

Input:

* `source` es el índice de dispositivo de la cámara (predeterminado=0).
* `show` es una opción para mostrar la entrada normal (0) o el punto de referencia facial (1) junto con la imagen generada (predeterminado = 0).
* `landmark-model` es el modelo de referencia facial que se utiliza para detectar las referencias.
* `tf-model` es el archivo del modelo congelado.
