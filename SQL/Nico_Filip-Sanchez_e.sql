select grade, avg(score)
from inspections
where grade != ''
group by grade;
