-- HBnB CRUD TEST SCRIPT

USE hbnb;

-- Verify tables exists 
SHOW TABLES;

DESCRIBE users;
DESCRIBE places;
DESCRIBE reviews;
DESCRIBE amenities;
DESCRIBE place_amenity;


-- Verify admin user exists and is admin
SELECT id, email, is_admin
FROM users
WHERE email = 'admin@hbnb.io';

-- Verify password is hashed (bcrypt hashes start with $2)
SELECT password
FROM users
WHERE email = 'admin@hbnb.io';

-- Verify amenities exist
SELECT * FROM amenities;


-- Insert a normal user
INSERT INTO users VALUES (
    UUID(),
    'John',
    'Doe',
    'john.doe@email.com',
    '$2b$12$examplehashedpasswordstring',
    FALSE
);

-- Insert a place owned by admin
INSERT INTO places VALUES (
    UUID(),
    'Beach House',
    'Nice house near the beach',
    250.00,
    24.7136,
    46.6753,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);

-- Insert a review
INSERT INTO reviews VALUES (
    UUID(),
    'Amazing place!',
    5,
    (SELECT id FROM users WHERE email = 'john.doe@email.com'),
    (SELECT id FROM places WHERE title = 'Beach House')
);

-- Link place with amenities
INSERT INTO place_amenity VALUES (
    (SELECT id FROM places WHERE title = 'Beach House'),
    (SELECT id FROM amenities WHERE name = 'WiFi')
);


SELECT * FROM users;
SELECT * FROM places;
SELECT * FROM reviews;
SELECT * FROM amenities;
SELECT * FROM place_amenity;


-- Update place price
UPDATE places
SET price = 300.00
WHERE title = 'Beach House';

-- Update review rating
UPDATE reviews
SET rating = 4
WHERE text = 'Amazing place!';


-- Delete review
DELETE FROM reviews
WHERE text = 'Amazing place!';

-- Remove amenity from place
DELETE FROM place_amenity
WHERE place_id = (SELECT id FROM places WHERE title = 'Beach House');

-- Delete place
DELETE FROM places
WHERE title = 'Beach House';

-- Delete test user
DELETE FROM users
WHERE email = 'john.doe@email.com';
