
###Database


```
# sqlite3 collector.db

CREATE table bme(
  id integer primary key autoincrement not null,
  humidity real,
  pressure real,
  temperature real,
  timestamp real
  );

CREATE table camera(
  id integer primary key autoincrement not null,
  filename char(50),
  timestamp real
  );

CREATE table status(
  id integer primary key autoincrement not null,
  size integer,
  free integer,
  timestamp real
  );

```
