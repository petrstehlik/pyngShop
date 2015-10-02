BEGIN

        FOR remove IN (

                SELECT 'DROP ' || object_type || ' ' || object_name || DECODE ( object_type, 'TABLE', ' CASCADE CONSTRAINTS PURGE' ) AS rmsql

                FROM user_objects

                WHERE object_type IN ( 'TABLE', 'VIEW', 'PACKAGE', 'TYPE', 'PROCEDURE', 'FUNCTION', 'TRIGGER', 'SEQUENCE' )

                ORDER BY object_type, object_name

        ) LOOP

                EXECUTE IMMEDIATE remove.rmsql;

        END LOOP;

END;

/

create sequence crayons_seq start with 1 increment by 1 nomaxvalue;
create table crayons (
  id          integer primary key,
  colour      varchar(255) not null,
  length      decimal(19,4) not null,
  type        varchar(255) not null,
  packaging   integer default 1
);

create sequence sketchbook_seq start with 1 increment by 1 nomaxvalue;
create table sketchbook (
  id          integer primary key,
  paper_size  varchar(255) not null,
  type        varchar(255) not null,
  packaging   integer default 1,
  weight      decimal(19,4) not null
);

create sequence product_seq start with 1 increment by 1 nomaxvalue;
CREATE TABLE product (
  product_id    integer       constraint PK_product_id primary key,
  name          varchar(255)  constraint product_name not null,
  description   varchar(1000) constraint product_description not null,
  price         decimal(19,4) constraint product_price not null,
  crayons_id    integer       constraint fk_crayons_id references crayons (id),
  sketchbook_id integer       constraint fk_sketchbook_id references sketchbook (id),
  in_stock      integer       default 0
);

alter table product add constraint uniq_product_type unique(crayons_id, sketchbook_id);
alter table crayons add constraint enum_crayons check(type in('pastelka', 'voskovka'));
alter table sketchbook add constraint enum_sketchbook check(paper_size in('A2', 'A3', 'A4', 'A5', 'A6'));

--crayons
insert into crayons values (crayons_seq.nextval, 'ruzova', 15.5, 'pastelka', 1);
insert into crayons values (crayons_seq.nextval, 'modra', 15.5, 'pastelka', 1);
insert into crayons values (crayons_seq.nextval, 'hneda', 10, 'voskovka', 5);


insert into product values (product_seq.nextval, 'Pastelka ruzova', 'Lorem Ipsum', 19.90, 1, null, 110);
insert into product values (product_seq.nextval, 'Pastelka modra', 'Lorem Ipsum', 19.90, 2, null, 154);
insert into product values (product_seq.nextval, 'Voskovka hneda', 'Lorem Ipsum', 9.90, 3, null, 23);

--sketchbooks
insert into sketchbook values (sketchbook_seq.nextval, 'A4', 'bily', 25, 100);
insert into sketchbook values (sketchbook_seq.nextval, 'A3', 'barevny', 10, 150);
insert into sketchbook values (sketchbook_seq.nextval, 'A6', 'bily', 100, 75);

insert into product values (product_seq.nextval, 'Skicak A4', 'Lorem Ipsum', 19.90, null, 1, 100);
insert into product values (product_seq.nextval, 'Barevny skicak A3', 'Lorem Ipsum', 59.90, null, 2, 42);
insert into product values (product_seq.nextval, 'Skicak A6', 'Lorem Ipsum', 9.90, null, 3, 76);

create sequence customer_seq start with 1 increment by 1 nomaxvalue;
create table customer (
  customer_id   integer       constraint PK_customer_id primary key,
  first_name    varchar(25)   constraint customer_first_name not null,
  last_name     varchar(25)   constraint customer_last_name not null,
  email         varchar(50)   constraint email not null,
  telephone     integer       default 0,
  address_1     varchar(50)   constraint customer_address_1 not null,
  address_2     varchar(50)   default null,
  city          varchar(50)   constraint customer_city not null,
  country       varchar(50)   constraint customer_country not null,
  postal_code   varchar(10)   constraint customer_postal_code not null,
  ID_number     decimal(8)    default 00000000,
  password      varchar(255)  not null
);

