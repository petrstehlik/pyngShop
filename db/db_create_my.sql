SET FOREIGN_KEY_CHECKS = 0;
drop table if exists product;
drop table if exists customer;
drop table if exists category;
drop table if exists product_category;
drop table if exists product_properties;
drop table if exists type_properties;
drop table if exists manufacturer;
drop table if exists product_supplier;
drop table if exists review;
drop table if exists ordered_products;
drop table if exists shipping;
drop table if exists customer_order;
drop table if exists settings;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE product 
(
   product_id    integer not null auto_increment,
   name          varchar(255)  not null,
   description   varchar(1000) not null,
   price         numeric(19,4) not null,
   in_stock      integer default 0,
   PRIMARY KEY (product_id)
);

CREATE TABLE category
(
   category_id   integer not null auto_increment,
   name          varchar(255)  not null,
   description   varchar(1000) not null,
   slug          varchar(255)  not null,
   parent        integer,
   PRIMARY KEY (category_id),
   FOREIGN KEY (parent) REFERENCES category(category_id)
);

CREATE TABLE product_category
(
   product_id     integer not null,
   category_id    integer not null,
   FOREIGN KEY (product_id) REFERENCES product(product_id),
   FOREIGN KEY (category_id) REFERENCES category(category_id),
   PRIMARY KEY (product_id, category_id)
);

CREATE TABLE product_properties
(
   product_property_id  integer not null auto_increment,
   name                 varchar(255)  not null,
   prefix               varchar(255)  not null,
   sufix                varchar(255)  not null,
   PRIMARY KEY (product_property_id)
);

CREATE TABLE type_properties
(
   product_id           integer not null,
   product_property_id  integer not null,
   FOREIGN KEY (product_id) REFERENCES product(product_id),
   FOREIGN KEY (product_property_id) REFERENCES product_properties(product_property_id),
   PRIMARY KEY (product_id, product_property_id)
);

CREATE TABLE manufacturer
(
   manufacturer_id   integer not null auto_increment,
   name              varchar(255)  not null,
   telephone         numeric(20),
   contact_person    varchar(255)  not null,
   PRIMARY KEY (manufacturer_id)
);

CREATE TABLE product_supplier
(
   product_id        integer not null,
   manufacturer_id   integer not null,
   FOREIGN KEY (product_id) REFERENCES product(product_id),
   FOREIGN KEY (manufacturer_id) REFERENCES manufacturer(manufacturer_id),
   PRIMARY KEY (product_id, manufacturer_id)
);

CREATE TABLE customer
(
   customer_id    integer not null auto_increment,
   first_name     varchar(255)  not null,
   last_name      varchar(255)  not null,
   email          varchar(255)  not null,
   address_1      varchar(255)  not null,
   address_2      varchar(255)  not null,
   telephone      numeric(20),
   city           varchar(255)  not null,
   state          varchar(255)  not null,
   postal_code    numeric(20)   not null,
   password       varchar(255)  not null,
   PRIMARY KEY (customer_id)
);

CREATE TABLE review
(
   product_id     integer not null,
   customer_id    integer not null,
   content        varchar(1000),
   rating         integer not null,
   timestamp      date    not null,
   type           varchar(255) not null,
   FOREIGN KEY (product_id) REFERENCES product(product_id),
   FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
   PRIMARY KEY (product_id, customer_id)
);

CREATE TABLE ordered_products
(
   product_id     integer not null,
   order_id       integer not null,
   quantity       integer not null,
   FOREIGN KEY (product_id) REFERENCES product(product_id),
   PRIMARY KEY (order_id)
);

CREATE TABLE shipping
(
   shipping_id    integer not null,
   name           varchar(255) not null,
   price          integer not null,
   PRIMARY KEY (shipping_id)
);

CREATE TABLE customer_order
(
   order_id       integer not null,
   customer_id    integer not null,
   shipping_id    integer not null,
   timestamp      date    not null,
   staus          varchar(255) not null,
   FOREIGN KEY (order_id) REFERENCES ordered_products(order_id),
   FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
   FOREIGN KEY (shipping_id) REFERENCES shipping(shipping_id),
   PRIMARY KEY (order_id, customer_id, shipping_id)
);

CREATE TABLE settings
(
	name 		varchar(255) not null,
	value 	varchar(255) not null
);

INSERT INTO `settings` (`name`, `value`) VALUES ('title', 'pyngShop Demo'), ('url', 'http://localhost/~petrstehlik/pyngShop'), ('vat', '21'), ('keywords', 'python, angular, eshop'), ('description', 'Just another pyngShop website'), ('currency', 'CZK');

CREATE TABLE menu 
(
   menu_id    integer not null auto_increment,
   name          varchar(255)  not null,
   link         varchar(255) not null,
   icon          varchar(255) not null,
   parent       integer default null,
   PRIMARY KEY (menu_id),
   FOREIGN KEY (parent) REFERENCES menu(menu_id)
);
