#!/usr/bin/env python
import csv, sys
from argparse import ArgumentParser
from ldif import LDIFParser

# Parse command-line arguments
arg_parser = ArgumentParser(description='Parse LDIF data and reformat as CSV')
arg_parser.add_argument('--columns', '-c', help='Comma-separated list of attributes to include in CSV output')
arg_parser.add_argument('--file', '-f', help='LDIF file (default is stdin)')
arg_parser.add_argument('--output', '-o', help='Output file (default is stdout)')
arg_parser.add_argument('--no-header', action='store_true', help='Omit header row')
args = arg_parser.parse_args()

# Parse LDIF
records = []
attributes = set()

class LDIF(LDIFParser):
    def handle(self, dn, entry):
        """
        This handler simplifies incoming LDIF data by reducing any multi-valued attributes
        to single, comma-delimited values. It also converts the attribute names to all-
        lowercase.

        This is done so that the attribute list specified on the command line
        can be case-insensitive. The trade-off is that if there are objects returned
        with attributes whose names only differ by case, there will be a dictionary key
        collision, and it will most likely be unpredictable which of the two attributes
        is stored in the entry's dictionary afterward.
        """
        simplified = {}
        for attr, vals in entry.items():
            simplified[attr.lower()] = ', '.join(vals)
            attributes.add(attr.lower())
        records.append(simplified)

if args.file and args.file != '-':
    input_file = open(args.file, 'r')
else:
    input_file = sys.stdin
    
ldif_parser = LDIF(input_file)
ldif_parser.parse()

# Generate CSV
if args.columns:
    csv_fields = args.columns.lower().split(',')
else:
    csv_fields = attributes

if args.output and args.output != '-':
    output_file = open(args.output, 'w')
else:
    output_file = sys.stdout

writer = csv.DictWriter(output_file, fieldnames=csv_fields)

if not args.no_header:
    writer.writeheader()

for record in records:
    # Prune out unwanted keys so writer.writerow will not throw ValueError exception
    pruned = {}
    for field in csv_fields:
        if field in record:
            pruned[field] = record[field]
    if len(pruned):
        writer.writerow(pruned)
