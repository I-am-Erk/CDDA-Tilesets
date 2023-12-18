

function Write-Log {
  param(
      [Parameter(Mandatory=$false)]
        [dateTime]$LastTime,
      [Parameter(Mandatory=$true)]
        [string]$LogText,
      [Parameter(Mandatory=$false)]
        [int]$Tab,
      [Parameter(Mandatory=$false)]
        [string]$Status
  )
  $CurrentTime = [dateTime]::Now
  if ([boolean]$LastTime) {
    $DeltaT = ($CurrentTime - $LastTime).TotalSeconds.ToString("00 s")
    $Time   = $CurrentTime.ToString("yyyy-MM-dd HH:mm:ss")
    $LogColor = ""
  } else {
    if ([System.Boolean]$Tab) {
      while ($Tab -gt 0) {
        Write-Host "  " -NoNewline
        $Tab = $Tab - 1
      }
    }
    $DeltaT = "    "
    $Time   = "                   "
    $LogColor = "Dark"
  }
  if ([boolean]$Status) {
      if     ($Status -match "error")   { $LogColor += "Red" }
      elseif ($Status -match "warning") { $LogColor += "Yellow" }
      else                              { $LogColor += "Green" }
  } else {
      $LogColor += "Cyan"
  }

Write-Host $Time " " -ForegroundColor Gray -NoNewline
Write-Host $DeltaT " "-ForegroundColor White -NoNewline
Write-Host $LogText -ForegroundColor $LogColor
  if ([boolean]$LastTime) {return $CurrentTime}
}


## Start
$LastLog = [dateTime]::Now
$StartTime = $LastLog
$LastLog = Write-Log $StartTime "Slicing source files"
Write-Log -LogText " "

