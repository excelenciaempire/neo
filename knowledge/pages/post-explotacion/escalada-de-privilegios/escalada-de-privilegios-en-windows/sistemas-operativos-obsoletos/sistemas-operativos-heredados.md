
# Sistemas operativos heredados

Si bien este módulo se centra principalmente en los sistemas operativos modernos (Windows 10/Windows Server 2016), como hemos visto, ciertos problemas (es decir, software vulnerable, configuraciones incorrectas, usuarios descuidados, etc.) no se pueden resolver simplemente actualizando a las últimas y mejores versiones de escritorio y servidor de Windows. Dicho esto, se han realizado mejoras de seguridad específicas a lo largo de los años que ya no afectan a las versiones modernas y compatibles del sistema operativo Windows. Durante nuestras evaluaciones, sin duda nos encontraremos con sistemas operativos heredados (especialmente contra grandes organizaciones como universidades, hospitales/organizaciones médicas, compañías de seguros, servicios públicos, gobiernos estatales/locales). Es esencial comprender las diferencias y ciertas fallas adicionales que debemos verificar para asegurarnos de que nuestras evaluaciones sean lo más exhaustivas posible.

***

## <mark style="color:purple;">End of Life Systems (EOL)</mark>

Con el tiempo, Microsoft decide dejar de ofrecer soporte continuo para versiones específicas del sistema operativo. Cuando dejan de brindar soporte para una versión de Windows, dejan de publicar actualizaciones de seguridad para la versión en cuestión. Los sistemas Windows primero pasan por un período de "soporte extendido" antes de ser clasificados como al final de su vida útil o que ya no reciben soporte oficial. Microsoft continúa creando actualizaciones de seguridad para estos sistemas que ofrece a grandes organizaciones a través de contratos de soporte a largo plazo personalizados. A continuación, se incluye una lista de versiones populares de Windows y sus fechas de finalización de vida útil:

### **Windows Desktop: fechas de fin de vida útil por versión**

| Versión                    | Fecha                   |
| -------------------------- | ----------------------- |
| Windows XP                 | 8 de abril de 2014      |
| Windows Vista              | 11 de abril de 2017     |
| Ventanas 7                 | 14 de enero de 2020     |
| Ventanas 8                 | 12 de enero de 2016     |
| Ventanas 8.1               | 10 de enero de 2023     |
| Versión 1507 de Windows 10 | 9 de mayo de 2017       |
| Versión 1703 de Windows 10 | 9 de octubre de 2018    |
| Versión 1809 de Windows 10 | 10 de noviembre de 2020 |
| Windows 10 versión 1903    | 8 de diciembre de 2020  |
| Windows 10 versión 1909    | 11 de mayo de 2021      |
| Windows 10 versión 2004    | 14 de diciembre de 2021 |
| Versión 20H2 de Windows 10 | 10 de mayo de 2022      |

### **Windows Server - Fechas de fin de vida útil por versión**

| Versión                  | Fecha                 |
| ------------------------ | --------------------- |
| Servidor Windows 2003    | 8 de abril de 2014    |
| Servidor Windows 2003 R2 | 14 de julio de 2015   |
| Servidor Windows 2008    | 14 de enero de 2020   |
| Servidor Windows 2008 R2 | 14 de enero de 2020   |
| Servidor Windows 2012    | 10 de octubre de 2023 |
| Servidor Windows 2012 R2 | 10 de octubre de 2023 |
| Servidor Windows 2016    | 12 de enero de 2027   |
| Servidor Windows 2019    | 9 de enero de 2029    |

