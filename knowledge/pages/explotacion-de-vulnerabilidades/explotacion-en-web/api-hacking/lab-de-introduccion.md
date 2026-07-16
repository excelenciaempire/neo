
# Lab de introducción

A medida que avancemos en el módulo, practicaremos la identificación y explotación de cada uno de los 10 principales riesgos de seguridad de la API de OWASP utilizando una API web `RESTful` para comprender completamente estas vulnerabilidades.

### Ecommerce de Inlanefreight <a href="#inlanefreight-e-commerce-marketplace" id="inlanefreight-e-commerce-marketplace"></a>

Nuestro fiel cliente, Inlanefreight, se ha adentrado en el mundo de los marketplaces online. El modelo de negocio del marketplace permite a los clientes explorar y comprar productos ofrecidos por proveedores. Cada proveedor está asociado a una empresa específica. El marketplace genera ingresos cobrando una tarifa por cada producto que un cliente compra a un proveedor.

Para operar el mercado y facilitar las transacciones entre clientes y proveedores, Inlanefreight ha desarrollado una API web multiusuario que utiliza `Role-based Access Control`(`RBAC`) como política de control de acceso. A lo largo de las secciones, interactuaremos con la API utilizando diferentes usuarios con distintos roles. Las credenciales asociadas al dominio `pentestercompany.com` representan cuentas de proveedor, mientras que las que tienen `hackthebox.com` se identifican como cuentas de cliente.

Cada usuario que autentiquemos tendrá roles preasignados, determinados por el administrador de `Inlanefreight E-Commerce Marketplace`. El administrador ha adoptado una convención de nomenclatura sencilla para los roles: comparten el mismo nombre que los endpoints a los que proporcionan acceso. Por ejemplo, si un usuario tiene el rol `Suppliers_GetAll`, implica que está autorizado a interactuar con el endpoint que recupera todos los registros de proveedores (que, en este caso, es `/api/v1/suppliers`).

Nuestro objetivo es informar al administrador de cualquier vulnerabilidad detectada en `Inlanefreight E-Commerce Marketplace`. Un informe detallado de todas las vulnerabilidades descubiertas ayudará al administrador a tomar las medidas necesarias para proteger la API. Cada vulnerabilidad se asignará a su debilidad [CWE correspondiente.](https://cwe.mitre.org/data/index.html)

#### Swagger API User Interface <a href="#swagger-api-user-interface" id="swagger-api-user-interface"></a>

Aunque el frontend `Inlanefreight E-Commerce Marketplace` aún se encuentra en desarrollo activo, se puede acceder a la API web mediante una interfaz de usuario [de Swagger](https://swagger.io/tools/swagger-ui/) en la ruta `/swagger`. Utilizaremos esta interfaz a lo largo del módulo para explorar y evaluar la seguridad de la API del marketplace, que incluye más de `60 endpoints`:

![Interfaz de usuario Swagger para la API del Marketplace de Comercio Electrónico de Inlanefreight](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/02_Introduction_to_Lab_Image_2.png)

Las entidades clave que abarca el mercado incluyen `Customers`, `Products`, `Supplier-Companies` y `Suppliers`. También interactuaremos con otras entidades a medida que avancemos en las secciones.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.63.174:31468
```

#### Interactúa con cualquier endpoint e inspecciona los encabezados de respuesta; ¿cuál es el nombre del servidor que utiliza la API web?

Accedemos a:

```
http://94.237.63.174:31468/swagger/index.html
```

Vamos por ejemplo a Products, y le damos a Execute:

<figure><img src="/files/xFw7WPD9HBYj3CFfZRwv" alt=""><figcaption></figcaption></figure>

Eso nos genera la respuesta del servidor, y encontramos el nombre del servidor:

<figure><img src="/files/6MhJX2u8c1EDGOaNvd3u" alt=""><figcaption></figcaption></figure>

#### Solo hay un endpoint que pertenece al grupo Roles. Envíe su ruta.

<figure><img src="/files/E2rSAw3FqKLO8R5nTLpe" alt=""><figcaption></figcaption></figure>
