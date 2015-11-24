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
drop table if exists menu;
drop table if exists sub_category;
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
   PRIMARY KEY (category_id)
);

CREATE TABLE sub_category
(
   parent   integer not null,
   child    integer not null,
   PRIMARY KEY (parent, child),
   FOREIGN KEY (parent) REFERENCES category(category_id),
   FOREIGN KEY (child) REFERENCES category(category_id)
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
   value                varchar(255) not null,
   FOREIGN KEY (product_id) REFERENCES product(product_id),
   FOREIGN KEY (product_property_id) REFERENCES product_properties(product_property_id),
   PRIMARY KEY (product_id, product_property_id)
);

CREATE TABLE manufacturer
(
   manufacturer_id   integer not null auto_increment,
   name              varchar(255)  not null,
   first_name        varchar(255)  not null,
   last_name        varchar(255)  not null,
   telephone         numeric(20),
   email             varchar(255)  not null,
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
   full_price     integer(11) not null,
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
   menu_id  integer not null auto_increment,
   name     varchar(255)  not null,
   link     varchar(255) not null,
   icon     varchar(255) not null,
   parent   integer default null,
   PRIMARY KEY (menu_id),
   FOREIGN KEY (parent) REFERENCES menu(menu_id)
);

INSERT INTO `category` (`name`, `description`, `slug`) VALUES
('Glasses', 'gl', 'glasses');

INSERT INTO `category` (`name`, `description`, `slug`) VALUES 
('Sunglasses', 'sun gl', 'sunglasses'), 
('Eyeglasses', 'eye gl', 'eyeglasses');

INSERT INTO `category` (`name`, `description`, `slug`) VALUES 
('Full frame', 'eye f', 'full_farame'), 
('Half frame', 'eye h', 'half_frame'),
('No frame', 'eye n', 'no_frame');

INSERT INTO `category` (`name`, `description`, `slug`) VALUES
('Vehicle', 'vehicles all', 'vehicle');

INSERT INTO `category` (`name`, `description`, `slug`) VALUES
('Utility vehicle', 'vehicles u', 'utility_vehicles'),
('personal vehicle', 'vehicles p', 'personal_vehicles');

INSERT INTO `sub_category` VALUES
(1,2),
(1,3),
(3,4),
(3,5),
(3,6),
(7,8),
(7,9);

INSERT INTO `product_properties` (`name`, `prefix`, `sufix`) VALUES 
('Colour', '', ''), 
('Weight', '', 'g'),
('Weight', '', 'kg'),
('Weight', '', 't'),
('material', '', '');

INSERT INTO `product` (`name`, `description`, `price`, in_stock) VALUES 
('Artur_B', 'sjkd ew fwef ', 100, 31), 
('Artur_R', 'nfjkwen', 150, 15), 
('Nexin', 'weklmf kewfm ekf', 20, 412),
('C130', 'kfmewfwe', 20000, 14),
('R8', 'weklmf kewfefwm ekf', 200000, 2);

INSERT INTO `type_properties` VALUES 
(1, 1, 'Black'), 
(1, 2, '50'), 
(1, 5, 'Plastick'), 
(2, 1, 'Red'), 
(2, 2, '70'),
(3, 1, 'Blue'), 
(3, 2, '45'), 
(3, 5, 'Titan'),
(4, 1, 'Black'), 
(4, 4, '2,5'),
(5, 1, 'Gold'), 
(5, 4, '10,5');

INSERT INTO `product_category` VALUES 
(1,5), 
(2,6), 
(4,9), 
(5,9), 
(5,8), 
(3,2);

INSERT INTO `manufacturer` VALUES 
('', 'Cesnet', 'Janko', 'Hraško', '222222222', 'jankohrasko@mail.com'), 
('', 'Mercedes', 'Róbert', 'Fico', '333333333', 'robetfico@mail.com'), 
('', 'Inveatech', 'Miloš', 'Zeman', '444444444', 'miloszeman@mail.com'); 

INSERT INTO `product_supplier` VALUES 
(1,1), 
(2,1), 
(3,1), 
(4,2), 
(5,1);


INSERT INTO `customer` VALUES 
('', 'Mário', 'Kuka', 'mariokuka@mail.com', 'Kolejni 2', '', 123456789, 'Brno', 'Czech', 1234, 'heslo'), 
('', 'Petr', 'Stehlík', 'petrstehlik@mail.com', 'Rečkovice 4', '', 987456321, 'Brno', 'Czech', 1235, 'heslo2'), 
('', 'Martin', 'Veis', 'martinveis@mail.com', 'Mánesova 4', 'Božetehova 5', 9999999999, 'Praha', 'Czech', 8564, 'heslo3');

INSERT INTO `review` VALUES 
(4, 1, 'je to na prd', 1, '2015-08-05 08:15:31'), 
(4, 2, 'je to vlovina', 2, '2015-08-05 10:15:31'), 
(2, 2, 'je to somarina', 10, '2015-09-06 07:14:31'); 