Esta [página](https://michaelspice.net/windows/end-of-life-microsoft-windows-and-office/) contiene una lista más detallada de las fechas de finalización de la vida útil de Microsoft Windows y otros productos como Exchange, SQL Server y Microsoft Office, que podemos encontrar durante nuestras evaluaciones.

***

## <mark style="color:purple;">Impacto</mark>

Cuando los sistemas operativos llegan al final de su vida útil y ya no reciben soporte oficial, pueden surgir muchos problemas:

<table data-header-hidden><thead><tr><th width="221.4609375"></th><th></th></tr></thead><tbody><tr><td>Asunto</td><td>Descripción</td></tr><tr><td>Falta de apoyo de las empresas de software</td><td>Algunas aplicaciones (como navegadores web y otras aplicaciones esenciales) pueden dejar de funcionar una vez que una versión de Windows ya no tenga soporte oficial.</td></tr><tr><td>Problemas de hardware</td><td>Es probable que los componentes de hardware más nuevos dejen de funcionar en sistemas heredados.</td></tr><tr><td>Fallas de seguridad</td><td>Este es el mayor problema, con algunas excepciones notables (como <a href="https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2020-1350">CVE-2020-1350</a> (SIGRed) o EternalBlue ( <a href="https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2017-0144">CVE-2017-0144</a> )), que eran fallas de seguridad fácilmente explotables y "virus" que afectaban a miles de sistemas en todo el mundo (incluidas infraestructuras críticas como hospitales). Microsoft ya no lanzará actualizaciones de seguridad para sistemas al final de su vida útil. Esto podría dejar los sistemas expuestos a la ejecución remota de código y fallas de escalada de privilegios que permanecerán sin parchear hasta que el sistema se actualice o se retire.</td></tr></tbody></table>

En algunos casos, es difícil o imposible para una organización actualizar o retirar un sistema que ha llegado al final de su vida útil debido a limitaciones de personal y de costos. El sistema puede estar ejecutando software crítico para la misión que ya no recibe soporte del proveedor original. Esto es común en entornos médicos y en el gobierno local, donde el proveedor de una aplicación crítica deja de operar o ya no brinda soporte para una aplicación, por lo que la organización se ve obligada a ejecutarla en una versión de Windows XP o incluso Server 2000/2003. Si descubrimos esto durante una evaluación, es mejor hablar con el cliente para comprender las razones comerciales por las que no puede actualizar o retirar el sistema o los sistemas y sugerir soluciones como una segmentación estricta de la red para aislar estos sistemas hasta que se puedan abordar de manera adecuada.

Como pentesters, a menudo nos encontraremos con sistemas operativos heredados. Aunque no veo muchos hosts que ejecuten estaciones de trabajo Server 2000 o Windows XP vulnerables a [MS08-067](https://docs.microsoft.com/en-us/security-updates/securitybulletins/2008/ms08-067) , existen y los encuentro en ocasiones. Es más común ver algunos hosts Server 2003 y 2008. Cuando nos encontramos con estos sistemas, a menudo son vulnerables a uno o varios fallos de ejecución de código remoto o vectores de escalada de privilegios locales. Pueden ser un gran punto de apoyo en el entorno. Sin embargo, al atacarlos, siempre debemos consultar con el cliente para asegurarnos de que no sean hosts frágiles que ejecuten aplicaciones de misión crítica que podrían causar una interrupción masiva. Hay varias protecciones de seguridad en las versiones más nuevas del sistema operativo Windows que no existen en las versiones heredadas, lo que hace que nuestras tareas de escalada de privilegios sean mucho más sencillas.

Existen algunas diferencias notables entre las versiones más antiguas y las más nuevas del sistema operativo Windows. Si bien este módulo tiene como objetivo enseñar técnicas de escalada de privilegios locales que se pueden usar contra las versiones modernas del sistema operativo Windows, sería un descuido no repasar algunas de las diferencias clave entre las versiones más comunes. El núcleo del módulo se centra en varias versiones de Windows 10, Server 2016 y 2019, pero hagamos un viaje al pasado y analicemos un sistema Windows 7 y un Server 2008 desde la perspectiva de un pentester con el objetivo de identificar las diferencias clave que son cruciales durante las evaluaciones de entornos grandes.
