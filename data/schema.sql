-- if want to add a column name that is a keyword, use 'quotes'
-- drop table if exists project_thumbnails;
create table post_summaries (
  id integer primary key autoincrement,
  prefix text not null,
  type text not null,
  title text not null,
  summary text not null,
  thumbnail_img_url text not null
);