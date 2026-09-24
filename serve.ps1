# ==============================================================================
# FarmRoute (फार्मरूट) - SIH 2026
# High-Performance Multi-Device Synchronized Server
# Supports: Zero-Admin LAN/Wi-Fi Binding + REST API (/api/state) + Static Files
# ==============================================================================

param(
    [int]$Port = 8085
)

$ErrorActionPreference = "Continue"

# Detect Local Area Network IPv4 Address
$lanIp = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notmatch 'Loopback|vEthernet' -and $_.IPAddress -notlike '169.254*' } | Select-Object -First 1 -ExpandProperty IPAddress)
if (-not $lanIp) { $lanIp = "127.0.0.1" }

$rootDir = $PSScriptRoot
$dataDir = Join-Path $rootDir "data"
if (-not (Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
}
$stateFile = Join-Path $dataDir "state.json"

# Initialize state file if empty
if (-not (Test-Path $stateFile)) {
    "{}" | Out-File -FilePath $stateFile -Encoding utf8 -NoNewline
}

$listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $Port)

try {
    $listener.Start()
    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host "  🌾 FarmRoute (फार्मरूट) - MULTI-DEVICE SYNC WEB SERVER RUNNING" -ForegroundColor Yellow
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host "  💻 [PC Local]:     http://localhost:$Port/" -ForegroundColor Cyan
    Write-Host "  📱 [Mobile/Phone]: http://$($lanIp):$Port/" -ForegroundColor Magenta
    Write-Host "  📂 Central DB:     $stateFile" -ForegroundColor Gray
    Write-Host "  🔄 Live Sync:      Enabled (/api/state GET & POST)" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host "  💡 Tip: Connect your phone to the same Wi-Fi or PC Hotspot and open the URL!" -ForegroundColor White
    Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor Gray
    Write-Host ""

    # Launch default browser on PC
    try { Start-Process "http://localhost:$Port/" } catch {}

    while ($true) {
        $client = $listener.AcceptTcpClient()
        [System.Threading.ThreadPool]::QueueUserWorkItem({
            param($tcpClient)
            try {
                $stream = $tcpClient.GetStream()
                $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
                $binaryWriter = New-Object System.IO.BinaryWriter($stream)

                $requestLine = $reader.ReadLine()
                if ([string]::IsNullOrEmpty($requestLine)) {
                    $tcpClient.Close()
                    return
                }

                $parts = $requestLine.Split(' ')
                $method = $parts[0].ToUpper()
                $rawPath = if ($parts.Length -gt 1) { $parts[1] } else { "/" }
                $cleanPath = $rawPath.Split('?')[0].TrimStart('/')

                # Read Headers
                $headers = @{}
                $contentLength = 0
                while ($true) {
                    $headerLine = $reader.ReadLine()
                    if ([string]::IsNullOrEmpty($headerLine)) { break }
                    $hParts = $headerLine.Split(':', 2)
                    if ($hParts.Length -eq 2) {
                        $hKey = $hParts[0].Trim().ToLower()
                        $hVal = $hParts[1].Trim()
                        $headers[$hKey] = $hVal
                        if ($hKey -eq "content-length") {
                            $contentLength = [int]$hVal
                        }
                    }
                }

                # Read Body if POST
                $bodyString = ""
                if ($contentLength -gt 0) {
                    $charBuffer = New-Object char[] $contentLength
                    $bytesRead = 0
                    while ($bytesRead -lt $contentLength) {
                        $read = $reader.Read($charBuffer, $bytesRead, $contentLength - $bytesRead)
                        if ($read -le 0) { break }
                        $bytesRead += $read
                    }
                    $bodyString = New-Object string ($charBuffer, 0, $bytesRead)
                }

                # Handle CORS Preflight
                if ($method -eq "OPTIONS") {
                    $resHeader = "HTTP/1.1 200 OK`r`nAccess-Control-Allow-Origin: *`r`nAccess-Control-Allow-Methods: GET, POST, OPTIONS`r`nAccess-Control-Allow-Headers: *`r`nContent-Length: 0`r`nConnection: close`r`n`r`n"
                    $hBytes = [System.Text.Encoding]::UTF8.GetBytes($resHeader)
                    $binaryWriter.Write($hBytes)
                    $binaryWriter.Flush()
                    $tcpClient.Close()
                    return
                }

                # 1. API: /api/ip
                if ($cleanPath -eq "api/ip") {
                    $json = "{`"ip`":`"$using:lanIp`",`"port`":$using:Port}"
                    $b = [System.Text.Encoding]::UTF8.GetBytes($json)
                    $resHeader = "HTTP/1.1 200 OK`r`nContent-Type: application/json; charset=utf-8`r`nAccess-Control-Allow-Origin: *`r`nContent-Length: $($b.Length)`r`nConnection: close`r`n`r`n"
                    $binaryWriter.Write([System.Text.Encoding]::UTF8.GetBytes($resHeader))
                    $binaryWriter.Write($b)
                    $binaryWriter.Flush()
                    $tcpClient.Close()
                    return
                }

                # 2. API: /api/state GET
                if ($cleanPath -eq "api/state" -and $method -eq "GET") {
                    $json = "{}"
                    if (Test-Path $using:stateFile) {
                        $json = [System.IO.File]::ReadAllText($using:stateFile, [System.Text.Encoding]::UTF8)
                        if ([string]::IsNullOrWhiteSpace($json)) { $json = "{}" }
                    }
                    $b = [System.Text.Encoding]::UTF8.GetBytes($json)
                    $resHeader = "HTTP/1.1 200 OK`r`nContent-Type: application/json; charset=utf-8`r`nAccess-Control-Allow-Origin: *`r`nContent-Length: $($b.Length)`r`nConnection: close`r`n`r`n"
                    $binaryWriter.Write([System.Text.Encoding]::UTF8.GetBytes($resHeader))
                    $binaryWriter.Write($b)
                    $binaryWriter.Flush()
                    $tcpClient.Close()
                    return
                }

                # 3. API: /api/state POST
                if ($cleanPath -eq "api/state" -and $method -eq "POST") {
                    if (-not [string]::IsNullOrWhiteSpace($bodyString)) {
                        [System.IO.File]::WriteAllText($using:stateFile, $bodyString, [System.Text.Encoding]::UTF8)
                    }
                    $resp = "{`"status`":`"synced`",`"timestamp`":$([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds())}"
                    $b = [System.Text.Encoding]::UTF8.GetBytes($resp)
                    $resHeader = "HTTP/1.1 200 OK`r`nContent-Type: application/json; charset=utf-8`r`nAccess-Control-Allow-Origin: *`r`nContent-Length: $($b.Length)`r`nConnection: close`r`n`r`n"
                    $binaryWriter.Write([System.Text.Encoding]::UTF8.GetBytes($resHeader))
                    $binaryWriter.Write($b)
                    $binaryWriter.Flush()
                    $tcpClient.Close()
                    return
                }

                # 4. Static Files
                if ([string]::IsNullOrEmpty($cleanPath)) {
                    $cleanPath = "index.html"
                }

                $filePath = Join-Path $using:rootDir $cleanPath
                if (Test-Path $filePath -PathType Leaf) {
                    $fileBytes = [System.IO.File]::ReadAllBytes($filePath)
                    $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
                    $mime = "application/octet-stream"
                    switch ($ext) {
                        ".html" { $mime = "text/html; charset=utf-8" }
                        ".css"  { $mime = "text/css; charset=utf-8" }
                        ".js"   { $mime = "application/javascript; charset=utf-8" }
                        ".json" { $mime = "application/json; charset=utf-8" }
                        ".png"  { $mime = "image/png" }
                        ".jpg"  { $mime = "image/jpeg" }
                        ".svg"  { $mime = "image/svg+xml" }
                    }

                    $resHeader = "HTTP/1.1 200 OK`r`nContent-Type: $mime`r`nAccess-Control-Allow-Origin: *`r`nContent-Length: $($fileBytes.Length)`r`nConnection: close`r`n`r`n"
                    $binaryWriter.Write([System.Text.Encoding]::UTF8.GetBytes($resHeader))
                    $binaryWriter.Write($fileBytes)
                    $binaryWriter.Flush()
                } else {
                    $err = "404 Not Found"
                    $b = [System.Text.Encoding]::UTF8.GetBytes($err)
                    $resHeader = "HTTP/1.1 404 Not Found`r`nContent-Type: text/plain`r`nContent-Length: $($b.Length)`r`nConnection: close`r`n`r`n"
                    $binaryWriter.Write([System.Text.Encoding]::UTF8.GetBytes($resHeader))
                    $binaryWriter.Write($b)
                    $binaryWriter.Flush()
                }

                $tcpClient.Close()
            } catch {
                try { $tcpClient.Close() } catch {}
            }
        }, $client) | Out-Null
    }
} catch {
    Write-Host "Server Exception: $($_.Exception.Message)" -ForegroundColor Red
} finally {
    $listener.Stop()
}
