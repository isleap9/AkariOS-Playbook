Add-Type -TypeDefinition @"
using System.Runtime.InteropServices;
public class WallpaperHelper {
    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
}
"@
$wp = "$env:SystemRoot\Web\Akari\img0.jpg"
[WallpaperHelper]::SystemParametersInfo(20, 0, $wp, 3) | Out-Null