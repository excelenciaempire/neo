
# Administradores de Contraseñas

Parece que hoy en día todo requiere una contraseña. Usamos contraseñas para el Wi-Fi de nuestro hogar, redes sociales, cuentas bancarias, correos electrónicos comerciales e incluso nuestras aplicaciones y sitios web favoritos. Según este [estudio de NordPass](https://www.techradar.com/news/most-people-have-25-more-passwords-than-at-the-start-of-the-pandemic) , la persona promedio tiene 100 contraseñas, que es una de las razones por las que la mayoría de la gente reutiliza contraseñas o crea contraseñas simples.

Teniendo todo esto en cuenta, necesitamos contraseñas diferentes y seguras, pero no todo el mundo puede memorizar cientos de contraseñas que cumplan con la complejidad necesaria para que una contraseña sea segura. Necesitamos algo que pueda ayudarnos a organizar nuestras contraseñas de forma segura. Un [administrador de contraseñas](https://en.wikipedia.org/wiki/Password_manager) es una aplicación que permite a los usuarios almacenar sus contraseñas y secretos en una base de datos cifrada. Además de mantener seguras nuestras contraseñas y datos sensibles, también cuentan con funciones para generar y administrar contraseñas robustas y únicas, 2FA, completar formularios web, integración del navegador, sincronización entre múltiples dispositivos, alertas de seguridad, entre otras características.

***

## <mark style="color:purple;">¿Cómo funciona un administrador de contraseñas?</mark>

La implementación de los administradores de contraseñas varía según el fabricante, pero la mayoría funciona con una contraseña maestra para cifrar la base de datos.

El cifrado y la autenticación funcionan utilizando diferentes [funciones hash criptográficas](https://en.wikipedia.org/wiki/Cryptographic_hash_function) y [funciones de derivación de claves](https://en.wikipedia.org/wiki/Key_derivation_function) , para evitar el acceso no autorizado a nuestra base de datos de contraseñas cifradas y su contenido. La forma en que funciona depende del fabricante y de si el administrador de contraseñas está en línea o sin conexión.

Analicemos los administradores de contraseñas comunes y cómo funcionan.

***

## <mark style="color:purple;">Administradores de contraseñas Online</mark>

Uno de los elementos clave a la hora de decidirse por un administrador de contraseñas es la comodidad. Una persona típica tiene 3 o 4 dispositivos y los usa para iniciar sesión en diferentes sitios web, aplicaciones, etc. Un administrador de contraseñas en línea permite al usuario sincronizar su base de datos de contraseñas cifradas entre múltiples dispositivos, la mayoría de ellos proporcionan:

* Una aplicación móvil.
* Un complemento del navegador.
* Algunas otras características que discutiremos más adelante en esta sección.

Todos los proveedores de administradores de contraseñas tienen su propia forma de gestionar su implementación de seguridad y, por lo general, proporcionan un documento técnico que describe cómo funciona. Puedes consultar la documentación [de Bitwarden](https://bitwarden.com/images/resources/security-white-paper-download.pdf) , [1Password](https://1passwordstatic.com/files/security/1password-white-paper.pdf) y [LastPass](https://assets.cdngetgo.com/da/ce/d211c1074dea84e06cad6f2c8b8e/lastpass-technical-whitepaper.pdf) como referencia, pero hay muchas otras. Hablemos de cómo funciona esto en general.

Una implementación común para los administradores de contraseñas en línea es derivar claves basadas en la contraseña maestra. Su propósito es proporcionar un [cifrado de conocimiento cero](https://blog.cubbit.io/blog-posts/what-is-zero-knowledge-encryption) , lo que significa que nadie, excepto usted (ni siquiera el proveedor de servicios), puede acceder a sus datos protegidos. Para lograr esto, comúnmente derivan la contraseña maestra. Usemos la implementación técnica de Bitwarden para derivar contraseñas para explicar cómo funciona:

1. Clave maestra: creada por alguna función para convertir la contraseña maestra en un hash.
2. Hash de contraseña maestra: creado mediante alguna función para convertir la contraseña maestra con una combinación de la clave maestra en un hash para autenticarse en la nube.
3. Clave de descifrado: creada mediante alguna función que utiliza la clave maestra para formar una clave simétrica para descifrar elementos de la bóveda.

![Diagrama de Bitwarden](https://academy.hackthebox.com/storage/modules/147/bitwarden_diagram.png)

Esta es una forma sencilla de ilustrar cómo funcionan los administradores de contraseñas, pero la implementación común es más compleja. Puede consultar los documentos técnicos anteriores o ver el vídeo [Cómo funcionan los administradores de contraseñas: Computerphile .](https://www.youtube.com/watch?v=w68BBPDAWr8)

Los administradores de contraseñas en línea más populares son:

1. [1Password](https://1password.com/)
2. [Bitwarden](https://bitwarden.com/)
3. [Dashlane](https://www.dashlane.com/)
4. [Keeper](https://www.keepersecurity.com/)
5. [Lastpass](https://www.lastpass.com/)
6. [NordPass](https://nordpass.com/)
7. [RoboForm](https://www.roboform.com/)

***

## <mark style="color:purple;">Administradores de contraseñas locales</mark>

Algunas empresas y particulares prefieren gestionar su seguridad por diferentes motivos y no depender de servicios proporcionados por terceros. Los administradores de contraseñas locales ofrecen esta opción al almacenar la base de datos localmente y responsabilizar al usuario de proteger su contenido y la ubicación donde se almacena.

Los administradores de contraseñas locales cifran el archivo de la base de datos utilizando una clave maestra. La clave maestra puede constar de uno o varios componentes: una contraseña maestra, un archivo de clave, un nombre de usuario, contraseña, etc. Por lo general, todas las partes de la clave maestra son necesarias para acceder a la base de datos.

El cifrado de los administradores de contraseñas locales es similar a las implementaciones en la nube. La diferencia más notable es la transmisión de datos y la autenticación. Para cifrar la base de datos, los administradores de contraseñas locales se centran en proteger la base de datos local utilizando diferentes funciones hash criptográficas (según el fabricante). También utilizan la función de derivación de claves (salt aleatorio) para evitar el cálculo previo de claves y obstaculizar los ataques de diccionario y adivinanzas. Algunos ofrecen protección de la memoria y protección del registrador de pulsaciones mediante un escritorio seguro, similar al Control de cuentas de usuario (UAC) de Windows.

Los administradores de contraseñas locales más populares son:

1. [KeePass](https://keepass.info/)
2. [KWalletManager](https://apps.kde.org/kwalletmanager5/)
3. [Pleasant Password Server](https://pleasantpasswords.com/)
4. [Password Safe](https://pwsafe.org/)

### Características

Imaginemos que usamos Linux, Android y Chrome OS. Accedemos a todas nuestras aplicaciones y sitios web desde cualquier dispositivo. Queremos sincronizar todas las contraseñas y notas seguras en todos los dispositivos. Necesitamos protección adicional con 2FA y nuestro presupuesto es de 1 USD mensual. Esa información puede ayudarnos a identificar el administrador de contraseñas correcto para nosotros.

Al decidirnos por un administrador de contraseñas local o en la nube, debemos comprender sus características. [Wikipedia](https://en.wikipedia.org/wiki/List_of_password_managers) tiene una lista de administradores de contraseñas (en línea y locales), así como algunas de sus características. Aquí hay una lista de las funciones más comunes para los administradores de contraseñas:

1. [Soporte 2FA](https://authy.com/what-is-2fa/) .
2. Multiplataforma (Android, iOS, Windows, Linux, Mac, etc.).
3. Extensión del navegador.
4. Iniciar sesión Autocompletar.
5. Capacidades de importación y exportación.
6. Generación de contraseña.

***

## <mark style="color:purple;">Alternativas</mark>

Las contraseñas son la forma más común de autenticación, pero no la única. Como aprendemos de este módulo, hay múltiples formas de comprometer una contraseña, descifrarla, adivinarla, navegar por el hombro, etc., pero ¿qué pasa si no necesitamos una contraseña para iniciar sesión? ¿Es posible tal cosa?

De forma predeterminada, la mayoría de los sistemas operativos y aplicaciones no admiten ninguna alternativa a una contraseña. Aún así, los administradores pueden utilizar aplicaciones o proveedores de identidad de terceros para configurar o mejorar la protección de identidad en sus organizaciones. Algunas de las formas más comunes de proteger identidades más allá de las contraseñas son:

1. [Autenticación multifactor](https://en.wikipedia.org/wiki/Multi-factor_authentication) .
2. [Estándar de autenticación abierto FIDO2](https://fidoalliance.org/fido2/) , que permite a los usuarios aprovechar dispositivos comunes como [Yubikey](https://www.yubico.com/) para autenticarse fácilmente. Para obtener una lista de dispositivos más amplia, puede consultar [Proveedores de claves de seguridad de Microsoft FIDO2](https://docs.microsoft.com/en-us/azure/active-directory/authentication/concept-authentication-passwordless#fido2-security-key-providers) .
3. [Contraseña de un solo uso (OTP)](https://en.wikipedia.org/wiki/One-time_password) .
4. [Contraseña de un solo uso basada en tiempo (TOTP)](https://en.wikipedia.org/wiki/Time-based_one-time_password) .
5. [Restricción de propiedad intelectual](https://news.gandi.net/en/2019/05/using-ip-restriction-to-help-secure-your-account/) .
6. Cumplimiento del dispositivo. Ejemplos: [Endpoint Manager](https://www.petervanderwoude.nl/post/tag/device-compliance/) o [Workspace ONE](https://www.loginconsultants.com/enabling-the-device-compliance-with-workspace-one-uem-authentication-policy-in-workspace-one-access)

***

## <mark style="color:purple;">Passwordless</mark>

Varias empresas como [Microsoft](https://www.microsoft.com/en-us) , [Auth0](https://auth0.com/) , [Okta](https://www.okta.com/) , [Ping Identity](https://www.pingidentity.com/en.html) , etc., están intentando promover la estrategia [Passwordless](https://en.wikipedia.org/wiki/Passwordless_authentication), para eliminar la contraseña como forma de autenticación.

[La autenticación sin contraseña](https://www.pingidentity.com/en/resources/blog/posts/2021/what-does-passwordless-really-mean.html) se logra cuando se utiliza un factor de autenticación distinto de una contraseña. Una contraseña es un factor de conocimiento, lo que significa que es algo que el usuario sabe. El problema de depender únicamente de un factor de conocimiento es que es vulnerable al robo, el intercambio, el uso repetido, el mal uso y otros riesgos. La autenticación sin contraseña significa, en última instancia, no más contraseñas. En cambio, se basa en un factor de posesión, algo que tiene un usuario, o un factor inherente, que es un usuario, para verificar la identidad del usuario con mayor seguridad.

A medida que evolucionan nuevas tecnologías y estándares, debemos investigar y comprender los detalles de su implementación para comprender si esas alternativas brindarán o no la seguridad que necesitamos para el proceso de autenticación. Puede leer más sobre la autenticación sin contraseña y las estrategias de diferentes proveedores:

1. [Microsoft Passwordless](https://www.microsoft.com/en-us/security/business/identity-access-management/passwordless-authentication)
2. [Auth0 Passwordless](https://auth0.com/passwordless)
3. [Okta Passwordless](https://www.okta.com/passwordless-authentication/)
4. [PingIdentity](https://www.pingidentity.com/en/resources/blog/posts/2021/what-does-passwordless-really-mean.html)

Existen muchas opciones a la hora de proteger contraseñas. Elegir el adecuado dependerá de los requisitos del individuo o de la empresa. Es común que las personas y las empresas utilicen diferentes métodos de protección con contraseña para diversos fines.
