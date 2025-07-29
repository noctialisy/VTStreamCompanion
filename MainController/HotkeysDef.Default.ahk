;This file is only an example
;Add your keys here and rename the file to HotkeysDef before launching the script
~< & Numpad0::
    {
        Run "python " A_ScriptDir "\..\pythonScripts\MixItUp_ExecuteCommand.py Twitch_Stream_Marker", ,"Hide"
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