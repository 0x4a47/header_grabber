# header_grabber
Grabs the HTTP Response headers from specified domains. Looks specifically for the 'Server' header but can be configured for anything.

```
usage: header_grabber.py [-h] [-d DOMAIN [DOMAIN ...]] [-i IFILE [IFILE ...]]

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN [DOMAIN ...], --domain DOMAIN [DOMAIN ...]
                        http/https FQDN.
  -i IFILE [IFILE ...], --ifile IFILE [IFILE ...]
                        Load domains from a .txt file.

```
