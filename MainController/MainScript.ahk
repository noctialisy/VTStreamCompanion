#Requires AutoHotkey >=2.0
#Include VMR.ahk
voicemeeter := VMR().Login()

;Persistent
;#include AHKv2\Lib\AutoHotInterception.ahk
;global AHI := AutoHotInterception()
;keyboard1Id := AHI.GetKeyboardId(0x04D9, 0x1702)
;cm1 := AHI.CreateContextManager(keyboard1Id)
;#HotIf cm1.IsActive	; Start the #if block
~< & Numpad0::
    {
        Run "python " A_ScriptDir "\..\pythonScripts\MixItUp_ExecuteCommand.py Twitch_Stream_Marker", ,"Hide"
        return
        
    }

~< & Numpad1::
    {
        Run "tsystem camera_settings", ,"Hide"
        return

    }

~< & Numpad2::
    {
        Run "python " A_ScriptDir "\..\pythonScripts\MixItUp_ExecuteCommand.py OBS_TEST", ,"Hide"
        return
        
    }

;Voicemeeter mute/unmute
~< & Numpad8::
    {
        if (voicemeeter.Bus[6].mute == true)
        {
            voicemeeter.Bus[6].mute := false
        }
        else
        {
            voicemeeter.Bus[6].mute := true
        }
        return

    }

~< & Numpad9::
    {
        if (voicemeeter.Bus[7].mute == true)
        {
            voicemeeter.Bus[7].mute := false
        }
        else
        {
            voicemeeter.Bus[7].mute := true
        }
        return

    }

#HotIf			; Close the #if block