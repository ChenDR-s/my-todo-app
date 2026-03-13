# 解决 "Shell Integration Unavailable" 警告

## 问题描述
在VSCode中看到"Shell Integration Unavailable"警告，这会影响Cline查看命令输出的能力。

## 解决方案（按推荐顺序尝试）

### 方案1：更新VSCode到最新版本
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Check for Updates" 或 "更新"
3. 如果有可用更新，点击"更新"
4. 更新完成后重启VSCode

### 方案2：更改默认终端Shell
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Terminal: Select Default Profile"
3. 从列表中选择一个支持的Shell：
   - **Windows PowerShell**（推荐，当前使用中）
   - **Command Prompt**（cmd.exe）
   - **Git Bash**（如果已安装）
4. 选择后关闭所有终端，重新打开

### 方案3：启用Shell集成功能
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Preferences: Open Settings (JSON)"
3. 在settings.json文件中添加或修改：
   ```json
   {
     "terminal.integrated.shellIntegration.enabled": true,
     "terminal.integrated.shellIntegration.decorationsEnabled": "both"
   }
   ```
4. 保存文件并重启VSCode

### 方案4：检查PowerShell执行策略
1. 在VSCode终端中运行：
   ```powershell
   Get-ExecutionPolicy
   ```
2. 如果显示 `Restricted`，需要更改为 `RemoteSigned`：
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. 输入 `Y` 确认更改

### 方案5：清理终端配置
1. 关闭所有VSCode实例
2. 删除VSCode的终端缓存：
   - 位置：`C:\Users\cc\AppData\Roaming\Code\User\globalStorage\ms-vscode.terminal`
   - 或运行：`Remove-Item -Path "$env:APPDATA\Code\User\globalStorage\ms-vscode.terminal" -Recurse -Force`
3. 重新启动VSCode

### 方案6：使用命令面板修复
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 "Developer: Reload Window"
3. 或输入 "Terminal: Reload"
4. 重启终端集成功能

## 验证解决方案
解决后，在VSCode终端中运行：
```powershell
echo "测试Shell集成"
```
应该能正常显示输出，且不再有警告。

## 备用方案
如果以上方法都不行：
1. 考虑使用其他终端，如Windows Terminal
2. 或在VSCode设置中暂时禁用Shell集成：
   ```json
   {
     "terminal.integrated.shellIntegration.enabled": false
   }
   ```

## 当前环境信息
- 操作系统：Windows 10
- 当前Shell：PowerShell
- Shell配置文件：`C:\Users\cc\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`
- Python版本：3.14.3

## 推荐尝试顺序
1. 方案2（更改默认终端）→ 最简单
2. 方案1（更新VSCode）→ 最根本
3. 方案4（检查执行策略）→ 常见问题
4. 方案3（启用集成）→ 配置调整
5. 方案5（清理缓存）→ 最后手段