--                           ID                     first_name  last_name   email                     telephone   address_1         address_2   city        country            postal   ID_number   Password
insert into customer values (customer_seq.nextval, 'Jan',       'Novak',    'honzanovak@email.cz',    null ,      'Stodolni 144',   null ,      'Praha',    'Ceska republika', '11200', null, 'df5ea29924d39c3be8785734f13169c6');
insert into customer values (customer_seq.nextval, 'Petr',      'Sup',      'petrsup@email.cz',       null ,      'Ruzova 15',      null ,      'Brno',     'Ceska republika', '53623', '32569818', '12c3de998cc272112872ea8a1c2f67b9');
insert into customer values (customer_seq.nextval, 'Monika',    'Novotna',  'monikanovotna@post.cz',  null ,      'Veselá 1',       null ,      'Brno',  'Ceska republika', '56941', null, '60710fc39180f03bb8b67a484a969021');
insert into customer values (customer_seq.nextval, 'Marie',     'Pokorná',  'mariepokorna@gmail.com', null ,      'Nová 568',       null ,      'Olomouc',  'Ceska republika', '38752', null, 'bf516925bb37a8544c8ee19a24e15c05');
insert into customer values (customer_seq.nextval, 'Andrea',    'Nemilá',  'anem@gmail.com',          null ,      'Ztracená 98',    null ,      'Ostrava',  'Ceska republika', '25400', null, 'bf516925bbs7a8564c8ee19a24e15c05');

create table basket (
  customer_id   integer       constraint fk_customer_id                         references customer (customer_id),
  product_id    integer       constraint fk_product_id                          references product (product_id),
  quantity      integer       not null,
  timestamp     date          not null
);

insert into basket values (1, 1, 1, TO_DATE('2015.01.02', 'YY.MM.DD'));
insert into basket values (2, 3, 4, TO_DATE('2015.01.15', 'YY.MM.DD'));
insert into basket values (3, 2, 1, TO_DATE('2015.02.03', 'YY.MM.DD'));
insert into basket values (4, 1, 3, TO_DATE('2015.02.09', 'YY.MM.DD'));
insert into basket values (2, 4, 2, TO_DATE('2015.02.25', 'YY.MM.DD'));
insert into basket values (3, 3, 1, TO_DATE('2015.03.05', 'YY.MM.DD'));
insert into basket values (3, 6, 1, TO_DATE('2015.03.28', 'YY.MM.DD'));
insert into basket values (4, 3, 2, TO_DATE('2015.03.29', 'YY.MM.DD'));


create sequence category_seq start with 1 increment by 1 nomaxvalue;
create table category (
  category_id   integer       constraint pk_category_id primary key,
  name          varchar(255)  not null,
  description   varchar(1000) default null,
  slug          varchar(255)  not null,
  parent        integer       constraint fk_category_id                         references category (category_id)
);

insert into category values (category_seq.nextval, 'Pastelky', 'Krasne pastelky vsech barev duhy.', 'pastelky', null);
insert into category values (category_seq.nextval, 'Skicaky', 'Papiry vsechny mozne i nemozne.', 'skicaky', null);
insert into category values (category_seq.nextval, 'Voskovky', 'Malujme a nezlobme s voskovkami.', 'voskovky', 1);


create table product_category (
  category_id   integer       constraint fk_product_cat_category_id             references category (category_id),
  product_id    integer       constraint fk_product_cat_product_id              references product (product_id)
);

insert into product_category values ('1', '1');
insert into product_category values ('1', '2');
insert into product_category values ('3', '3');
insert into product_category values ('2', '4');
insert into product_category values ('2', '5');
insert into product_category values ('2', '6');



create table supplier (
  id_number     decimal(8)    constraint pk_supplier_id_number primary key,
  name          varchar(50)   not null,
  telephone     decimal(20)   not null,
  e_mail        varchar(50)   not null,
  contact_person  varchar(50)
);

insert into supplier values (36594568, 'Pastelky s.r.o.', 732654987, 'info@pastelkysro.cz', 'Tomas Nachovy');
insert into supplier values (06594868, 'Voskovy a.s.', 736547987, 'info@voskovky.cz', 'Jan Tuhy');
insert into supplier values (98752568, 'Papirny hebke listy s.r.o.', 608954367, 'info@hebkelisty.cz', 'Mikulas Fousaty');

