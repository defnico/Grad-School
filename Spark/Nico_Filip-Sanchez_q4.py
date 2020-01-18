from __future__ import print_function
from pyspark import SparkContext
import sys

if len(sys.argv) != 5:
    print("Usage: q4.py <likes_file> <frequents_file> <sells_file> <output_file>", file=sys.stderr)
    sys.exit(-1)
sc = SparkContext(appName="q4")

likes_file = sys.argv[1]
frequents_file = sys.argv[2]
sells_file = sys.argv[3]
output_file = sys.argv[4]

likes = sc.textFile(likes_file)
frequents = sc.textFile(frequents_file)
sells = sc.textFile(sells_file)

barsToDrinkers = frequents.map(lambda s: (s.split(',')[1], s.split(',')[0]))

barsToBeers = sells.map(lambda s: s.split(','))
barsToBeers = barsToBeers.map(lambda s: (s[0], s[1]))

drinkersToBars = frequents.map(lambda s: s.split(','))

joinPairs = barsToDrinkers.leftOuterJoin(barsToBeers)

drinkerToBeer = likes.map(lambda s: s.split(','))

l = drinkerToBeer.map(lambda s: tuple(s))
d = joinPairs.map(lambda s: s[1])
intersectPairs = d.intersection(l)

of = open(output_file, "w")
of.write("Drinker\tBeer\n")
for kv in intersectPairs.collect():
    of.write("{}\t{}\n".format(kv[0], kv[1]))
of.close()
