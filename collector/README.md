
###Database


```
# sqlite3 collector.db

CREATE table bme(
  id int primary key not null,
  humidity real,
  pressure real,
  temperature real,
  timestamp integer
  );

CREATE table camera(
  id int primary key not null,
  filename char(50),
  timestamp integer
  );

CREATE table status(
  id int primary key not null,
  size integer,
  free integer,
  timestamp integer
  );
```
