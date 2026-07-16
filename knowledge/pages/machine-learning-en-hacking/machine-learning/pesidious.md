
# Pesidious

[<mark style="color:purple;">https://github.com/CyberForce/Pesidious</mark>](https://github.com/CyberForce/Pesidious)

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a enviar archivos maliciosos al sistema objetivo haciendo el bypass de los antivirus, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Instalación</mark>

{% hint style="warning" %}
Dado que esta herramienta trabaja con archivos maliciosos, se recomienda encarecidamente utilizar una máquina virtual. Después de la instalación de la herramienta, asegúrese de desconectarse de la red.
{% endhint %}

Los siguientes pasos lo guiarán a través de todas las instalaciones necesarias para configurar el entorno:

1. [Instalar y configurar Python 3.6](https://realpython.com/installing-python/)
2. Clonar el repositorio

   ```
   git clone https://github.com/CyberForce/Pesidious
   ```
3. Moverse dentro del directorio

   ```
   cd Pesidious
   ```
4. [Configurar y activar un entorno virtual con Python 3.6](https://docs.python.org/3/tutorial/venv.html)

   > Se recomienda utilizar un entorno virtual para evitar conflictos entre paquetes utilizados por diferentes aplicaciones
5. Asegúrese de tener pip 8.1.1 instalado y configurado.

   > Esto se debe a que las versiones posteriores de pip no funcionan bien con la biblioteca PyTorch.

   ```
   pip install pip==8.1.1
   ```
6. Instale todas las bibliotecas requeridas instalando el archivo requirements.txt.

   ```
   pip install -r pip_requirements/requirements.txt
   ```

## <mark style="color:purple;">Mutando el malware</mark>

La salida de GAN ya se almacenó como (RL\_Features/adverarial\_imports\_set.pk y RL\_Features/adverarial\_sections\_set.pk), que se usará al agregar importaciones y secciones al malware para la mutación.

1. Puede probar el clasificador de muestra para puntuar archivos de malware.

   ```
   python classifier.py -d /path/to/directory/with/malware/files
   ```
2. Ejecute el script de python mutate.py para mutar sus muestras de malware.

   ```
   python mutate.py -d /path/to/directory/with/malware/files
   ```
3. Los archivos de malware mutados se almacenarán en un directorio llamado Mutated\_malware en el siguiente formato

   ```
   Mutated_malware/mutated_<name-of-the-file>
   ```
4. Una vez que los archivos de malware están mutados, puede ejecutar el clasificador nuevamente para calificar el malware mutado.

   ```
   python classifier.py -d Mutated_malware/
   ```
