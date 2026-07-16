
# Host Discovery & Port Scanning

## <mark style="color:purple;">Metodología</mark>

<figure><img src="/files/J5JPaQNQ9DWbUTFYoQjl" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Networking</mark>

### Fundamentals

#### **Protocolos de Red**

* En las redes informáticas, los hosts se comunican entre sí mediante el uso de protocolos de red.
* Los protocolos de red garantizan que diferentes sistemas informáticos, que utilizan distinto hardware y software, puedan comunicarse entre sí.
* Existe una gran cantidad de protocolos de red utilizados por diferentes servicios para distintos objetivos o funcionalidades.
* La comunicación entre diferentes hosts a través de protocolos se transfiere o facilita mediante el uso de paquetes.

#### **Paquetes**

* El objetivo principal de las redes es el intercambio de información entre computadoras conectadas en una red; esta información se transfiere mediante paquetes.
* Los paquetes no son más que flujos de bits que viajan como señales eléctricas a través de medios físicos utilizados para la transmisión de datos (Ethernet, Wi-Fi, etc.).
* Estas señales eléctricas luego se interpretan como bits (ceros y unos) que conforman la información.

#### **El Modelo OSI**

* El modelo OSI (Interconexión de Sistemas Abiertos) es un marco conceptual que estandariza las funciones de un sistema de telecomunicaciones o informático en siete capas de abstracción.
* Fue desarrollado por la Organización Internacional de Normalización (ISO) para facilitar la comunicación entre diferentes sistemas y dispositivos, garantizando la interoperabilidad y el entendimiento a través de una amplia variedad de tecnologías de red.
* El modelo OSI se divide en siete capas, cada una representando una funcionalidad específica dentro del proceso de comunicación en red.

<table><thead><tr><th width="55.66668701171875">#</th><th width="128.66668701171875">CAPA OSI</th><th width="420.6666259765625">FUNCIÓN</th><th>EJEMPLOS</th></tr></thead><tbody><tr><td>7</td><td>Capa de Aplicación</td><td>Proporciona servicios de red directamente a los usuarios finales o aplicaciones.</td><td>HTTP, FTP, IRC, SSH, DNS</td></tr><tr><td>6</td><td>Capa de Presentación</td><td>Traduce los datos entre la capa de aplicación y las capas inferiores. Responsable de la traducción de formatos, cifrado y compresión para garantizar que los datos se presenten en un formato legible.</td><td>SSL/TLS, JPEG, GIF, SSH, IMAP</td></tr><tr><td>5</td><td>Capa de Sesión</td><td>Gestiona sesiones o conexiones entre aplicaciones. Maneja la sincronización, control de diálogo y gestión de tokens (comunicación entre hosts).</td><td>APIs, NetBIOS, RPC</td></tr><tr><td>4</td><td>Capa de Transporte</td><td>Garantiza la comunicación extremo a extremo y proporciona control de flujo.</td><td>TCP, UDP</td></tr><tr><td>3</td><td>Capa de Red</td><td>Responsable del direccionamiento lógico y el enrutamiento (direccionamiento lógico).</td><td>IP, ICMP, IPsec</td></tr><tr><td>2</td><td>Capa de Enlace de Datos</td><td>Gestiona el acceso al medio físico y proporciona detección de errores. Responsable del encapsulamiento (framing), direccionamiento y verificación de errores de las tramas (direccionamiento físico).</td><td>Ethernet, PPP, Switches</td></tr><tr><td>1</td><td>Capa Física</td><td>Se encarga de la conexión física entre dispositivos.</td><td>USB, Cables Ethernet, Coaxial, Fibra, Hubs</td></tr></tbody></table>
