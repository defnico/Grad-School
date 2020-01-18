select facility_name
from violations
group by facility_name
having count(facility_id) >= all(select count(facility_id) from violations group by facility_id);
