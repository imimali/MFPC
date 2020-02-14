
## A concurrent application, project topic of chioce: 
- it has to be distributed, but not just a simple app, instead, with multiple layers (client/web - business/middleware - date etc.).
- it has to involve aspects of concurrency at the level of external data(database transactions)
- use at least two databases (even if the database servers are the same), at least three tables to be involved
- at least 6-8 use-cases
- implement a distributed transaction at the level of the application. You will consider that a transaction is not made of read 
and write operation as we did at the course, but you will consider a transaction to be formed of simple SQL instructions
(at least three of the insert, update, delete, select), operating on different tables. you must assure on the level of the
application the ACID properties of these transactions. In other words, implement:
    - a scheduling algorithm, on of those discussed at the lectures(the ones based on timestamp ordering on locking, or ordering),
    the algorithm should be distributed, and use two databases. Those qho implement timestamp ordering must also implement
    a muldiversioning mechanism that restarts every transaction the scheduler aborts
    - a rollback mechanism (timestamp ordering, rollback for each sql instruction)
    - a commit mechanism (might be designed together with the rollback)
    - a deadlock detection and resolution method(graphs/conflict lists)
    
The focus of the application has to be on the transactional system, not on the frameworks used or on the UI. You can use any 
framework to make your work easier(Hibernate, JPA, Spring, .NET MVC) but you must not use any transactional support from those)

    
    
