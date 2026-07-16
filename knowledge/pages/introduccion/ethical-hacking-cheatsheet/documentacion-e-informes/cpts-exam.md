
# CPTS Exam

## <mark style="color:purple;">Introduction</mark>

### Letter of Engagement

You are a penetration tester for **Acme Security, LLC**. Fresh off your long-term engagement with Inlanefreight, the company **Trilocor Robotics** has hired your firm to conduct an external penetration test to map out their external footprint and identify and exploit any vulnerabilities present within the in-scope hosts.

This is their first penetration test as they have only performed vulnerability scans in the past and have run a successful bug bounty program for the past year, which has revealed multiple high-risk flaws. They expanded the scope of this penetration test to include hosts not part of their bug bounty program scope.

Your task is to enumerate the external network thoroughly, documenting all "live hosts" and running services, identify any vulnerable or misconfigured hosts, attempt to gain access to sensitive data, and a foothold into the internal network. The client would like to keep the test as real-world as possible, so if you can breach the DMZ, they would like you to demonstrate how far you can take your access and what data you can locate within the internal network.

Your client wants as thorough an assessment as possible, so evasive testing is not required. They prefer a "grey box" approach and have provided the in-scope network ranges but no further information about the hosts, OS versions, or running applications/services. Enumerate the network thoroughly, identify all hosts and corresponding running services, determine exploitability and take your foothold into the network as far as possible.

Obtain a minimum of **85 points** to complete the hands-on portion of the exam. Take detailed notes and log output to complete the required exam assessment report.

***

### General Tips

* Watch your **Pwnbox/lab time** and extend as necessary so you don't lose shells.
* **Document and write your attack chain as you go.** Don't leave reporting to the last minute!\
  Refer to the Documentation and Reporting module before you start the exam and before submitting your final report to make sure it is commercial grade.
* Review the **report template** before you start your assessment. This will help you to structure your notes and make sure you are gathering adequate data to populate the report properly.
* The customer would like any **changes made during testing to be reverted and notated in the report**.\
  If a change cannot be reverted, please report it and notate it as such.\
  It's always a great idea to show **evidence of reverting any changes** that you make as part of the evidence for a finding and also include information regarding any changes, exploitation attempts, compromised hosts, and compromised users in the report appendices.
* **Document your complete attack chain in the report** (the path you took from start to finish).\
  Also, break out individual findings from the attack chain (i.e., SQL Injection if this vector is present) and show detailed reproduction steps, not just a single screenshot.
* Though evasive testing is not required, this customer is **sensitive to configuration changes** within their environment.\
  Treat this like a real-world engagement and opt to **add a local administrator account** over changing an account password wherever possible.
* Treat this network as a **busy corporate network** where there are live users working.
* Review the **Penetration Tester path** module content as much as needed. Utilize the module cheat sheets and global search to your advantage!

***

### Scope

The scope of this assessment is as follows:

* `www.trilocor.local`
* Any identified `*.trilocor.local` subdomain
* Any open web server ports discovered on the "Entry Point" IP address that will become visible upon pressing **"SPAWN INSTANCE"** (Step 2 below).

> **Important:** Scanning any other IP in the Entry Point's network is **NOT allowed**!\
> Multiple different subdomains exist on the entry point host.

#### URL/CIDR Range Description

| URL/CIDR          | Description             |
| ----------------- | ----------------------- |
| `trilocor.local`  | Main Trilocor website   |
| `172.16.139.0/24` | Internal network subnet |
| `172.16.210.0/24` | Internal network subnet |

***

### Rules of Engagement

#### In-Scope Findings

The following types of findings are in-scope for this penetration test assessment:

* Sensitive or personally identifiable information disclosure
* Remote Code Execution (RCE)
* Arbitrary file upload
* Authentication or authorization flaws, such as insecure direct object references (IDOR) and authentication bypasses
* All forms of injection vulnerabilities
* Directory traversal
* Local file read
* Significant security misconfigurations and business logic flaws
* Exposed credentials that could be leveraged to gain further access
* Windows and Linux local privilege escalation vulnerabilities
* Vulnerable services and applications
* Active Directory vulnerabilities & misconfigurations

#### Out-of-Scope Activities

The following types of activities are considered **out-of-scope** for this penetration test:

* Scanning and assessing any other IP in the entry point's network or hosts that do not fall within the in-scope internal subnets
* Physical attacks against Trilocor properties
* Unverified scanner output
* Any vulnerabilities identified through DDoS or spam attacks
* Self-XSS
* Login/logout CSRF
* Issues with SSL certificates, open ports, TLS versions, or missing HTTP response headers
* Vulnerabilities in third-party libraries unless they can be leveraged to significantly impact the target
* Any theoretical attacks or attacks that require significant user interaction or are low risk
* Phishing or social engineering attacks against Trilocor employees or contractors

***

### Connectivity Prerequisites

* If you are using **Pwnbox** to perform this penetration test, please ensure that `eu-academy-exams-X` or `us-academy-exams-X` is visible when opening a terminal.\
  Then and only then will Pwnbox be able to reach the exam lab's applications.\
  If you see otherwise, you will need to terminate any spawned Pwnbox in a module and spawn a new one from inside the exam lab's page (Step 1 below).
