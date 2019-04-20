# RisLive

A python script, and docker image, to start making use of RIPE's new RIS Live prototype service.  Includes an option to provide a plugin for handling the incoming RIS data is available.

## Getting Started

Just download and run, or feel free to grab the docker image at https://cloud.docker.com/repository/docker/dockerhama/riperis

If you've already got docker and docker-compose installed, then `docker-compose -f docker-compose.yml up` will take care of the rest.

### Dependencies
Python 3.7

See requirements.txt ( or just pip it :p )

## Examples
Writing to a unix domain socket for streaming to influxdb via telegraf:
```
ripeRisLive.py --host rrc21 -o socket -s /etc/telegraf/risdata.sock --format influx
```

Sending the RIPE RIS Live feeds straight to stdout:
```
ripeRisLive.py --host rrc21
```

## Options
I attempted to provide 1:1 access to all the available filters that the RIS Live service provides: 
```
optional arguments:
  -h, --help            show this help message and exit
  --host FILTER_HOST, -fh FILTER_HOST
                        Only include messages collected by a particular RRC.
  --type {UPDATE,OPEN,NOTIFICATION,KEEPALIVE,RIS_PEER_STATE}, -t {UPDATE,OPEN,NOTIFICATION,KEEPALIVE,RIS_PEER_STATE}
                        Only include messages of a given BGP or RIS type.
  --require-key FILTER_KEY, -k FILTER_KEY
                        Only include messages containing a given key. Useful
                        values are "announcements" or "withdrawals".
  --peer FILTER_PEER, -p FILTER_PEER
                        Only include messages sent by the given BGP peer.
  --aspath FILTER_ASPATH, -ap FILTER_ASPATH
                        Match based on the ASNs in the AS path. Can optionally
                        begin with ^ to only match the beginning of the path,
                        or end with $ to only match the end of the path. e.g.
                        "^123,456,789$"
  --prefix FILTER_PREFIX, -cp FILTER_PREFIX
                        Only include UPDATE messages concerning a particular
                        prefix.
  --more-specific MATCH_MORE_SPECIFIC, -m MATCH_MORE_SPECIFIC
                        If true, match prefixes that are more specific (part
                        of) prefix.
  --less-specific MATCH_LESS_SPECIFIC, -l MATCH_LESS_SPECIFIC
                        If true, match prefixes that are less specific
                        (contain) prefix.
  --include-raw INCLUDE_RAW, -r INCLUDE_RAW
                        Include a Base64-encoded version of the original
                        binary BGP message.
  --output-plugin OUTPUT_PLUGIN, -op OUTPUT_PLUGIN
                        Load an external plugin to process incoming RIS data.
                        This will override other output and format options.
  --output {screen,socket}, -o {screen,socket}
                        Where to send the data. Defaults to stdout.
  --socket-path SOCKET_PATH, -s SOCKET_PATH
                        The filename of the unix dgram on which the consumer
                        is listening. Defaults to /tmp/risdata.sock.
  --format {influx}, -f {influx}
                        Alternate output format.
  --auto-reconnect AUTO_RECONNECT, -ar AUTO_RECONNECT
                        Auto-reconnect if the connection drops or is severed.
                        Defaults to True.
```
## Contributing

Contributions are welcome.

## Authors

* **IPCHama** - *Initial work* - [ipchama](https://github.com/ipchama)

## License

This project is licensed under the GPL v3 License - see the [LICENSE.md](LICENSE.md) file for details
