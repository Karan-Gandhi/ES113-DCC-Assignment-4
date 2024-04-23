CREATE USER 'testing'@'%' IDENTIFIED BY 'password'; 
GRANT ALL PRIVILEGES ON *.* TO 'testing'@'%' WITH GRANT OPTION;

use dccassignment4;
set sql_safe_updates = 0;
update purchased set Denominations = replace(Denominations, ",", "");
alter table purchased modify column denominations bigint;
update encashed set denominations = replace(denominations, ",", "");
alter table encashed modify column denominations bigint;
