import json

class Plugin:
    
    def __init__(self, parent, options):
        if options.output_plugin_config_data:
            self._config = json.loads(options.output_plugin_config_data)
            
    def send_message(self, msg):
        print(msg)
        
    def format(self, msg):
        #<measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>]] <field_key>=<field_value>[,<field_key>=<field_value>] [<timestamp>]
        msgobj = json.loads(msg).get('data')
        msgobj['timestamp'] = int(msgobj['timestamp']) * 1000000000
        if 'announcements' in msgobj:            
            msg = ""
            for ann in msgobj['announcements']:
                for prefix in ann['prefixes']:
                    msg = msg + f"riperis,host={msgobj['host']},prefix={prefix},peer={msgobj['peer']},peer_asn={msgobj['peer_asn']},ris_id={msgobj['id']},type={msgobj['type']},origin={msgobj.get('origin', 'unk')} prefix_count=1 {msgobj['timestamp']}\n"
            return(msg)
        else:
            msgobj['announcement_count'] = 0
            return(f"riperis,host={msgobj['host']},peer={msgobj['peer']},peer_asn={msgobj['peer_asn']},ris_id={msgobj['id']},type={msgobj['type']},origin={msgobj.get('origin', 'unk')} prefix_count=0,event_count=1 {msgobj['timestamp']}")
