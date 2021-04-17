postgresql database installation
=

This document describes the creation of the battleship database in the postgresql server.
It is assumed that the postgresql server is installed and running.
See https://fedoraproject.org/wiki/PostgreSQL for installing postgresql on Fedora. 

## check the status of the postgresql server

1. login as root:

```shell script
# login as root
$ sudo -i
```

2. when root login as the postgres user:

```shell script
$ su - postgres
```

3. connect to the postgresql server
```shell script
$ psql
```


## create the battleship database
This section describes the actual creation of the battleship database in the postgresql server
It is assumed you are connected to postgresql database, see previous section

execute the following commands in the postgresql server
```
postgres=# create database battleship encoding 'utf8';
postgres=# create user battleship_owner with encrypted password 'battleship_owner' login ;
postgres=# grant all privileges on database battleship to battleship_owner;
```

disconnect from the postgresql server
```shell script
postgres=# \q
```

## connect to the battleship database

```shell script
$ PGPASSWORD=battleship_owner psql --host=localhost --username=battleship_owner --dbname=battleship
```

## install the uuid-ossp module
The uuid-ossp module is used to generate uuid's

1. login as root:

```shell script
# login as root
$ sudo -i
```

2. when root login as the postgres user:

```shell script
$ su - postgres
```

3. install the uuid-ossp module in the battleship database
```shell script
$ psql -d battleship -c 'create extension "uuid-ossp";' 
```

4. check as normal user if the module is installed
```shell script
$ PGPASSWORD=battleship_owner psql --host=localhost --username=battleship_owner --dbname=battleship
postgres=# select * from pg_extension;
```

## other postgresql commands

* switch database : \c
* show databases  : \l
* show tables     : \dt
* show users      : \du
* exit            : \q
  

