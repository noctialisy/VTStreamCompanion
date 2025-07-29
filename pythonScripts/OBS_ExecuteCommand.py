import websocket, sys, json, requests

# Enable / Disable debug logging
debug = False

# Read arguments passed to the script
arguments = sys.argv

if debug:
    print(arguments)

def test():
    ws = websocket.create_connection("ws://localhost:4455")

    scene_data = {
        "request-type": "SetCurrentScene",
        "scene-name": "TestScene" 

    }

    #print(json.dumps(scene_data))
    ws.send(json.dumps(scene_data))
    ws.close()
  
test()