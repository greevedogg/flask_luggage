drop table if exists luggage;
create table luggage (
  id integer primary key autoincrement,
  name text not null,
  ticket text not null,
  location text not null,
  bagCount text not null
);
