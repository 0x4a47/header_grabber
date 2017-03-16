import argparse
import requests
import sys
import json
from urlparse import urlparse
import os.path

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
        #sys.exit()
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print "There was a timeout, try again."
        #sys.exit()
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print "There were TooManyRedirects"
        #sys.exit()
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

        # if "Server" == header:
            # print header,value
        print header,value
        #print header, value
        num_headers_printed += 1

    #python 3.0 implementation for those who upgraded already
    #for header, value in d.items():
    #    print header, value
    #    num_headers_printed += 1

    print num_headers_printed

def main():
    fqdn =''
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', nargs='+',help='http/https FQDN.',default=None)
    parser.add_argument('-i', '--ifile', nargs='+',help='Load domains from a .txt file.',default=None)
    args = parser.parse_args()

    #check that both arguments are not set
    if args.domain is not None and args.ifile is not None:
        print "Can only specify one of either -d or -i"
        sys.exit()

    #check that the arguments exist so it doesnt try to load every run.
    #-d option functionaltu
    if args.domain is not None:
        #[DEBUG]
        #print "Domain argument specified"

        #remove it from the array and store it in a domain name variable.
        fqdn = vars(args)['domain'][0]
        if uri_validator(fqdn) is True:
            #[DEBUG]
            #print 'True'
            #make the request and get the headers
            #set the return headers to r_headers
            r_headers = request_headers(fqdn)
            #extract the header information from the server.
            parse_headers(r_headers)
            print "x"

        else:
            print 'Please enter a valid URL/domain'
            sys.exit()

    #-i option functionality
    if args.ifile is not None:
        #[DEBUG]
        #print "input file specified"
        #remove it from the array and store it in the ifile variable
        ifile = vars(args)['ifile'][0]
        #extract the file extension and check it is a text file
        file_extension = os.path.splitext(ifile)[1]
        if file_extension == ".txt":
            #[DEBUG]
            #print "Valid"
            with open(ifile) as f:
                for file_fqdn in f:
                    if uri_validator(file_fqdn) is True:
                        #[DEBUG]
                        #print 'True'
                        #make the request and get the headers
                        #set the return headers to r_headers
                        print "Requesting:", file_fqdn
                        r_headers = request_headers(file_fqdn)
                        if r_headers is not None:
                            #extract the header information from the server.
                            #[DEBUG]
                            #print r_headers
                            parse_headers(r_headers)
                        else:
                            continue
                    else:
                        print file_fqdn, " Is an invalid domain / url"

        else:
            print "Invalid file. Please provide a valid .txt file"
            sys.exit()





if __name__ == '__main__':
    main()
