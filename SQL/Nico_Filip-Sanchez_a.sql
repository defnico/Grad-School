select distinct facility_name
from violations
where facility_name like '%cafe%' and violation_code = 'F030';
