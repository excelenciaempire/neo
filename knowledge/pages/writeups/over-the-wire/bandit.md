
# Bandit

{% hint style="danger" %}
**DISCLAIMER**: Esta página contiene spoilers sobre el juego y sus diferentes niveles. Como hackers éticos debéis intentar pensar "Out of the Box" y resolver los niveles con vuestros propios conocimientos y investigaciones.
{% endhint %}

## <mark style="color:purple;">Bandit</mark>

The goal of this level is for you to log into the game using SSH. The host to which you need to connect is **bandit.labs.overthewire.org**, on port 2220. The username is **bandit0** and the password is **bandit0**. Once logged in, go to the next section to find out how to beat Level 1.

```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220 Password: bandit0
```

```
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|                           

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

bandit0@bandit.labs.overthewire.org's password: 
```

### Bandit 0

The password for the next level is stored in a file called **readme** located in the home directory. Use this password to log into bandit1 using SSH. Whenever you find a password for a level, use SSH (on port 2220) to log into that level and continue the game.

```bash
cat readme
NH2SXQwcBdpmTEzi3bvBHMM9H66vVXjL
```

### Bandit 1

The password for the next level is stored in a file called **-** located in the home directory.

```bash
cat < - 
rRGizSaX8Mk1RTb1CNQoXTcYZWU6lgzi
```

### Bandit 2

The password for the next level is stored in a file called **spaces in this filename** located in the home directory.

```bash
cat <tab>
cat spaces\ in\ this\ filename
aBZ0W5EmUfAf7kHTQeOwd8bauFJ2lAiG
```

### Bandit 3

The password for the next level is stored in a hidden file in the **inhere** directory.

```bash
cd inhere
ls -la
cat .hidden 
2EW7BBsr6aMMoJ2HjW067dm8EgX26xNe
```

### Bandit 4

The password for the next level is stored in the only human-readable file in the **inhere** directory. Tip: if your terminal is messed up, try the “reset” command.

```bash
cd inhere
ls -la
cat < -file07 
lrIWWI6bB37kxfiCQZqUdOIYfr6eEeqR
```

### Bandit 5

The password for the next level is stored in a file somewhere under the **inhere** directory and has all of the following properties:

* human-readable
* 1033 bytes in size
* not executable

```bash
cd inhere
find ./ -type f -size 1033c ! -executable
cat ./maybehere07/.file2 
P4L4vucdmLnm8I7Vl7jG1ApGSfjYKqJU
```

### Bandit 6

The password for the next level is stored **somewhere on the server** and has all of the following properties:

* owned by user bandit7
* owned by group bandit6
* 33 bytes in size

```bash
cd
find * -type f -user bandit7 -group bandit6 -size 33c 
var/lib/dpkg/info/bandit7.password 
cat var/lib/dpkg/info/bandit7.password 
z7WtoNQU2XfjmMtWA8u5rN4vzqu4v99S
```

### Bandit 7

The password for the next level is stored in the file **data.txt** next to the word **millionth.**

```bash
cat data.txt | sort # millionth 
TESKZC0XvTetK0S9xNwm25STk5iWrBvP
```

### Bandit 8

The password for the next level is stored in the file **data.txt** and is the only line of text that occurs only once.

```bash
cat data.txt | sort | uniq -u # Archivo que solo se encuentra 1 vez 
EN632PlfYiZbn3PhVK3XOGSlNInNE00t
```

### Bandit 9

The password for the next level is stored in the file **data.txt** in one of the few human-readable strings, preceded by several ‘=’ characters.

```bash
strings data.txt | grep "=" | grep -oP '=+\s*\K[^=]+' 
the# GnFE password 5 is _ TU% ^,T,? y W K, G7w8LIi6J3kTb8A7j9LgrywtEUlyyp6s (
```

### Bandit 10

The password for the next level is stored in the file **data.txt**, which contains base64 encoded data.

```bash
cat data.txt | grep -E '^[A-Za-z0-9+/]+={0,2}$' 
VGhlIHBhc3N3b3JkIGlzIDZ6UGV6aUxkUjJSS05kTllGTmI2blZDS3pwaGxYSEJNCg== 
echo 'VGhlIHBhc3N3b3JkIGlzIDZ6UGV6aUxkUjJSS05kTllGTmI2blZDS3pwaGxYSEJNCg==' | base64 -d 
The password is 6zPeziLdR2RKNdNYFNb6nVCKzphlXHBM
```

### Bandit 11

The password for the next level is stored in the file data.txt, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions.

```bash
tr 'A-Za-z' 'N-ZA-Mn-za-m' < data.txt 
The password is JVNBBFSmZwKKOP0XbFXOoW8chDz5yVRv
```

### Bandit 12

The password for the next level is stored in the file **data.txt**, which is a hexdump of a file that has been repeatedly compressed. For this level it may be useful to create a directory under /tmp in which you can work using mkdir. For example: mkdir /tmp/myname123. Then copy the datafile using cp, and rename it using mv (read the manpages!)

#### Commands you may need to solve this level <a href="#commands-you-may-need-to-solve-this-level" id="commands-you-may-need-to-solve-this-level"></a>

grep, sort, uniq, strings, base64, tr, tar, gzip, bzip2, xxd, mkdir, cp, mv, file

```bash
# Crear directorio en /tmp
bandit12@bandit:~$ cd /tmp
bandit12@bandit:/tmp$ mktemp -d
/tmp/tmp.W5t1vua6G9
bandit12@bandit:/tmp$ cd /tmp/tmp.W5t1vua6G9
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ cp ~/data.txt .
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ ls
data.txt
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ mv data.txt hexdump_data
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ ls
hexdump_data

# Revertir hexdump
cat hexdump_data | head
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ xxd -r hexdump_data compressed_data
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ ls
compressed_data  hexdump_data
cat compressed_data | head

# Repetir descomprimido
andit12@bandit:/tmp/tmp.W5t1vua6G9$ cat hexdump_data 
00000000: 1f8b 0808 0650 b45e 0203 6461 7461 322e  .....P.^..data2.

bandit12@bandit:/tmp/tmp.W5t1vua6G9$ mv compressed_data compressed_data.gz
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ ls
compressed_data.gz  hexdump_data
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ gzip -d compressed_data.gz 
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ ls
compressed_data  hexdump_data

# BZIP2
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ xxd compressed_data 
00000000: 425a 6839 3141 5926 5359 8e4f 1cc8 0000  BZh91AY&SY.O....

andit12@bandit:/tmp/tmp.W5t1vua6G9$ mv compressed_data compressed_data.bz2
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ ls
compressed_data.bz2  hexdump_data
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ bzip2 -d compressed_data.bz2

# GZIP
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ mv compressed_data compressed_data.gz
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ gzip -d compressed_data.gz

# Archivos TAR
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ xxd compressed_data | head                                                      
00000000: 6461 7461 352e 6269 6e00 0000 0000 0000  data5.bin.......
00000010: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000020: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000030: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000040: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000050: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000060: 0000 0000 3030 3030 3634 3400 3030 3030  ....0000644.0000

bandit12@bandit:/tmp/tmp.W5t1vua6G9$ mv compressed_data compressed_data.tar
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ tar -xf compressed_data.tar 
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ ls
compressed_data.tar  data5.bin  hexdump_data

bandit12@bandit:/tmp/tmp.W5t1vua6G9$ tar -xf data5.bin

# BZIP2
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ xxd data6.bin 
00000000: 425a 6839 3141 5926 5359 080c 2b0b 0000  BZh91AY&SY..+...
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ bzip2 -d data6.bin
bzip2: Can't guess original name for data6.bin -- using data6.bin.out
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ ls
compressed_data.tar  data5.bin  data6.bin.out  hexdump_data

# Archivo TAR
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ tar -xf data6.bin.out
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ ls
compressed_data.tar  data5.bin  data6.bin.out  data8.bin  hexdump_data

# GZIP
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ xxd data8.bin
00000000: 1f8b 0808 0650 b45e 0203 6461 7461 392e  .....P.^..data9.
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ mv data8.bin data8.gz
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ gzip -d data8.gz
bandit12@bandit:/tmp/tmp.W5t1vua6G9$ ls
compressed_data.tar  data5.bin  data6.bin.out  data8  hexdump_data

bandit12@bandit:/tmp/tmp.W5t1vua6G9$ cat data8
The password is wbWdlBxEir4CaE8LaPhauuOo6pwRmrDw
```

