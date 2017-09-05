
"""" Part of JobMan
This program is intended for test of JobMan.
It's only purpose is to be started in 100 different copies,
to calculate some values, which is returned as results.
More specific it's called with a commandline option, a number n
between 1-100. It will then walk through all numbers n, n+100, n+200
until reaching 100.000, and for each checking if that number is prime.
Nothing more - quite pointless - but suited to test JobMan..."""

__version__ = '0.2'
__build__ = '2017-08-08 09:07'

import sys


def usage():
    print "Usage:  spndtime.py n\n\twhere n is an integer [1..100]"


def is_prime(n):
    for i in range(3, n):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    print "Begin..."
    if len(sys.argv) > 1:
        try:
            m = int(sys.argv[1])
        except:
            usage()
            sys.exit(998)
        fil_out = open('spndtime_{}.ecr'.format(str(m)), "w")
        print "Running spndtime for {}".format(str(m))
        while m < 100000:
            if is_prime(m):
                fil_out.write(str(m)+"\n")
            m += 100
        fil_out.close()
    else:
        usage()
        sys.exit(999)
    print "Done... {}".format(str(m))
