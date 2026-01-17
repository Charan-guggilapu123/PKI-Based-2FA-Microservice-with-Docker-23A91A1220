# Load encrypted seed
$enc_seed = Get-Content -Raw "encrypted_seed.txt"
Write-Host "Encrypted seed loaded, length: $($enc_seed.Length)"

# POST /decrypt-seed
$body = @{
    encrypted_seed = $enc_seed
} | ConvertTo-Json

Write-Host "Posting to /decrypt-seed..."
$resp = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/decrypt-seed" `
    -ContentType "application/json" `
    -Body $body

Write-Host "Response: $($resp | ConvertTo-Json -Compress)"

# GET /generate-2fa
Write-Host "Getting 2FA code..."
$code_resp = Invoke-RestMethod -Uri "http://localhost:8080/generate-2fa"
Write-Host "2FA Response: $($code_resp | ConvertTo-Json -Compress)"

# POST /verify-2fa with the code
$code = $code_resp.code
Write-Host "Verifying code: $code"
$verify_body = @{
    code = $code
} | ConvertTo-Json

$verify_resp = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/verify-2fa" `
    -ContentType "application/json" `
    -Body $verify_body

Write-Host "Verify Response: $($verify_resp | ConvertTo-Json -Compress)"

# POST /verify-2fa with invalid code
Write-Host "Verifying invalid code..."
$invalid_body = @{
    code = "000000"
} | ConvertTo-Json

$invalid_resp = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/verify-2fa" `
    -ContentType "application/json" `
    -Body $invalid_body

Write-Host "Invalid Verify Response: $($invalid_resp | ConvertTo-Json -Compress)"

# Check cron logs
Write-Host "`nChecking cron logs in container..."
docker exec pki-2fa cat /cron/last_code.txt | Select-Object -Last 5
