drop table if exists systems;
drop table if exists bearers;
drop table if exists radios;
drop table if exists aps;
drop table if exists a429s;
drop table if exists labels;
drop table if exists maps;
drop table if exists rcairshows;
drop table if exists functions;
drop table if exists ports;

create table functions (
  serial varchar(16),
  id     varchar(32),
  gpio   int 
);

create table a429s (
  serial varchar(16),
  id     varchar(32),
  parity varchar(8), 
  speed  varchar(8) 
);

create table labels (
  serial varchar(16),
  name   varchar(32), 
  label  varchar(8),
  port   int
);

create table maps (
  serial   varchar(16),
  mlabel   varchar(32), 
  alabel   varchar(32) 
);

create table systems (
  serial  varchar(16),
  version int,
  profile varchar(32),
  wow     varchar(16)
);

create table bearers (
  serial varchar(16),
  bearer varchar(32),
  enabled boolean
);

create table radios (
  serial varchar(16),
  device varchar(32),
  cabin  boolean,
  fbo    boolean,
  band   float
);

create table aps (
  serial varchar(16),
  device varchar(32),
  ssid varchar(128),
  psk varchar(128)
);

create table rcairshows (
  serial varchar(16),
  nonkey varchar(32),
  nonval varchar(128)
);

create table ports (
  serial varchar(16),
  name   varchar(16),
  equip  varchar(16),
  vid    int
);


