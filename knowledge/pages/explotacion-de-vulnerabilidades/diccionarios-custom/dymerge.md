
# DyMerge

{% embed url="<https://github.com/k4m4/dymerge>" %}

## <mark style="color:purple;">**1. Instalación**</mark>

```bash
git clone https://github.com/k4m4/dymerge.git
cd dymerge/
python2 dymerge.py
```

## <mark style="color:purple;">**2. Uso**</mark>

```bash
python2 dymerge.py -h
Usage: python dymerge.py {dictionaries} [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        output filename
  -i INCLUDE_VALUES, --include=INCLUDE_VALUES
                        include specified values in dictionary
  -z ZIP_TYPE, --zip=ZIP_TYPE
                        zip file with specified archive format
  -s, --sort            sort output alphabetically
  -u, --unique          remove dictionary duplicates
  -r, --reverse         reverse dictionary items
  -f, --fast            finish task asap

Examples:
  python dymerge.py ~/dictionaries/ -s -u -o ~/powerful.txt
  python dymerge.py /usr/share/wordlists/rockyou.txt /lists/cewl.txt -s -u
  python dymerge.py /lists/cewl.txt /lists/awlg.txt -s -u -i and,this
  python dymerge.py ~/fsocity.dic -u -r -o ~/clean.txt
  python dymerge.py /dicts/crunch.txt /dicts/john.txt -u -f -z bz2
```

## <mark style="color:purple;">**3. Unificar diccionarios**</mark>

```bash
ls
dict-1.txt    dict-2.txt    dict-3.txt    dict-4.txt    dict-5.txt

python2 dymerge.py *.txt -s -u -o final.txt
```

Esto unificará los diccionarios de una carpeta en un archivo llamado `final.txt`.

```
python2 dymerge.py *.txt -s -u -o final.txt
DyMerge 0.2 Nikolaos Kamarinakis (nikolaskama.me)
  ____                                                  
 /\  _`\           /'\_/`\
 \ \ \/\ \  __  __/\      \     __   _ __    __      __ 
  \ \ \ \ \/\ \/\ \ \ \__\ \  /'__`\/\` __\/'_ `\  /'__`\
   \ \ \_\ \ \ \_\ \ \ \_/\ \/\  __/\ \ \//\ \_\ \/\  __/
    \ \____/\/`____ \ \_\\ \_\ \____\\ \_\\ \____ \ \____\
     \/___/  `/___/  \/_/ \/_/\/____/ \/_/ \/____\ \/____/
                /\___/                       /\____/
                \/__/  Made with <3 by k4m4  \_/__/

[+] Starting Dictionary Merge Task
[+] Reading Dictionaries
[+] Merging Dictionaries
[+] Removing All Duplicates
[+] Sorting Dictionary Alphabetically
[+] Task Successfully Complete
[+] Final Dictionary Saved As --> final.txt
Comp/tional Time Elapsed: 0.044933
```

## <mark style="color:purple;">4. Ver cantidad de palabras</mark>

```bash
wc -c final.txt
454801 final.txt
```
