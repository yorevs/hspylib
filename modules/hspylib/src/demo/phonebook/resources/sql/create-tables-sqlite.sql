drop table if exists PERSONS;

create table if not exists PERSONS
(
  UUID       TEXT    not null,
  EMAIL      TEXT    not null,
  NAME       TEXT    not null,
  AGE        INTEGER not null,
  PHONE      TEXT    null,
  ADDRESS    TEXT    null,
  complement TEXT    null,

  constraint PERSONS_pk primary key (UUID),
  constraint PERSONS_uk unique (EMAIL)
);

drop table if exists COMPANIES;

create table if not exists COMPANIES
(
  UUID       TEXT not null,
  CNPJ       TEXT not null,
  NAME       TEXT not null,
  WEBSITE    TEXT null,
  PHONE      TEXT null,
  ADDRESS    TEXT null,
  COMPLEMENT TEXT null,

  constraint COMPANIES_pk primary key (UUID),
  constraint COMPANIES_uk unique (CNPJ)
);
