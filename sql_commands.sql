create database `hotel database`;
use `hotel database`;

create table `rates` (
`room type` int (3) primary key,
`beds` int(2) not null,
`AC` bool NOT NULL DEFAULT FALSE,
`rate` int(6) not null,
check (`AC` between 0 and 1) -- bool defaults to tinyint(1) which can also be 2,3 etc.
);

/*
 We use constraint on rooms rather than types because you
 should not have rooms without types, but you may want to upgrade
 some of the existing rooms to a new type
*/

create table `rooms` (
`room number` int (6) primary key,
`room type` int (3),
`occupied` bool NOT NULL default False,
foreign key (`room type`) references `rates` (`room type`) -- since the manager can add new room types anytime he/she wants, but not the other way round
ON UPDATE CASCADE ON DELETE RESTRICT
);

create user 'guest'@'localhost';
revoke all on *.* from 'guest'@'localhost';
grant select on `hotel database` . `rates` to 'guest'@'localhost';
grant select(`room number`), select(`room type`), select(`occupied`) on `hotel database` . `rooms` to 'guest'@'localhost';

create user 'manager'@'localhost';
revoke all on *.* from 'manager'@'localhost';
grant all on `hotel database` . * to 'manager'@'localhost' with grant option;



-- vim: et