### Bandit 13

The password for the next level is stored in **/etc/bandit\_pass/bandit14 and can only be read by user bandit14**. For this level, you don’t get the next password, but you get a private SSH key that can be used to log into the next level. **Note:** **localhost** is a hostname that refers to the machine you are working on

#### Commands you may need to solve this level <a href="#commands-you-may-need-to-solve-this-level" id="commands-you-may-need-to-solve-this-level"></a>

ssh, telnet, nc, openssl, s\_client, nmap

<pre class="language-bash"><code class="lang-bash">bandit13@bandit:~$ cat sshkey.private 

-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxkkOE83W2cOT7IWhFc9aPaaQmQDdgzuXCv+ppZHa++buSkN+
gg0tcr7Fw8NLGa5+Uzec2rEg0WmeevB13AIoYp0MZyETq46t+jk9puNwZwIt9XgB
ZufGtZEwWbFWw/vVLNwOXBe4UWStGRWzgPpEeSv5Tb1VjLZIBdGphTIK22Amz6Zb
ThMsiMnyJafEwJ/T8PQO3myS91vUHEuoOMAzoUID4kN0MEZ3+XahyK0HJVq68KsV
ObefXG1vvA3GAJ29kxJaqvRfgYnqZryWN7w3CHjNU4c/2Jkp+n8L0SnxaNA+WYA7
jiPyTF0is8uzMlYQ4l1Lzh/8/MpvhCQF8r22dwIDAQABAoIBAQC6dWBjhyEOzjeA
J3j/RWmap9M5zfJ/wb2bfidNpwbB8rsJ4sZIDZQ7XuIh4LfygoAQSS+bBw3RXvzE
pvJt3SmU8hIDuLsCjL1VnBY5pY7Bju8g8aR/3FyjyNAqx/TLfzlLYfOu7i9Jet67
xAh0tONG/u8FB5I3LAI2Vp6OviwvdWeC4nOxCthldpuPKNLA8rmMMVRTKQ+7T2VS
nXmwYckKUcUgzoVSpiNZaS0zUDypdpy2+tRH3MQa5kqN1YKjvF8RC47woOYCktsD
o3FFpGNFec9Taa3Msy+DfQQhHKZFKIL3bJDONtmrVvtYK40/yeU4aZ/HA2DQzwhe
ol1AfiEhAoGBAOnVjosBkm7sblK+n4IEwPxs8sOmhPnTDUy5WGrpSCrXOmsVIBUf
laL3ZGLx3xCIwtCnEucB9DvN2HZkupc/h6hTKUYLqXuyLD8njTrbRhLgbC9QrKrS
M1F2fSTxVqPtZDlDMwjNR04xHA/fKh8bXXyTMqOHNJTHHNhbh3McdURjAoGBANkU
1hqfnw7+aXncJ9bjysr1ZWbqOE5Nd8AFgfwaKuGTTVX2NsUQnCMWdOp+wFak40JH
PKWkJNdBG+ex0H9JNQsTK3X5PBMAS8AfX0GrKeuwKWA6erytVTqjOfLYcdp5+z9s
8DtVCxDuVsM+i4X8UqIGOlvGbtKEVokHPFXP1q/dAoGAcHg5YX7WEehCgCYTzpO+
xysX8ScM2qS6xuZ3MqUWAxUWkh7NGZvhe0sGy9iOdANzwKw7mUUFViaCMR/t54W1
GC83sOs3D7n5Mj8x3NdO8xFit7dT9a245TvaoYQ7KgmqpSg/ScKCw4c3eiLava+J
3btnJeSIU+8ZXq9XjPRpKwUCgYA7z6LiOQKxNeXH3qHXcnHok855maUj5fJNpPbY
iDkyZ8ySF8GlcFsky8Yw6fWCqfG3zDrohJ5l9JmEsBh7SadkwsZhvecQcS9t4vby
9/8X4jS0P8ibfcKS4nBP+dT81kkkg5Z5MohXBORA7VWx+ACohcDEkprsQ+w32xeD
qT1EvQKBgQDKm8ws2ByvSUVs9GjTilCajFqLJ0eVYzRPaY6f++Gv/UVfAPV4c+S0
kAWpXbv5tbkkzbS0eaLPTKgLzavXtQoTtKwrjpolHKIHUz6Wu+n4abfAIRFubOdN
/+aLoRQ0yBDRbdXMsZN/jvY44eM+xRLdRVyMmdPtP8belRi2E2aEzA==
-----END RSA PRIVATE KEY-----

<strong># Copiar a:
</strong>nano sshkey-14

chmod 600 sshkey-14
ssh -i sshkey-14 bandit14@bandit.labs.overthewire.org -p 2220
</code></pre>

### Bandit 14

The password for the next level can be retrieved by submitting the password of the current level to **port 30000 on localhost**.

```bash
# Primero necesitamos encontrar el password del nivel anterior
cat /etc/bandit_pass/bandit14
fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq

# Enviar el password al puerto 30000 en localhost
bandit14@bandit:~$ nc localhost 30000
fGrHPx402xGC7U7rXKDaxiWFTOiF0ENq
Correct!
jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt
```

### Bandit 15

The password for the next level can be retrieved by submitting the password of the current level to **port 30001 on localhost** using SSL encryption.

{% hint style="info" %}
**Helpful note:** Getting “HEARTBEATING” and “Read R BLOCK”? Use -ign\_eof and read the “CONNECTED COMMANDS” section in the manpage. Next to ‘R’ and ‘Q’, the ‘B’ command also works in this version of that command…
{% endhint %}

