function Encrypt-AES {
    param(
        [Parameter(Mandatory = $true)]
        [String]$plaintext,

        [Parameter(Mandatory = $true)]
        [String]$key
    )

    $keyBytes = [System.Text.Encoding]::UTF8.GetBytes($key)
    $plaintextBytes = [System.Text.Encoding]::UTF8.GetBytes($plaintext)

    $aes = New-Object System.Security.Cryptography.AesManaged
    $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
    $aes.Key = $keyBytes
    $aes.IV = new-object byte[] 16

    $encryptor = $aes.CreateEncryptor()

    $memoryStream = New-Object System.IO.MemoryStream
    $cryptoStream = New-Object System.Security.Cryptography.CryptoStream($memoryStream, $encryptor, [System.Security.Cryptography.CryptoStreamMode]::Write)

    $cryptoStream.Write($plaintextBytes, 0, $plaintextBytes.Length)
    $cryptoStream.FlushFinalBlock()

    $ciphertextBytes = $memoryStream.ToArray()
    $ciphertextBase64 = [System.Convert]::ToBase64String($ciphertextBytes)

    return $ciphertextBase64
}

$WorkstationName = $env:COMPUTERNAME
$Secret = Read-Host -Prompt 'Ingresa el Secret del servicio Activity'
$EncrWorkstation = Encrypt-AES -plaintext $WorkstationName -key $Secret
Write-Host "Tu key para la instalacion del servicio Activity es: $EncrMachine a" 
Write-Host "a $ComputerName a"
Read-Host -Prompt "Presiona Enter para salir"