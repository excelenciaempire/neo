
# Kerberos

## <mark style="color:purple;">Introducción a Kerberos</mark>

Kerberos permite la autenticación mutua entre un usuario y un servicio a través de un intercambio de mensajes cifrados. En Active Directory, Kerberos se utiliza como el protocolo principal de autenticación para la autenticación de usuarios y servicios. Cuando un usuario inicia sesión en un sistema de Windows, su nombre de usuario y contraseña se envían a un controlador de dominio de Active Directory para su verificación. El controlador de dominio utiliza el protocolo Kerberos para autenticar al usuario y proporcionar una clave de sesión para su uso en la comunicación posterior con el sistema de Windows.

Kerberos funciona utilizando una estructura de tres partes: el cliente, el servidor de autenticación (AS) y el servidor de tickets (TGS). Cuando un usuario intenta acceder a un recurso protegido, el cliente solicita un ticket de servicio al servidor de autenticación. El servidor de autenticación verifica la identidad del usuario y proporciona un ticket de sesión para el recurso solicitado. El cliente presenta el ticket de sesión al servidor de tickets, que proporciona una clave de sesión para su uso en la comunicación posterior con el recurso protegido.

<figure><img src="/files/hyEBd73XcNf3QLMxsEFi" alt=""><figcaption><p>Funcionamiento de Kerberos en Active Directory</p></figcaption></figure>

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir credenciales y tickets de servicio de usuarios en una organización, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Ticket Granting Ticket</mark>

El TGT es un ticket de seguridad emitido por el Servicio de Autenticación (AS) de Kerberos después de que un usuario se autentica en un controlador de dominio en Active Directory. El TGT se utiliza para autenticar al usuario en otros servicios de la red que utilizan el protocolo Kerberos. Una vez que el usuario tiene un TGT válido, puede solicitar tickets de servicio para acceder a recursos protegidos en la red.

* Ticket que almacena la contraseña para un servicio
* Tiene un tiempo de vida limitado (Time Stamp)

## <mark style="color:purple;">Ticket Granting Service</mark>

El TGS es un servidor que proporciona tickets de servicio a un usuario después de que se ha autenticado mediante un TGT. El usuario presenta el TGT al TGS y solicita un ticket de servicio para acceder a un recurso protegido en la red. El TGS verifica la autenticidad del usuario y, si es auténtico, proporciona un ticket de servicio que se utiliza para acceder al recurso protegido.

* Ticket que contiene el Ticket Granting Ticket cifrado

## <mark style="color:purple;">Autenticator</mark>

El Authenticator es un componente importante del protocolo Kerberos utilizado en entornos de Active Directory para proporcionar autenticación segura de usuarios y servicios. El Authenticator es un mensaje cifrado que se utiliza para verificar la identidad del usuario o servicio que solicita acceso a un recurso protegido en la red.

* Clave de sesión + TGT

## <mark style="color:purple;">Key Distribution Center (KDC)</mark>

El KDC es un servidor que consta de dos componentes principales: el Servicio de Autenticación (AS) y el Servicio de Concesión de Tickets (TGS). El Servicio de Autenticación es responsable de autenticar a los usuarios y proporcionar un Ticket Granting Ticket (TGT) después de que se haya verificado la autenticidad del usuario. El TGT se utiliza para solicitar tickets de servicio para acceder a recursos protegidos en la red. El Servicio de Concesión de Tickets es responsable de proporcionar tickets de servicio a los usuarios autenticados para acceder a recursos protegidos en la red.

## <mark style="color:purple;">Kerberos en Active Directory</mark>

* Cuenta de Servicio por defecto: KRBTGT
* Se encarga de cifrar las peticiones
* Key Distribution Center

A continuación se muestran las técnicas de hacking más utilizadas para el protocolo Kerberos.
