import mysql.connector
import sys

output_file = open(sys.argv[1], "a")

cnx = mysql.connector.connect(user='inf551', password='inf551', host='127.0.0.1', database='inf551')
cursor = cnx.cursor()

query = """
select distinct facility_name
from inspections
where facility_id not in (
  select facility_id
  from violations)
order by facility_name asc;
"""

cursor.execute(query)

for name in cursor:
  output_file.write(''.join(name) + '\n')

output_file.close()
cursor.close()
cnx.close()
