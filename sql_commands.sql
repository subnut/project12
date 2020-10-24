create database `hotel database`;
use hotel database; -- yes, that's right, WITHOUT quotes or backticks
/* EVERYTHING that comes after the 'use' command (and before the ';') is taken as the database name */

create table `rates` (
`room type` int (3) primary key,
`beds` int(2) not null,
`rate` int(6) not null
);

create table `rooms` (
`room number` int (6)  primary key,
`room type` int (3),
`occupied` bool NOT NULL default False,
foreign key (`room type`) references `rates` (`room type`) -- since the manager can add new room types anytime he/she wants, but not the other way round
);

create user 'guest'@'localhost';
revoke all on *.* from 'guest'@'localhost';
grant select on `hotel database` . `rates` to 'guest'@'localhost';
grant select(`room number`), select(`room type`), select(`occupied`) on `hotel database` . `rooms` to 'guest'@'localhost';

create user 'manager'@'localhost';
revoke all on *.* from 'manager'@'localhost';
grant all on `hotel database` . * to 'manager'@'localhost' with grant option;



-- vim: et
