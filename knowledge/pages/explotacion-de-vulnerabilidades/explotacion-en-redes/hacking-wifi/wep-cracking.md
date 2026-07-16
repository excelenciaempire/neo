
# WEP Cracking

{% hint style="danger" %}
**Disclaimer:** Vamos a realizar ataques a redes WiFi, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Tipos de ataques</mark>&#x20;

* Ataques de pre-conexión
* Obtención de accesos
* Ataques de post-conexión

## <mark style="color:purple;">Redes WEP</mark>

WEP (Wired Equivalent Privacy) fue el primer estándar de seguridad diseñado para proteger las redes inalámbricas, específicamente las redes Wi-Fi. Sin embargo, ha quedado obsoleto y se considera inseguro debido a varias vulnerabilidades significativas. Algunos puntos clave sobre WEP incluyen:

1. **Encriptación débil:** WEP utiliza un algoritmo de cifrado RC4 para proteger la comunicación inalámbrica. Sin embargo, la longitud de la clave predeterminada es corta (generalmente 64 bits o 128 bits), lo que hace que sea vulnerable a ataques de fuerza bruta.
2. **Claves estáticas:** En muchas implementaciones de WEP, las claves de cifrado son estáticas y no cambian con frecuencia. Esto facilita que un atacante capture suficiente tráfico cifrado para luego descifrarlo offline.
3. **Vectores de inicialización débiles:** WEP utiliza vectores de inicialización (IV) para introducir variabilidad en el proceso de cifrado. Sin embargo, la forma en que se gestionan los IV en WEP conduce a la repetición y reutilización, lo que debilita aún más la seguridad.
4. **Vulnerabilidades conocidas:** A lo largo de los años, se han descubierto varias vulnerabilidades críticas en WEP, lo que lo hace altamente susceptible a ataques, como el ataque Fluhrer-Mantin-Shamir (FMS) y el ataque KoreK.

Debido a estas debilidades, WEP ha sido ampliamente abandonado en favor de protocolos de seguridad más robustos, como WPA (Wi-Fi Protected Access) y WPA2. Se recomienda encarecidamente no utilizar WEP en entornos de red, ya que no proporciona una protección adecuada contra las amenazas actuales.

## <mark style="color:purple;">Teoría del WEP Craking</mark>

* El cliente encripta el mensaje con una llave
* El archivo encriptado es enviado por el aire, sie el atacante toma el paquete no puede ver su interior
* Cada paquete es encriptado con una llave única
* Para esto se genera un vector random de 24 bits
* El vector de inicialización más la contraseña generan la llave que encripta el paquete

### Problemas de WEP

* El IV (vector de inicialización) es solo de 24 bits
* El IV envía los mensajes en texto plano
* Las IV´s se repiten en redes congestionadas
* Vulnerable a ataques estáticos
* Se puede determinar fácilmente la llave de transmisión (Key Stream)

## <mark style="color:purple;">Ataques</mark>

{% content-ref url="/pages/hrnoLjVL8oErAFh1kL8j" %}
[Ataque a WEP](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/wep-cracking/ataque-a-wep.md)
{% endcontent-ref %}

{% content-ref url="/pages/hoxQMW9xIUWd61KaAfVg" %}
[Fake Autentication](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/wep-cracking/fake-autentication.md)
{% endcontent-ref %}

{% content-ref url="/pages/cZ705NbTXGG6lXGOibYa" %}
[Packet Injection](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/wep-cracking/packet-injection.md)
{% endcontent-ref %}

{% content-ref url="/pages/RsFnwDGaPJABzDggoUmu" %}
[Redes SKA](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-redes/hacking-wifi/wep-cracking/redes-ska.md)
{% endcontent-ref %}
