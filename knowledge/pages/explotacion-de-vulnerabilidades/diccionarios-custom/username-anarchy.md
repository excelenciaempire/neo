
# Username Anarchy

{% embed url="<https://github.com/urbanadventurer/username-anarchy>" %}

Incluso con un nombre aparentemente sencillo como "Jane Smith", generar un nombre de usuario manualmente puede convertirse rápidamente en una tarea complicada. Aunque las combinaciones obvias como `jane`, `smith`, `janesmith`, `j.smith` o `jane.s` pueden parecer adecuadas, apenas rozan la superficie del potencial de nombres de usuario.

La creatividad humana no tiene límites, y los nombres de usuario a menudo se convierten en un lienzo para la expresión personal. Jane podía combinar a la perfección su segundo nombre, año de nacimiento o una afición que le encantaba, dando lugar a variaciones como `janemarie`, `smithj87` o `jane_the_gardener`. El atractivo de `leetspeak`, donde las letras se sustituyen por números o símbolos, podría manifestarse en nombres de usuario como `j4n3`, `5m1th`o `j@n3_5m1th`. Su pasión por un libro, una película o un grupo musical en particular podría inspirar nombres de usuario como `winteriscoming`, `potterheadjane` o `smith_beatles_fan`.

Aquí es donde `Username Anarchy` destaca. Tiene en cuenta iniciales, sustituciones comunes y más, ampliando la red en tu búsqueda para descubrir el nombre de usuario del objetivo.

```shell-session
afsh4ck@kali$ ./username-anarchy -l

Plugin name             Example
--------------------------------------------------------------------------------
first                   anna
firstlast               annakey
first.last              anna.key
firstlast[8]            annakey
first[4]last[4]         annakey
firstl                  annak
f.last                  a.key
flast                   akey
lfirst                  kanna
l.first                 k.anna
lastf                   keya
last                    key
last.f                  key.a
last.first              key.anna
FLast                   AKey
first1                  anna0,anna1,anna2
fl                      ak
fmlast                  abkey
firstmiddlelast         annaboomkey
fml                     abk
FL                      AK
FirstLast               AnnaKey
First.Last              Anna.Key
Last                    Key
```

## <mark style="color:purple;">Instalación</mark>

```shell-session
afsh4ck@kali$ sudo apt install ruby -y
afsh4ck@kali$ git clone https://github.com/urbanadventurer/username-anarchy.git
afsh4ck@kali$ cd username-anarchy
```

A continuación, ejecútalo con el nombre y apellido del objetivo. Esto generará posibles combinaciones de nombre de usuario.

```shell-session
afsh4ck@kali$ ./username-anarchy Jane Smith > jane_smith_usernames.txt
```

Al inspeccionar `jane_smith_usernames.txt`, encontrarás una variedad diversa de nombres de usuario, que incluyen:

* Combinaciones básicas: `janesmith`, `smithjane`, `jane.smith`, `j.smith`, etc.
* Iniciales: `js`, `j.s.`, `s.j.`, etc.
* etc.

Esta lista completa, adaptada al nombre del objetivo y valiosa en un ataque de fuerza bruta.
