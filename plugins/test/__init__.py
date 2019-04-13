import json

def send_message(msg):
    print(msg)
    
def format(msg):
    msgobj = json.loads(msg).get('data')
    return(f"{msgobj['timestamp']} {msgobj['peer']}")