* If you are using your **own attacking virtual machine** to connect to the exam lab's VPN, then you can test your connectivity by adding an entry regarding `trilocor.local` in your virtual machine's hosts file and browsing:\
  `http://trilocor.local`.

***

### Exam Objectives

To be awarded the **HTB Certified Penetration Testing Specialist (CPTS)** certification, you must:

*(Exam objective details to be filled in as provided by the exam instructions.)*

#### Flag Locations – Scope

* `www.trilocor.local`
* Any identified `*.trilocor.local` subdomain
* Any open web server ports discovered on the "Entry Point" IP address that will become visible upon pressing **"SPAWN INSTANCE"** (Step 2 below).

> **Important:** Scanning any other IP in the Entry Point's network is **NOT allowed**!\
> Multiple different subdomains exist on the entry point host.

## <mark style="color:purple;">Machines</mark>

* DMZ01
* SRV01
* WKS01
* DC02
* DC01
* DEV01
* MGMT01

## <mark style="color:purple;">Flags</mark>&#x20;

#### Gain RCE and submit the flag found within the /home/websvc directory on DMZ01 <mark style="color:$primary;">(5 points)</mark>

#### Obtain a shell on DMZ01 and submit the contents of the flag in the /home/srvadm directory <mark style="color:$primary;">(5 points)</mark>

#### Submit the contents of the flag in /root on DMZ01 <mark style="color:$primary;">(5 points)</mark>

#### Submit the user flag on SRV01 <mark style="color:$primary;">(5 points)</mark>

#### Submit the root flag on SRV01 <mark style="color:$primary;">(5 points)</mark>

#### Submit the user flag on WKS01 <mark style="color:$primary;">(10 points)</mark>

#### Submit the root flag on WKS01 <mark style="color:$primary;">(5 points)</mark>

#### Submit the user flag on DC01 <mark style="color:$primary;">(10 points)</mark>

#### Submit the root flag on DC01 <mark style="color:$primary;">(10 points)</mark>

#### Submit the user flag on DC02 <mark style="color:$primary;">(5 points)</mark>

#### Submit the root flag on DC02 <mark style="color:$primary;">(10 points)</mark>

#### Submit the user flag on DEV01 <mark style="color:$primary;">(10 points)</mark>

#### Submit the root flag on DEV01 <mark style="color:$primary;">(5 points)</mark>

#### Submit the root flag on MGMT01 <mark style="color:$primary;">(10 points)</mark>

## <mark style="color:purple;">Feedback primer intento</mark>

Hi Alex Fernández,

We regret to inform you that you did not achieve the passing score on the HTB Certified Penetration Testing Specialist (CPTS) exam. You found 0 flags which resulted in only 0 points out of the 85 required to pass the lab portion of the exam. Your report was well written, so once you are more comfortable with the material we feel you will have no issue with creating an excellent report.

Here are some observations we made from your progress in the exam and some focus areas that we believe you should revisit in the Penetration Tester path before taking a second attempt at the exam:

* Whenever conducting any penetration testing assessment, always keep notes on everything you discover on any of the targets, as you never know when such information may become handy. On a couple of occasions, you were close and only had to look at your earlier notes and put the two together to proceed.
* The very first step you perform for any target network or web application is to study and understand what is in front of you. Take a few minutes to navigate any discovered web applications and understand how they work and function. Interact with any interesting services or other types of applications. As you do so, keep noting down possible attacks on each functionality (e.g. login: brute force, SQL injection, etc.). If you have already exploited any hosts, make sure to perform thorough post-exploitation as what you need to proceed may be present on a host in the network. If you have compromised users (especially Active Directory users), make sure to thoroughly enumerate all of the objects they can access, modify, etc., both on target systems where they have login rights and in Active Directory. Once you are done, try to prioritize potential attacks and then test them one by one.
* If you are ever stuck for too long on a single target, it means that you are stuck on a single way of thinking, and without taking a break from it you would not be able to change this way of thinking. This is why it is advisable to step back from the exercise for a while or move to another, and then come back to it, by which time you would be able to look at it from a different perspective.
* It is strongly recommended that you submit the flags as you find them. This also helps you gauge your progress through the exam.
* It is crucial to understand how networks, web applications and Active Directory work and what options are available to us in any penetration testing assessment. Tools available to us during a penetration test can be helpful but will often not find all vulnerabilities. Therefore, we recommend that you study the fundamentals and internalize them to understand the penetration testing process.
* Remember that multiple tools and techniques exist for enumerating web applications, networks, and especially Active Directory; some may find information that others do not. It is important to be flexible and thorough in your enumeration.
* Also, I recommend having all of the module cheat sheets on hand, and don't forget to use the search feature on Academy to search modules for tools/techniques.

Additionally, here are some areas that we believe you should focus on before starting your exam retake:

When attacking a web application, make sure to thoroughly map it out and note down any discovered parameters that could then be fuzzed using various tools/techniques.

While you do have the right to start a second exam attempt within the 14-day exam retake window, we highly recommend that you spend a good amount of time reviewing the course material before attempting the exam again.

Thank you