create table product_supplier (
  id_number     decimal(8)    constraint fk_product_supplier_id_number          references supplier (id_number),
  product_id    integer       constraint fk_product_supplier_product_id         references product (product_id)
);

insert into product_supplier values (36594568, 1);
insert into product_supplier values (36594568, 2);
insert into product_supplier values (36594568, 3);

insert into product_supplier values (06594868, 3);

insert into product_supplier values (98752568, 4);
insert into product_supplier values (98752568, 5);
insert into product_supplier values (98752568, 6);


create sequence shipping_seq start with 1 increment by 1 nomaxvalue;
create table shipping(
  shipping_id   integer         constraint pk_shipping_id primary key,
  name          varchar(50)     not null,
  price         decimal(19,4)   not null
);

insert into shipping values (shipping_seq.nextval, 'Ceska posta - dobirka', 99);
insert into shipping values (shipping_seq.nextval, 'PPL', 129);
insert into shipping values (shipping_seq.nextval, 'Osobni odber', 0);


create sequence order_seq start with 1 increment by 1 nomaxvalue;
create table customer_order (
  order_id    integer         constraint pk_order_id primary key,
  customer_id integer         constraint fk_order_customer_id                   references customer (customer_id),
  shipping_id integer         constraint fk_order_shipping_id                   references shipping (shipping_id),
  status      varchar(255)    not null,
  timestamp   date            not null
);

alter table customer_order add constraint enum_status check(status in('cekajici', 'prijata', 'zpracovana', 'odeslana', 'zaplacena'));

insert into customer_order values (order_seq.nextval, '1', '1', 'zaplacena', TO_DATE('2015.01.07', 'YY.MM.DD'));
insert into customer_order values (order_seq.nextval, '1', '2', 'cekajici', TO_DATE('2015.02.07', 'YY.MM.DD'));
insert into customer_order values (order_seq.nextval, '2', '1', 'zpracovana', TO_DATE('2015.02.13', 'YY.MM.DD'));
insert into customer_order values (order_seq.nextval, '3', '2', 'odeslana', TO_DATE('2015.02.28', 'YY.MM.DD'));
insert into customer_order values (order_seq.nextval, '4', '2', 'odeslana', TO_DATE('2015.03.07', 'YY.MM.DD'));
insert into customer_order values (order_seq.nextval, '1', '3', 'prijata', TO_DATE('2015.03.17', 'YY.MM.DD'));


create table ordered_product (
  order_id    integer         constraint fk_ordered_order_id                    references customer_order (order_id),
  product_id  integer         constraint fk_ordered_product_id                  references product (product_id),
  quantity    integer         not null,
  check (quantity > 0)
);

insert into ordered_product values (1, 1, 5);
insert into ordered_product values (1, 2, 10);
insert into ordered_product values (1, 5, 1);

insert into ordered_product values (2, 1, 1);
insert into ordered_product values (2, 6, 1);

insert into ordered_product values (3, 2, 5);

insert into ordered_product values (4, 3, 10);

insert into ordered_product values (5, 4, 1);
insert into ordered_product values (5, 5, 5);

insert into ordered_product values (6, 6, 6);

create table review (
  customer_id integer       constraint fk_review_customer_id                    references customer (customer_id),
  product_id  integer       constraint fk_review_product_id                     references product (product_id),
  content     varchar(1000),
  rating      smallint      not null,
  timestamp   DATE          not null,
  check (rating < 6)
);

insert into review values (2, 1, null, 4, TO_DATE('2015.02.05', 'YYYY.MM.DD'));
insert into review values (3, 1, 'Pastelky prisly zlomene a vsechny okousane. Ale pak jsem nasla v krabici krasnou malou mysku, takze vse OK.', 3, TO_DATE('2015.03.08', 'YYYY.MM.DD'));
insert into review values (1, 1, 'Kreckum moc chutnala', 5, TO_DATE('2015.03.21', 'YYYY.MM.DD'));
insert into review values (2, 6, 'Nelibila se mi struktura papiru. Ani zviratum na hnizda se to nehodi!', 1, TO_DATE('2015.04.01', 'YYYY.MM.DD'));
insert into review values (1, 6, null, 5, TO_DATE('2015.04.05', 'YYYY.MM.DD'));