## Detect tilename
$CurrentTileName = (Split-Path -Path (Get-Location)).split("\")[-1]
Write-Log -LogText ("Tile name  : " + $CurrentTileName) -Status Info

## Detect size
$FullPath = Get-Location
$PathDetails = $FullPath.ToString().split("\")

foreach ($PathLevel in $PathDetails) {
  if ($PathLevel -like "*png*x*") {
    $LevelParts = $PathLevel.Split("_")
    $Dimensions = $LevelParts[$LevelParts.Length-1]
    $DimX = $Dimensions.Split("x")[0]
    $DimY = $Dimensions.Split("x")[1]
  }
}
Write-Log -LogText ("Dimensions : " + $DimX + " x " + $DimY) -Status Info
Write-Log -LogText " "

## Detect variants
$TestName = $CurrentTileName + "_var*.png"
$AnyFiles = Get-ChildItem -Filter $TestName
if ([boolean]$AnyFiles) {
  Write-Log -LogText "There is a source file(s) for variants"
  foreach ($File in $AnyFiles) {
    $PythonExecutable = (get-command py.exe).Path
    $PythonCommand = @(
      (get-command slice_variants.py).Path
      $File.Name
      $DimX
      $DimY
      "--tile"
      $CurrentTileName
      "--append"
      "--out"
      "..\"
    )
    Write-Log -LogText $File.Name -Status Info -Tab 1
    $PythonOut = & $PythonExecutable $PythonCommand
    if ([boolean]$PythonOut) { $LastLog = Write-Log $LastLog $PythonOut -Status "Error" -Tab 2}
  }
  $AffectedFiles = (Get-ChildItem -Path "..\" | Where-Object { $_.LastWriteTime -gt $StartTime }).Count
  Write-Log -LogText ("Affected files : " + $AffectedFiles)
  Write-Log -LogText " "
}

## Detect seasons
$TestName = (
  ($CurrentTileName + "_winter.png"),
  ($CurrentTileName + "_spring.png"),
  ($CurrentTileName + "_summer.png"),
  ($CurrentTileName + "_autumn.png")
)
$AnyFiles = Get-ChildItem ".\*" -Include $TestName
if ([boolean]$AnyFiles) {
  Write-Log -LogText "There is a source files for seasonal multitiles"
  foreach ($File in $AnyFiles) {
    $Season = ($File.Name.Split(".")[0].Split("_"))[-1]
    $PythonExecutable = (get-command py.exe).Path
    $PythonCommand = @(
      (get-command slice_multitile.py).Path
      $File.Name
      $DimX
      $DimY
      "--tile"
      ($CurrentTileName + "_season_" + $Season)
      "--out"
      "..\"
    )
    Write-Log -LogText $File.Name -Status Info -Tab 1
    if ([boolean](Get-ChildItem -Path "..\" -Filter ($CurrentTileName + "_season_" + $Season + ".json") -ErrorAction SilentlyContinue)) {
      Write-Log -LogText "There is a JSON file aready. Will not modify it." -Status "Warning" -Tab 2
      $PythonCommand += "--no-json"
    }
    $PythonOut = & $PythonExecutable $PythonCommand
    if ([boolean]$PythonOut) { $LastLog = Write-Log $LastLog $PythonOut -Status "Error" -Tab 2}
  }
  $AffectedFiles = (Get-ChildItem -Path "..\" | Where-Object { $_.LastWriteTime -gt $StartTime }).Count
  Write-Log -LogText ("Affected files : " + $AffectedFiles)
  Write-Log -LogText " "
}

## Detect seasonal transparent
$TestName = (
  ($CurrentTileName + "_winter_t*.png"),
  ($CurrentTileName + "_spring_t*.png"),
  ($CurrentTileName + "_summer_t*.png"),
  ($CurrentTileName + "_autumn_t*.png")
)
$AnyFiles = Get-ChildItem ".\*" -Include $TestName
if ([boolean]$AnyFiles) {
  Write-Log -LogText "There is a source files for seasonal transparent multitiles"
  foreach ($File in $AnyFiles) {
    $Season = ($File.Name.Split(".")[0].Split("_"))[-2]
    $PythonExecutable = (get-command py.exe).Path
    $PythonCommand = @(
      (get-command slice_multitile.py).Path
      $File.Name
      $DimX
      $DimY
      "--tile"
      ($CurrentTileName + "_season_" + $Season + "_transparent")
      "--out"
      "..\"
    )
    Write-Log -LogText $File.Name -Status Info -Tab 1
    if ([boolean](Get-ChildItem -Path "..\" -Filter ($CurrentTileName + "_season_" + $Season + "_transparent.json") -ErrorAction SilentlyContinue)) {
      Write-Log -LogText "There is a JSON file aready. Will not modify it." -Status "Warning" -Tab 2
      $PythonCommand += "--no-json"
    }
    $PythonOut = & $PythonExecutable $PythonCommand
    if ([boolean]$PythonOut) { $LastLog = Write-Log $LastLog $PythonOut -Status "Error" -Tab 2}
  }
  $AffectedFiles = (Get-ChildItem -Path "..\" | Where-Object { $_.LastWriteTime -gt $StartTime }).Count
  Write-Log -LogText ("Affected files : " + $AffectedFiles)
  Write-Log -LogText " "
}

## Detect just a simple multitile
$TestName = $CurrentTileName + ".png"
$AnyFiles = Get-ChildItem -Filter $TestName
if ([boolean]$AnyFiles) {
  Write-Log -LogText "There is a source files for simple multitile"
  $File = $AnyFiles[0]
  $PythonExecutable = (get-command py.exe).Path
  $PythonCommand = @(
    (get-command slice_multitile.py).Path
    $File.Name
    $DimX
    $DimY
    "--tile"
    $CurrentTileName
    "--out"
    "..\"
  )
  Write-Log -LogText $File.Name -Status Info -Tab 1
  if ([boolean](Get-ChildItem -Path "..\" -Filter ($CurrentTileName + ".json") -ErrorAction SilentlyContinue)) {
    Write-Log -LogText "There is a JSON file aready. Will not modify it." -Status "Warning" -Tab 2
    $PythonCommand += "--no-json"
  }
  $PythonOut = & $PythonExecutable $PythonCommand
  if ([boolean]$PythonOut) { $LastLog = Write-Log $LastLog $PythonOut -Status "Error" -Tab 2}

  $AffectedFiles = (Get-ChildItem -Path "..\" | Where-Object { $_.LastWriteTime -gt $StartTime }).Count
  Write-Log -LogText ("Affected files : " + $AffectedFiles)
  Write-Log -LogText " "
}

## Detect just a simple multitile transparent
$TestName = $CurrentTileName + "_t*.png"
$AnyFiles = Get-ChildItem -Filter $TestName
if ([boolean]$AnyFiles) {
  Write-Log -LogText "There is a source files for simple multitile transparency"
  $File = $AnyFiles[0]
  $PythonExecutable = (get-command py.exe).Path
  $PythonCommand = @(
    (get-command slice_multitile.py).Path
    $File.Name
    $DimX
    $DimY
    "--tile"
    ($CurrentTileName + "_transparent")
    "--out"
    "..\"
  )
  Write-Log -LogText $File.Name -Status Info -Tab 1
  if ([boolean](Get-ChildItem -Path "..\" -Filter ($CurrentTileName + "_transparent.json") -ErrorAction SilentlyContinue)) {
    Write-Log -LogText "There is a JSON file aready. Will not modify it." -Status "Warning" -Tab 2
    $PythonCommand += "--no-json"
  }
  $PythonOut = & $PythonExecutable $PythonCommand
  if ([boolean]$PythonOut) { $LastLog = Write-Log $LastLog $PythonOut -Status "Error" -Tab 2}

  $AffectedFiles = (Get-ChildItem -Path "..\" | Where-Object { $_.LastWriteTime -gt $StartTime }).Count
  Write-Log -LogText ("Affected files : " + $AffectedFiles)
  Write-Log -LogText " "
}

$JSONFiles = (Get-ChildItem -Path "..\" -Filter "*.json").Count
$PNGFiles  = (Get-ChildItem -Path "..\" -Filter "*.png" ).Count
$AllFiles  = (Get-ChildItem -Path "..\").Count
$StartTime = Write-Log $StartTime ("Files (total/json/png) : " + $AllFiles + " / " + $JSONFiles + " / " + $PNGFiles)
