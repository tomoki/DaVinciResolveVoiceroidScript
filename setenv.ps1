$Env:RESOLVE_SCRIPT_API = $env:ProgramData + "\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
$Env:RESOLVE_SCRIPT_LIB="C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
$Env:PYTHONPATH += ";" + $Env:RESOLVE_SCRIPT_API + "\Modules\"
$Env:PATH = $Env:UserProfile + "\AppData\Local\Programs\Python\Python36\;" + $Env:PATH