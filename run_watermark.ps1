#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Bulk Image Watermark Script Runner
    
.DESCRIPTION
    PowerShell wrapper for the bulk image watermark script with additional features
    like progress bars and better error handling.
    
.PARAMETER InputFolder
    Source directory containing images to process
    
.PARAMETER OutputFolder
    Destination directory for watermarked images
    
.PARAMETER WatermarkFile
    Path to PNG watermark file
    
.PARAMETER DryRun
    Show what would be processed without actually processing
    
.PARAMETER CustomOptions
    Additional command-line options to pass to the watermark script
    
.EXAMPLE
    .\run_watermark.ps1 -InputFolder "C:\Photos" -OutputFolder "C:\Watermarked" -WatermarkFile "C:\logo.png"
    
.EXAMPLE
    .\run_watermark.ps1 -InputFolder ".\photos" -OutputFolder ".\output" -WatermarkFile ".\logo.png" -DryRun
    
.EXAMPLE
    .\run_watermark.ps1 -InputFolder ".\photos" -OutputFolder ".\output" -WatermarkFile ".\logo.png" -CustomOptions "--png-opacity 0.5 --margin 30"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$InputFolder,
    
    [Parameter(Mandatory=$true)]
    [string]$OutputFolder,
    
    [Parameter(Mandatory=$true)]
    [string]$WatermarkFile,
    
    [switch]$DryRun,
    
    [string]$CustomOptions = ""
)

# Function to check if Python is available
function Test-Python {
    try {
        $pythonVersion = py --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
            return $true
        }
    } catch {
        # Continue to next check
    }
    
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
            return $true
        }
    } catch {
        # Continue to next check
    }
    
    Write-Host "❌ Python not found. Please install Python 3.7+ and ensure 'py' or 'python' command works." -ForegroundColor Red
    return $false
}

# Function to check if watermark script exists
function Test-WatermarkScript {
    if (Test-Path "watermark_script.py") {
        Write-Host "✓ Watermark script found" -ForegroundColor Green
        return $true
    } else {
        Write-Host "❌ watermark_script.py not found in current directory" -ForegroundColor Red
        return $false
    }
}

# Function to validate paths
function Test-Paths {
    $errors = @()
    
    if (-not (Test-Path $InputFolder)) {
        $errors += "Input folder does not exist: $InputFolder"
    }
    
    if (-not (Test-Path $WatermarkFile)) {
        $errors += "Watermark file does not exist: $WatermarkFile"
    }
    
    if ($errors.Count -gt 0) {
        Write-Host "❌ Validation errors:" -ForegroundColor Red
        foreach ($err in $errors) {
            Write-Host "  - $err" -ForegroundColor Red
        }
        return $false
    }
    
    Write-Host "✓ Paths validated successfully" -ForegroundColor Green
    return $true
}

# Main execution
Write-Host "🚀 Bulk Image Watermark Script - PowerShell Runner" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
if (-not (Test-Python)) { exit 1 }
if (-not (Test-WatermarkScript)) { exit 1 }

# Validate paths
Write-Host "Validating paths..." -ForegroundColor Yellow
if (-not (Test-Paths)) { exit 1 }

# Build command
$baseCommand = "py watermark_script.py --input-folder `"$InputFolder`" --output-folder `"$OutputFolder`" --png-watermark `"$WatermarkFile`" --enable-numbering"

if ($DryRun) {
    $baseCommand += " --dry-run"
    Write-Host "DRY RUN MODE - No files will be processed" -ForegroundColor Yellow
}

if ($CustomOptions) {
    $baseCommand += " $CustomOptions"
}

Write-Host ""
Write-Host "Command to execute:" -ForegroundColor Cyan
Write-Host $baseCommand -ForegroundColor White
Write-Host ""

# Confirm execution (unless dry run)
if (-not $DryRun) {
    $confirmation = Read-Host "Do you want to proceed with watermarking? (y/N)"
    if ($confirmation -notmatch '^[Yy]') {
        Write-Host "Operation cancelled by user." -ForegroundColor Yellow
        exit 0
    }
}

# Execute command
Write-Host ""
Write-Host "Executing watermark script..." -ForegroundColor Green
Write-Host ""

try {
    if ($DryRun) {
        Invoke-Expression $baseCommand
    } else {
        # Show progress for actual processing
        Write-Progress -Activity "Processing images" -Status "Starting..." -PercentComplete 0
        
        $process = Start-Process -FilePath "py" -ArgumentList "watermark_script.py", "--input-folder", $InputFolder, "--output-folder", $OutputFolder, "--png-watermark", $WatermarkFile, "--enable-numbering" -NoNewWindow -PassThru -Wait
        
        if ($process.ExitCode -eq 0) {
            Write-Host "✓ Watermarking completed successfully!" -ForegroundColor Green
        } else {
            Write-Host "❌ Watermarking failed with exit code: $($process.ExitCode)" -ForegroundColor Red
            exit $process.ExitCode
        }
    }
} catch {
    Write-Host "❌ Error executing watermark script: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 Process completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Output folder: $OutputFolder" -ForegroundColor Cyan
Write-Host "Log file: watermark_script.log" -ForegroundColor Cyan
