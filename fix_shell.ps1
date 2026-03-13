# PowerShell脚本：修复VSCode Shell集成问题

Write-Host "正在修复VSCode Shell集成问题..." -ForegroundColor Cyan
Write-Host "=" * 60

# 1. 检查当前终端配置
Write-Host "`n1. 检查当前终端配置..." -ForegroundColor Yellow
$terminalConfig = "$env:APPDATA\Code\User\settings.json"
if (Test-Path $terminalConfig) {
    $config = Get-Content $terminalConfig -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($config.'terminal.integrated.shellIntegration.enabled' -eq $false) {
        Write-Host "  发现Shell集成被禁用" -ForegroundColor Red
    } else {
        Write-Host "  Shell集成已启用" -ForegroundColor Green
    }
} else {
    Write-Host "  未找到VSCode配置文件" -ForegroundColor Yellow
}

# 2. 检查PowerShell版本
Write-Host "`n2. 检查PowerShell版本..." -ForegroundColor Yellow
$psVersion = $PSVersionTable.PSVersion
Write-Host "  PowerShell版本: $psVersion" -ForegroundColor Green

# 3. 检查执行策略（已确认是RemoteSigned）
Write-Host "`n3. 检查执行策略..." -ForegroundColor Yellow
$execPolicy = Get-ExecutionPolicy
Write-Host "  执行策略: $execPolicy" -ForegroundColor Green
if ($execPolicy -eq "Restricted") {
    Write-Host "  警告：执行策略为Restricted，需要更改" -ForegroundColor Red
    Write-Host "  运行: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
}

# 4. 建议的手动操作步骤
Write-Host "`n4. 建议的手动修复步骤:" -ForegroundColor Cyan
Write-Host "  a. 在VSCode中按 Ctrl+Shift+P" -ForegroundColor White
Write-Host "  b. 输入 'Terminal: Select Default Profile'" -ForegroundColor White
Write-Host "  c. 选择 'Windows PowerShell'" -ForegroundColor White
Write-Host "  d. 关闭所有终端，重新打开" -ForegroundColor White

Write-Host "`n  e. 或者尝试更新VSCode:" -ForegroundColor White
Write-Host "     Ctrl+Shift+P → 输入 'Check for Updates'" -ForegroundColor White

# 5. 快速修复：重新加载VSCode窗口
Write-Host "`n5. 快速修复尝试:" -ForegroundColor Yellow
Write-Host "  在VSCode中按 Ctrl+Shift+P，然后输入:" -ForegroundColor White
Write-Host "  - 'Developer: Reload Window' (重新加载窗口)" -ForegroundColor White
Write-Host "  - 或 'Terminal: Reload' (重新加载终端)" -ForegroundColor White

# 6. 验证命令
Write-Host "`n6. 验证修复效果:" -ForegroundColor Cyan
Write-Host "  修复后，在终端中运行以下命令测试:" -ForegroundColor White
Write-Host "  echo 'Shell集成测试'" -ForegroundColor White
Write-Host "  python --version" -ForegroundColor White

Write-Host "`n" + "=" * 60
Write-Host "修复脚本执行完成！" -ForegroundColor Green
Write-Host "请按照上述步骤操作，然后重新启动VSCode。" -ForegroundColor Yellow

# 等待用户按键
Write-Host "`n按任意键继续..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")