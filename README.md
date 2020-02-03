# Two Phase Locking


## Requirements 
Proiect - o aplicatie concurenta distribuita la alegerea studentului. Aplicatia trebuie sa respecte urmatoarele cerinte:
- sa fie distribuita, dar nu simpla, client-server, ci pe mai multe nivele (client/web - business/middleware - date etc.).
- sa implice aspecte de concurenta la nivel de date externe manipulate (i.e. tranzactii in baze de date).
- sa foloseasca doua baza de date diferite (cel putin 3 tabele) si sa se foloseasca tranzactii distribuite. (nu este obligatoriu sa fie 2 servere distincte de baze de date)
- sa aiba cel putin 6-8 operatii/cazuri de utilizare.
- Foarte important: Sa implementeze o tranzactie distribuita la nivel aplicatie. Adica veti considera ca o tranzactie nu consta din operatii de read() si write() de pagini de memorie asa cum facem la curs ci veti considera o tranzactie ca fiind formata din operatii SQL simple (minim 3 instructiuni SQL - insert, delete, update, select) desigur, aceste operatii SQL vor opera pe tabele diferite. Trebuie sa asigurati, la nivel aplicatie, proprietatile ACID ale acestei tranzactii. Cu alte cuvinte sa se implementeze urmatoarele:

  - un algoritm de planificare (i.e. algoritm de controlul concurentei) din cele discutate la curs (bazat pe blocari sau pe ordonari, timestamp-uri etc.); algoritmul de planificare sa fie distribuit (e.g. 2 Phase Commit, 2 Phase Locking distribuit sau o forma distribuita de ordonare timestamp) si aplicatia sa foloseasca 2 baze de date. Cei care implementati planificare bazata pe ordonarea timestamp-urilor trebuie sa implementati obligatoriu si un mecanism de multiversionare si sa reporniti automat orice tranzactie la care planificatorul ii da abort.
  - un mecanism de rollback discutat la curs (multivesiuni, rollback pentru fiecare instructiune SQL simpla etc.)
  - un mecanism de commit (poate fi gandit impreuna cu cell de rollback)
  - un mecanism de detectie si rezolvare a deadlock-urilor (grafuri/liste de conflicte etc.)
  Atentie:: Focus-ul aplicatiei trebuie sa cada pe implementarea sistemului tranzactional, nu pe cazuri de utilizare, intrefata web sau frameworkuri pe care le-ati folosit. Puteti folosi framework-uri care sa va usureze munca (e.g. Hibernate sau alt JPA, Spring, .NET MVC etc.), dar nu trebuie sa folositi nici un fel de suport tranzactional de la acestea.


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
- the synced table holds an array of generic entities, and supports
deletion, addition and lookup of certain fields of these entities in a synchronized manner
## Future improvements  
- generalise key inference
- support multiple arguments for delete operation
- gracefully shut down cycle checker thread