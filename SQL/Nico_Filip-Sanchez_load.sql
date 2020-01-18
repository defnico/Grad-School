drop database if exists inf551;
create database inf551;
use inf551;

create table violations (
  serial_number char(9),
  activity_date datetime,
  facility_name varchar(256),
  violation_code char(4),
  violation_description varchar(1024),
  violation_status varchar(64),
  points int,
  grade char(1),
  facility_address varchar(128),
  facility_city varchar(32),
  facility_id char(9),
  facility_state char(2),
  facility_zip char(5),
  employee_id char(9),
  owner_id char(9),
  owner_name varchar(64),
  pe_description varchar(256),
  program_element_pe int,
  program_name varchar(256),
  program_status varchar(16),
  record_id char(9),
  score int,
  service_code int,
  service_description varchar(128),
  row_id char(13)
);

load data local infile 'violations.csv' into table violations fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines;

create table inspections (
  serial_number char(9),
  activity_date datetime,
  facility_name varchar(256),
  score int,
  grade char(1),
  service_code int,
  service_description varchar(128),
  employee_id char(9),
  facility_address varchar(128),
  facility_city varchar(32),
  facility_id char(9),
  facility_state char(2),
  facility_zip char(5),
  owner_id char(9),
  owner_name varchar(64),
  pe_description varchar(256),
  program_element_pe int,
  program_name varchar(256),
  program_status varchar(16),
  record_id char(9)
);

load data local infile 'inspections.csv' into table inspections fields terminated by ',' enclosed by '"' lines terminated by '\n' ignore 1 lines;
