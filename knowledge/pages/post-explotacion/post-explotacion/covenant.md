
# Covenant

<figure><img src="/files/g45bbJkYD1IaqxyEy68y" alt=""><figcaption></figcaption></figure>

Covenant está diseñado para ser utilizado después de que un atacante ha obtenido acceso inicial a un sistema Windows y ha logrado escalar los privilegios necesarios para instalar Covenant en el sistema comprometido. Una vez instalado, Covenant <mark style="color:purple;">crea un servidor web seguro</mark> que permite al atacante interactuar con el sistema comprometido y ejecutar comandos y herramientas a través de una interfaz gráfica de usuario (GUI) o una línea de comandos.

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir acceso a un sistema con un ejecutable, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

{% hint style="warning" %}
Covenant es una herramienta conocida, por lo que puede ser detectada por los antivirus.
{% endhint %}

## <mark style="color:purple;">Empleo</mark>

{% embed url="<https://github.com/cobbr/Covenant>" %}

Para utilizar Covenant en Kali Linux para postexplotación, sigue estos pasos:

1. Descarga e instala Covenant en el sistema comprometido. Puedes encontrar más información sobre cómo instalar Covenant en la [documentación oficial](https://github.com/cobbr/Covenant/wiki).
2. Inicia el servidor web de Covenant en el sistema comprometido. Puedes hacerlo desde la línea de comandos o la interfaz gráfica de usuario de Covenant.
3. Abre un navegador web en Kali Linux y navega hasta la dirección URL del servidor web de Covenant en el sistema comprometido.
4. Inicia sesión en Covenant utilizando las credenciales de inicio de sesión que creaste durante la instalación.
5. Utiliza la interfaz gráfica o la línea de comandos de Covenant para ejecutar comandos y herramientas en el sistema comprometido de forma remota.
