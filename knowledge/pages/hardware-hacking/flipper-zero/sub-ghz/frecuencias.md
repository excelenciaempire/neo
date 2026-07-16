
# Frecuencias

<figure><img src="https://images.archbee.com/3GUDYkC5JgUWgo6RW8piO-GJIKj73NIJ5Vk6xcbgphX-20241024-180639.png?format=webp" alt=""><figcaption></figcaption></figure>

El módulo sub-1 GHz de Flipper Zero es capaz de recibir señales en todas las frecuencias en las bandas operativas de 300-348 MHz, 387-464 MHz y 779-928 MHz. Sin embargo, **Flipper Zero transmite señales solo en frecuencias permitidas para uso civil**.

### Cómo determinar su región y las frecuencias permitidas <a href="#ger9a" id="ger9a"></a>

Flipper Zero tiene la función de envío deshabilitada de fábrica hasta que el dispositivo se [actualice](https://docs.flipperzero.one/basics/firmware-update) mediante **la aplicación móvil Flipper** o **qFlipper** con una [tarjeta microSD](https://docs.flipperzero.one/basics/sd-card) insertada. Si intenta usar la función Sub-GHz antes de actualizar Flipper Zero, verá el siguiente mensaje: **Se necesita una actualización de firmware. Actualice el firmware antes de usar esta función flipp.dev/upd** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/_nSs4ft2_vYH_BkvD8mRR_monosnap-miro-2023-10-02-18-57-00.jpg?format=webp" alt=""><figcaption></figcaption></figure>

Al actualizar Flipper Zero, se determina la región en la que se encuentra el dispositivo y se desbloquean las frecuencias permitidas para la transmisión en esa región. Para ver el código de su región en [formato ISO](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) mientras está en el escritorio, **mantenga presionado** el botón **ABAJO** .

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/9EcNUzfy10CdwQOi-eqvS_monosnap-miro-2023-10-02-18-57-32.jpg?format=webp" alt=""><figcaption></figcaption></figure>

Para obtener más información sobre las regiones y frecuencias permitidas para uso civil, consulte la siguiente tabla:

<table data-header-hidden><thead><tr><th width="280"></th><th></th></tr></thead><tbody><tr><td><strong>Bandas de frecuencia</strong></td><td><strong>Regiones</strong></td></tr><tr><td><p>433,05 - 434,79 MHz</p><p>868,15 - 868,55 MHz</p></td><td>Unión Europea, Reino Unido, Rusia, Ucrania, Bielorrusia, Bosnia y Herzegovina, Polinesia Francesa, Santa Sede, Islandia, Kazajstán, Liechtenstein, Moldavia, Macedonia del Norte, Noruega, Serbia, Suiza, Turquía, Jersey, Montenegro, Albania, Kosovo, Armenia, Georgia, Azerbaiyán, Argelia, Líbano, Siria, Egipto, Libia, Túnez, Marruecos, Jordania, Palestina, Reunión, Andorra, Kirguistán, Uzbekistán</td></tr><tr><td><p>304,10 - 321,95 MHz</p><p>433,05 - 434,79 MHz</p><p>915,00 - 928,00 MHz</p></td><td>Estados Unidos de América, Canadá, Australia, Nueva Zelanda, México, Brasil, Chile, Argentina, Islas menores alejadas de los Estados Unidos, Puerto Rico, Colombia, Perú, Bolivia</td></tr><tr><td>420,00 - 440,00 MHz</td><td>Emiratos Árabes Unidos</td></tr><tr><td><p>304,50 - 321,95 MHz</p><p>433.075 - 434.775 MHz</p><p>915,00 - 927,95 MHz</p></td><td>Taiwán</td></tr><tr><td><p>300,00 - 300,30 MHz</p><p>312,00 - 316,00 MHz</p><p>433,50 - 434,79 MHz</p><p>444,40 - 444,80 MHz</p></td><td>Singapur</td></tr><tr><td>433,05 - 434,79 MHz</td><td>Israel</td></tr><tr><td>430,00 - 440,00 MHz</td><td>Filipinas</td></tr><tr><td>433,05 - 434,79 MHz</td><td>India</td></tr><tr><td><p>314,00 - 316,00 MHz</p><p>430,00 - 432,00 MHz</p><p>433,05 - 434,79 MHz</p></td><td>Porcelana</td></tr><tr><td>312,00 - 315,25 MHz 920,50 - 923,50 MHz</td><td>El resto del mundo</td></tr></tbody></table>

Para saber en qué frecuencia funciona su control remoto, utilice [el Analizador de frecuencia](https://docs.flipperzero.one/sub-ghz/read#bwvDc) .

Si intenta enviar señales grabadas en frecuencias que están prohibidas para uso civil en su región, verá el siguiente mensaje: **La transmisión está bloqueada. La transmisión en esta frecuencia está restringida en su región.**

<figure><img src="https://images.archbee.com/3StCFqarJkJQZV-7N79yY/JeIB7dTSKTohFsEAy7pJ6_monosnap-miro-2023-10-02-18-56-36.jpg?format=webp" alt=""><figcaption></figcaption></figure>
