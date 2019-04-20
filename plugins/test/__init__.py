import json

class Plugin:
    
    def __init__(self, parent, options):
        if options.output_plugin_config_data:
            self._config = json.loads(options.output_plugin_config_data)
            
    def send_message(self, msg):
        print(msg)
        
    def format(self, msg):
        msgobj = json.loads(msg).get('data')
        return(f"{msgobj['timestamp']} {msgobj['peer']}")