--SQL DOTAZY

--spojeni 2 tabulek
--najit vsechny pastelky a vypsat jmeno, popis, cenu a barvu
select name, description, price, crayons.COLOUR
from product
join crayons on product.crayons_id = crayons.id;

--vypsat vsechna hodnoceni a recenze s <5* a jejich autorem, obsahema casem
select customer.first_name, customer.last_name ,rating, content, timestamp
from review
join customer on review.customer_id = customer.customer_id
where rating < 5;

--spojeni 3 tabulek
--najit vsechny dodavatele voskovek a zobrazit ico, jmeno a email
select supplier.id_number, supplier.name, supplier.e_mail
from supplier
join product_supplier on supplier.id_number = product_supplier.id_number
join product on product_supplier.product_id = product.product_id
where product.product_id = 3;

--GROUP BY
--celkovy pocet objednavek na zakaznika
select count(customer_order.order_id) as total_orders, customer.first_name, customer.last_name
from customer_order
join customer on customer_order.customer_id = customer.customer_id
group by customer.first_name, customer.last_name;

--celkovy pocet produktu, kteri jednotlivi dodavatele dodavaji
select count(supplier.id_number) as number_of_suppliers, supplier.name
from product_supplier
join product on product_supplier.product_id = product.product_id
join supplier on product_supplier.id_number = supplier.id_number
group by supplier.name;

--EXISTS
--najit vsechny objednavky z Brna
select distinct cu.first_name, cu.last_name, cu.address_1, co.order_id
from customer cu, customer_order co
where cu.customer_id = co.customer_id and cu.city='Brno' and not exists
( select *
  from customer_order co
  where co.customer_id = cu.customer_id and cu.city<>'Brno');

--IN se selectem  
--najit vsechny "bludne duse" (zakazniky bez jedine objednavky)
select cu.first_name, cu.last_name, cu.email
from customer cu
where  cu.customer_id not in (
  select co.customer_id
  from customer_order co
  where cu.customer_id = co.customer_id
  );


--============================================================================--
--                              TRIGGERS                                      --
--============================================================================--

--trigger, ktery pri smazani objednavky smaze i korespondujici polozky uvedene 
--v objednavce (ordered_products)
create or replace trigger delete_order
  before delete on customer_order
  referencing old as old_table
  for each row
  --declare ord_id integer;
BEGIN
  --DBMS_OUTPUT.put_line(:OLD.order_id);
  --select order_id into ord_id from ordered_product where ordered_product.order_id = :OLD.order_id;
  --update ordered_product set order_id = '5' where order_id = :OLD.order_id;
  delete from ordered_product where order_id = :old_table.order_id;
END;
/

--demonstrace funkcnosti triggeru delete_order, smaze i odpovidajici polozku 
--v ordered_product 
delete from customer_order where order_id = '3';


--trigger na inkrementaci product_id v product, pokud je product_id null
--product_id je nejdulezitejsi PK v cele databazi
create or replace trigger add_product_id
  before insert on product  
  for each row
BEGIN
  if :new.product_id is NULL then
    :NEW.product_id := product_seq.nextval;
    --pro starsi verzi oracle 11g
    --select product_seq.nextval into :NEW.product_id from dual;
  end if;
END;
/
--spusti autoinkrementalni trigger
insert into product values (NULL, 'Pastelka zlata', 'Lorem Ipsum', 129.90, null, null, 10);

--trigger pro kontrolu IC v supplier a customer
create or replace trigger check_id_number
  before insert or update of id_number on supplier
  for each row
declare 
   num supplier.id_number%type;
BEGIN
  check_id(num, :NEW.id_number);
 -- DBMS_OUTPUT.put_line(num);
END check_id_number;

/

--trigger pro kontrolu IC v supplier a customer
create or replace trigger check_id_number_customer
  before insert or update of id_number on customer
  for each row
declare 
   num supplier.id_number%type;
BEGIN
  check_id(num, :NEW.id_number);
 -- DBMS_OUTPUT.put_line(num);
END check_id_number;

/


