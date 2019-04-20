import json

class Plugin:
    
    def __init__(self, parent, options):
        self._init=True

    def send_message(self, msg):
        print(msg)
        
    def format(self, msg):
        msgobj = json.loads(msg).get('data')
        return(f"{msgobj['timestamp']} {msgobj['peer']}")