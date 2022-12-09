insert into users
VALUES      (1, 'K2L 1Z8', '72 Peary Way', 'isaacwbg@gmail.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', '72 Peary Way', '72 Peary Way'), -- password is 'password'
            (2, 'K2L 3H4', '11 Baeldrung Way', 'dragon@gmail.com', 'a9c43be948c5cabd56ef2bacffb77cdaa5eec49dd5eb0cc4129cf3eda5f0e74c', '11 Baeldrung Way','11 Baeldrung Way'); -- password is 'dragon'

insert into publisher
VALUES      ('Puffin Classics', '72 Baeldrung Crescent', 'pclassics@puff.com', 6138057007, '11023201231'),
            ('BooksBooksBooks', '11 Books Drive', 'books@booksbooks.com', 6138007555, 'A-609812322');


update publisher -- they moved
set address='12 Paper Way'
where pub_name='BooksBooksBooks';


insert into book
VALUES      (1, 'Stephen King', 'Revival', 'Puffin Classics', 20.80, 100, 'Thriller', 384, 0.025),
            (2, 'Stephen King', 'IT', 'BooksBooksBooks', 20.80, 12, 'Thriller', 299, 0.030),
            (3, 'Roald Dahl', 'James and the Giant Peach', 'Puffin Classics', 11.95, 22, 'Children', 140, 0.100),
            (4, 'Leo Tolstoy', 'War and Peace', 'BooksBooksBooks', 28.17, 8, 'Political', 210, 0.011);

-- didn't insert into holds or orders because there are no holds by default! Users will
-- make them using the client

insert into owners
VALUES      ('Root', 'root@root.com', 'Root', 'Rootkins', 6133011799,'4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2' ); -- obviously the password is 'root'
