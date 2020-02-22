import json
import socket as s

# Socket creation example based on the default socket path:
#     nc -lkUu /tmp/rislive.sock

# Example options to use an alternate socket path:
# --output-plugin plugins.socket --output-plugin-config-data '{"socket-path": "/tmp/some-other-path.sock"}'

class Plugin:
    
    def __init__(self, parent, options):
        self._config = {'socket_path': '/tmp/rislive.sock'}
         
        if options.output_plugin_config_data:
            self._config = json.loads(options.output_plugin_config_data)

        self._sock = s.socket(s.AF_UNIX, s.SOCK_DGRAM)
        self._sock.connect(self._config['socket-path'])
            
    def send_message(self, msg):
        try:
            self._sock.send(msg.encode())
        except BaseException as e:
            print(str(e))
        
    def format(self, msg):
        return(msg)
