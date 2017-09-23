-- if want to add a column name that is a keyword, use 'quotes'
drop table if exists appointments;
create table appointments (
  id integer primary key autoincrement,
  start integer,
  end integer,
  length integer,
  'date' text
);