#!/usr/bin/python3

import argparse
import signal
import sys
import RipeRisStreamer

# ripeRisLive --more-specific true --host rrc21 -o socket -s /etc/telegraf/risdata.sock --format influx

##### Install a signal handler for CTRL+C #####

def signal_handler(signal, frame, streamer):
    try:
        # Try to shut things down gracefully.
        print('Disconnecting...')
        streamer.disconnect()
    except BaseException as e:
        print(str(e))
        pass
    
    print('Shutting down...')
    sys.exit(0) # Raise a SystemExit exception

def main():

    ##### Get command-line arguments
    parser = argparse.ArgumentParser(description='Monitor the streams from Ripe RIS Live,')
    
    parser.add_argument('--host','-fh', dest='filter_host', default=None,
                        help='Only include messages collected by a particular RRC.')
    
    parser.add_argument('--type','-t', dest='filter_type', default=None, choices=["UPDATE", "OPEN", "NOTIFICATION", "KEEPALIVE", "RIS_PEER_STATE"],
                        help='Only include messages of a given BGP or RIS type.')

    parser.add_argument('--require-key','-k', dest='filter_key', default=None,
                        help='Only include messages containing a given key. Useful values are "announcements" or "withdrawals".')
    
    parser.add_argument('--peer','-p', dest='filter_peer', default=None,
                        help='Only include messages sent by the given BGP peer.')
    
    parser.add_argument('--aspath','-ap', dest='filter_aspath', default=None,
                        help='Match based on the ASNs in the AS path. Can optionally begin with ^ to only match the beginning of the path, or end with $ to only match the end of the path. e.g. "^123,456,789$"')
    
    parser.add_argument('--prefix','-cp', dest='filter_prefix', default=None,
                        help='Only include UPDATE messages concerning a particular prefix.')

    parser.add_argument('--more-specific','-m', dest='match_more_specific', default=False, type=bool,
                        help='If true, match prefixes that are more specific (part of) prefix.')

    parser.add_argument('--less-specific','-l', dest='match_less_specific', default=False, type=bool,
                        help='If true, match prefixes that are less specific (contain) prefix.')

    parser.add_argument('--include-raw','-r', dest='include_raw', default=False, type=bool,
                        help='Include a Base64-encoded version of the original binary BGP message.')

    parser.add_argument('--output','-o', dest='output', default='screen', choices=['screen', 'socket'],
                        help='Where to send the data.  Currently only "screen" is supported, which is the default.')
    
    parser.add_argument('--socket-path','-s', dest='socket_path', default='/tmp/risdata.sock',
                        help='The filename of the unix dgram on which the consumer is listening.')

    parser.add_argument('--format','-f', dest='format', default=None, choices=["influx"],
                        help='Alternate output format.')

    parser.add_argument('--auto-reconnect','-ar', dest='auto_reconnect', default=True, type=bool,
                        help='Auto-reconnect if the connection drops or is severed.')
                        
    args = parser.parse_args()
    
    
    ##### Prep the result handler
    streamer = RipeRisStreamer.RipeRisStreamer(args)

    # Register our signal handler.
    signal.signal(signal.SIGINT, lambda signal, frame: signal_handler(signal, frame, streamer))

    while args.auto_reconnect:
        try:
            streamer.start_streaming()
        except SystemExit:
            break
        except BaseException as e:
            print("Streamer broke down.")
    
    """
        Shut down everything - This will only be reached if we CTRL+C, but the disconnect should have already been performed by the signal handler,
        or if start_streaming() returns, which should not happen.
    """
    try:
        streamer.disconnect()
    except:
        pass
    
    return(0)

if __name__ == "__main__":
    main()
