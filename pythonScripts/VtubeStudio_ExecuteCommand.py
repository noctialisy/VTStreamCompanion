import sys, json
from websocket import create_connection

class VtubeStudioWebHandler:
    def __init__(self):
        with open('./../settings.json', 'r', encoding='utf8') as settings_file:
            json_settings = json.load(settings_file)
            self.ws_url = json_settings['vtube_studio_websocket_url']
            self.ws_token = json_settings['vtube_studio_websocket_token']
            self.plugin_name = json_settings['vtube_studio_plugin_name']
            self.plugin_developer = json_settings['vtube_studio_plugin_developer']
            self.ws = create_connection(self.ws_url)

            # Check if the WebSocket token is set
            # If not, request it from the VTube Studio API
            if not self.ws_token:
                print("VTube Studio WebSocket token is not set in settings.")
                self.auth_request()

            else:
                print("Token is present in settings.")

                # Must have at least one argument besides the script name
                if len(sys.argv) <= 1:
                    print('No command specified.')
                    print('')
                    exit()

                else:
                    # Execute the command based on the first argument
                    result = self.run_hotkey(req = sys.argv[1])
                    print(result)


    def auth_request(self):
        data = """{
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": \"""" + self.plugin_name + """\",
                "pluginDeveloper": \"""" + self.plugin_developer + """\"
            }
        }"""
        self.ws.send(data)
        result = self.ws.recv()
        print("Received '%s'" % result)

        result = json.loads(result)

        if result['messageType'] == 'AuthenticationTokenResponse':
            print("Authentication token received.")
            self.ws_token = result['data']['authenticationToken']

            # Update the settings.json with the new token
            with open('./../settings.json', 'r+', encoding='utf8') as settings_file:
                json_settings = json.load(settings_file)
                json_settings['vtube_studio_websocket_token'] = self.ws_token
                settings_file.seek(0)
                json.dump(json_settings, settings_file, indent=4)
                settings_file.truncate()


    def run_hotkey(self, req):
        data = """{
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "AuthenticationRequest",
            "data": {
                "pluginName": \"""" + self.plugin_name + """\",
                "pluginDeveloper": \"""" + self.plugin_developer + """\",
                "authenticationToken": \"""" + self.ws_token + """\"
            }
        }"""
        self.ws.send(data)
        auth_state = self.ws.recv()
        print(auth_state)

        # Check if the authentication was successful
        auth_state = json.loads(auth_state)
        if auth_state['data']['authenticated'] != True:
            print("Authentication failed. Running authentication request.")
            self.auth_request()

            data = """{
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "SomeID",
                "messageType": "AuthenticationRequest",
                "data": {
                    "pluginName": \"""" + self.plugin_name + """\",
                    "pluginDeveloper": \"""" + self.plugin_developer + """\",
                    "authenticationToken": \"""" + self.ws_token + """\"
                }
            }"""
            self.ws.send(data)
            auth_state = self.ws.recv()
            print(auth_state)

        # Request all Hotkeys
        hotkey_req = """{
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "SomeID",
            "messageType": "HotkeysInCurrentModelRequest"
            
        }"""
        self.ws.send(hotkey_req)
        hotkeys = self.ws.recv()
        hotkeys_container = json.loads(hotkeys)

        # Find the matching hotkey ID
        hotkey_id = None
        for hotkey in hotkeys_container['data']['availableHotkeys']:
            if hotkey['name'] == req:
                hotkey_id = hotkey['hotkeyID']
                break


        if hotkey_id is None:
            print(f"Hotkey '{req}' not found.")
            return
        else:
            hotkey_req = """{
                "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": "SomeID",
                "messageType": "HotkeyTriggerRequest",
                "data": {
                    "hotkeyID": \"""" + hotkey_id + """\",
                    "itemInstanceID": ""
                }
            }"""

        # Execute hotkey
        self.ws.send(hotkey_req)
        return self.ws.recv()


# Create an instance of the VtubeStudioWebHandler to execute the command
vtube_studio_handler = VtubeStudioWebHandler()