--============================================================================--
--                              PROCEDURES                                    --
--============================================================================--

--kontrola IC jako procedura
create or replace procedure check_id (num IN OUT supplier.id_number%type, id_num IN supplier.id_number%type)
IS
  bad_id exception;
BEGIN

  num := (substr(id_num,1,1)*8) + (substr(id_num,2,1)*7) + (substr(id_num,3,1)*6);
  
  num := num + (substr(id_num,4,1)*5) + (substr(id_num,5,1)*4) + (substr(id_num,6,1)*3) + (substr(id_num,7,1)*2);
  
  num := mod(num, 11);
    
  if ( num = 0 ) then 
      if substr(id_num,8,1) != 1 then raise bad_id;
      end if;
  elsif (num = 10) then  
      if substr(id_num,8,1) != 1 then raise bad_id;
      end if;
  elsif (num = 1) then
      if substr(id_num,8,1) != 0 then raise bad_id;
      end if;
  else
      if substr(id_num,8,1) != (11 - num) then raise bad_id;
      end if;
  end if;
  
  exception
    when bad_id then
      Raise_Application_Error (-20200, 'Invalid ID number');

END;
/

--pro kontrolu funkcnosti trigerru a procedury
update supplier set id_number = 00000000 where id_number = 12345687;
insert into supplier values (12345680, 'Drsny grafit s.r.o.', 608954367, 'info@hebkelisty.cz', 'sadfasdf Fousaty');
delete from supplier where id_number = 12345680;

--procedura pro vypocet celkoveho hodnoceni konkretniho produktu
create or replace procedure total_rating_proc (re_id IN review.product_id%type)
is
  total_rating integer;
  cnt_rating integer;
  cursor c1 is
    select rating from review where product_id = re_id;
BEGIN
  cnt_rating := 0;
  total_rating := 0;
  
  for rating_val in c1
  LOOP  
    total_rating := total_rating + rating_val.rating;
    cnt_rating := cnt_rating + 1;
  END loop;
  
  DBMS_OUTPUT.PUT_LINE (total_rating/cnt_rating);
  
END;
/

--pro test procedury na produktu s ID 1
execute total_rating_proc(1);

--============================================================================--
--                              INDEXES                                       --
--============================================================================--

--optimalizace pomoci indexu
explain plan for
select distinct cu.first_name, cu.last_name, cu.address_1, co.order_id
from customer cu, customer_order co
where cu.customer_id = co.customer_id and cu.city='Brno' and not exists
( select *
  from customer_order co
  where co.customer_id = cu.customer_id and cu.city<>'Brno');

select plan_table_output from table(dbms_xplan.display());

create index customer_city on customer(city);
create index customer_id_ind on customer_order(customer_id);
drop index customer_city;
drop index customer_id_ind;


--optimalizovany dotaz pomoci left outer join
explain plan for
select count(customer_order.order_id) as total_orders, customer.first_name, customer.last_name
from customer_order
left outer join customer on customer_order.customer_id = customer.customer_id
group by customer.first_name, customer.last_name;

--neoptimalizovany dotaz s inner join
explain plan for
select count(customer_order.order_id) as total_orders, customer.first_name, customer.last_name
from customer_order
join customer on customer_order.customer_id = customer.customer_id
group by customer.first_name, customer.last_name;

select plan_table_output from table(dbms_xplan.display());


--============================================================================--
--                         MATERIALIZED VIEW                                  --
--============================================================================--
--materializovany pohled na bludne duse
create materialized view dead_soul 
  nologging
  cache
  build immediate
 -- refresh fast
  enable query rewrite 
as
select cu.first_name, cu.last_name, cu.email
from customer cu
where  cu.customer_id not in (
  select co.customer_id
  from customer_order co
  where cu.customer_id = co.customer_id
  );
  
drop materialized view dead_soul;

--dukaz pouziti materializovaneho pohledu  
explain plan for
select cu.first_name, cu.last_name, cu.email
from customer cu
where  cu.customer_id not in (
  select co.customer_id
  from customer_order co
  where cu.customer_id = co.customer_id
  );
  
--prava pro kolegyni na materializovany pohled
grant select, insert, update on CUSTOMER to XSNOBL01;
/
