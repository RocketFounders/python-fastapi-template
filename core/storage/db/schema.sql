BEGIN;
drop table if exists api_profile;
drop type if exists role;

create type role as enum ('admin', 'guest', 'junior', 'expert', 'worker');

create table if not exists api_profile
(
    id           varchar(16) primary key,
    username     varchar(32)  not null,
    password     varchar(256) not null,
    email        varchar(128) not null,
    phone_number varchar(16)  not null,
    first_name   varchar(32),
    last_name    varchar(32),
    photo_url    text,
    role         role default 'guest',
    is_internal  bool default false
);

alter table api_profile alter column id set default 'pr_'::text  || substr(random()::text, 3, 13);

COMMIT;
