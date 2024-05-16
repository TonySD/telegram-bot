CREATE USER repl_user WITH REPLICATION ENCRYPTED PASSWORD 'Qq12345';

CREATE TABLE phone_numbers (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(16)
);

CREATE TABLE emails (
    id SERIAL PRIMARY KEY,
    email VARCHAR(128)
);

INSERT INTO phone_numbers (phone) VALUES
('89065119192'),
('83476378633'),
('89161606677');

INSERT INTO emails (email) VALUES
('aaa@bbb.ccc'),
('ahtoxa.b@gmail.com'),
('hehehe@hihihi.ru');