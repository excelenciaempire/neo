
# Hardening en Linux - Privesc

Un correcto hardening de Linux puede eliminar la mayoría de las oportunidades de escalada de privilegios locales (si no todas). Se deben tomar las siguientes medidas, como mínimo, para reducir el riesgo de que un ataque pueda alcanzar el acceso a nivel raíz:

***

## <mark style="color:purple;">Actualizaciones y parches</mark>

Existen muchos exploits de escalada de privilegios rápidos y sencillos para kernels Linux desactualizados y versiones vulnerables conocidas de servicios integrados y de terceros. Realizar actualizaciones periódicas eliminará algunas de las "frutas al alcance de la mano" que se pueden aprovechar para escalar privilegios. En Ubuntu, el paquete [unattended-upgrades](https://packages.ubuntu.com/jammy/admin/unattended-upgrades) se instala de forma predeterminada a partir de la versión 18.04 y se puede instalar manualmente en Ubuntu a partir de al menos la versión 10.04 (Lucid). Los sistemas operativos basados ​​en Debian anteriores a Jessie también tienen este paquete disponible. En los sistemas basados ​​en Red Hat, el paquete [yum-cron](https://man7.org/linux/man-pages/man8/yum-cron.8.html) realiza una tarea similar.

***

## <mark style="color:purple;">Gestión de configuración</mark>

Esta no es de ninguna manera una lista exhaustiva, pero algunas medidas de endurecimiento simples son:

* Audita archivos y directorios escribibles y cualquier binario configurado con el bit SUID.
* Asegúrese de que todos los trabajos cron y los privilegios sudo especifiquen todos los binarios utilizando la ruta absoluta.
* No almacene credenciales en texto sin formato en archivos legibles para todo el mundo.
* Limpia los directorios de inicio y el historial de bash.
* Asegúrese de que los usuarios con pocos privilegios no puedan modificar ninguna biblioteca personalizada llamada por los programas.
* Elimine todos los paquetes y servicios innecesarios que puedan aumentar potencialmente la superficie de ataque.
* Considere implementar [SELinux](https://www.redhat.com/en/topics/linux/what-is-selinux) , que proporciona controles de acceso adicionales en el sistema.

***

## <mark style="color:purple;">Gestión de usuarios</mark>

Debemos limitar la cantidad de cuentas de usuario y de administrador en cada sistema, asegurarnos de que los intentos de inicio de sesión (válidos/no válidos) se registren y controlen. También es una buena idea aplicar una política de contraseñas segura, rotar las contraseñas periódicamente y restringir que los usuarios reutilicen contraseñas antiguas mediante el archivo /etc/security/opasswd con el módulo PAM. Debemos comprobar que los usuarios no se ubiquen en grupos que les otorguen derechos excesivos que no necesitan para sus tareas diarias y limitar los derechos de sudo según el principio del mínimo privilegio.

Existen plantillas para herramientas de automatización de la gestión de la configuración, como [Puppet](https://puppet.com/use-cases/configuration-management/) , [SaltStack](https://github.com/saltstack/salt) , [Zabbix](https://en.wikipedia.org/wiki/Zabbix) y [Nagios](https://en.wikipedia.org/wiki/Nagios) , para automatizar dichas comprobaciones, y se pueden utilizar para enviar mensajes a un canal de Slack o a un buzón de correo electrónico, así como a través de otros métodos. Se pueden utilizar acciones remotas (Zabbix) y acciones de remediación (Nagios) para encontrar y corregir automáticamente estos problemas en una flota de nodos. Herramientas como Zabbix también cuentan con funciones como la verificación de suma de comprobación, que se puede utilizar tanto para el control de versiones como para confirmar que no se han alterado los binarios confidenciales. Por ejemplo, a través del archivo [vfs.file.cksum .](https://www.zabbix.com/documentation/4.0/manual/config/items/itemtypes/zabbix_agent)

***

## <mark style="color:purple;">Auditoría</mark>

Realice comprobaciones periódicas de seguridad y configuración de todos los sistemas. Existen varias líneas de base de seguridad, como las [Guías de implementación técnica de seguridad (STIG) de](https://public.cyber.mil/stigs/) DISA , que se pueden seguir para establecer un estándar de seguridad en todos los tipos de sistemas operativos y dispositivos. Existen muchos marcos de cumplimiento, como [ISO27001](https://www.iso.org/isoiec-27001-information-security.html) , [PCI-DSS](https://www.pcisecuritystandards.org/pci_security/) e [HIPAA](https://www.hhs.gov/hipaa/for-professionals/security/index.html) , que una organización puede utilizar para ayudar a establecer líneas de base de seguridad. Todas ellas deben utilizarse como guías de referencia y no como base para un programa de seguridad. Un programa de seguridad sólido debe tener controles adaptados a las necesidades de la organización, el entorno operativo y los tipos de datos que almacena y procesa (es decir, información personal de salud, datos financieros, secretos comerciales o información disponible públicamente).

Una auditoría y una revisión de configuración no reemplazan una prueba de penetración ni otros tipos de evaluaciones técnicas y prácticas, y suelen considerarse como un ejercicio de "verificación de casillas" en el que una organización "aprueba" una auditoría de controles por realizar lo mínimo indispensable. Estas revisiones pueden ayudar a complementar los análisis de vulnerabilidades y las pruebas de penetración habituales, así como los programas sólidos de gestión de parches, vulnerabilidades y configuración.

Una herramienta útil para auditar sistemas basados ​​en Unix (Linux, MacOS, BDS, etc.) es [Lynis](https://github.com/CISOfy/lynis) . Esta herramienta audita la configuración actual de un sistema y proporciona consejos de refuerzo adicionales, teniendo en cuenta varios estándares. Puede ser utilizada por equipos internos, como administradores de sistemas, así como por terceros (auditores y evaluadores de penetración) para obtener una "línea de base" de la configuración de seguridad actual del sistema. Nuevamente, esta herramienta u otras similares no deben reemplazar las técnicas manuales analizadas en este módulo, pero pueden ser un complemento sólido para cubrir áreas que pueden pasarse por alto.

Después de clonar todo el repositorio, podemos ejecutar la herramienta escribiendo `./lynis audit system` y recibir un informe completo.

```shell-session
htb_student@NIX02:~$ ./lynis audit system

[ Lynis 3.0.1 ]

################################################################################
  Lynis comes with ABSOLUTELY NO WARRANTY. This is free software, and you are
  welcome to redistribute it under the terms of the GNU General Public License.
  See the LICENSE file for details about using this software.

  2007-2020, CISOfy - https://cisofy.com/lynis/
  Enterprise support available (compliance, plugins, interface and tools)
################################################################################


[+] Initializing program
------------------------------------

  ###################################################################
  #                                                                 #
  #   NON-PRIVILEGED SCAN MODE                                      #
  #                                                                 #
  ###################################################################

  NOTES:
  --------------
  * Some tests will be skipped (as they require root permissions)
  * Some tests might fail silently or give different results

  - Detecting OS...                                           [ DONE ]
  - Checking profiles...                                      [ DONE ]

  ---------------------------------------------------
  Program version:           3.0.1
  Operating system:          Linux
  Operating system name:     Ubuntu
  Operating system version:  16.04
  Kernel version:            4.4.0
  Hardware platform:         x86_64
  Hostname:                  NIX02
```

El análisis resultante se desglosará en advertencias:

```shell-session
Warnings (2):
  ----------------------------
  ! Found one or more cronjob files with incorrect file permissions (see log for details) [SCHD-7704] 
      https://cisofy.com/lynis/controls/SCHD-7704/

  ! systemd-timesyncd never successfully synchronized time [TIME-3185] 
      https://cisofy.com/lynis/controls/TIME-3185/
```

Sugerencias:

```shell-session
Suggestions (53):
  ----------------------------
  * Set a password on GRUB boot loader to prevent altering boot configuration (e.g. boot in single user mode without password) [BOOT-5122] 
      https://cisofy.com/lynis/controls/BOOT-5122/

  * If not required, consider explicit disabling of core dump in /etc/security/limits.conf file [KRNL-5820] 
      https://cisofy.com/lynis/controls/KRNL-5820/

  * Run pwck manually and correct any errors in the password file [AUTH-9228] 
      https://cisofy.com/lynis/controls/AUTH-9228/

  * Configure minimum encryption algorithm rounds in /etc/login.defs [AUTH-9230] 
      https://cisofy.com/lynis/controls/AUTH-9230/
```

y una sección de detalles generales del escaneo:

```shell-session
Lynis security scan details:

  Hardening index : 60 [############        ]
  Tests performed : 256
  Plugins enabled : 2

  Components:
  - Firewall               [X]
  - Malware scanner        [X]

  Scan mode:
  Normal [ ]  Forensics [ ]  Integration [ ]  Pentest [V] (running non-privileged)

  Lynis modules:
  - Compliance status      [?]
  - Security audit         [V]
  - Vulnerability scan     [V]

  Files:
  - Test and debug information      : /home/mrb3n/lynis.log
  - Report data                     : /home/mrb3n/lynis-report.dat
```

La herramienta es útil para informar rutas de escalada de privilegios y realizar una verificación de configuración rápida y realizará aún más verificaciones si se ejecuta como usuario root.

***

## <mark style="color:purple;">Conclusión</mark>

Como hemos visto, existen varias formas de aumentar los privilegios en los sistemas Linux/Unix, desde simples errores de configuración y exploits públicos para servicios vulnerables conocidos hasta el desarrollo de exploits basados ​​en bibliotecas personalizadas. Una vez que se obtiene el acceso root, resulta más fácil usarlo como punto de apoyo para una mayor explotación de la red. El fortalecimiento de Linux (y de todos los sistemas) es fundamental para las organizaciones de todos los tamaños. Las pautas y controles de mejores prácticas existen en muchas formas diferentes. Las revisiones deben incluir una combinación de pruebas y revisiones manuales prácticas y escaneo y validación de los resultados automatizados de la configuración.
