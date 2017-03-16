import argparse
import requests
import sys
import json
from urlparse import urlparse

def uri_validator(x):
    try:
        result = urlparse(x)
        #[DEBUG]
        #print result
        #check for http or https and that there is actually a domain name
        if result.scheme == 'https' or result.scheme == 'http' and result.netloc:
            return True
        else:
            return False
    except:
        return False

def request_headers(url):
    try:
        r = requests.get(url)
        return r.headers
    #http://docs.python-requests.org/en/master/_modules/requests/exceptions/
    #parse specific errors
    except requests.exceptions.ConnectionError:
        print "The was a connection error, check your domain!"
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print "There was a timeout, try again."
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print "There were TooManyRedirects"
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print "This is bad."
        #[DEBUG]
        #print e
        sys.exit(1)

def parse_headers(headers):
    #for each header specified in https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
    #create an if to check whether it exists in the response. If so, print the value.

    #store the number of headers in the response.
    #then, increment each 'print' of a header by 1 to check if any header was missed.
    #if a header was missed, the response contained custom headers and should be
    #manually checked.
    num_headers_present = len(headers)
    num_headers_printed = 0
    # print "Last-Modified:",headers['Last-Modified']
    # print "X-Powered-By:", headers['X-Powered-By']
    # print "Content-Length:", headers['Content-Length']

    print "[Found ",num_headers_present, "headers]"
    #Big 'switch' like if statement for printing of the headers.
    #[TO-DO] could be changed to a for each?
    #Server should be first as it is the most important for this PoC.
    #if "Access-Control-Allow-Credentials" in headers:

    #Python 2.7 implementation.
    for header, value in headers.iteritems():
        #[TEMP] filter out set-cookie for the moment.
        #header filter
        if "Set-Cookie" == header:
            continue
        print header, value
        #print header, value
        num_headers_printed += 1

    #python 3.0 implementation for those who upgraded already
    #for header, value in d.items():
    #    print header, value
    #    num_headers_printed += 1

    print num_headers_printed

    #[LIST OF 'COMMON' RESPONSE HEADERS]
    # Access-Control-Allow-Credentials
    # Access-Control-Allow-Headers
    # Access-Control-Allow-Methods
    # Access-Control-Allow-Origin
    # Access-Control-Expose-Headers
    # Access-Control-Max-Age
    # Accept-Ranges
    # Age
    # Allow
    # Alternate-Protocol
    # Cache-Control
    # Client-Date
    # Client-Peer
    # Client-Response-Num
    # Connection
    # Content-Disposition
    # Content-Encoding
    # Content-Language
    # Content-Length
    # Content-Location
    # Content-MD5
    # Content-Range
    # Content-Security-Policy
    #X-Content-Security-Policy
    # X-WebKit-CSP
    # Content-Security-Policy-Report-Only
    # Content-Type
    # Date
    # ETag
    # Expires
    # HTTP
    # Keep-Alive
    # Last-Modified
    # Link
    # Location
    # P3P
    # Pragma
    # Proxy-Authenticate
    # Proxy-Connection
    # Refresh
    # Retry-After
    # Server
    # Set-Cookie
    # Status
    # Strict-Transport-Security
    # Timing-Allow-Origin
    # Trailer
    # Transfer-Encoding
    # Upgrade
    # Vary
    # Via
    # Warning
    # WWW-Authenticate
    # X-Aspnet-Version
    # X-Content-Type-Options
    # X-Frame-Options
    # X-Permitted-Cross-Domain-Policies
    # X-Pingback
    # X-Powered-By
    # X-Robots-Tag
    # X-UA-Compatible
    # X-XSS-Protection


def main():
    fqdn =''
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', nargs='+',help='http/https FQDN.',default=None)
    parser.add_argument('-i', '--ifile', nargs='+',help='Load domains from input file.',default=None)

    args = parser.parse_args()
    #remove it from the array and store it in a domain name variable.
    fqdn = vars(args)['domain'][0]
    if uri_validator(fqdn) is True:
        #[DEBUG]
        #print 'True'
        #make the request and get the headers
        #[TO-DO]
        #print parse_headers(request_headers(fqdn))
        #set the return headers to r_headers
        r_headers = request_headers(fqdn)
        #extract the header information from the server.
        parse_headers(r_headers)

    else:
        print 'Please enter a valid URL/domain'



if __name__ == '__main__':
    main()