```bash
bandit15@bandit:~$ echo "jN2kgmIXJ6fShzhT2avhotn4Zcka6tnt" | openssl s_client -connect localhost:30001 -ign_eof
....SNIP....
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 84BAD1BD3A25F62C3F83D8C0DC6ABC20F3A610A5821C48A9C759BC729B9B701E
    Session-ID-ctx: 
    Resumption PSK: 5A08E75E69A3844B8732C1673A0687357600E935B14FB4855D619E97B4CA9A94C14CCFC625F84D0E722DF4529E764B79
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 2b c1 99 67 0b 63 23 4c-0c c7 d6 1d b8 f4 53 09   +..g.c#L......S.
    0010 - da 9c 55 36 14 20 38 ef-c7 30 54 d2 b8 2f db 55   ..U6. 8..0T../.U
    0020 - 33 8e c1 b5 e0 47 72 d9-67 ef b2 1c 41 97 9b cd   3....Gr.g...A...
    0030 - 6a f9 93 d9 ad 46 75 02-0b e0 92 ad b5 93 60 f9   j....Fu.......`.
    0040 - b2 33 b6 26 28 ca 8b 39-6d 28 73 b4 39 35 69 a6   .3.&(..9m(s.95i.
    0050 - e2 14 3a 25 3a ed fe 64-fa 35 d9 e4 f7 25 9f 45   ..:%:..d.5...%.E
    0060 - bf 5b 6e 23 34 4e 70 ba-e5 af e4 66 52 4f 1c 04   .[n#4Np....fRO..
    0070 - 52 0c f9 1f ef 7b 1c 60-ba 99 f6 e8 6f dd d6 cc   R....{.`....o...
    0080 - 9e 8d db 1e bc ae 63 c3-e6 32 20 ce bd 11 4c 92   ......c..2 ...L.
    0090 - 8f 89 2b 29 4d ff 33 62-c3 27 fe af 41 3e 78 1e   ..+)M.3b.'..A>x.
    00a0 - b8 73 cb d4 01 2c fe 7b-66 5e 91 fc 55 68 90 ea   .s...,.{f^..Uh..
    00b0 - a5 4a ad 64 b4 a7 f4 a0-e4 6c 37 ba ce b2 c0 bf   .J.d.....l7.....
    00c0 - 28 f4 83 a8 e1 59 92 1a-64 44 86 47 58 0b f1 e4   (....Y..dD.GX...

    Start Time: 1698223465
    Timeout   : 7200 (sec)
    Verify return code: 10 (certificate has expired)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
Correct!
JQttfApK4SeyHwDlI9SXGR50qclOAil1
```

### Bandit 16

The credentials for the next level can be retrieved by submitting the password of the current level to **a port on localhost in the range 31000 to 32000**. First find out which of these ports have a server listening on them. Then find out which of those speak SSL and which don’t. There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.

```bash
# Bucle for para encontrar puertos abiertos
for port in {31000..32000}; do
    nc -zv localhost $port 2>&1 | grep succeeded && echo "Puerto $port abierto"
done

# Encontramos los siguientes puertos
Connection to localhost (127.0.0.1) 31046 port [tcp/*] succeeded!
Puerto 31046 abierto
Connection to localhost (127.0.0.1) 31518 port [tcp/*] succeeded!
Puerto 31518 abierto
Connection to localhost (127.0.0.1) 31691 port [tcp/*] succeeded!
Puerto 31691 abierto
Connection to localhost (127.0.0.1) 31790 port [tcp/*] succeeded!
Puerto 31790 abierto
Connection to localhost (127.0.0.1) 31960 port [tcp/*] succeeded!
Puerto 31960 abierto

# Identificar servicios SSL
openssl s_client -connect localhost:PUERTO

# Recibimos respuesta positiva
Puerto 31518
Puerto 31790

# Enviamos el password del nivel actual a estos puertos
echo "JQttfApK4SeyHwDlI9SXGR50qclOAil1" | openssl s_client -connect localhost:31790 -ign_eof

# Nos devuelve un SSH Private Key
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
imZzeyGC0gtZPGujUSxiJSWI/oTqexh+cAMTSMlOJf7+BrJObArnxd9Y7YT2bRPQ
Ja6Lzb558YW3FZl87ORiO+rW4LCDCNd2lUvLE/GL2GWyuKN0K5iCd5TbtJzEkQTu
DSt2mcNn4rhAL+JFr56o4T6z8WWAW18BR6yGrMq7Q/kALHYW3OekePQAzL0VUYbW
JGTi65CxbCnzc/w4+mqQyvmzpWtMAzJTzAzQxNbkR2MBGySxDLrjg0LWN6sK7wNX
x0YVztz/zbIkPjfkU1jHS+9EbVNj+D1XFOJuaQIDAQABAoIBABagpxpM1aoLWfvD
KHcj10nqcoBc4oE11aFYQwik7xfW+24pRNuDE6SFthOar69jp5RlLwD1NhPx3iBl
J9nOM8OJ0VToum43UOS8YxF8WwhXriYGnc1sskbwpXOUDc9uX4+UESzH22P29ovd
d8WErY0gPxun8pbJLmxkAtWNhpMvfe0050vk9TL5wqbu9AlbssgTcCXkMQnPw9nC
YNN6DDP2lbcBrvgT9YCNL6C+ZKufD52yOQ9qOkwFTEQpjtF4uNtJom+asvlpmS8A
vLY9r60wYSvmZhNqBUrj7lyCtXMIu1kkd4w7F77k+DjHoAXyxcUp1DGL51sOmama
+TOWWgECgYEA8JtPxP0GRJ+IQkX262jM3dEIkza8ky5moIwUqYdsx0NxHgRRhORT
8c8hAuRBb2G82so8vUHk/fur85OEfc9TncnCY2crpoqsghifKLxrLgtT+qDpfZnx
SatLdt8GfQ85yA7hnWWJ2MxF3NaeSDm75Lsm+tBbAiyc9P2jGRNtMSkCgYEAypHd
HCctNi/FwjulhttFx/rHYKhLidZDFYeiE/v45bN4yFm8x7R/b0iE7KaszX+Exdvt
SghaTdcG0Knyw1bpJVyusavPzpaJMjdJ6tcFhVAbAjm7enCIvGCSx+X3l5SiWg0A
R57hJglezIiVjv3aGwHwvlZvtszK6zV6oXFAu0ECgYAbjo46T4hyP5tJi93V5HDi
Ttiek7xRVxUl+iU7rWkGAXFpMLFteQEsRr7PJ/lemmEY5eTDAFMLy9FL2m9oQWCg
R8VdwSk8r9FGLS+9aKcV5PI/WEKlwgXinB3OhYimtiG2Cg5JCqIZFHxD6MjEGOiu
L8ktHMPvodBwNsSBULpG0QKBgBAplTfC1HOnWiMGOU3KPwYWt0O6CdTkmJOmL8Ni
blh9elyZ9FsGxsgtRBXRsqXuz7wtsQAgLHxbdLq/ZJQ7YfzOKU4ZxEnabvXnvWkU
YOdjHdSOoKvDQNWu6ucyLRAWFuISeXw9a/9p7ftpxm0TSgyvmfLF2MIAEwyzRqaM
77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
-----END RSA PRIVATE KEY-----

# Lo copiamos en un archivo
nano sshkey-17
chmod 600 sshkey-17
ssh -i sshkey-17 bandit17@bandit.labs.overthewire.org -p 2220
# Ya estamos dentro

# Encontrar el password en plano del nivel actual
cat /etc/bandit_pass/bandit17
VwOSWtCA7lRKkTfbr2IDh6awj9RNZM5e
```

### Bandit 17

There are 2 files in the home directory: **passwords.old** and **passwords.new**. The password for the next level is in **passwords.new** and is the only line that has been changed between **passwords.old and passwords.new**

{% hint style="info" %}
**NOTE:** if you have solved this level and see ‘Byebye!’ when trying to log into bandit18, this is related to the next level, **bandit19**
{% endhint %}

```bash
bandit17@bandit:~$ ls
passwords.new  passwords.old

bandit17@bandit:~$ diff passwords.old passwords.new | grep '^>'
> hga5tuuCLF6fFzUpnagiMN8ssu9LFrdg
```

### Bandit 18

The password for the next level is stored in a file **readme** in the home directory. Unfortunately, someone has modified **.bashrc** to log you out when you log in with SSH.

```bash
# Al hacer login por SSH nos expulsa del servidor
# Evitar .bashrc
ssh -t bandit18@bandit.labs.overthewire.org -p 2220  "cat /home/bandit18/readme"
hga5tuuCLF6fFzUpnagiMN8ssu9LFrdg

# Nos devuelve el password
awhqfNnAbc1naukrpqDYcF95h7HoMTrC
```

### Bandit 19

To gain access to the next level, you should use the setuid binary in the home directory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (/etc/bandit\_pass), after you have used the setuid binary.

{% code overflow="wrap" %}

```bash
bandit19@bandit:~$ ls
bandit20-do

# Nos encontramos un archivo ejecutable
bandit19@bandit:~$ file bandit20-do 
bandit20-do: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=037b97b430734c79085a8720c90070e346ca378e, for GNU/Linux 3.2.0, not stripped

# Lo ejecutamos
bandit19@bandit:~$ ./bandit20-do 
Run a command as another user.
  Example: ./bandit20-do id
  
bandit19@bandit:~$ ./bandit20-do id
uid=11019(bandit19) gid=11019(bandit19) euid=11020(bandit20) groups=11019(bandit19)

bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
VxCazJaVykI6W36BkBU0mJTCM8rR95XT
```

{% endcode %}

### Bandit 20

There is a setuid binary in the home directory that does the following: it makes a connection to localhost on the port you specify as a command line argument. It then reads a line of text from the connection and compares it to the password in the previous level (bandit20). If the password is correct, it will transmit the password for the next level (bandit21).

{% hint style="info" %}
**NOTE:** Try connecting to your own network daemon to see if it works as you think
{% endhint %}

{% code overflow="wrap" %}

```bash
bandit20@bandit:~$ ./suconnect

Usage: ./suconnect <portnumber>
This program will connect to the given port on localhost using TCP. If it receives the correct password from the other side, the next password is transmitted back.

bandit20@bandit:~$ ./suconnect 1234
Read: VxCazJaVykI6W36BkBU0mJTCM8rR95XT
Password matches, sending next password

# En otra terminal nos volvemos a conectar por SSH a Bandit 20
bandit20@bandit:~$ nc -nlvp 1234
Listening on 0.0.0.0 1234
Connection received on 127.0.0.1 45922
VxCazJaVykI6W36BkBU0mJTCM8rR95XT
NvEJF7oVjkddltPSrdKEFOllh9V1IBcq

#Password
NvEJF7oVjkddltPSrdKEFOllh9V1IBcq
```

{% endcode %}

### Bandit 21

A program is running automatically at regular intervals from **cron**, the time-based job scheduler. Look in **/etc/cron.d/** for the configuration and see what command is being executed.

```bash
bandit21@bandit:/etc/cron.d$ ls
cronjob_bandit15_root  cronjob_bandit22  cronjob_bandit24       e2scrub_all  sysstat
cronjob_bandit17_root  cronjob_bandit23  cronjob_bandit25_root  otw-tmp-dir

bandit21@bandit:/etc/cron.d$ cat cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null

bandit21@bandit:/etc/cron.d$  cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv

bandit21@bandit:~$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
WdDozAdTM2z9DiFEQ2mGlwngMfj4EZff
```

### Bandit 22

A program is running automatically at regular intervals from **cron**, the time-based job scheduler. Look in **/etc/cron.d/** for the configuration and see what command is being executed.

{% hint style="info" %}
**NOTE:** Looking at shell scripts written by other people is a very useful skill. The script for this level is intentionally made easy to read. If you are having problems understanding what it does, try executing it to see the debug information it prints.
{% endhint %}

{% code overflow="wrap" %}

```bash
bandit22@bandit:~$ cd /etc/cron.d/ 

bandit22@bandit:/etc/cron.d$ ls
cronjob_bandit15_root  cronjob_bandit22  cronjob_bandit24  e2scrub_all  sysstat  cronjob_bandit17_root  cronjob_bandit23  cronjob_bandit25_root  otw-tmp-dir

bandit22@bandit:/etc/cron.d$ cat cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null

bandit22@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit23.sh
#!/bin/bash
myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)
echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"
cat /etc/bandit_pass/$myname > /tmp/$mytarget

# Necesitamos ejecutarlo como bandit23 para obtener el password

# No podemos modificar el script porque no tenemos permisos de escritura, por lo que vamos a ejecutarlo manualmente

# Obtener el hash MD5, que se almacena en /tmp
bandit22@bandit:~$ echo "I am user bandit23" | md5sum | cut -d ' ' -f 1
8ca319486bfbbc3663ea0fbe81326349

bandit22@bandit:~$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
QYw0Y2aiA672PsMmh9puTQuhoz8SyR2G
```

{% endcode %}

### Bandit 23

A program is running automatically at regular intervals from **cron**, the time-based job scheduler. Look in **/etc/cron.d/** for the configuration and see what command is being executed.

{% hint style="info" %}
**NOTE:** This level requires you to create your own first shell-script. This is a very big step and you should be proud of yourself when you beat this level!
{% endhint %}

{% hint style="warning" %}
**NOTE 2:** Keep in mind that your shell script is removed once executed, so you may want to keep a copy around…
{% endhint %}

```bash
bandit23@bandit:/etc/cron.d$ cd /etc/cron.d/
bandit23@bandit:/etc/cron.d$ cat cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null

# Vemos el script
bandit23@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash
myname=$(whoami)

cd /var/spool/$myname/foo
echo "Executing and deleting all scripts in /var/spool/$myname/foo:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" ./$i)"
        if [ "${owner}" = "bandit23" ]; then
            timeout -s 9 60 ./$i
        fi
        rm -f ./$i
    fi
done
```

El script cronjob\_bandit24.sh indica que se ejecutan todos los scripts en el directorio /var/spool/bandit24/foo. Se eliminan después de ser ejecutados. Esto implica que puedes agregar un script en ese directorio para que se ejecute.

<pre class="language-bash" data-overflow="wrap"><code class="lang-bash"># Creamos un script (myscript.sh) que imprima el contenido del archivo de contraseña en un lugar donde puedas verlo:
mktemp -d
/tmp/tmp.hTgJOFcPaH

cd /tmp/tmp.hTgJOFcPaH
nano myscript.sh

<strong>#!/bin/bash
</strong>cat /etc/bandit_pass/bandit24 > /tmp/tmp.hTgJOFcPaH/password

<strong># Le damos permisos de ejecución
</strong>bandit23@bandit:/tmp/tmp.cwnhwiGK8y$ chmod +rx myscript.sh 
bandit23@bandit:/tmp/tmp.cwnhwiGK8y$ chmod 777 /tmp/tmp.cwnhwiGK8y
bandit23@bandit:/tmp/tmp.cwnhwiGK8y$ touch password
bandit23@bandit:/tmp/tmp.cwnhwiGK8y$ chmod +rwx password
bandit23@bandit:/tmp/tmp.cwnhwiGK8y$ ls
myscript.sh  password

# Copia el script al directorio /var/spool/bandit24/foo:
bandit23@bandit:/tmp/tmp.hTgJOFcPaH$ cp myscript.sh /var/spool/bandit24/foo/

# Esperar 1 minuto a que el cron ejecute el script
bandit23@bandit:/tmp/tmp.hTgJOFcPaH$ cat password 
VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar
</code></pre>

### Bandit 24

A daemon is listening on port 30002 and will give you the password for bandit25 if given the password for bandit24 and a secret numeric 4-digit pincode. There is no way to retrieve the pincode except by going through all of the 10000 combinations, called brute-forcing. You do not need to create new connections each time.

***

Para realizar un ataque de fuerza bruta en el pincode de bandit25, vamos a escribir un script en bash para iterar a través de todas las combinaciones posibles de 4 dígitos y enviarlas al daemon en el puerto 30002 junto con la contraseña de bandit24:

{% code overflow="wrap" %}

```bash
# Nos intentamos conectar por netcat a localhost puerto 30002
bandit24@bandit:$ nc localhost 30002
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.

VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar 0000
Wrong! Please enter the correct pincode. Try again.

# Creamos directorio temporal y accedemos
bandit24@bandit:~$ mktemp -d
/tmp/tmp.YirnrWx7mB
bandit24@bandit:~$ cd /tmp/tmp.YirnrWx7mB

# Creamos el script en bash
bandit24@bandit:/tmp/tmp.YirnrWx7mB nano brute-pin.sh
```

{% endcode %}

{% code title="brute-pin.sh" %}

```bash
#!/bin/bash

for i in {0000..9999}
do 
	echo "VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar $i"
done
```

{% endcode %}

```bash
bandit24@bandit:/tmp/tmp.YirnrWx7mB$ ./brute-pin.sh > combinations.txt
bandit24@bandit:/tmp/tmp.YirnrWx7mB$ cat combinations.txt | nc localhost 30002
....SNIP....
Wrong! Please enter the correct pincode. Try again.
Wrong! Please enter the correct pincode. Try again.
Wrong! Please enter the correct pincode. Try again.
Wrong! Please enter the correct pincode. Try again.
Wrong! Please enter the correct pincode. Try again.
Wrong! Please enter the correct pincode. Try again.
Wrong! Please enter the correct pincode. Try again.
Correct!
The password of user bandit25 is p7TaowMYrmu23Ol8hiZh9UvD0O9hpx8d
```

### Bandit 25

Logging in to bandit26 from bandit25 should be fairly easy… The shell for user bandit26 is not **/bin/bash**, but something else. Find out what it is, how it works and how to break out of it.

```bash
bandit25@bandit:~$ ls
bandit26.sshkey

bandit25@bandit:~$ cat bandit26.sshkey 
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEApis2AuoooEqeYWamtwX2k5z9uU1Afl2F8VyXQqbv/LTrIwdW
pTfaeRHXzr0Y0a5Oe3GB/+W2+PReif+bPZlzTY1XFwpk+DiHk1kmL0moEW8HJuT9
/5XbnpjSzn0eEAfFax2OcopjrzVqdBJQerkj0puv3UXY07AskgkyD5XepwGAlJOG
xZsMq1oZqQ0W29aBtfykuGie2bxroRjuAPrYM4o3MMmtlNE5fC4G9Ihq0eq73MDi
1ze6d2jIGce873qxn308BA2qhRPJNEbnPev5gI+5tU+UxebW8KLbk0EhoXB953Ix
3lgOIrT9Y6skRjsMSFmC6WN/O7ovu8QzGqxdywIDAQABAoIBAAaXoETtVT9GtpHW
qLaKHgYtLEO1tOFOhInWyolyZgL4inuRRva3CIvVEWK6TcnDyIlNL4MfcerehwGi
il4fQFvLR7E6UFcopvhJiSJHIcvPQ9FfNFR3dYcNOQ/IFvE73bEqMwSISPwiel6w
e1DjF3C7jHaS1s9PJfWFN982aublL/yLbJP+ou3ifdljS7QzjWZA8NRiMwmBGPIh
Yq8weR3jIVQl3ndEYxO7Cr/wXXebZwlP6CPZb67rBy0jg+366mxQbDZIwZYEaUME
zY5izFclr/kKj4s7NTRkC76Yx+rTNP5+BX+JT+rgz5aoQq8ghMw43NYwxjXym/MX
c8X8g0ECgYEA1crBUAR1gSkM+5mGjjoFLJKrFP+IhUHFh25qGI4Dcxxh1f3M53le
wF1rkp5SJnHRFm9IW3gM1JoF0PQxI5aXHRGHphwPeKnsQ/xQBRWCeYpqTme9amJV
tD3aDHkpIhYxkNxqol5gDCAt6tdFSxqPaNfdfsfaAOXiKGrQESUjIBcCgYEAxvmI
2ROJsBXaiM4Iyg9hUpjZIn8TW2UlH76pojFG6/KBd1NcnW3fu0ZUU790wAu7QbbU
i7pieeqCqSYcZsmkhnOvbdx54A6NNCR2btc+si6pDOe1jdsGdXISDRHFb9QxjZCj
6xzWMNvb5n1yUb9w9nfN1PZzATfUsOV+Fy8CbG0CgYEAifkTLwfhqZyLk2huTSWm
pzB0ltWfDpj22MNqVzR3h3d+sHLeJVjPzIe9396rF8KGdNsWsGlWpnJMZKDjgZsz
JQBmMc6UMYRARVP1dIKANN4eY0FSHfEebHcqXLho0mXOUTXe37DWfZza5V9Oify3
JquBd8uUptW1Ue41H4t/ErsCgYEArc5FYtF1QXIlfcDz3oUGz16itUZpgzlb71nd
1cbTm8EupCwWR5I1j+IEQU+JTUQyI1nwWcnKwZI+5kBbKNJUu/mLsRyY/UXYxEZh
ibrNklm94373kV1US/0DlZUDcQba7jz9Yp/C3dT/RlwoIw5mP3UxQCizFspNKOSe
euPeaxUCgYEAntklXwBbokgdDup/u/3ms5Lb/bm22zDOCg2HrlWQCqKEkWkAO6R5
/Wwyqhp/wTl8VXjxWo+W+DmewGdPHGQQ5fFdqgpuQpGUq24YZS8m66v5ANBwd76t
IZdtF5HXs2S5CADTwniUS5mX1HO9l5gUkk+h0cH5JnPtsMCnAUM+BRY=
-----END RSA PRIVATE KEY-----
```

Copiamos la SSH Private Key a un archivo y nos conectamos por SSH a bandit 26:

```bash
ssh -i sshkey-26 bandit26@bandit.labs.overthewire.org -p 2220

  Enjoy your stay!

  _                     _ _ _   ___   __  
 | |                   | (_) | |__ \ / /  
 | |__   __ _ _ __   __| |_| |_   ) / /_  
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \ 
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/ 
Connection to bandit.labs.overthewire.org closed.

# Al intentar conectarnos por SSH nos loguea bien pero nos expulsa
# La pista dice que la shell para bandit26 no es /bin/bash

bandit25@bandit:~$ cat /etc/passwd | grep bandit26
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext

# Encontramos que ejecuta un archivo "showtext" en bash
bandit25@bandit:~$ cat /usr/bin/showtext

#!/bin/sh
export TERM=linux
exec more ~/text.txt
exit 0
```

exec more nos indica que debemos hacer mas pequeño el alto de nuestra terminal para acceder al archivo de texto.

<figure><img src="/files/1vIU6xMC9V89CDHOXSB7" alt=""><figcaption></figcaption></figure>

Efectivamente al loguearnos ahora no nos expulsa por lo que vamos a intentar leer la contraseña de bandit 26 con el editor de texto vim. Pulsamos `v` para iniciar vim y nos muestra la siguiente pantalla:

<figure><img src="/files/qsPMgtq3SmjBi1rJ8UOP" alt=""><figcaption></figcaption></figure>

{% code title="Modo de edición" %}

```vim
:e /etc/bandit_pass/bandit26
```

{% endcode %}

<figure><img src="/files/MpoyFCpSbgd0ows62rZO" alt=""><figcaption></figcaption></figure>

```
c7GvcKlw9mC7aUQaPx7nwFstuAIBw1o1
```

### Bandit 26

Good job getting a shell! Now hurry and grab the password for bandit27!

```bash
# Al intentar conectarnos por SSH nos expulsa al igual que en el nivel anterior

  Enjoy your stay!

  _                     _ _ _   ___   __  
 | |                   | (_) | |__ \ / /  
 | |__   __ _ _ __   __| |_| |_   ) / /_  
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \ 
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/ 
Connection to bandit.labs.overthewire.org closed.

# El usuario bandit26 tenia una shell diferente a /bin/bash
/usr/bin/showtext

# Vamos a cambiarlo con vim con la ventana pequeña:
:set shell=/bin/bash
```

<figure><img src="/files/B4JS8Sqk10yWXzpkVtM6" alt=""><figcaption></figcaption></figure>

En este punto podemos acceder por shell con el comando `:shell`

<figure><img src="/files/paGOUBPWNhueBRjwJfBS" alt=""><figcaption></figcaption></figure>

```shell-session
  _                     _ _ _   ___   __
 | |                   | (_) | |__ \ / /  
 | |__   __ _ _ __   __| |_| |_   ) / /_  
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
:shell
bandit26@bandit:~$ ls
bandit27-do  text.txt

bandit26@bandit:~$ ./bandit27-do 
Run a command as another user.
  Example: ./bandit27-do id
  
bandit26@bandit:~$ ./bandit27-do id
uid=11026(bandit26) gid=11026(bandit26) euid=11027(bandit27) groups=11026(bandit26)

bandit26@bandit:~$ ./bandit27-do cat /etc/bandit_pass/bandit27
YnQpBuifNMas1hcUFk70ZmqkhUU2EuaS
```

### Bandit 27

There is a git repository at `ssh://bandit27-git@localhost/home/bandit27-git/repo` via the port `2220`. The password for the user `bandit27-git` is the same as for the user `bandit27`.

Clone the repository and find the password for the next level.

```bash
bandit27@bandit:~$ git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo
Password: YnQpBuifNMas1hcUFk70ZmqkhUU2EuaS
fatal: could not create work tree dir 'repo': Permission denied

# Creamos directorio temporal
bandit27@bandit:~$ mktemp -d
/tmp/tmp.MqNkecAg2I
bandit27@bandit:~$ cd /tmp/tmp.MqNkecAg2I
bandit27@bandit:/tmp/tmp.MqNkecAg2I$ git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo
Password: YnQpBuifNMas1hcUFk70ZmqkhUU2EuaS
Cloning into 'repo'...
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

bandit27-git@localhost's password: 
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.

bandit27@bandit:/tmp/tmp.MqNkecAg2I$ ls
repo
bandit27@bandit:/tmp/tmp.MqNkecAg2I$ cd repo
bandit27@bandit:/tmp/tmp.MqNkecAg2I/repo$ ls
README
bandit27@bandit:/tmp/tmp.MqNkecAg2I/repo$ cat README
The password to the next level is: AVanL161y9rsbcJIsFHuw35rjaOM19nR
```

### Bandit 28

There is a git repository at `ssh://bandit28-git@localhost/home/bandit28-git/repo` via the port `2220`. The password for the user `bandit28-git` is the same as for the user `bandit28`.

Clone the repository and find the password for the next level.

{% code overflow="wrap" %}

```bash
bandit28@bandit:~$ git clone ssh://bandit28-git@localhost:2220/home/bandit28-git/repo
fatal: could not create work tree dir 'repo': Permission denied

# Creamos un directorio temporal
bandit28@bandit:~$ mktemp -d
/tmp/tmp.7wMuSspT90
bandit28@bandit:~$ cd /tmp/tmp.7wMuSspT90
bandit28@bandit:/tmp/tmp.7wMuSspT90$ git clone ssh://bandit28-git@localhost:2220/home/bandit28-git/repo
Cloning into 'repo'...
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

bandit28-git@localhost's password: 
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 9 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (9/9), done.
Resolving deltas: 100% (2/2), done.
bandit28@bandit:/tmp/tmp.7wMuSspT90$ ls
repo
bandit28@bandit:/tmp/tmp.7wMuSspT90$ cd repo
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo$ ls
README.md
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo$ cat README.md 
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx

# Vemos otros archivos ocultos en la carpeta repo
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo$ ls -la
total 16
drwxrwxr-x 3 bandit28 bandit28 4096 Oct 29 23:14 .
drwx------ 3 bandit28 bandit28 4096 Oct 29 23:13 ..
drwxrwxr-x 8 bandit28 bandit28 4096 Oct 29 23:14 .git
-rw-rw-r-- 1 bandit28 bandit28  111 Oct 29 23:14 README.md
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo$ cd .git
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo/.git$ ls
branches  config  description  HEAD  hooks  index  info  logs  objects  packed-refs  refs

# En la carpeta logs encontramos algo parecido a un password
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo/.git$ cd logs
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo/.git/logs$ ls
HEAD  refs
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo/.git/logs$ cat HEAD 
0000000000000000000000000000000000000000 14f754b3ba6531a2b89df6ccae6446e8969a41f3 Ben Dover <noone@overthewire.org> 1698621247 +0000	clone: from ssh://localhost:2220/home/bandit28-git/repo

# EN la carpeta objects/pack tambien nos encontramos 2 archivos interesantes
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo/.git/objects$ cd pack/
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo/.git/objects/pack$ ls
pack-a8af65113ecbd080fb1996a9cc4e30f4f580a2f3.idx
pack-a8af65113ecbd080fb1996a9cc4e30f4f580a2f3.pack

```

{% endcode %}

Los archivos con extensión `.idx` y `.pack` están asociados a Git, un sistema de control de versiones distribuido. Estos archivos forman parte de la estructura interna de Git y se utilizan para almacenar datos de manera eficiente.

`.idx (Index)`: Este archivo es un índice binario que proporciona un acceso rápido y eficiente a los objetos almacenados en la base de datos de Git. Contiene un mapeo de nombres de objetos (hashes) a ubicaciones de disco, lo que facilita la búsqueda rápida y la recuperación de datos.

`.pack (Pack)`: Estos archivos almacenan objetos Git comprimidos para ahorrar espacio en disco. Git utiliza la técnica de "packing" para combinar varios objetos en un solo archivo y comprimirlos. Los archivos .pack suelen estar acompañados por un archivo .idx correspondiente que sirve como índice para acceder a los objetos dentro del archivo .pack.

```bash
# Acceder al contenido del pack
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo/.git/objects/pack$ git verify-pack -v pack-a8af65113ecbd080fb1996a9cc4e30f4f580a2f3.pack | sort -k3 -n
chain length = 1: 1 object
chain length = 2: 1 object
pack-a8af65113ecbd080fb1996a9cc4e30f4f580a2f3.pack: ok
non delta: 7 objects
7ba2d2f7eeef87bafac4745906c7a5312f68cd86 blob   12 22 758 2 5c6457b17de03b5f47fb2353b80db051d595c46e
5c6457b17de03b5f47fb2353b80db051d595c46e blob   18 22 640 1 b3021059432503a2f1dbd069cc13c3afc37a6cb2
1f29f2105c227ab27d29cfa85b3773bbf3330908 tree   37 48 662
42107e671543d9ace63ab9265e34abaf31b051ba tree   37 48 710
e275285b34f49c17ebf234a873f37aeaace5ad45 tree   37 48 463
b3021059432503a2f1dbd069cc13c3afc37a6cb2 blob   133 129 511 # Aquí está el pass
a645bcc508c63f081234911d2f631f87cf469258 commit 194 137 326
14f754b3ba6531a2b89df6ccae6446e8969a41f3 commit 232 156 12
f08b9cc63fa1a4602fb065257633c2dae6e5651b commit 235 158 168

# Acceder al contenido de un tree
# git ls-tree <hash-tree>
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo/.git/objects/pack$ git ls-tree 42107e671543d9ace63ab9265e34abaf31b051ba
100644 blob 7ba2d2f7eeef87bafac4745906c7a5312f68cd86	README.md
# No encontramos nada relevante en los tree

# Acceder al contenido de un blob
# git show <hash-blob>
bandit28@bandit:/tmp/tmp.7wMuSspT90/repo/.git/objects/pack$ git show b3021059432503a2f1dbd069cc13c3afc37a6cb2
# Bandit Notes
Some notes for level29 of bandit.
## credentials
- username: bandit29
- password: tQKvmcwNYcFS6vmPHIUSI3ShmsrQZK8S
```

### Bandit 29

There is a git repository at `ssh://bandit29-git@localhost/home/bandit29-git/repo` via the port `2220`. The password for the user `bandit29-git` is the same as for the user `bandit29`.

Clone the repository and find the password for the next level.

```bash
# Creamos un directorio temporal
bandit29@bandit:~$ mktemp -d
/tmp/tmp.uAqSuX2b4y
bandit29@bandit:~$ cd /tmp/tmp.uAqSuX2b4y
bandit29@bandit:/tmp/tmp.uAqSuX2b4y$ git clone ssh://bandit29-git@localhost:2220/home/bandit29-git/repo
Cloning into 'repo'...
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

bandit29-git@localhost's password: 
remote: Enumerating objects: 16, done.
remote: Counting objects: 100% (16/16), done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 16 (delta 2), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (16/16), done.
Resolving deltas: 100% (2/2), done.
bandit29@bandit:/tmp/tmp.uAqSuX2b4y$ ls
repo
bandit29@bandit:/tmp/tmp.uAqSuX2b4y$ cd repo
bandit29@bandit:/tmp/tmp.uAqSuX2b4y/repo$ ls
README.md
bandit29@bandit:/tmp/tmp.uAqSuX2b4y/repo$ cat README.md 
# Bandit Notes
Some notes for bandit30 of bandit.
## credentials
- username: bandit30
- password: <no passwords in production!>

# Al igual que en el anterior nivel hay una carpeta .git oculta
bandit29@bandit:/tmp/tmp.uAqSuX2b4y/repo$ ls -la
total 16
drwxrwxr-x 3 bandit29 bandit29 4096 Oct 29 23:44 .
drwx------ 3 bandit29 bandit29 4096 Oct 29 23:44 ..
drwxrwxr-x 8 bandit29 bandit29 4096 Oct 29 23:44 .git # Carpeta oculta
-rw-rw-r-- 1 bandit29 bandit29  131 Oct 29 23:44 README.md
bandit29@bandit:/tmp/tmp.uAqSuX2b4y/repo$ cd .git
bandit29@bandit:/tmp/tmp.uAqSuX2b4y/repo/.git$ ls
branches  config  description  HEAD  hooks  index  info  logs  objects  packed-refs  refs
bandit29@bandit:/tmp/tmp.uAqSuX2b4y/repo/.git$ cd objects/
bandit29@bandit:/tmp/tmp.uAqSuX2b4y/repo/.git/objects$ ls
info  pack
bandit29@bandit:/tmp/tmp.uAqSuX2b4y/repo/.git/objects$ cd pack/
bandit29@bandit:/tmp/tmp.uAqSuX2b4y/repo/.git/objects/pack$ ls
pack-4d153e0bc1d6bbc4cadcf178df5ed91af05a8f2f.idx
pack-4d153e0bc1d6bbc4cadcf178df5ed91af05a8f2f.pack

# Verificamos el .pack
bandit29@bandit:/tmp/tmp.uAqSuX2b4y/repo/.git/objects/pack$ git verify-pack -v pack-4d153e0bc1d6bbc4cadcf178df5ed91af05a8f2f.pack
4364630b3b27c92aff7b36de7bb6ed2d30b60f88 commit 227 154 12
1d160de5f8f647f00634bbf3d49b9244275217b6 commit 250 169 166
07b750deb96fe4c903a3f93e41518adb3866f336 commit 268 187 335
fca34ddb7d1ff1f78df36538252aea650b0b040d commit 194 138 522
73d0f769233ffc2f59595412e22f41afc6218c04 commit 228 154 660
142b5e592d0aaf696b49d99d9a8427c8561e324b tree   37 48 814
a4b1cf1547e5efd9834d866a770095acb6b71635 blob   134 125 862 # Aquí está el pass
1af21d3f1b0e56e36ecec7175fb2a9fa9af0aeb6 blob   38 49 987 1 a4b1cf1547e5efd9834d866a770095acb6b71635
6208795cc5074c0f5160a3377083fdc7b3c70343 tree   68 78 1036
0c5f36d5895023c36035b7352c5b0113f6326550 tree   40 51 1114
8b137891791fe96927ad78e64b0aad7bded08bdc blob   1 10 1165
3d7503a65449fdbc36fa829d3faae16b644e9f69 tree   72 83 1175
7faa0cec7a6deda017a0ebe41d23b1c9fa3d1627 tree   37 48 1258
a9476df74c81524c8049b0a9ef122a5e78715b44 tree   37 48 1306
2da2f39a66514440bfb172c48508fbc6ab9569ff blob   12 23 1354 2 1af21d3f1b0e56e36ecec7175fb2a9fa9af0aeb6
4f5f3b22dd8480c80d8fffd956bc11046fa9b575 tree   68 78 1377
non delta: 14 objects
chain length = 1: 1 object
chain length = 2: 1 object
pack-4d153e0bc1d6bbc4cadcf178df5ed91af05a8f2f.pack: ok

# Accedemos al contenido de un blob
bandit29@bandit:/tmp/tmp.uAqSuX2b4y/repo/.git/objects/pack$ git show a4b1cf1547e5efd9834d866a770095acb6b71635
# Bandit Notes
Some notes for bandit30 of bandit.
## credentials
- username: bandit30
- password: xbhV3HpNGlTIdnjUrdAlPzc2L6y9EOnS
```

### Bandit 30

There is a git repository at `ssh://bandit30-git@localhost/home/bandit30-git/repo` via the port `2220`. The password for the user `bandit30-git` is the same as for the user `bandit30`.

Clone the repository and find the password for the next level.

```bash
bandit30@bandit:~$ mktemp -d
/tmp/tmp.LuHgAz3njQ
bandit30@bandit:~$ cd /tmp/tmp.LuHgAz3njQ
bandit30@bandit:/tmp/tmp.LuHgAz3njQ$ git clone ssh://bandit30-git@localhost:2220/home/bandit30-git/repo
Cloning into 'repo'...
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

bandit30-git@localhost's password: 
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Total 4 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (4/4), done.
bandit30@bandit:/tmp/tmp.LuHgAz3njQ$ ls
repo
bandit30@bandit:/tmp/tmp.LuHgAz3njQ$ cd repo
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo$ ls
README.md
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo$ cat README.md 
just an epmty file... muahaha

# Al igual que en los niveles anteriores hay una carpeta oculta
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo$ ls -la
total 16
drwxrwxr-x 3 bandit30 bandit30 4096 Oct 29 23:56 .
drwx------ 3 bandit30 bandit30 4096 Oct 29 23:56 ..
drwxrwxr-x 8 bandit30 bandit30 4096 Oct 29 23:56 .git
-rw-rw-r-- 1 bandit30 bandit30   30 Oct 29 23:56 README.md
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo$ cd .git
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo/.git$ ls
branches  config  description  HEAD  hooks  index  info  logs  objects  packed-refs  refs
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo/.git$ ls -la
total 52
drwxrwxr-x 8 bandit30 bandit30 4096 Oct 29 23:56 .
drwxrwxr-x 3 bandit30 bandit30 4096 Oct 29 23:56 ..
drwxrwxr-x 2 bandit30 bandit30 4096 Oct 29 23:56 branches
-rw-rw-r-- 1 bandit30 bandit30  281 Oct 29 23:56 config
-rw-rw-r-- 1 bandit30 bandit30   73 Oct 29 23:56 description
-rw-rw-r-- 1 bandit30 bandit30   23 Oct 29 23:56 HEAD
drwxrwxr-x 2 bandit30 bandit30 4096 Oct 29 23:56 hooks
-rw-rw-r-- 1 bandit30 bandit30  137 Oct 29 23:56 index
drwxrwxr-x 2 bandit30 bandit30 4096 Oct 29 23:56 info
drwxrwxr-x 3 bandit30 bandit30 4096 Oct 29 23:56 logs
drwxrwxr-x 4 bandit30 bandit30 4096 Oct 29 23:56 objects
-rw-rw-r-- 1 bandit30 bandit30  172 Oct 29 23:56 packed-refs
drwxrwxr-x 5 bandit30 bandit30 4096 Oct 29 23:56 refs

# En niveles anteriores siempre han estado los pass en objects
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo/.git$ cd objects/
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo/.git/objects$ ls
info  pack
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo/.git/objects$ cd pack
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo/.git/objects/pack$ ls
pack-5dd047e45dd131498476a052c2995fd1aae73453.idx
pack-5dd047e45dd131498476a052c2995fd1aae73453.pack
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo/.git/objects/pack$ git verify-pack -v pack-5dd047e45dd131498476a052c2995fd1aae73453.pack
d39631d73f786269b895ae9a7b14760cbf40a99f commit 194 138 12
831aac2e2341f009e40e46392a4f5dd318483019 blob   33 43 150 # Aquí está el pass
bd85592e905590f084b8df33363a46f9ac4aa708 tree   37 48 193
029ba421ef4c34205d52133f8da3d69bc1853777 blob   30 38 241
non delta: 4 objects
pack-5dd047e45dd131498476a052c2995fd1aae73453.pack: ok

# Encontramos el password en el blob
bandit30@bandit:/tmp/tmp.LuHgAz3njQ/repo/.git/objects/pack$ git show 831aac2e2341f009e40e46392a4f5dd318483019
OoffzGDlzhAlerFJ2cAiz1D41JW1Mhmt # Este es el password de bandit31
```

### Bandit 31

There is a git repository at `ssh://bandit31-git@localhost/home/bandit31-git/repo` via the port `2220`. The password for the user `bandit31-git` is the same as for the user `bandit31`.

Clone the repository and find the password for the next level.

```shell-session
# Creamos como siempre un directorio temporal
bandit31@bandit:~$ mktemp -d
/tmp/tmp.703FYu1tN7
bandit31@bandit:~$ cd /tmp/tmp.703FYu1tN7
bandit31@bandit:/tmp/tmp.703FYu1tN7$ git clone ssh://bandit31-git@localhost:2220/home/bandit31-git/repo
Cloning into 'repo'...
                        _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password: 
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 4 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (4/4), done.
bandit31@bandit:/tmp/tmp.703FYu1tN7$ ls
repo
bandit31@bandit:/tmp/tmp.703FYu1tN7$ cd repo
bandit31@bandit:/tmp/tmp.703FYu1tN7/repo$ ls
README.md
bandit31@bandit:/tmp/tmp.703FYu1tN7/repo$ cat README.md 
This time your task is to push a file to the remote repository.

Details:
    File name: key.txt
    Content: 'May I come in?'
    Branch: master
```

```shell-session
# Debemos enviar un archivo a un repositorio remoto

bandit31@bandit:/tmp/tmp.703FYu1tN7/repo$ echo 'May I come in?' > key.txt
bandit31@bandit:/tmp/tmp.703FYu1tN7/repo$ git add -f key.txt
bandit31@bandit:/tmp/tmp.703FYu1tN7/repo$ git commit -m "Add key.txt file"
[master 47fb29d] Add key.txt file
 1 file changed, 1 insertion(+)
 create mode 100644 key.txt
bandit31@bandit:/tmp/tmp.703FYu1tN7/repo$ git push origin master
                        _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password: 
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 2 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 329 bytes | 329.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
remote: ### Attempting to validate files... ####
remote: 
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote: 
remote: Well done! Here is the password for the next level:
remote: rmCBvG56y58BXzv98yZGdO7ATVL5dW8y 
```

### Bandit 32

After all this `git` stuff its time for another escape. Good luck!

```shell-session
# Al loguearnos entramos a una shell en mayúsculas, por lo que no funcionan los comandos

WELCOME TO THE UPPERCASE SHELL
>> ls
sh: 1: LS: Permission denied
>> cd ..
sh: 1: CD: Permission denied
>> sudo -l
sh: 1: SUDO: Permission denied
>> whoami
sh: 1: WHOAMI: Permission denied

# Para arreglarlo establecemos la variable $0
>> $0
$ ls
uppershell
$ pwd
/home/bandit32
$ cat /etc/bandit_pass/bandit33
odHo63fHiFqcWWJG9rLiLDtPm45KzUKy

```

### Bandit 33

**At this moment, level 34 does not exist yet.**

```shell-session
bandit33@bandit:~$ ls
README.txt
bandit33@bandit:~$ cat README.txt 
Congratulations on solving the last level of this game!

At this moment, there are no more levels to play in this game. However, we are constantly working
on new levels and will most likely expand this game with more levels soon.
Keep an eye out for an announcement on our usual communication channels!
In the meantime, you could play some of our other wargames.

If you have an idea for an awesome new level, please let us know!
```
