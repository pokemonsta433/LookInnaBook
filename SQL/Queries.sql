select * from users where email='isaacwbg@gmail.com'; --when logging in, we do this. This will allow us to manipulate our user info and to learn if user needs registering
select user_id from users where email='isaacwbg@gmail.com'; -- saving our uid for future use
select author, title, price, genre, qty, book_id from book order by sales DESC; -- for our popular book section
select author, title, price, genre, qty, book_id from book where author like King order by sales DESC; -- for searching
select author, title, price, genre, qty, book_id from book where book_id = 2; -- when checking out, we can use the saved book_id
select email from publisher where pub_name='Puffin classics'; -- we can use this to get  the email of our publisher to request books
select bank_num from publisher where pub_name='Puffin classics'; -- we can use this to get the banking info of our publisher to send them money
insert into orders VALUES ('123 Address', '234 OtherAddress, 'processing', 'http://exampletrackinglink.com/order=A1234', 2022-12-09 01:51:03, null, 1); -- create a new order
select order_num from orders where start_t = 2022-12-09 01:51:03; -- find our new order numer

-- all the necessary things to make an order
update book set qty= qty - 1 where book_id = 1;
update book set sales= sales + 1 where book_id = 1;
insert into holds VALUES (1, 4, 1);
