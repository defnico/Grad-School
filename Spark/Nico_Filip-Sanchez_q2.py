from __future__ import print_function
from pyspark import SparkContext
import sys

if len(sys.argv) != 3:
    print("Usage: q2.py <input_file> <output_file>", file=sys.stderr)
    sys.exit(-1)
sc = SparkContext(appName="q2")

input_file = sys.argv[1]
output_file = sys.argv[2]
lines = sc.textFile(input_file)


def bar_price_mapper(s):
    arr = s.split(',')
    bar = arr[0]
    price = int(arr[2])
    return bar, price


barsToPrices = lines.map(bar_price_mapper)

barsToTotalAndCount = barsToPrices.aggregateByKey((0, 0), \
                                                  lambda U, v: (U[0] + v, U[1] + 1), \
                                                  lambda U, V: (U[0] + V[0], U[1] + V[1]))

barsToAvg = barsToTotalAndCount.mapValues(lambda total_count: total_count[0] / total_count[1])

output = barsToAvg.collect()

of = open(output_file, "w")
of.write('Bar\tAverage_price\n')
for (bar, avg) in output:
    of.write('{}\t{}\n'.format(bar, avg))
of.close()
