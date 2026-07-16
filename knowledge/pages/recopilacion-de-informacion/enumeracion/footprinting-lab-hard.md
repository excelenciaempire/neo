
# Footprinting Lab - Hard

## <mark style="color:purple;">Introducción</mark>

***

El tercer servidor es un servidor MX y de gestión para la red interna. Posteriormente, este servidor tiene la función de servidor de respaldo de las cuentas internas del dominio. En consecuencia, aquí también se creó un usuario llamado `HTB`, a cuyas credenciales debemos acceder.

***

## <mark style="color:purple;">Escaneo de puertos</mark>

```bash
sudo nmap -v -sV 10.129.187.203

PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
110/tcp open  pop3     Dovecot pop3d
143/tcp open  imap     Dovecot imapd (Ubuntu)
993/tcp open  ssl/imap Dovecot imapd (Ubuntu)
995/tcp open  ssl/pop3 Dovecot pop3d
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Vemos que se trata de una máquina Linux con varios puertos abiertos. Vamos a hacer un escaneo más exhaustivo:

```bash
sudo nmap -v -sV -sC 10.129.187.203 -p110,143,993,995

PORT    STATE SERVICE  VERSION
110/tcp open  pop3     Dovecot pop3d
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=NIXHARD
| Subject Alternative Name: DNS:NIXHARD
| Issuer: commonName=NIXHARD
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-11-10T01:30:25
| Not valid after:  2031-11-08T01:30:25
| MD5:   2b45:ec3c:508f:3cfb:9f6a:750c:63f8:2077
|_SHA-1: ed43:7d5a:3c46:54ac:9902:8dc4:9d86:6efb:2ae3:357c
143/tcp open  imap     Dovecot imapd (Ubuntu)
|_imap-capabilities: more have post-login STARTTLS IMAP4rev1 LOGIN-REFERRALS listed LITERAL+ IDLE ENABLE OK Pre-login ID SASL-IR capabilities AUTH=PLAINA0001
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=NIXHARD
| Subject Alternative Name: DNS:NIXHARD
| Issuer: commonName=NIXHARD
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-11-10T01:30:25
| Not valid after:  2031-11-08T01:30:25
| MD5:   2b45:ec3c:508f:3cfb:9f6a:750c:63f8:2077
|_SHA-1: ed43:7d5a:3c46:54ac:9902:8dc4:9d86:6efb:2ae3:357c
993/tcp open  ssl/imap Dovecot imapd (Ubuntu)
| ssl-cert: Subject: commonName=NIXHARD
| Subject Alternative Name: DNS:NIXHARD
| Issuer: commonName=NIXHARD
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-11-10T01:30:25
| Not valid after:  2031-11-08T01:30:25
| MD5:   2b45:ec3c:508f:3cfb:9f6a:750c:63f8:2077
|_SHA-1: ed43:7d5a:3c46:54ac:9902:8dc4:9d86:6efb:2ae3:357c
|_ssl-date: TLS randomness does not represent time
995/tcp open  ssl/pop3 Dovecot pop3d
| ssl-cert: Subject: commonName=NIXHARD
| Subject Alternative Name: DNS:NIXHARD
| Issuer: commonName=NIXHARD
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2021-11-10T01:30:25
| Not valid after:  2031-11-08T01:30:25
| MD5:   2b45:ec3c:508f:3cfb:9f6a:750c:63f8:2077
|_SHA-1: ed43:7d5a:3c46:54ac:9902:8dc4:9d86:6efb:2ae3:357c
|_ssl-date: TLS randomness does not represent time
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Encontramos un nombre común en todos los puertos: `NIXHARD`

Empezemos por el  `143`, el puerto `IMAP`. en el que en principio no encontramos ninguna credencial expuesta:

