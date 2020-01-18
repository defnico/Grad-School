from __future__ import print_function
from pyspark import SparkContext
import sys

if len(sys.argv) != 3:
    print("Usage: q1.py <input_file> <output_file>", file=sys.stderr)
    sys.exit(-1)
sc = SparkContext(appName="q1")

input_file = sys.argv[1]
output_file = sys.argv[2]
lines = sc.textFile(input_file)


def bar_price_mapper(s):
    arr = s.split(',')
    bar = arr[0]
    price = int(arr[2])
    return bar, price


def bud_filter(s):
    arr = s.split(',')
    if len(arr) == 3:
        beer = arr[1]
        return beer[0:3] == "Bud"
    else:
        return False


def price_filter(bar_prices):
    return max(bar_prices[1]) <= 5


barsToBudPrices = lines.filter(bud_filter).map(bar_price_mapper).groupByKey()
output = barsToBudPrices.filter(price_filter).mapValues(lambda l: len(l)).collect()

of = open(output_file, "w")
for (bar, count) in output:
    of.write("{}\t{}\n".format(bar, count))
of.close()
