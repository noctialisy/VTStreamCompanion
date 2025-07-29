import sys, json, requests

# Enable / Disable debug logging
debug = False

# Read arguments passed to the script
arguments = sys.argv

if debug:
    print(arguments)

# Read settings.json to find bots paths and commands (doesn't do anything if the file is not found)
with open('./../settings.json', 'r', encoding='utf8') as settings_file:
    json_settings = json.load(settings_file)
    api_url = json_settings['mixitup_api_url'] + json_settings['api_commands_address']

    if debug:
        print(api_url)

    # Must have at least one argument besides the script name
    if len(arguments) <= 1:
        print('No command specified.')
        print('')
        exit()

    # Find command id based on script argument
    command_list = requests.get(api_url + '?skip=0&pageSize=1000').json()

    if debug:
        print(command_list)
    
    # Must be a valid json object response
    if not isinstance(command_list, object):
        print('Command list wasn\'t an object')
        exit()

    for command in command_list['Commands']:
        if command['Name'] == arguments[1]:
            command_id = command['ID']
            
            if debug:
                print(command_id)

    # Create a default object to send with params for the command trigger
    # Arguments can be set programmatically for the command otherwise default is applied
    myobj = {
        'Platform': 'Twitch',
        'Arguments': ''
    }

    # Triggers the command
    x = requests.post(api_url + command_id, json = myobj)

    if debug:
        print(x)