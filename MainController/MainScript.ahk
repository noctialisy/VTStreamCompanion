#Requires AutoHotkey >=2.0
#Include VMR.ahk
voicemeeter := VMR().Login()

;Persistent
;#include AHKv2\Lib\AutoHotInterception.ahk
;global AHI := AutoHotInterception()
;keyboard1Id := AHI.GetKeyboardId(0x04D9, 0x1702)
;cm1 := AHI.CreateContextManager(keyboard1Id)
;#HotIf cm1.IsActive	; Start the #if block

#Include HotkeysDef.ahk


;#HotIf			; Close the #if block