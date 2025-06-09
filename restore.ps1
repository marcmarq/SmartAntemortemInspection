# Parameters
param(
    [Parameter(Mandatory=$true)]
    [string]$BackupName
)

$backupDir = "..\..\antemortem-app-backups"
$backupPath = Join-Path $backupDir $BackupName

# Check if backup exists
if (-not (Test-Path $backupPath)) {
    Write-Host "Error: Backup not found at $backupPath"
    exit 1
}

# Create temporary directory for current files
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$tempDir = "..\..\antemortem-app-current-$timestamp"

# Move current files to temporary directory
Write-Host "Creating backup of current files..."
if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $tempDir
Get-ChildItem -Path . -Exclude @('node_modules', '.git', 'backup.ps1', 'restore.ps1') | Copy-Item -Destination $tempDir -Recurse -Force

# Remove current files
Get-ChildItem -Path . -Exclude @('node_modules', '.git', 'backup.ps1', 'restore.ps1') | Remove-Item -Recurse -Force

# Copy backup files
Write-Host "Restoring from backup..."
Copy-Item -Path "$backupPath\*" -Destination . -Recurse -Force

Write-Host "Restore completed successfully!"
Write-Host "Your previous files were backed up to: $tempDir" 