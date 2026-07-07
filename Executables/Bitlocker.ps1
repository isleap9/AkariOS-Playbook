$AllFixedDrives = Get-Volume | Where-Object DriveLetter

foreach ($Drive in $AllFixedDrives) {

    $MountPoint = "$($Drive.DriveLetter):"

    try {
        Disable-BitLocker -MountPoint $MountPoint -ErrorAction Stop
        Write-Host "-> Disable BitLocker issued on $MountPoint" -ForegroundColor Green
		pause
    }
    catch {
        Write-Host "-> $MountPoint : $($_.Exception.Message)" -ForegroundColor DarkGray
		pause
	}
}
