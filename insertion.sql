insert into category(category_name) values('instrument');

insert into currency(name, currency_code) values('Peso', 'Philippine Peso');

insert into products(name, description, price, sku, stock, variation, brand, specification, product_image) values(
    'Model-D', 'Concert Grand', 1000000, 'model', 20, 'none', 'steinway',
    'At 8 11¾ (274 cm) in length, this majestic musical instrument — the pinnacle of concert grands — is the overwhelming choice of the world greatest pianists and for anyone who demands the highest level of musical expression.',
    'static/img/Model/Model-D-4.PNG'
);

insert into products(name, description, price, sku, stock, variation, brand, specification, product_image) values(
    'Model-B', 'Classic Grand', 1000000, 'model', 20, 'none', 'steinway',
    'This magnificent 6 11 (211 cm) grand piano is often referred to by pianists as “the perfect piano. It is a wonderfully balanced and versatile instrument that does extremely well in refined homes, teaching studios, and mid-sized venues and is also available as a STEINWAY SPIRIO, the worlds finest high resolution player piano.',
    'static/img/Model/Model-B-1.PNG'
);

insert into products(name, description, price, sku, stock, variation, brand, specification, product_image) values(
    'Model-A', 'Salon Grand', 1000000, 'model', 20, 'none', 'steinway',
    'At 6 2(188 cm), the Model A is known for delivering a grand sound in a medium-scale instrument. This grand offers power and warmth, with a design that allows the solid spruce soundboard to freely and efficiently resonate, like its larger counterparts.',
    'static/img/Model/Model-A-1.PNG'
);

insert into products(name, description, price, sku, stock, variation, brand, specification, product_image) values(
    'Model-O', 'Living Room Grand', 1000000, 'model', 20, 'none', 'steinway',
    'At 5 10¾ (180 cm), the Model O is the largest of Steinways small grands. This piano is large enough to satisfy those who demand a full, rich sound, yet sized to fit in almost any home.',
    'static/img/Model/Model-O-1.PNG'
);

insert into products(name, description, price, sku, stock, variation, brand, specification, product_image) values(
    'Model-M', 'Medium Grand', 1000000, 'model', 20, 'none', 'steinway',
    'At 5 7 (170 cm) in length, this piano rich tone, responsive action and manageable size makes it perfect for conservatories, and many homes as well. The Model M is also available as a STEINWAY SPIRIO, the worlds finest high resolution player piano.',
    'static/img/Model/Model-M-1.PNG'
);

insert into products(name, description, price, sku, stock, variation, brand, specification, product_image) values(
    'Model-S', 'Baby Grand', 1000000, 'model', 20, 'none', 'steinway',
    'At 5 1 (155 cm), this piano is the smallest of the Steinway grands. This design was introduced in the 1930s to invite the majesty of the Steinway sound into almost any space.',
    'static/img/Model/Model-S-1.PNG'
);

insert into product_image(product_id, image_name) values(5, 'img/Model/modelD-spec.PNG');
insert into product_image(product_id, image_name) values(6, 'img/Model/modelA-spec.PNG');
insert into product_image(product_id, image_name) values(7, 'img/Model/modelO-spec.PNG');
insert into product_image(product_id, image_name) values(8, 'img/Model/modelM-spec.PNG');
insert into product_image(product_id, image_name) values(9, 'img/Model/modelS-spec.PNG');
insert into product_image(product_id, image_name) values(10, 'img/Model/modelB-spec.PNG');

insert into courier(name, price) values('Steinway Express', 50);
insert into courier(name, price) values('Yamaha Express', 50);
insert into courier(name, price) values('Bösendorfer Express', 50);


