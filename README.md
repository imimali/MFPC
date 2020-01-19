# Two Phase Locking
This document does not yet have a predefined structure, it just serves
as the dumping ground of my ideas regarding design decisions about this projec

- rollback by selecting from every involved table every involved row, saving them
as json. The rollback then purges everything from the involved tables and inserts
every row back from the saved json.
- ```is_explicit``` tells whether the names of the rows are explicitly specified by the parameters,
that is, whether the query is of the form:
```postgresql
INSERT INTO table_name (id,name, whatever) VALUES (1,'Simon Petrikov',2)
```
or of the form  
```postgresql
INSERT INTO table_name VALUES (1,'Simon Petrikov',2)
```
- the key of a resource is specified not only by the possible id of a row
in a table, but by the name of the database and the table it resides in too
