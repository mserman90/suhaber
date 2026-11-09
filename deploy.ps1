# deploy.ps1
# Gazete portalını ve RSS yayınını GitHub Pages'e tek tıkla gönderir
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " Su Haber Bülteni - GitHub Pages Dağıtım Aracı" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan

# Sistemdeki Git uygulamasını dinamik tespit et
$gitExe = "git"
if (Get-Command "git" -ErrorAction SilentlyContinue) {
    $gitExe = (Get-Command "git").Source
} elseif (Test-Path "C:\Users\murat.erman\.local\git\cmd\git.exe") {
    $gitExe = "C:\Users\murat.erman\.local\git\cmd\git.exe"
}

$token = $(gh auth token 2>$null)
if ($token) {
    $token = $token.Trim()
}

if (-not $token) {
    Write-Host "[-] GitHub CLI oturumu bulunamadı. Lütfen 'gh auth login' yapın." -ForegroundColor Red
    exit 1
}

Write-Host "[*] Uzak depo adresi güncelleniyor..." -ForegroundColor Gray
& $gitExe remote set-url origin "https://${token}@github.com/mserman90/suhaber.git"

Write-Host "[*] Kodlar GitHub'a gönderiliyor (push)..." -ForegroundColor Cyan
& $gitExe push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[+] TEBRİKLER! Tüm değişiklikler GitHub'a başarıyla yüklendi!" -ForegroundColor Green
    Write-Host "[+] GitHub Actions iş akışı otomatik olarak başladı." -ForegroundColor Green
    Write-Host "[+] Portal adresiniz: https://mserman90.github.io/suhaber/" -ForegroundColor Yellow
    Write-Host "[+] Sabit RSS adresiniz: https://mserman90.github.io/suhaber/rss.xml" -ForegroundColor Yellow
} else {
    Write-Host "`n[-] Bağlantı hatası: Kurumsal güvenlik duvarı GitHub bağlantısını engelliyor." -ForegroundColor Red
    Write-Host "[-] Lütfen VPN veya mobil internetinizi (hotspot) açıp bu betiği tekrar çalıştırın." -ForegroundColor Yellow
}
