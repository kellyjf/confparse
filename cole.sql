drop table if exists systems;
drop table if exists bearers;
drop table if exists radios;
drop table if exists aps;

create table systems (
  serial varchar(16),
  version int
);

create table bearers (
  serial varchar(16),
  bearer varchar(32),
  enabled boolean
);

create table radios (
  serial varchar(16),
  device varchar(32),
  cabin boolean,
  fbo boolean
);

create table aps (
  serial varchar(16),
  device varchar(32),
  ssid varchar(128),
  psk varchar(128)
);