```bash
openssl s_client -connect 10.129.187.203:imaps

CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 CN = NIXHARD
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN = NIXHARD
verify return:1
---
Certificate chain
 0 s:CN = NIXHARD
   i:CN = NIXHARD
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
   v:NotBefore: Nov 10 01:30:25 2021 GMT; NotAfter: Nov  8 01:30:25 2031 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIC0zCCAbugAwIBAgIUC6tYfrtqQqCrhjYv11bUtaKet3EwDQYJKoZIhvcNAQEL
BQAwEjEQMA4GA1UEAwwHTklYSEFSRDAeFw0yMTExMTAwMTMwMjVaFw0zMTExMDgw
MTMwMjVaMBIxEDAOBgNVBAMMB05JWEhBUkQwggEiMA0GCSqGSIb3DQEBAQUAA4IB
DwAwggEKAoIBAQDEBpDfkH4Ro5ZXW44NvnF3N9lKz27V1hgRppyUk5y/SEPKt2zj
EU+r2tEHUeHoJHQZBbW0ybxh+X2H3ZPNEG9nV1GtFQfTBVcrUEpN5VV15aIbdh+q
j53pp/wcL/d8+Zg2ZAaVYWvQHVqtsAudQmynrV1MHA39A44fG3/SutKlurY8AKR0
MW5zMPtflMc/N3+lH8UUMBf2Q+zNSyZLiBEihxK3kfMW92HqWeh016egSIFuxUsH
kk4xpGmyG9NDYna47dQzoHCg+42KgqFvWrGw2nIccaEIX5XA8rU9u53C7EQzDzmQ
vAtHpKWBwNmiivxAz/QC7MPExWIWtZtOqxmfAgMBAAGjITAfMAkGA1UdEwQCMAAw
EgYDVR0RBAswCYIHTklYSEFSRDANBgkqhkiG9w0BAQsFAAOCAQEAG+Dm9pLJgNGC
X1YmznmtBUekhXMrU67tQl745fFasJQzIrDgVtK27fjAtQRwvIbDruSwTj47E7+O
XdS7qyjFNBerklWNq4fEAVI7BmkxnTS9542okA/+UmeG70LdKjzFS+LjjOnyWzTh
YwU8uUjLfnRca74kY0DkVHOIkwZQha0J+BrKSADq/zDjkG0g4v0vzHINOmHx9eiE
67NoJKJPY5S3RYWxl/4x8Kphx7PNJBPC75gYjlxxDhxdYu9a3daqJUa58/qOm6P8
w1P9nA6lkg7NopyqepulLAzIcqnTjb/nMD2Pd9b6vgWc3IqSfFreqjzshZ+FjNZo
zR+tR6z4TQ==
-----END CERTIFICATE-----
subject=CN = NIXHARD
issuer=CN = NIXHARD
---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: RSA-PSS
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 1283 bytes and written 503 bytes
Verification error: self-signed certificate
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 2048 bit
This TLS version forbids renegotiation.
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 18 (self-signed certificate)
---
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 4AAEE15B4D5E5DE908E7B49A27F18F76AFF6BFDA2CC28F594F93D40CF9075281
    Session-ID-ctx: 
    Resumption PSK: D5DBB4EE07D03DA763608DABBD857E9D17939F2C0288DA0E601990F72A20BA83387745DEE5460D69C21E9F61D60A449E
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 99 f9 0e 10 7b e9 11 33-8e 49 5f 9a 37 7b 0d ed   ....{..3.I_.7{..
    0010 - 21 7b 4b bf 11 a2 8b e1-3d 1c d7 53 49 7c 32 f4   !{K.....=..SI|2.
    0020 - 0f 7b 6c 8b 60 4d 2f a6-2e 37 3a ad d8 58 dc 32   .{l.`M/..7:..X.2
    0030 - 8e fe 84 f5 5b ba bf d9-00 3f 57 73 e9 4a 9a fa   ....[....?Ws.J..
    0040 - 17 62 c8 a1 95 96 05 c7-27 17 07 30 98 a4 d1 c6   .b......'..0....
    0050 - 4e 2f b8 69 f8 9a 3b 49-e8 75 e4 96 56 dd ab 27   N/.i..;I.u..V..'
    0060 - 81 67 67 28 ab 54 18 86-f6 bd 9a 75 d5 ff 66 df   .gg(.T.....u..f.
    0070 - b2 b2 c0 e5 61 ab f3 9a-84 1b 2e 6f 03 b3 da 1d   ....a......o....
    0080 - 31 c2 da 5f 1c db 4b 49-37 f1 12 93 42 86 6b 67   1.._..KI7...B.kg
    0090 - e0 40 17 56 4a 65 c1 0d-46 18 39 a5 31 10 a1 eb   .@.VJe..F.9.1...
    00a0 - 09 6c 2d b9 39 f2 45 e0-d0 2c cf 1b 26 8c f4 88   .l-.9.E..,..&...
    00b0 - f3 09 2f 76 2d d6 21 1a-92 cc 8d 2d 3f 3f 43 05   ../v-.!....-??C.

    Start Time: 1708090788
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 21A858355D7FD46595A61AFF333C316705D76BEC966A07349277455D4E721908
    Session-ID-ctx: 
    Resumption PSK: 3CC3C91A20BC734BB85AA760693471A77329
A9923F4C4187EC9935BF7821D1E74DAEF25E52487F731171557B106590DA
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 99 f9 0e 10 7b e9 11 33-8e 49 5f 9a 37 7b 0d ed   ....{..3.I_.7{..
    0010 - ed ad 05 93 a1 ec ee e6-61 bc f9 df f4 87 7b 2d   ........a.....{-
    0020 - e8 0b 68 6e fa 00 03 c2-f4 fb 35 55 2b 71 bf 14   ..hn......5U+q..
    0030 - 9e 18 fb 6a 86 c4 c3 8d-3a e8 a1 25 59 eb 93 78   ...j....:..%Y..x
    0040 - eb 7a 93 aa b9 af bb 0d-d4 c1 34 fd 82 8a c0 67   .z........4....g
    0050 - 8c 7e 69 b2 ae a0 26 f7-1d 6f 4c 5c 23 91 a3 bb   .~i...&..oL\#...
    0060 - 91 2f d6 99 45 bf 52 ba-26 16 a0 bc 84 67 8b d1   ./..E.R.&....g..
    0070 - a8 ab 3f 2b bc 7f 65 7c-8c 6d d3 2d 2c e4 b2 04   ..?+..e|.m.-,...
    0080 - ee f9 d3 d7 6e 38 21 ab-a6 79 ff 2d 2e 76 6b 4e   ....n8!..y.-.vkN
    0090 - 08 39 68 1f 24 fd 3d aa-5a f6 b0 57 e7 aa 27 b1   .9h.$.=.Z..W..'.
    00a0 - 82 0a bc 70 c3 7b 43 a7-10 2a 9d fa eb 3d f1 73   ...p.{C..*...=.s
    00b0 - 02 3d 94 69 27 6e 86 94-aa 5d 16 b0 c1 eb 89 04   .=.i'n...]......

    Start Time: 1708090788
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
* OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ AUTH=PLAIN] Dovecot (Ubuntu) ready.
```

Vamos a probar con el puerto `110 POP3`, a ver si encontramos algún dato relevante.

```bash
openssl s_client -connect 10.129.187.203:pop3s

CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 CN = NIXHARD
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN = NIXHARD
verify return:1
---
Certificate chain
 0 s:CN = NIXHARD
   i:CN = NIXHARD
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
   v:NotBefore: Nov 10 01:30:25 2021 GMT; NotAfter: Nov  8 01:30:25 2031 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIC0zCCAbugAwIBAgIUC6tYfrtqQqCrhjYv11bUtaKet3EwDQYJKoZIhvcNAQEL
BQAwEjEQMA4GA1UEAwwHTklYSEFSRDAeFw0yMTExMTAwMTMwMjVaFw0zMTExMDgw
MTMwMjVaMBIxEDAOBgNVBAMMB05JWEhBUkQwggEiMA0GCSqGSIb3DQEBAQUAA4IB
DwAwggEKAoIBAQDEBpDfkH4Ro5ZXW44NvnF3N9lKz27V1hgRppyUk5y/SEPKt2zj
EU+r2tEHUeHoJHQZBbW0ybxh+X2H3ZPNEG9nV1GtFQfTBVcrUEpN5VV15aIbdh+q
j53pp/wcL/d8+Zg2ZAaVYWvQHVqtsAudQmynrV1MHA39A44fG3/SutKlurY8AKR0
MW5zMPtflMc/N3+lH8UUMBf2Q+zNSyZLiBEihxK3kfMW92HqWeh016egSIFuxUsH
kk4xpGmyG9NDYna47dQzoHCg+42KgqFvWrGw2nIccaEIX5XA8rU9u53C7EQzDzmQ
vAtHpKWBwNmiivxAz/QC7MPExWIWtZtOqxmfAgMBAAGjITAfMAkGA1UdEwQCMAAw
EgYDVR0RBAswCYIHTklYSEFSRDANBgkqhkiG9w0BAQsFAAOCAQEAG+Dm9pLJgNGC
X1YmznmtBUekhXMrU67tQl745fFasJQzIrDgVtK27fjAtQRwvIbDruSwTj47E7+O
XdS7qyjFNBerklWNq4fEAVI7BmkxnTS9542okA/+UmeG70LdKjzFS+LjjOnyWzTh
YwU8uUjLfnRca74kY0DkVHOIkwZQha0J+BrKSADq/zDjkG0g4v0vzHINOmHx9eiE
67NoJKJPY5S3RYWxl/4x8Kphx7PNJBPC75gYjlxxDhxdYu9a3daqJUa58/qOm6P8
w1P9nA6lkg7NopyqepulLAzIcqnTjb/nMD2Pd9b6vgWc3IqSfFreqjzshZ+FjNZo
zR+tR6z4TQ==
-----END CERTIFICATE-----
subject=CN = NIXHARD
issuer=CN = NIXHARD
---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: RSA-PSS
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 1283 bytes and written 503 bytes
Verification error: self-signed certificate
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 2048 bit
This TLS version forbids renegotiation.
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 18 (self-signed certificate)
---
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 972397ECD580ED6AFF372C507095014D5D08F0524F9ED84D1CF8B2EEA350D56E
    Session-ID-ctx: 
    Resumption PSK: 8E7098D52D90A4DEF18FEA78DC74BDB729BF232752CABD07C14F366B3B37DFE875A177ACC49123BADCF94CCB48D45EB4
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - ec cb 32 8e 06 ec ec 99-5a 6c 7f d1 5d b9 28 b2   ..2.....Zl..].(.
    0010 - ac 4a de 60 e3 88 6a ff-9c cd 51 a5 0e 7d 03 d8   .J.`..j...Q..}..
    0020 - e8 69 42 f1 83 75 8b 41-74 b6 09 b2 64 1c 74 b9   .iB..u.At...d.t.
    0030 - 85 67 14 d9 f9 42 7b b9-61 8e 10 44 bd 93 7e d9   .g...B{.a..D..~.
    0040 - e1 7a 9c 66 2a b4 ca dc-1a 59 ab 7f 02 31 d8 b4   .z.f*....Y...1..
    0050 - 75 2e 45 68 cd b9 c7 c8-6f fc aa 93 da 1b 5c 47   u.Eh....o.....\G
    0060 - 5e bb 15 58 f8 3b 45 00-af e0 94 29 7a 6c 3f 87   ^..X.;E....)zl?.
    0070 - 11 37 29 70 68 76 52 7d-ab c6 97 c0 73 2a 74 e5   .7)phvR}....s*t.
    0080 - 8b ee aa ef dc cc 89 99-fb d0 69 45 3e 54 31 3d   ..........iE>T1=
    0090 - 10 7f ba b6 81 e4 fb 17-07 c3 86 bb 5b bd 4f 6a   ............[.Oj
    00a0 - bd 8e 66 60 be ab 18 c3-e4 0b 6a b0 b2 f6 39 9b   ..f`......j...9.
    00b0 - 36 32 4a bc 4c 92 fd 37-1f b9 a4 e9 d6 bb 6a 00   62J.L..7......j.

    Start Time: 1708091021
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
    Protocol  : TLSv1.3
    Cipher    : TLS_AES_256_GCM_SHA384
    Session-ID: 67FA3BEC9DF184E5B6EBC055065EB044F38DC7E6ECD68E7127B30CBA7C708185
    Session-ID-ctx: 
    Resumption PSK: 2BEF419221BDC15F8A58F8C9FFE1701054449172F85C2CA6EB1E791A74EDA2CD51DC5013477C705BECEEAD2A1CE3022E
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - ec cb 32 8e 06 ec ec 99-5a 6c 7f d1 5d b9 28 b2   ..2.....Zl..].(.
    0010 - ab 3d 96 ca 9b a8 22 7b-e1 ba 89 51 2b c1 ab 5d   .=...."{...Q+..]
    0020 - 93 65 91 d7 e6 b0 c9 38-d2 18 1d 9e 37 12 ed f4   .e.....8....7...
    0030 - 7b 6f 15 fa b6 02 4b c9-fa 3d e2 e6 23 30 a4 dd   {o....K..=..#0..
    0040 - c5 b1 cd 6a 05 d5 e1 73-3e 7c 35 d3 04 87 f9 cd   ...j...s>|5.....
    0050 - f7 c3 d7 39 e8 19 ae 37-ca 6f 76 95 13 9f fe e5   ...9...7.ov.....
    0060 - 95 d6 be 5d d2 94 e5 b1-92 8d 68 62 a6 a3 b1 81   ...]......hb....
    0070 - 39 6a 3c df 07 13 c7 a6-91 7d 8b 5c ca 76 a8 d0   9j<......}.\.v..
    0080 - e8 03 90 cd c9 8b dd 8f-f0 9c e8 63 98 4a ae ab   ...........c.J..
    0090 - 60 1d 2b cf c2 f7 73 96-51 e4 b3 36 0d 5d d3 a3   `.+...s.Q..6.]..
    00a0 - e7 e5 06 46 7b d6 68 8e-c1 37 9c 31 c1 32 a5 02   ...F{.h..7.1.2..
    00b0 - d9 cf 8d aa 8f 2c 5b e1-a7 9c 83 6b 36 43 6b 0a   .....,[....k6Ck.

    Start Time: 1708091021
    Timeout   : 7200 (sec)
    Verify return code: 18 (self-signed certificate)
    Extended master secret: no
    Max Early Data: 0
---
read R BLOCK
+OK Dovecot (Ubuntu) ready.
```

Tampoco encontramos nada relevante expuesto, por lo que vamos a probar otras técnicas para obtener las credenciales de acceso.

## <mark style="color:purple;">SMTP</mark>

{% content-ref url="/pages/o3lTcldCu7rwocSYG66V" %}
[SMTP](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion/smtp.md)
{% endcontent-ref %}

Al ejecutar `onesistyone` contra la máquina nos da la Community String `backup`, que nos servirá para ejecutar otras herramientas:

```bash
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt 10.129.187.203

Scanning 1 hosts, 3219 communities
10.129.251.193 [backup] Linux NIXHARD 5.4.0-90-generic #101-Ubuntu SMP Fri Oct 15 20:00:55 UTC 2021 x86_64
```

Con esta información vamos a ejecutar [`snpwalk`](/ethical-hacking-cheatsheet/recopilacion-de-informacion/enumeracion/snmp.md) de la siguiente manera:

```bash
snmpwalk -v2c -c backup 10.129.187.203    
                         
iso.3.6.1.2.1.1.1.0 = STRING: "Linux NIXHARD 5.4.0-90-generic #101-Ubuntu SMP Fri Oct 15 20:00:55 UTC 2021 x86_64"
iso.3.6.1.2.1.1.2.0 = OID: iso.3.6.1.4.1.8072.3.2.10
iso.3.6.1.2.1.1.3.0 = Timeticks: (182183) 0:30:21.83
iso.3.6.1.2.1.1.4.0 = STRING: "Admin <tech@inlanefreight.htb>"
iso.3.6.1.2.1.1.5.0 = STRING: "NIXHARD"
iso.3.6.1.2.1.1.6.0 = STRING: "Inlanefreight"
iso.3.6.1.2.1.1.7.0 = INTEGER: 72
iso.3.6.1.2.1.1.8.0 = Timeticks: (11) 0:00:00.11
iso.3.6.1.2.1.1.9.1.2.1 = OID: iso.3.6.1.6.3.10.3.1.1
iso.3.6.1.2.1.1.9.1.2.2 = OID: iso.3.6.1.6.3.11.3.1.1
iso.3.6.1.2.1.1.9.1.2.3 = OID: iso.3.6.1.6.3.15.2.1.1
iso.3.6.1.2.1.1.9.1.2.4 = OID: iso.3.6.1.6.3.1
iso.3.6.1.2.1.1.9.1.2.5 = OID: iso.3.6.1.6.3.16.2.2.1
iso.3.6.1.2.1.1.9.1.2.6 = OID: iso.3.6.1.2.1.49
iso.3.6.1.2.1.1.9.1.2.7 = OID: iso.3.6.1.2.1.4
iso.3.6.1.2.1.1.9.1.2.8 = OID: iso.3.6.1.2.1.50
iso.3.6.1.2.1.1.9.1.2.9 = OID: iso.3.6.1.6.3.13.3.1.3
iso.3.6.1.2.1.1.9.1.2.10 = OID: iso.3.6.1.2.1.92
iso.3.6.1.2.1.1.9.1.3.1 = STRING: "The SNMP Management Architecture MIB."
iso.3.6.1.2.1.1.9.1.3.2 = STRING: "The MIB for Message Processing and Dispatching."
iso.3.6.1.2.1.1.9.1.3.3 = STRING: "The management information definitions for the SNMP User-based Security Model."
iso.3.6.1.2.1.1.9.1.3.4 = STRING: "The MIB module for SNMPv2 entities"
iso.3.6.1.2.1.1.9.1.3.5 = STRING: "View-based Access Control Model for SNMP."
iso.3.6.1.2.1.1.9.1.3.6 = STRING: "The MIB module for managing TCP implementations"
iso.3.6.1.2.1.1.9.1.3.7 = STRING: "The MIB module for managing IP and ICMP implementations"
iso.3.6.1.2.1.1.9.1.3.8 = STRING: "The MIB module for managing UDP implementations"
iso.3.6.1.2.1.1.9.1.3.9 = STRING: "The MIB modules for managing SNMP Notification, plus filtering."
iso.3.6.1.2.1.1.9.1.3.10 = STRING: "The MIB module for logging SNMP Notifications."
iso.3.6.1.2.1.1.9.1.4.1 = Timeticks: (11) 0:00:00.11
iso.3.6.1.2.1.1.9.1.4.2 = Timeticks: (11) 0:00:00.11
iso.3.6.1.2.1.1.9.1.4.3 = Timeticks: (11) 0:00:00.11
iso.3.6.1.2.1.1.9.1.4.4 = Timeticks: (11) 0:00:00.11
iso.3.6.1.2.1.1.9.1.4.5 = Timeticks: (11) 0:00:00.11
iso.3.6.1.2.1.1.9.1.4.6 = Timeticks: (11) 0:00:00.11
iso.3.6.1.2.1.1.9.1.4.7 = Timeticks: (11) 0:00:00.11
iso.3.6.1.2.1.1.9.1.4.8 = Timeticks: (11) 0:00:00.11
iso.3.6.1.2.1.1.9.1.4.9 = Timeticks: (11) 0:00:00.11
iso.3.6.1.2.1.1.9.1.4.10 = Timeticks: (11) 0:00:00.11
iso.3.6.1.2.1.25.1.1.0 = Timeticks: (183195) 0:30:31.95
iso.3.6.1.2.1.25.1.2.0 = Hex-STRING: 07 E8 02 10 0E 03 0C 00 2B 00 00 
iso.3.6.1.2.1.25.1.3.0 = INTEGER: 393216
iso.3.6.1.2.1.25.1.4.0 = STRING: "BOOT_IMAGE=/vmlinuz-5.4.0-90-generic root=/dev/mapper/ubuntu--vg-ubuntu--lv ro ipv6.disable=1 maybe-ubiquity
"
iso.3.6.1.2.1.25.1.5.0 = Gauge32: 0
iso.3.6.1.2.1.25.1.6.0 = Gauge32: 159
iso.3.6.1.2.1.25.1.7.0 = INTEGER: 0
iso.3.6.1.2.1.25.1.7.1.1.0 = INTEGER: 1
iso.3.6.1.2.1.25.1.7.1.2.1.2.6.66.65.67.75.85.80 = STRING: "/opt/tom-recovery.sh"
iso.3.6.1.2.1.25.1.7.1.2.1.3.6.66.65.67.75.85.80 = STRING: "tom NMds732Js2761"
iso.3.6.1.2.1.25.1.7.1.2.1.4.6.66.65.67.75.85.80 = ""
iso.3.6.1.2.1.25.1.7.1.2.1.5.6.66.65.67.75.85.80 = INTEGER: 5
iso.3.6.1.2.1.25.1.7.1.2.1.6.6.66.65.67.75.85.80 = INTEGER: 1
iso.3.6.1.2.1.25.1.7.1.2.1.7.6.66.65.67.75.85.80 = INTEGER: 1
iso.3.6.1.2.1.25.1.7.1.2.1.20.6.66.65.67.75.85.80 = INTEGER: 4
iso.3.6.1.2.1.25.1.7.1.2.1.21.6.66.65.67.75.85.80 = INTEGER: 1
iso.3.6.1.2.1.25.1.7.1.3.1.1.6.66.65.67.75.85.80 = STRING: "chpasswd: (user tom) pam_chauthtok() failed, error:"
iso.3.6.1.2.1.25.1.7.1.3.1.2.6.66.65.67.75.85.80 = STRING: "chpasswd: (user tom) pam_chauthtok() failed, error:
Authentication token manipulation error
chpasswd: (line 1, user tom) password not changed
Changing password for tom."
iso.3.6.1.2.1.25.1.7.1.3.1.3.6.66.65.67.75.85.80 = INTEGER: 4
iso.3.6.1.2.1.25.1.7.1.3.1.4.6.66.65.67.75.85.80 = INTEGER: 1
iso.3.6.1.2.1.25.1.7.1.4.1.2.6.66.65.67.75.85.80.1 = STRING: "chpasswd: (user tom) pam_chauthtok() failed, error:"
iso.3.6.1.2.1.25.1.7.1.4.1.2.6.66.65.67.75.85.80.2 = STRING: "Authentication token manipulation error"
iso.3.6.1.2.1.25.1.7.1.4.1.2.6.66.65.67.75.85.80.3 = STRING: "chpasswd: (line 1, user tom) password not changed"
iso.3.6.1.2.1.25.1.7.1.4.1.2.6.66.65.67.75.85.80.4 = STRING: "Changing password for tom."
iso.3.6.1.2.1.25.1.7.1.4.1.2.6.66.65.67.75.85.80.4 = No more variables left in this MIB View (It is past the end of the MIB tree)
```

Con esto obtenemos varios datos relevantes:

```bash
Admin:   "Admin <tech@inlanefreight.htb>"
Nombre:  "NIXHARD"
Empresa: "Inlanefreight"
Dominio: "inlanefreight.htb"
```

También obtenemos las posibles credenciales del usuario `tom`:

```bash
User: "tom" 
Pass: "NMds732Js2761"
```

Lo primero de todo vamos a añadir el `dominio` a nuestro `/etc/hosts`

## <mark style="color:purple;">Conexión por IMAP</mark>

```bash
openssl s_client -connect 10.129.187.203:imaps

CONNECTED(00000003)
Can't use SSL_get_servername
depth=0 CN = NIXHARD
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN = NIXHARD
verify return:1
---
Certificate chain
 0 s:CN = NIXHARD
   i:CN = NIXHARD
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
   v:NotBefore: Nov 10 01:30:25 2021 GMT; NotAfter: Nov  8 01:30:25 2031 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIC0zCCAbugAwIBAgIUC6tYfrtqQqCrhjYv11bUtaKet3EwDQYJKoZIhvcNAQEL
BQAwEjEQMA4GA1UEAwwHTklYSEFSRDAeFw0yMTExMTAwMTMwMjVaFw0zMTExMDgw
MTMwMjVaMBIxEDAOBgNVBAMMB05JWEhBUkQwggEiMA0GCSqGSIb3DQEBAQUAA4IB
DwAwggEKAoIBAQDEBpDfkH4Ro5ZXW44NvnF3N9lKz27V1hgRppyUk5y/SEPKt2zj
EU+r2tEHUeHoJHQZBbW0ybxh+X2H3ZPNEG9nV1GtFQfTBVcrUEpN5VV15aIbdh+q
j53pp/wcL/d8+Zg2ZAaVYWvQHVqtsAudQmynrV1MHA39A44fG3/SutKlurY8AKR0
MW5zMPtflMc/N3+lH8UUMBf2Q+zNSyZLiBEihxK3kfMW92HqWeh016egSIFuxUsH
kk4xpGmyG9NDYna47dQzoHCg+42KgqFvWrGw2nIccaEIX5XA8rU9u53C7EQzDzmQ
vAtHpKWBwNmiivxAz/QC7MPExWIWtZtOqxmfAgMBAAGjITAfMAkGA1UdEwQCMAAw
EgYDVR0RBAswCYIHTklYSEFSRDANBgkqhkiG9w0BAQsFAAOCAQEAG+Dm9pLJgNGC
X1YmznmtBUekhXMrU67tQl745fFasJQzIrDgVtK27fjAtQRwvIbDruSwTj47E7+O
XdS7qyjFNBerklWNq4fEAVI7BmkxnTS9542okA/+UmeG70LdKjzFS+LjjOnyWzTh
YwU8uUjLfnRca74kY0DkVHOIkwZQha0J+BrKSADq/zDjkG0g4v0vzHINOmHx9eiE
67NoJKJPY5S3RYWxl/4x8Kphx7PNJBPC75gYjlxxDhxdYu9a3daqJUa58/qOm6P8
w1P9nA6lkg7NopyqepulLAzIcqnTjb/nMD2Pd9b6vgWc3IqSfFreqjzshZ+FjNZo
zR+tR6z4TQ==
-----END CERTIFICATE-----
subject=CN = NIXHARD
issuer=CN = NIXHARD
---
<-----------SNIP----------->
---
read R BLOCK
* OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ AUTH=PLAIN] Dovecot (Ubuntu) ready.

# Aquí nos vamos a loguear con las credenciales que encontramos
```

{% code overflow="wrap" %}

```bash
# Login
1 LOGIN tom NMds732Js2761
1 OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE SORT SORT=DISPLAY THREAD=REFERENCES THREAD=REFS THREAD=ORDEREDSUBJECT MULTIAPPEND URL-PARTIAL CATENATE UNSELECT CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 CONDSTORE QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS BINARY MOVE SNIPPET=FUZZY PREVIEW=FUZZY LITERAL+ NOTIFY SPECIAL-USE] Logged in

# Listado de buzones
1 LIST "" *
* LIST (\HasNoChildren) "." Notes
* LIST (\HasNoChildren) "." Meetings
* LIST (\HasNoChildren \UnMarked) "." Important
* LIST (\HasNoChildren) "." INBOX
1 OK List completed (0.005 + 0.000 + 0.004 secs).
```

{% endcode %}

Tenemos 4 buzones a los que podemos acceder para ver los emails: `Notes`, `Meetings`, `Important` y `INBOX`. Enumerando cada uno en particular, solamente nos encontramos email en el buzón `INBOX`:

{% code overflow="wrap" %}

```bash
# Seleccionamos el buzon INBOX
1 SELECT INBOX
* OK [CLOSED] Previous mailbox closed.
* FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
* OK [PERMANENTFLAGS (\Answered \Flagged \Deleted \Seen \Draft \*)] Flags permitted.
* 1 EXISTS
* 0 RECENT
* OK [UIDVALIDITY 1636509064] UIDs valid
* OK [UIDNEXT 2] Predicted next UID
1 OK [READ-WRITE] Select completed (0.003 + 0.000 + 0.002 secs).

# Vemos todos los emails del buzon
1 FETCH 1 ALL
* 1 FETCH (FLAGS (\Seen) INTERNALDATE "10-Nov-2021 01:44:26 +0000" RFC822.SIZE 3661 ENVELOPE ("Wed, 10 Nov 2010 14:21:26 +0200" "KEY" ((NIL NIL "MISSING_MAILBOX" "MISSING_DOMAIN")) ((NIL NIL "MISSING_MAILBOX" "MISSING_DOMAIN")) ((NIL NIL "MISSING_MAILBOX" "MISSING_DOMAIN")) ((NIL NIL "tom" "inlanefreight.htb")) NIL NIL NIL NIL))
1 OK Fetch completed (0.003 + 0.000 + 0.002 secs).

# Accedemos al contenido del email
1 FETCH 1 BODY[]
* 1 FETCH (BODY[] {3661}
HELO dev.inlanefreight.htb
MAIL FROM:<tech@dev.inlanefreight.htb>
RCPT TO:<bob@inlanefreight.htb>
DATA
From: [Admin] <tech@inlanefreight.htb>
To: <tom@inlanefreight.htb>
Date: Wed, 10 Nov 2010 14:21:26 +0200
Subject: KEY

-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAACFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAgEA9snuYvJaB/QOnkaAs92nyBKypu73HMxyU9XWTS+UBbY3lVFH0t+F
+yuX+57Wo48pORqVAuMINrqxjxEPA7XMPR9XIsa60APplOSiQQqYreqEj6pjTj8wguR0Sd
hfKDOZwIQ1ILHecgJAA0zY2NwWmX5zVDDeIckjibxjrTvx7PHFdND3urVhelyuQ89BtJqB
abmrB5zzmaltTK0VuAxR/SFcVaTJNXd5Utw9SUk4/l0imjP3/ong1nlguuJGc1s47tqKBP
HuJKqn5r6am5xgX5k4ct7VQOQbRJwaiQVA5iShrwZxX5wBnZISazgCz/D6IdVMXilAUFKQ
X1thi32f3jkylCb/DBzGRROCMgiD5Al+uccy9cm9aS6RLPt06OqMb9StNGOnkqY8rIHPga
H/RjqDTSJbNab3w+CShlb+H/p9cWGxhIrII+lBTcpCUAIBbPtbDFv9M3j0SjsMTr2Q0B0O
jKENcSKSq1E1m8FDHqgpSY5zzyRi7V/WZxCXbv8lCgk5GWTNmpNrS7qSjxO0N143zMRDZy
Ex74aYCx3aFIaIGFXT/EedRQ5l0cy7xVyM4wIIA+XlKR75kZpAVj6YYkMDtL86RN6o8u1x
3txZv15lMtfG4jzztGwnVQiGscG0CWuUA+E1pGlBwfaswlomVeoYK9OJJ3hJeJ7SpCt2GG
cAAAdIRrOunEazrpwAAAAHc3NoLXJzYQAAAgEA9snuYvJaB/QOnkaAs92nyBKypu73HMxy
U9XWTS+UBbY3lVFH0t+F+yuX+57Wo48pORqVAuMINrqxjxEPA7XMPR9XIsa60APplOSiQQ
qYreqEj6pjTj8wguR0SdhfKDOZwIQ1ILHecgJAA0zY2NwWmX5zVDDeIckjibxjrTvx7PHF
dND3urVhelyuQ89BtJqBabmrB5zzmaltTK0VuAxR/SFcVaTJNXd5Utw9SUk4/l0imjP3/o
ng1nlguuJGc1s47tqKBPHuJKqn5r6am5xgX5k4ct7VQOQbRJwaiQVA5iShrwZxX5wBnZIS
azgCz/D6IdVMXilAUFKQX1thi32f3jkylCb/DBzGRROCMgiD5Al+uccy9cm9aS6RLPt06O
qMb9StNGOnkqY8rIHPgaH/RjqDTSJbNab3w+CShlb+H/p9cWGxhIrII+lBTcpCUAIBbPtb
DFv9M3j0SjsMTr2Q0B0OjKENcSKSq1E1m8FDHqgpSY5zzyRi7V/WZxCXbv8lCgk5GWTNmp
NrS7qSjxO0N143zMRDZyEx74aYCx3aFIaIGFXT/EedRQ5l0cy7xVyM4wIIA+XlKR75kZpA
Vj6YYkMDtL86RN6o8u1x3txZv15lMtfG4jzztGwnVQiGscG0CWuUA+E1pGlBwfaswlomVe
oYK9OJJ3hJeJ7SpCt2GGcAAAADAQABAAACAQC0wxW0LfWZ676lWdi9ZjaVynRG57PiyTFY
jMFqSdYvFNfDrARixcx6O+UXrbFjneHA7OKGecqzY63Yr9MCka+meYU2eL+uy57Uq17ZKy
zH/oXYQSJ51rjutu0ihbS1Wo5cv7m2V/IqKdG/WRNgTFzVUxSgbybVMmGwamfMJKNAPZq2
xLUfcemTWb1e97kV0zHFQfSvH9wiCkJ/rivBYmzPbxcVuByU6Azaj2zoeBSh45ALyNL2Aw
HHtqIOYNzfc8rQ0QvVMWuQOdu/nI7cOf8xJqZ9JRCodiwu5fRdtpZhvCUdcSerszZPtwV8
uUr+CnD8RSKpuadc7gzHe8SICp0EFUDX5g4Fa5HqbaInLt3IUFuXW4SHsBPzHqrwhsem8z
tjtgYVDcJR1FEpLfXFOC0eVcu9WiJbDJEIgQJNq3aazd3Ykv8+yOcAcLgp8x7QP+s+Drs6
4/6iYCbWbsNA5ATTFz2K5GswRGsWxh0cKhhpl7z11VWBHrfIFv6z0KEXZ/AXkg9x2w9btc
dr3ASyox5AAJdYwkzPxTjtDQcN5tKVdjR1LRZXZX/IZSrK5+Or8oaBgpG47L7okiw32SSQ
5p8oskhY/He6uDNTS5cpLclcfL5SXH6TZyJxrwtr0FHTlQGAqpBn+Lc3vxrb6nbpx49MPt
DGiG8xK59HAA/c222dwQAAAQEA5vtA9vxS5n16PBE8rEAVgP+QEiPFcUGyawA6gIQGY1It
4SslwwVM8OJlpWdAmF8JqKSDg5tglvGtx4YYFwlKYm9CiaUyu7fqadmncSiQTEkTYvRQcy
tCVFGW0EqxfH7ycA5zC5KGA9pSyTxn4w9hexp6wqVVdlLoJvzlNxuqKnhbxa7ia8vYp/hp
6EWh72gWLtAzNyo6bk2YykiSUQIfHPlcL6oCAHZblZ06Usls2ZMObGh1H/7gvurlnFaJVn
CHcOWIsOeQiykVV/l5oKW1RlZdshBkBXE1KS0rfRLLkrOz+73i9nSPRvZT4xQ5tDIBBXSN
y4HXDjeoV2GJruL7qAAAAQEA/XiMw8fvw6MqfsFdExI6FCDLAMnuFZycMSQjmTWIMP3cNA
2qekJF44lL3ov+etmkGDiaWI5XjUbl1ZmMZB1G8/vk8Y9ysZeIN5DvOIv46c9t55pyIl5+
fWHo7g0DzOw0Z9ccM0lr60hRTm8Gr/Uv4TgpChU1cnZbo2TNld3SgVwUJFxxa//LkX8HGD
vf2Z8wDY4Y0QRCFnHtUUwSPiS9GVKfQFb6wM+IAcQv5c1MAJlufy0nS0pyDbxlPsc9HEe8
EXS1EDnXGjx1EQ5SJhmDmO1rL1Ien1fVnnibuiclAoqCJwcNnw/qRv3ksq0gF5lZsb3aFu
kHJpu34GKUVLy74QAAAQEA+UBQH/jO319NgMG5NKq53bXSc23suIIqDYajrJ7h9Gef7w0o
eogDuMKRjSdDMG9vGlm982/B/DWp/Lqpdt+59UsBceN7mH21+2CKn6NTeuwpL8lRjnGgCS
t4rWzFOWhw1IitEg29d8fPNTBuIVktJU/M/BaXfyNyZo0y5boTOELoU3aDfdGIQ7iEwth5
vOVZ1VyxSnhcsREMJNE2U6ETGJMY25MSQytrI9sH93tqWz1CIUEkBV3XsbcjjPSrPGShV/
H+alMnPR1boleRUIge8MtQwoC4pFLtMHRWw6yru3tkRbPBtNPDAZjkwF1zXqUBkC0x5c7y
XvSb8cNlUIWdRwAAAAt0b21ATklYSEFSRAECAwQFBg==
-----END OPENSSH PRIVATE KEY-----
)
1 OK Fetch completed (0.001 + 0.000 secs).
```

{% endcode %}

## <mark style="color:purple;">Conexión por SSH con ID\_RSA</mark>

Bingo, obtenemos una clave privada `ID_RSA` para conectarnos por SSH sin contraseña. Nos vamos a guardar la clave en un archivo `id_rsa` y nos vamos a conectar:

```bash
ssh -i id_rsa tom@10.129.187.203

The authenticity of host '10.129.187.203 (10.129.187.203)' can't be established.
ED25519 key fingerprint is SHA256:AtNYHXCA7dVpi58LB+uuPe9xvc2lJwA6y7q82kZoBNM.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:12: [hashed name]
    ~/.ssh/known_hosts:14: [hashed name]
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.102.155' (ED25519) to the list of known hosts.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for 'id_rsa' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "id_rsa": bad permissions
tom@10.129.102.155: Permission denied (publickey).
```

Al conectarnos nos da un error de que los permisos son demasiado amplios, asi que vamos a reducirlos con chmod:

```bash
chmod 600 id_rsa 

ssh -i id_rsa tom@10.129.187.203

Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-90-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Fri 16 Feb 2024 04:06:37 PM UTC

  System load:  0.0               Processes:               183
  Usage of /:   66.4% of 5.70GB   Users logged in:         0
  Memory usage: 31%               IPv4 address for ens192: 10.129.102.155
  Swap usage:   0%

 * Super-optimized for small spaces - read how we shrank the memory
   footprint of MicroK8s to make it the smallest full K8s around.

   https://ubuntu.com/blog/microk8s-memory-optimisation

0 updates can be applied immediately.

The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Wed Nov 10 02:51:52 2021 from 10.10.14.20
tom@NIXHARD:~$
```

Accedemos correctamente por SSH! Ahora vamos a buscar la información que necesitamos. Recordemos que debemos acceder a las credenciales del usuario `HTB`.

{% code overflow="wrap" %}

```bash
tom@NIXHARD:~$ ls
mail  Maildir
tom@NIXHARD:~$ cd mail/
tom@NIXHARD:~/mail$ la
.imap
tom@NIXHARD:~/mail$ cd .imap
tom@NIXHARD:~/mail/.imap$ ls
dovecot.list.index.log  dovecot-uidvalidity  dovecot-uidvalidity.618b21ea  Important  key  Meetings  TESTING
```

{% endcode %}

Parece que en las carpetas de `email` y `Maildir` no hay nada relevante. Vamos a ver los usuarios humanos presentes en el sistema:

```bash
tom@NIXHARD:~$ awk -F: '$3 >= 1000 && $3 < 65534 {print $1}' /etc/passwd
ubuntu
cry0l1t3
tom
```

Solo hay 3 usuarios en el sistema y ninguno es `HTB`, por lo que tendremos que buscar información dentro del sistema. Dentro de la carpeta tom encontramos varios archivos ocultos que podrían darnos alguna pista de donde encontrar esta información:

```bash
tom@NIXHARD:~$ ls -la
total 48
drwxr-xr-x 6 tom  tom  4096 Nov 10  2021 .
drwxr-xr-x 5 root root 4096 Nov 10  2021 ..
-rw------- 1 tom  tom   577 Feb 19 14:07 .bash_history
-rw-r--r-- 1 tom  tom   220 Nov 10  2021 .bash_logout
-rw-r--r-- 1 tom  tom  3771 Nov 10  2021 .bashrc
drwx------ 2 tom  tom  4096 Nov 10  2021 .cache
drwx------ 3 tom  tom  4096 Nov 10  2021 mail
drwx------ 8 tom  tom  4096 Nov 10  2021 Maildir
-rw------- 1 tom  tom   169 Nov 10  2021 .mysql_history
-rw-r--r-- 1 tom  tom   807 Nov 10  2021 .profile
drwx------ 2 tom  tom  4096 Nov 10  2021 .ssh
-rw------- 1 tom  tom  2018 Nov 10  2021 .viminfo
```

El archivo `.bash_history` contiene información que nos podría ser útil, ya que contiene comandos que otros usuarios han utilizado en el sistema:

```bash
tom@NIXHARD:~$ cat .bash_history 
mysql -u tom -p
ssh-keygen -t rsa -b 4096
ls
ls -al
cd .ssh/
ls
cd mail/
ls
ls -al
cd .imap/
ls
cd Important/
ls
set term=xterm
vim key
cat ~/.ssh/id_rsa
vim key
ls
mv key ..
cd ..
ls
mv key Important/
mv Important/key ../
cd ..
ls
ls -l
id
cat /etc/passwd
ls
cd mail/
ls
ls -al
cd mail/
ls
rm Meetings 
rm TESTING Important 
ls -l
cd ..
ls -al
mv mail/key Maildir/.Important/new/
mv Maildir/.Important/new/key Maildir/new/
cd Maildir/new/
ls
cd ..
tree .
cat cur/key
cd cur/
ls
ls -al
cat "key:2,"
mysql -u tom -p 
mysql -u tom -p
```

Vemos que en los comandos que han ejecutado anteriormente, acceden a `mysql` desde dentro del servidor SSH, utilizando las credenciales que ya obtuvimos de tom, por lo que vamos a probar eso.

## <mark style="color:purple;">Acceso por MySQL</mark>

```bash
tom@NIXHARD:~$ mysql -u tom -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.27-0ubuntu0.20.04.1 (Ubuntu)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

No entry for terminal type "xterm-kitty";
using dumb terminal settings.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| users              |
+--------------------+
5 rows in set (0.01 sec)

mysql> 
```

Efectivamente, accedemos a la base de datos correctamente y empezamos a enumerar información sobre los usuarios:

```bash
mysql> use users;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> use users;
Database changed
mysql> show tables;
+-----------------+
| Tables_in_users |
+-----------------+
| users           |
+-----------------+
1 row in set (0.00 sec)

mysql> show columns from users;
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| id       | int         | YES  |     | NULL    |       |
| username | varchar(50) | YES  |     | NULL    |       |
| password | varchar(50) | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+
3 rows in set (0.01 sec)

mysql> select * from users;
+------+-------------------+------------------------------+
| id   | username          | password                     |
+------+-------------------+------------------------------+
|    1 | ppavlata0         | 6znAfvTbB2                   |
|    2 | ktofanini1        | TP2NxFD62e                   |
|    3 | rallwell2         | t1t7WaqvEfv                  |
|    4 | efernier3         | ZRYOBO9PI                    |
|    5 | fpoon4            | 5Spyx2Jb                     |
|    6 | jgurnell5         | LMCnWKD                      |
|    7 | aminter6          | ngCyGg3                      |
|    8 | dwattinham7       | H2bpGC5                      |
|    9 | ddumphreys8       | eGek5Q8                      |
|   10 | etookey9          | kXBd88ZX                     |
|   11 | mlindbacka        | H9uTnIvli92                  |
|   12 | awebbeb           | RALeM2IfuwA                  |

<--------SNIP-------->

|  144 | eblamphin3z       | 7Zjz7RvcC9x                  |
|  145 | lwederell40       | eyWsJl                       |
|  146 | nverick41         | Mr1r2H                       |
|  147 | mlawlie42         | XrHEZJbuUd                   |
|  148 | swahlberg43       | 46gOiZ                       |
|  149 | crubinivitz44     | FLlYii1mQz84                 |
|  150 | HTB               | cr3n4o7rzse7rzhnckhssncif7ds |
```

Y bum! Obtenemos las credenciales de todos los usuarios del sistema, incluído `HTB`. También podríamos filtrar la información de la siguiente manera:

```bash
mysql> select * from users where username = "HTB";          
+------+----------+------------------------------+
| id   | username | password                     |
+------+----------+------------------------------+
|  150 | HTB      | cr3n4o7rzse7rzhnckhssncif7ds |
+------+----------+------------------------------+
1 row in set (0.00 sec)
```
