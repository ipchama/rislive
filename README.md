# RisLive

A python script, and docker image, to start making use of RIPE's new RIS Live prototype service.  Includes an option to provide a plugin for handling the incoming RIS data is available.

## Getting Started

Just download and run, or feel free to grab the docker image at https://hub.docker.com/r/dockerhama/riperis

If you've already got docker and docker-compose installed, then `docker-compose -f docker-compose.yml up` will take care of the rest.

### Dependencies
Python 3.7

See requirements.txt ( or just pip it :p )

## Examples

Sending the RIPE RIS Live feeds straight to stdout:
```
ripeRisLive.py --host rrc21
```

Sending the RIPE RIS Live feeds output to a domain socket:
```
ripeRisLive.py --more-specific true --host rrc21 --output-plugin plugins.socket --output-plugin-config-data '{"socket-path": "/tmp/some-path.sock"}'
```
## Plugins
Plugins are just normal python classes.  The easiest way to use one is to create a plugins directory in the same location as the main ripeRisLive script and add in your class directories.
The repo has a test plugin to be used as an example/boilerplate.  Plugins will be passed the parent RipeRisStream object and the argparse args object containing the original arguments passed to the script. The --output-plugin-config-data helper option is available to pass in plugin-specific data/configs.

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
  --output-plugin-config-data OUTPUT_PLUGIN_CONFIG_DATA, -opc OUTPUT_PLUGIN_CONFIG_DATA
                        Config data to be passed to the plugin if --output-
                        plugin was used. Will be passed as-is and format will
                        depend on the plugin.
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
