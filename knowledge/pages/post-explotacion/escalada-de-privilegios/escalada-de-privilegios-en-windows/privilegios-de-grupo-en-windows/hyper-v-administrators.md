
# Hyper-V Administrators

El grupo [de administradores de Hyper-V](https://docs.microsoft.com/en-us/windows/security/identity-protection/access-control/active-directory-security-groups#hyper-v-administrators) tiene acceso total a todas [las funciones de Hyper-V](https://docs.microsoft.com/en-us/windows-server/manage/windows-admin-center/use/manage-virtual-machines) . Si se han virtualizado los controladores de dominio, los administradores de virtualización deben considerarse administradores de dominio. Pueden crear fácilmente un clon del controlador de dominio activo y montar el disco virtual sin conexión para obtener el archivo NTDS.dit y extraer los hashes de contraseñas NTLM de todos los usuarios del dominio.

También está bien documentado en este [blog](https://decoder.cloud/2020/01/20/from-hyper-v-admin-to-system/) que, al eliminar una máquina virtual `vmms.exe`, se intentan restaurar los permisos de archivo originales en el archivo `.vhdx` correspondiente y lo hace como `NT AUTHORITY\SYSTEM`, sin hacerse pasar por el usuario. Podemos eliminar el archivo `.vhdx` y crear un enlace físico nativo para apuntar este archivo a un archivo SYSTEM protegido, sobre el cual tendremos permisos completos.

Si el sistema operativo es vulnerable a [CVE-2018-0952](https://www.tenable.com/cve/CVE-2018-0952) o [CVE-2019-0841](https://www.tenable.com/cve/CVE-2019-0841) , podemos aprovechar esto para obtener privilegios de SYSTEM. De lo contrario, podemos intentar aprovechar una aplicación en el servidor que haya instalado un servicio que se ejecuta en el contexto de SYSTEM, que puede ser iniciado por usuarios sin privilegios.

## <mark style="color:purple;">**Archivo de destino**</mark>

Un ejemplo de esto es Firefox, que instala el archivo `Mozilla Maintenance Service`. Podemos actualizar [este exploit](https://raw.githubusercontent.com/decoder-it/Hyper-V-admin-EOP/master/hyperv-eop.ps1) (una prueba de concepto para el enlace duro de NT) para otorgarle a nuestro usuario actual permisos completos en el archivo siguiente:

```shell-session
C:\Program Files (x86)\Mozilla Maintenance Service\maintenanceservice.exe
```

### **Tomando posesión del archivo**

Después de ejecutar el script de PowerShell, deberíamos tener control total de este archivo y poder tomar propiedad de él.

```cmd-session
C:\htb> takeown /F C:\Program Files (x86)\Mozilla Maintenance Service\maintenanceservice.exe
```

### **Iniciando** MozillaMaintenance

A continuación, podemos reemplazar este archivo con uno malicioso `maintenanceservice.exe`, iniciar el servicio de mantenimiento y obtener la ejecución del comando como SISTEMA.

```cmd-session
C:\htb> sc.exe start MozillaMaintenance
```

{% hint style="info" %}
Nota: Este vector se ha mitigado con las actualizaciones de seguridad de Windows de marzo de 2020, que cambiaron el comportamiento relacionado con los enlaces duros.
{% endhint %}
