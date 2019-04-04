#include %A_ScriptDir%\VA.ahk

device := VA_GetDevice("playback")
deviceName := VA_GetDeviceName(device)

IfInString, deviceName, Headset
  ExitApp, 1
else
  ExitApp, 0
