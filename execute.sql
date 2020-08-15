create table countries(
    country_code varchar(50) PRIMARY KEY,
    name varchar(255)
);

create table customers(
    customer_id SERIAL PRIMARY KEY,
    first_name varchar(50),
    last_name varchar(50),
    gender varchar(10),
    birthday date,
    email_address varchar(255),
    username varchar(255),
    password varchar(255),
    contact varchar(50)
);

create table addresses(
    customer_id INTEGER REFERENCES customers(customer_id),
    address1 varchar(255),
    address2 varchar(255),
    city varchar(255),
    postal_code varchar(50),
    country_code varchar(50) REFERENCES countries(country_code)
);

create table courier(
    courier_id SERIAL PRIMARY KEY,
    name varchar(255),
    price numeric(13, 6),
    logo varchar(255)
);

create table currency(
    currency_id SERIAL PRIMARY KEY,
    name varchar(50),
    currency_code varchar(50)
);

create table payment_type(
    payment_id SERIAL PRIMARY KEY,
    payment_method varchar(50),
    credit_card_number varchar(50),
    currency_id INTEGER REFERENCES currency(currency_id)
);

create table products(
    product_id SERIAL PRIMARY KEY,
    name varchar(255),
    description text,
    price numeric(13,6),
    sku varchar(50),
    stock int,
    variation varchar(255),
    brand varchar(255),
    category_id int,
    specification text,
    product_image varchar(255)
);

create table category(
    product_id INTEGER REFERENCES products(product_id),
    category_name varchar(255)
);

create table product_image(
    product_id INTEGER REFERENCES products(product_id),
    image_name varchar(255),
    image_sorting int
);

create table orders(
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    status varchar(10),
    courier_id INTEGER REFERENCES courier(courier_id),
    address_id int,
    product_id INTEGER REFERENCES products(product_id),
    invoice_no varchar(50),
    shipping_fee numeric(13,6),
    total_tax numeric(13,6),
    total_price numeric(13,6),
    payment_id INTEGER REFERENCES payment_type(payment_id),
    delivery_date date,
    product_image varchar(255),
    quantity int,
    name varchar(255),
    description text
);

create table ordered_products(
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity int,
    total_price numeric(13,6)
);

create table buy(
    order_id SERIAL PRIMARY KEY,
    customer_id int,
    status varchar(255),
    courier_id int,
    product_id int,
    shipping_fee numeric(13,6),
    total_price numeric(13,6),
    product_image varchar(255),
    quantity int,
    name varchar(255),
    description text
);
create table history(
    order_id int,
    product_id int,
    quantity int,
    total_price numeric(13,6),
    customer_id int,
    product_name, varchar(255)
);