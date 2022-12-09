# LookInnaBook
Project for COMP3005 Databases course

# Setting up the Database
In PGAdmin, create an empty database on a server 
(for an easier setup process, use the following parameters: username 'postgres', password 'pass' hostname 'localhost' port '5432' and db_name 'Final_project')
- run the DDL_setup.sql file on the database 
- run the DML_setup.sql file.

Your database is good to go with someexample books

# using the database
From there, you can choose either the client.py or the backend.py file provided in the clients directory. The client can log in (feel free to use the default user, isaacwbg@gmail.com with password 'password') and make orders for books, and the backend can log in to make new books.

If you deviated from the suggested parameters earlier, you will have to modify the client.py and backend.py files at the top to match the connection parameters of your own database.
