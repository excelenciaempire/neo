
# Políticas de Contraseñas

Ahora que hemos analizado numerosas formas de capturar credenciales y contraseñas, cubramos algunas de las mejores prácticas relacionadas con contraseñas y protección de identidad. Los límites de velocidad y las leyes de tránsito existen para que conduzcamos con seguridad. Sin ellos, conducir sería un caos. Lo mismo ocurre cuando una empresa no cuenta con políticas adecuadas; todos podrían hacer lo que quisieran sin consecuencias. Es por eso que los proveedores y administradores de servicios utilizan diferentes políticas y aplican métodos para hacerlas cumplir para una mayor seguridad.

Conozcamos a Mark, un nuevo empleado de Inlanefreight Corp. Mark no trabaja en TI y no es consciente del riesgo de una contraseña débil. Necesita establecer su contraseña para su correo electrónico comercial. Él elige la contraseña `password123`. Sin embargo, recibe un error que dice que la contraseña no cumple con la política de contraseñas de la empresa y un mensaje que le informa el requisito mínimo para que la contraseña sea más segura.

En este ejemplo, tenemos dos piezas esenciales: una definición de la política de contraseñas y su aplicación. La definición es una directriz y la aplicación es la tecnología utilizada para que los usuarios cumplan con la política. Ambos aspectos de la implementación de la política de contraseñas son esenciales. Durante esta lección, exploraremos ambos y comprenderemos cómo podemos crear una política de contraseñas eficaz y su implementación.

***

## <mark style="color:purple;">Política de contraseñas</mark>

