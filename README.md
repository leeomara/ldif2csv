# ldif2csv
Author: [Darren Struthers](mailto:struthdm@plu.edu)

This is a basic script to reformat LDIF data as CSV. It is designed to receive
output from ldapsearch directly over STDIN.

## Basic Usage

    $ ldapsearch sn=Anderson | python ldif2csv.py -c uid,sn,givenName

Run `python ldif2csv.py -h` for more detailed usage information.

## Installation

If you want to be fancy and install this utility on your system, you can do
something like:

    $ sudo cp ldif2csv.py /usr/local/bin/ldif2csv
    $ sudo chmod +x `which ldif2csv`
