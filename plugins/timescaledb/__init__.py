import json
import psycopg2

class Plugin:
    
    def __init__(self, parent, options):
        if not options.output_plugin_config_data:
            raise BaseException("Timescaledb plugin needs configuration data.")
        
        self._config = json.loads(options.output_plugin_config_data)

        self._connection = psycopg2.connect(
           user = self._config['username'],
           password = self._config['password'],
           host = self._config['host'],
           port = "5432",
           database = self._config['db'])
        
        self._connection.autocommit = True;
        
        self._cursor = self._connection.cursor()
        
        init_items = []
        
        if self._config.get('reset', False):
            init_items = ["DROP TABLE IF EXISTS events"]
        
        init_items.extend([            
            """
CREATE TABLE events (
  time        TIMESTAMPTZ               NOT NULL,
  peer        varchar(255)              NOT NULL,
  peer_asn    int                       NOT NULL,
  prefix      varchar(255)              ,
  next_hop    varchar(255)              ,
  id          varchar(255)              NOT NULL,
  type        varchar(255)              NOT NULL,
  origin      varchar(255)              NOT NULL,
  event_count      int                  NOT NULL
);""",
"SELECT create_hypertable('events', 'time');"
        ])
        
        for init_item in init_items:
            try:
                self._cursor.execute(init_item)
            except:
                pass

    def send_message(self, msg):

        try:
            msgobj = json.loads(msg).get('data')
            announcements = msgobj.get('announcements', False)
            if announcements:
                for announcement in announcements:
                    for prefix in announcement['prefixes']: 
                        self._cursor.execute("INSERT INTO events (time, peer, peer_asn, prefix, next_hop, id, type, origin, event_count) VALUES (TO_TIMESTAMP(%s), %s, %s, %s, %s, %s, %s, %s, 1)", [
                                msgobj['timestamp'],
                                msgobj['peer'],
                                msgobj['peer_asn'],
                                prefix,
                                announcement['next_hop'],
                                msgobj['id'],
                                msgobj['type'],
                                msgobj.get('origin', 'unk')
                            ])
            else:
                    self._cursor.execute("INSERT INTO events (time, peer, peer_asn, id, type, origin, event_count) VALUES (TO_TIMESTAMP(%s), %s, %s, %s, %s, %s, 1)", [
                            msgobj['timestamp'],
                            msgobj['peer'],
                            msgobj['peer_asn'],
                            msgobj['id'],
                            msgobj['type'],
                            msgobj.get('origin', 'unk')
                        ])
                
                
            self._connection.commit()
        except Exception as e:
            print(str(e))
        
    def format(self, msg):
        return(msg)