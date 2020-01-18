select distinct facility_name
from inspections
where score >= all(
		select score
		from inspections);
