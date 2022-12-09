create table Users -- Same deal, "User" is a keyword so we might as tell just call it "Users"
	(User_ID		SERIAL not null,
	 Postal_Code	varchar(7), -- Zip Codes not supported
	 Address		varchar(30),
	 Email			varchar(30) unique not null, -- they will use this to log in
	 Passwd			varchar(64) not null, -- SHA-256 is woefully inadequate in today's day and age but for this demo it's fine
	 Shipping_Addr	varchar(30) default null, -- default to address, but allow users to change their defaults seperately
	 Billing_Addr	varchar(30) default null,
	 primary key (User_ID)
	);

create table Publisher
	(Pub_Name			varchar(30) not null, -- Company names can be long
	 Address		varchar(30),
	 Email			varchar(30) not null,
	 Phone_Num		numeric(10,0),
	 Bank_Num		varchar(15) not null, -- should be enough to store bank numbers for every bank in Canada
	 primary key (Pub_Name)
	);

create table Book
	(Book_ID		numeric(7,0) not null,  -- this is the ISBN (truncated for size)
	 Author			varchar(20) not null,
	 Title		    varchar(50) not null,
	 Publisher		varchar(15) not null,
	 Price			numeric(5,2) not null, -- books shouldn't cost 1000+ dollars
	 Qty			numeric(5,0) not null, -- 10,000
	 Genre			varchar(20),
	 Pages			numeric(4,0) not null,
	 Pb_Royalty		numeric(4,3) not null, -- stored as a pecentage, so all numbers are between 0 and 1
	 Sales			numeric(7,0) not null default 0,
	 primary key (Book_ID),
	 foreign key (Publisher) references Publisher(Pub_Name)
	);

create table Orders --you can't actually call a table "Order", because it's an SQL keyword
	(Shipping_Addr		varchar(30) not null,
	 Billing_Addr		varchar(30) not null,
	 Status				varchar(16), -- "our for delivery"
	 Tracking_Link		varchar(50),
	 Start_T			timestamp,
	 Deliver_T			timestamp,
	 User_ID			numeric(8,0) not null,
	 Order_Num			SERIAL not null,
	 primary key (Order_Num),
	 foreign key (User_ID) references Users
	);

create table Holds
	(Book_ID		numeric(7,0) not null,
	 Order_Num		numeric(7,0) not null,
	 Qty			numeric(2,0) not null, -- probably shouldn't allow orders of 100+ books
	 primary key (Book_ID, Order_Num),
	 foreign key (Book_ID) references Book,
	 foreign key (Order_Num) references Orders
	);

create table Owners
	(Owner_ID		varchar(5) not null,
	 Email			varchar(30) not null,
	 Fname			varchar(15),
	 Lname			varchar(15),
	 Phone_Num		numeric(10,0),
	 Passwd			varchar(64) not null, -- same as before - it'll do for a demo
	 primary key (Owner_ID)
	);
