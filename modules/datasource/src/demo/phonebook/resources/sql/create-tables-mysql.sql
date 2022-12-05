drop table if exists PERSONS;

create table if not exists PERSONS
(
  UUID       varchar(32)  not null,
  EMAIL      varchar(256) not null,
  NAME       varchar(60)  not null,
  AGE        int          not null,
  PHONE      varchar(20)  null,
  ADDRESS    varchar(512) null,
  complement varchar(256) null,

  constraint PERSONS_pk primary key (UUID),
  constraint PERSONS_uk unique key (EMAIL)
);

drop table if exists COMPANIES;

create table if not exists COMPANIES
(
  UUID       varchar(32)  not null,
  CNPJ       varchar(18)  not null,
  NAME       varchar(128) not null,
  WEBSITE    varchar(256) null,
  PHONE      varchar(20)  null,
  ADDRESS    varchar(512) null,
  COMPLEMENT varchar(256) null,

  constraint COMPANIES_pk primary key (UUID),
  constraint COMPANIES_uk unique key (CNPJ)
);
