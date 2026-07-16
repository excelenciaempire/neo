
# Bloodhound Enumeration

#### Relacionado

Es muy recomendable leer el siguiente artículo para entender como funciona BloodHound en versiones modernas con Docker, ya que en INE solamente enseñan el ejecutable antiguo de BloodHound:

{% content-ref url="/pages/TEIs7wP6Kqu4uwenlqgM" %}
[BloodHound](/ethical-hacking-cheatsheet/active-directory/active-directory/bloodhound.md)
{% endcontent-ref %}

***

## <mark style="color:purple;">Lab:</mark> <mark style="color:purple;"></mark><mark style="color:purple;">**BloodHound Reconnaissance**</mark>

El reconocimiento de Active Directory (AD) es un paso crucial para evaluar la seguridad de un entorno de Active Directory. Consiste en recopilar información sobre la infraestructura de Active Directory para identificar posibles vulnerabilidades y debilidades de seguridad. Una herramienta poderosa para realizar dicho reconocimiento es BloodHound.

BloodHound es una aplicación web de una sola página en JavaScript, basada en Linkurious y compilada con Electron, que utiliza una base de datos Neo4j alimentada por un recolector de datos en C# o PowerShell. BloodHound emplea la teoría de grafos para revelar las relaciones ocultas y a menudo involuntarias dentro de un entorno de Active Directory o Azure. Los atacantes pueden usar BloodHound para identificar fácilmente rutas de ataque muy complejas que, de otro modo, serían imposibles de detectar rápidamente. Los defensores pueden usar BloodHound para identificar y eliminar esas mismas rutas de ataque. Tanto los equipos azules como los rojos pueden usar BloodHound para comprender mejor las relaciones de privilegios en un entorno de Active Directory o Azure.

{% embed url="<https://github.com/BloodHoundAD/BloodHound>" %}

***

### Ejecutar SharpHound

SharpHound es el recolector para extraer todos los datos de Active Directory. Se encuentra en la ruta:

```
C:\Tools\BloodHound\BloodHound\resources\app\Collectors\SharpHound.exe
```

Una vez que lo ejecutamos nos genera un zip que debemos importar en la interfaz gráfica de BloodHound:

<figure><img src="/files/KSWDLcKN2WFKZJXEZCZQ" alt=""><figcaption></figcaption></figure>

### Importar en Bloodhound

Primero ejecutamos BloodHound:

<figure><img src="/files/RvggU51YqRFU997GKSBf" alt=""><figcaption></figcaption></figure>

Nos logueamos con:

* **Nombre de usuario:** neo4j
* **Contraseña:** Password\@123

<figure><img src="/files/u9CMLRUv5nsaXSwIJTUj" alt=""><figcaption></figcaption></figure>

Y en el apartado Upload Data subimos el zip que nos generó SharpHound:

### Encontrar Domain Admins

En la pestaña Analysis > Find all Domain Admins

{% hint style="info" %}
Pulsando Control podemos mostrar y ocultar las etiquetas
{% endhint %}

<figure><img src="/files/6Zooc469d7SkPhgF3hFy" alt=""><figcaption></figcaption></figure>

A hacer click en un usuario podemos ver información detallada como el SID:

<figure><img src="/files/o9bQryqkjOBH6uO5LbFK" alt=""><figcaption></figcaption></figure>

### Cuentas Kerberoasteables

Analysis > Find Kerberoasteable Accounts

<figure><img src="/files/06CRiQYoPFYOs9UBxpun" alt=""><figcaption></figcaption></figure>

### Usuarios Kerberoasteables de grupos de alto valor

<figure><img src="/files/leRZuJx56AhEnzItObTW" alt=""><figcaption></figcaption></figure>

### Cuentas AS-REP Roasteables

<figure><img src="/files/WBtw7Ep6UajTEHneb29W" alt=""><figcaption></figcaption></figure>

### Usuarios con permisos DCSync

Analysis > Find principals with DCSync Rights

<figure><img src="/files/NEmi6CNzwVsKaca65xW9" alt=""><figcaption></figcaption></figure>

### Pasos de explotación

<figure><img src="/files/RnXKrRy8t9lxdQc3LVTQ" alt=""><figcaption></figcaption></figure>

Podemos hacer click derecho sobre el permiso para obtener más información:

<figure><img src="/files/p4zt2FBCtMEhSkHm7aMd" alt=""><figcaption></figcaption></figure>

Y comandos de explotación para Windows y Linux:

<figure><img src="/files/uS8XbJXXho2DhVyQu5Pw" alt=""><figcaption></figcaption></figure>

***

Para más información consultar la sección dedicada y actualizada:

{% content-ref url="/pages/TEIs7wP6Kqu4uwenlqgM" %}
[BloodHound](/ethical-hacking-cheatsheet/active-directory/active-directory/bloodhound.md)
{% endcontent-ref %}
