1 database
create table cpy_products(
    id bigint auto_increment primary key,
    product_url text,
    shop_name varchar(128),
    shop_url varchar(254),
    created_time timestamp default current_timestamp() ,
    updated_time timestamp default current_timestamp() on update current_timestamp()
)


2 https://www.jb51.net/article/196655.htm
