select distinct facility_name
from inspections
where facility_id not in (
	select facility_id
	from violations)
order by facility_name asc;
