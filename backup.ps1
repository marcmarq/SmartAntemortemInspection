# Get current timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$backupDir = "..\..\antemortem-app-backups"
$backupName = "antemortem-app-backup-$timestamp"

# Create backup directory if it doesn't exist
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir
}

# Create backup
$exclude = @(
    'node_modules',
    'dist',
    'build',
    '.venv',
    'venv',
    '__pycache__',
    '.git'
)

$destination = Join-Path $backupDir $backupName

# Create destination directory
New-Item -ItemType Directory -Path $destination

# Copy files excluding specified directories
Get-ChildItem -Path . -Exclude $exclude | Copy-Item -Destination $destination -Recurse -Force

Write-Host "Backup created successfully at: $destination" 