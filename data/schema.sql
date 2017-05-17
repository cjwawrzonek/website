-- if want to add a column name that is a keyword, use 'quotes'
-- drop table if exists project_thumbnails;
create table projects (
  id integer primary key autoincrement,
  title text not null,
  summary text not null,
  thumbnail_img_url text not null,
  'text' text not null
);