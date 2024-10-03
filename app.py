import csv
import sys
import argparse


parser=argparse.ArgumentParser()

parser.add_argument("--content", help="A path to rates CSV file")

args=parser.parse_args()


result = csv.writer(sys.stdout, lineterminator='\n')
result.writerow(
    ['rate_name', 'class', 'quality', 'bathroom', 'bedding', 'capacity', 'club', 'balcony', 'view']
)

with open(args.content) as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        result.writerow(
            ['Test Room', 'villa', 'deluxe', 'private bathroom', 'bunk bed', 'double', 'not club',
             'with balcony', 'mountain view']
        )
