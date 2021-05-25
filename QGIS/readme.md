# Coordinates Title Label

```
[%concat(
	round(x(@map_extent_center), 2)
	, ' / '
	, round(y(@map_extent_center), 2)
)
%]
```

# Visualize tile extents

DB Manager:

```sql
with t as (
	select * from (values
		(7, 91, 51)
		, (7, 92, 52)
		, (7, 95, 53)
		, (7, 96, 53)
		, (7, 96, 56)
		, (7, 97, 53)
		, (7, 98, 53)
		, (7, 95, 54)
		, (7, 95, 55)
		, (7, 96, 55)
	) v (z, x, y)
)
select 
	row_number() over() fid
	, t.z
	, t.x
	, t.y
	, st_tileenvelope(t.z, t.x, t.y) geom
from t 
```
