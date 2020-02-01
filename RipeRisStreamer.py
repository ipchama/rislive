#!/usr/bin/python3

import asyncio
import websockets
import json
import ssl
import logging
import os
from importlib import import_module

class RipeRisStreamer:
    """A class for streaming updates from the RIPE RIS Live project"""

    def __init__(self, options):
        self._options = options
        self._ws = None

        self._sslcontext = ssl.create_default_context()
        self._sslcontext.check_hostname = False
        self._sslcontext.verify_mode = ssl.CERT_NONE

        self._report = self._send_message_screen
        self._format = self._format_none

        if(self._options.output_plugin):
            imported_module = import_module(self._options.output_plugin)            
            plugin = imported_module.Plugin(self, options)
            
            self._report = plugin.send_message
            self._format = plugin.format

    def _format_none(self, msg):
        return(msg)
    
    def _send_message_screen(self, msg):
        print(msg)

    def disconnect(self):
        self._ws.close()
        return(True)    

    def start_streaming(self):      
        async def _start_streaming(uri):
            logging.debug("Going to create websocket connection...")
            async with websockets.connect(uri, ssl=self._sslcontext) as websocket:
                self._ws = websocket
                
                logging.debug("Sending RIS parameters...")
                await websocket.send(self._get_ris_params())
                
                logging.debug("Going to start the reception loop...")
                async for message in websocket:
                    try:
                        self._report(self._format(message))
                    except Exception as e:
                        print(str(e))
                        pass            
                    
        asyncio.get_event_loop().run_until_complete(_start_streaming('wss://ris-live.ripe.net/v1/ws/?client=RipeRisStreamer'))

    def _get_ris_params(self):
        #params = {
        #    "moreSpecific": True,
        #    "host": "rrc21",
        #    "socketOptions": {
        #        "includeRaw": True
        #    }
        #}
        
        params = {}
        
        if self._options.include_raw:
            params['socketOptions']['socketOptions'] = {'includeRaw': True}

        if self._options.filter_host:
            params['host'] = self._options.filter_host

        if self._options.filter_type:
            params['type'] = self._options.filter_type

        if self._options.filter_key:
            params['require'] = self._options.filter_key

        if self._options.filter_peer:
            params['peer'] = self._options.filter_peer

        if self._options.filter_aspath:
            params['path'] = self._options.filter_aspath

        if self._options.filter_prefix:
            params['prefix'] = self._options.filter_prefix

        if self._options.match_more_specific:
            params['moreSpecific'] = self._options.match_more_specific

        if self._options.match_less_specific:
            params['lessSpecific'] = self._options.match_less_specific

        return(json.dumps({
            "type": "ris_subscribe",
            "data": params
        }))
