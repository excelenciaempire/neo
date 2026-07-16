
# Personalización del entorno

<table><thead><tr><th width="352">Antes: Kali Default</th><th>Después: KaliPWM</th></tr></thead><tbody><tr><td><img src="/files/2shbKougKDEfUQo0DRjQ" alt="" data-size="original"></td><td><img src="/files/vx3haNUavhIBqvERNiHR" alt="" data-size="original"></td></tr><tr><td><img src="/files/q3LvmxeWSBjqPDfdfUJu" alt="" data-size="original"></td><td><img src="/files/4DpJoKbirD7HyoDZQfqg" alt="" data-size="original"></td></tr></tbody></table>

## <mark style="color:purple;">KaliPWM</mark>

{% embed url="<https://github.com/afsh4ck/kalipwm>" %}

Al ejecutar este script en nuestro Kali Linux, nos configurará automáticamente un entorno profesional de Hacking, altamente personalizable. KaliPWM tiene instalado `OhMyZSH` y el tema `Powerlevel10K` por defecto.

### Pasos de instalación

```bash
git clone https://github.com/afsh4ck/kalipwm.git
cd kalipwm
bash kalipwm.sh
sudo reboot

# Una vez reiniciado cambia a bspwm en la pantalla de inicio de sesión
```

### Video de instalación del entorno

{% embed url="<https://youtu.be/3clLjO8W7Q4>" %}

<figure><img src="/files/vx3haNUavhIBqvERNiHR" alt=""><figcaption></figcaption></figure>

<figure><img src="/files/4DpJoKbirD7HyoDZQfqg" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Personalización de Shell</mark>

Lo primero de todo comprobamos la shell en la que se esta trabajando.

Recuerda que $$ se corresponde con el pid del proceso actual.

```bash
ls -l /proc/$$/exe
```

### OhmyZSH

<figure><img src="/files/VOyFf0RKKUNRuUAfH3Ff" alt=""><figcaption><p>OhMyZSH</p></figcaption></figure>

{% embed url="<https://github.com/ohmyzsh/ohmyzsh>" %}

### 1. Instalación de OhMyZSH

<table><thead><tr><th width="111">Método</th><th>Command</th></tr></thead><tbody><tr><td><strong>curl</strong></td><td><code>sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"</code></td></tr><tr><td><strong>wget</strong></td><td><code>sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"</code></td></tr><tr><td><strong>fetch</strong></td><td><code>sh -c "$(fetch -o - https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"</code></td></tr></tbody></table>

### 2. Instalar el tema Powerlevel10k

{% embed url="<https://github.com/romkatv/powerlevel10k>" %}

```bash
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

* Modificamos el fichero de configuración `~/.zshrc`

```bash
gedit ~/.zshrc
```

* Cambiamos el nombre del tema:

```bash
ZSH_THEME="powerlevel10k/powerlevel10k"
```

* Para cambiar la apariencia del prompt reiniciamos la terminal o ejecutamos el siguiente comando:

```
p10k configure
```

* Modificamos el fichero de configuración `~/.p10k.zsh` y seleccionamos las características que nos interesen:

```
gedit ~/.p10k.zsh
```

### 3. ZSH Autosuggestions

Plugin para sugerencias automáticas de comandos.

{% embed url="<https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md#oh-my-zsh>" %}

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

### 4. ZSH Syntax Highlighting

Plugin que nos resalta la sintaxis en distintos colores.

{% embed url="<https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md#oh-my-zsh>" %}

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### 5. Vincular plugins a OhMyZSH

Modificamos el fichero de configuración `~/.zshrc` y los añadimos en el apartado plugins de la siguiente manera:

```bash
gedit ~/.zshrc
```

```bash
plugins=( 
    # other plugins...
    zsh-autosuggestions
    zsh-syntax-highlighting
)
```

Por último cambiamos la configuración de la terminal y creamos los siguientes atajos de teclado:

* Split Terminal Horizontally -> `Ctrl+space`
* Split Terminal Vertically -> `Ctrl-\`
* Collapse Subterminal -> `Ctrl-Backspace`
* Right subterminal -> `Ctrl-]`
* Left subterminal -> `Ctrl-[`

## <mark style="color:purple;">Tipografía para terminal</mark>

Recomiendo la tipografía Jetbrains Mono, ya que tiene una mejor legibilidad en pantalla:

{% embed url="<https://www.jetbrains.com/es-es/lp/mono/>" %}

### Instalación

#### 🔹 Método 1: Instalación desde los Repositorios

JetBrains Mono no siempre está disponible en los repos de Kali, pero puedes probar:

```bash
sudo apt update
sudo apt install fonts-jetbrains-mono
```

Si este método no funciona, usa la instalación manual

#### 🔹 Método 2: Instalación Manual (Recomendado)

**Descargar la fuente**

```bash
mkdir -p ~/.local/share/fonts/JetBrainsMono
cd ~/.local/share/fonts/JetBrainsMono
wget -qO JetBrainsMono.zip "https://download.jetbrains.com/fonts/JetBrainsMono-2.304.zip"
unzip -o JetBrainsMono.zip
rm JetBrainsMono.zip
```

**Actualizar la caché de fuentes**

```bash
fc-cache -fv
```

**Verificar la instalación**

```bash
fc-list | grep "JetBrains"
```

Ahora solo tendríamos que cambiar la fuente desde los ajustes de la terminal:

<figure><img src="/files/Vr37lYbhMudmnopbhTUv" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Tmux</mark>

Tmux (Terminal Multiplexer) es una herramienta de línea de comandos que te permite administrar múltiples sesiones y ventanas en un entorno de terminal único. Con Tmux, puedes dividir tu terminal en paneles y trabajar en varias tareas a la vez. Aquí tienes una guía básica sobre cómo usar Tmux:

<figure><img src="/files/iXqt8Xuu4yyKBi7WqcCA" alt=""><figcaption></figcaption></figure>

### Instalación

```bash
sudo apt install tmux -y
```

| Acción                           | Comando Tmux                                                   |
| -------------------------------- | -------------------------------------------------------------- |
| Iniciar una nueva sesión         | `tmux`                                                         |
| Navegar entre sesiones           | `Ctrl-b s`                                                     |
| Crear una nueva ventana          | `Ctrl-b c`                                                     |
| Cambiar a ventana siguiente      | `Ctrl-b n`                                                     |
| Cambiar a ventana anterior       | `Ctrl-b p`                                                     |
| Cambiar a una ventana específica | `Ctrl-b 0` (para ventana 0), `Ctrl-b 1` (para ventana 1), etc. |
| Dividir verticalmente            | `Ctrl-b %`                                                     |
| Dividir horizontalmente          | `Ctrl-b "`                                                     |
| Cambiar al panel izquierdo       | `Ctrl-b Left Arrow`                                            |
| Cambiar al panel derecho         | `Ctrl-b Right Arrow`                                           |
| Cambiar al panel superior        | `Ctrl-b Up Arrow`                                              |
| Cambiar al panel inferior        | `Ctrl-b Down Arrow`                                            |
| Salir de Tmux                    | `exit`                                                         |
| Detener una sesión               | `Ctrl-b d`                                                     |
| Reanudar una sesión              | `tmux attach -t <nombre_o_número_de_sesión>`                   |
