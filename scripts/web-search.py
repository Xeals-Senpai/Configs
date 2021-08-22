#!/usr/bin/python3

########################################
##### Rofi Web-search script ###########
########################################

import json
import re
import urllib.parse
import urllib.request
import sys
import os
import datetime
import gzip

import subprocess as sp

import html

# URLs configurations

CONFIG = {
    'BROWSER_PATH' : {
        'firefox' : ['firefox']
    },

    'USER_AGENT' : {
        'firefox' : ' 	Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'
    },

    'SEARCH_ENGINE_NAME' : {
        'google' : 'Google'
    },

    'SEARCH_URL' : {
        'google' : 'https://www,google.com/search?q='
    },

    'SUGGESTION_URL' : {
        'google' : 'https://www.google.com/complete/search'
    }

    def cleanhtml(txt):
        return re.sub(r'<.*?>', '', txt)

    def fetch_suggestions(search_string ):
        if SEARCH_ENGINE == 'google':
            r = {
            'q' : search_string,
            'cp' : '11',
            'client' : 'psy-ab',
            'xssi' : 't',
            'gs_ri' : 'gws-wiz',
            'hl' : 'en-IT',
            'authuser' : '0'
            }

            url = urllib.request.Request(url, headers=headers, method='GET')
            reply_data = gzip.decompress(urllib.request.urlopen(req).read()).split(b'\n')[1]
            reply_data = json.loads(reply_data)
            
            return [ cleanhtml(res[0]).strip() for res in reply_data[0] ]

    def main() :
        search_string = html.unescape((''.join(sys.argv[1:])).strip())

        if search_string.endswith('!'):
            search_string = search_string.rstrip('!').strip()
            results = fetch_suggestions(search_string)
            for r in results:
                print(html.unescape(r))
            elif search_string == '':
                print('!!-- Please type something and search it with %s' % CONFIG[ 'SEARCH_ENGINE_NAME'])
                print('!!-- Close your search query with "!" to get suggestions')
            else:
                url = CONFIG['SEARCH_URL'] [SEARCH_ENGINE] + urllib.parse.quote_plus(search_string)
                sp.Popen(CONFIG['BROWSER_PATH'][BROWSER]+ [url], stdout=sp.DEVNULL, stderr=sp.DEVNULL, shell=False)

    def validate_config(c):
    if type(c) != dict:
        print('Configuration file must be a JSON object', file=sys.stderr)
        sys.exit(1)
    for k in ('SEARCH_ENGINE', 'BROWSER', 'TERMINAL'):
        if k not in c:
            print('Configuration file is missing %s' % k, file=sys.stderr)
            sys.exit(1)
    for k in ('SEARCH_ENGINE', 'BROWSER'):
        if type(c[k]) != str:
            print('Configuration Error: The value of %s must be a string' % k, file=sys.stderr)
    if type(c['TERMINAL']) != list:
        print('Configuration Error: The value of TERMINAL must be a list of strings', file=sys.stderr)
        sys.exit(1)
    for x in c['TERMINAL']:
        if type(x) != str:
            print('Configuration Error: The value of TERMINAL must be a list of strings', file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    try:
        fname = os.path.expanduser('~/.config/rofi-web-search/config.json')
        if os.path.exists(fname):
            try:
                config = json.loads(open(fname, 'r').read())
            except json.JSONDecodeError:
                print('Configuration file %s is not a valid JSON' % fname, file=sys.stderr)
                sys.exit(1)
            validate_config(config)
            SEARCH_ENGINE = config['SEARCH_ENGINE']
            BROWSER = config['BROWSER']
            TERMINAL = config['TERMINAL']
        else:
            # Create default config
            config = {
                    'SEARCH_ENGINE' : SEARCH_ENGINE,
                    'BROWSER' : BROWSER,
                    'TERMINAL' : TERMINAL
                }
            os.makedirs(os.path.dirname(fname))
            f = open(fname, 'w')
            f.write(json.dumps(config, indent=4))
            f.write('\n')
            f.close()
        main()
    except:
        sys.exit(1)
}