Una [política de contraseñas](https://en.wikipedia.org/wiki/Password_policy) es un conjunto de reglas diseñadas para mejorar la seguridad informática al alentar a los usuarios a emplear contraseñas seguras y utilizarlas adecuadamente según la definición de la empresa. El alcance de una política de contraseñas no se limita a los requisitos mínimos de la contraseña, sino a todo el ciclo de vida de una contraseña (como manipulación, almacenamiento y transmisión).

***

## <mark style="color:purple;">Estándares de política de contraseñas</mark>

Debido al cumplimiento y las mejores prácticas, muchas empresas utilizan [estándares de seguridad de TI](https://en.wikipedia.org/wiki/IT_security_standards) . Si bien cumplir con un estándar no significa que estemos 100% seguros, es una práctica común dentro de la industria que define una línea base de controles de seguridad para las organizaciones. Esa no debería ser la única forma de medir la eficacia de los controles de seguridad organizacionales.

Algunos estándares de seguridad incluyen una sección para políticas de contraseñas o pautas de contraseñas. Aquí hay una lista de los más comunes:

1. [NIST SP800-63B](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63b.pdf)
2. [Guía de política de contraseñas de CIS](https://www.cisecurity.org/insights/white-papers/cis-password-policy-guide)
3. [PCI DSS](https://www.pcisecuritystandards.org/document_library?category=pcidss\&document=pci_dss)

Podemos utilizar esos estándares para comprender diferentes perspectivas de las políticas de contraseñas. Después de eso, podemos usar esta información para crear nuestra política de contraseñas. Tomemos un caso de uso en el que diferentes estándares utilizan un enfoque diferente: `Expiración de contraseñas`.

Puede que `Cambie su contraseña periódicamente (por ejemplo, 90 días) para estar más seguro` sea una frase que hayamos escuchado varias veces, pero lo cierto es que no todas las empresas están utilizando esta política. Algunas empresas sólo exigen a sus usuarios que cambien sus contraseñas cuando hay evidencia de compromiso. Si nos fijamos en algunos de los estándares anteriores, algunos exigen que los usuarios cambien la contraseña periódicamente y otros no. Deberíamos detenernos a pensar, desafiar los estándares y definir qué es lo mejor para nuestras necesidades.

***

## <mark style="color:purple;">Recomendaciones de políticas de contraseñas</mark>

Creemos una política de contraseñas de muestra para ilustrar algunas cosas importantes a tener en cuenta al crear una política de contraseñas. Nuestra política de contraseñas de muestra indica que todas las contraseñas deben tener:

* Mínimo de 8 caracteres.
* Incluye letras mayúsculas y minúsculas.
* Incluye al menos un número.
* Incluya al menos un carácter especial.
* No debería ser el nombre de usuario.
* Debe cambiarse cada 60 días.

Nuestro nuevo empleado, Mark, que recibió un error al crear el correo electrónico con la contraseña `password123`, ahora elige la siguiente contraseña `Inlanefreight01!` y registra exitosamente su cuenta. Aunque esta contraseña cumple con las políticas de la empresa, no es segura ni fácil de adivinar porque utiliza el nombre de la empresa como parte de la contraseña. En la sección "[Mutaciones de contraseñas](/ethical-hacking-cheatsheet/explotacion-de-vulnerabilidades/explotacion-en-hosts/password-attacks/password-mutations.md)" aprendimos que esta es una práctica común de los empleados y los atacantes son conscientes de ello.

Una vez que esta contraseña llega al tiempo de vencimiento, Mark puede cambiar de 01 a 02 y su contraseña cumple con la política de contraseñas de la empresa, pero la contraseña es casi la misma. Debido a esto, los profesionales de la seguridad tienen una discusión abierta sobre la caducidad de la contraseña y cuándo exigirle a un usuario que la cambie.

Con base en este ejemplo, debemos incluir, como parte de nuestras políticas de contraseñas, algunas palabras en la lista negra, que incluyen, entre otras:

* Nombre de la compania
* Palabras comunes asociadas a la empresa.
* nombres de meses
* nombres de estaciones
* Variaciones de la palabra bienvenida y contraseña.
* Palabras comunes y fáciles de adivinar, como contraseña, 123456 y abcde.

***

## <mark style="color:purple;">Hacer cumplir la política de contraseñas</mark>

Una política de contraseñas es una guía que define cómo debemos crear, manipular y almacenar contraseñas en la organización. Para aplicar esta guía, debemos hacerla cumplir, utilizando la tecnología a nuestra disposición o adquiriendo lo necesario para que funcione. La mayoría de las aplicaciones y administradores de identidad proporcionan métodos para aplicar nuestra política de contraseñas.

Por ejemplo, si utilizamos Active Directory para la autenticación, necesitamos configurar un [GPO de Política de contraseña de Active Directory](https://activedirectorypro.com/how-to-configure-a-domain-password-policy/) para obligar a nuestros usuarios a cumplir con nuestra política de contraseña.

Una vez cubierto el aspecto técnico, debemos comunicar la política a la empresa y crear procesos y procedimientos para garantizar que nuestra política de contraseñas se aplique en todas partes.

***

## <mark style="color:purple;">Creando una buena contraseña</mark>

Crear una buena contraseña puede ser fácil. Usemos [PasswordMonster](https://www.passwordmonster.com/) , un sitio web que nos ayuda a probar qué tan seguras son nuestras contraseñas, y [1Password Password Generator](https://1password.com/password-generator/) , otro sitio web para generar contraseñas seguras.

![Contraseña segura generada por la herramienta](https://academy.hackthebox.com/storage/modules/147/strong_password_1.png)

`CjDC2x[U` fue la contraseña generada por la herramienta, y es una buena contraseña. Se tardaría mucho en descifrarlo y probablemente no se adivinaría ni se obtendría en un ataque de Password Spraying, pero es difícil de recordar.

Podemos crear buenas contraseñas con palabras, frases e incluso canciones comunes y corrientes que nos gusten. A continuación se muestra un ejemplo de una buena contraseña `This is my secure password` o `The name of my dog is Poppy`. Podemos combinar esas contraseñas con caracteres especiales para hacerlas más complejas, como `()The name of my dog is Poppy!`. Aunque es difícil de adivinar, debemos tener en cuenta que los atacantes pueden usar OSINT para obtener información sobre nosotros, y debemos tener esto en cuenta al crear contraseñas.

![Contraseña segura con una frase](https://academy.hackthebox.com/storage/modules/147/strong_password_phrase.png)

Con este método podremos crear y memorizar 3, 4 o más contraseñas, pero a medida que la lista aumente será complicado recordar todas nuestras contraseñas. En la siguiente sección, analizaremos el uso de un Administrador de contraseñas para ayudarnos a crear y mantener la gran cantidad de contraseñas que tenemos.<br>
