
# Añadir nuevos controles remotos

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-qAZzVSgmyPF0e_mObcbsk-20241107-102457.png?format=webp" alt=""><figcaption></figcaption></figure>

En caso de que haya perdido su control remoto por radio o si desea tener otro control remoto, puede emparejar Flipper Zero con su receptor como control remoto. La función **Agregar manualmente** le permite crear un control remoto por radio virtual del mismo tipo que un receptor. Luego, puede emparejar su Flipper Zero con su receptor como control remoto emulando el control remoto virtual creado.

En esta página, aprenderá cómo agregar un nuevo control remoto y vincularlo con su receptor.

## <mark style="color:orange;">Procedimiento de adición</mark> <a href="#id-6byjo" id="id-6byjo"></a>

Antes de usar Flipper Zero como control remoto por radio, debes crear un control remoto virtual manualmente siguiendo estos pasos:

1. Vaya al **Menú principal -> Sub-GHz -> Add manually**
2. Seleccione un protocolo de la lista y luego presione **OK**
3. Ponle un nombre al control remoto y luego presiona **Guardar**

### Lista de protocolos soportados <a href="#id-3iglu" id="id-3iglu"></a>

| **Nombre del protocolo**                                                     | **Frecuencia de transmisión, MHz** | **Tipo de código** |
| ---------------------------------------------------------------------------- | ---------------------------------- | ------------------ |
| Princeton\_433 (funciona con la mayoría de los sistemas de código estático)﻿ | 433,92                             | Estático           |
| Nice Flo 12bit\_433                                                          | 433,92                             | Estático           |
| Nice Flo 24bit\_433                                                          | 433,92                             | Estático           |
| CAME 12bit\_433                                                              | 433,92                             | Estático           |
| CAME 24bit\_433                                                              | 433,92                             | Estático           |
| Linear\_300                                                                  | 300,00                             | Estático           |
| CAME TWEE                                                                    | 433,92                             | Estático           |
| Gate TX\_433                                                                 | 433,92                             | Estático           |
| DoorHan\_315                                                                 | 315,00                             | Dinámico           |
| DoorHan\_433                                                                 | 433,92                             | Dinámico           |
| LiftMaster\_315                                                              | 315,00                             | Dinámico           |
| LiftMaster\_390                                                              | 390,00                             | Dinámico           |
| Security+2.0\_310                                                            | 310,00                             | Dinámico           |
| Security+2.0\_315                                                            | 315,00                             | Dinámico           |
| Security+2.0\_390                                                            | 390,00                             | Dinámico           |

## <mark style="color:orange;">Procedimiento de emparejamiento</mark> <a href="#hmfpr" id="hmfpr"></a>

Una vez que se haya agregado el control remoto de la lista y guardado, podrá emparejar Flipper Zero con su receptor como control remoto por radio. Para emparejarlo, debe activar el modo de emparejamiento en su receptor y enviar una señal desde Flipper Zero de acuerdo con las instrucciones de su receptor.

Lea las instrucciones del receptor antes de emparejarloLos receptores tienen diferentes procedimientos de emparejamiento, así que lea las instrucciones antes de emparejar Flipper Zero con su receptor.﻿<br>
