import csv
import sys
import argparse


parser=argparse.ArgumentParser()

parser.add_argument("--content", help="A path to rates CSV file")

args=parser.parse_args()

# TODO: do something with the content

result = csv.writer(sys.stdout, lineterminator='\n')
result.writerow(
    ['rate_name', 'class', 'quality', 'bathroom', 'bedding', 'capacity', 'club', 'bedrooms', 'balcony', 'view', 'floor']
)

with open(args.content) as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        result.writerow(
            ['Test Room', 'villa', 'deluxe', 'private bathroom', 'bunk bed', 'double', 'not club', '1 bedroom',
             'with balcony', 'mountain view', 'attic floor']
        )
