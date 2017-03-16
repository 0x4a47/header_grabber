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
    print "Content-Type:",headers['Content-Type']
    #print headers['Content-Type']


def main():
    fqdn =''
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', nargs='+',help='http/https FQDN.',default=None)

    args = parser.parse_args()
    #remove it from the array and store it in a domain name variable.
    fqdn = vars(args)['domain'][0]
    if uri_validator(fqdn) is True:
        #[DEBUG]
        #print 'True'
        #make the request and get the headers
        #[TO-DO]
        #print parse_headers(request_headers(fqdn))
        print request_headers(fqdn)
    else:
        print 'Please enter a valid URL/domain'



if __name__ == '__main__':
    main()
