-- =====================================
-- HBnB Database Test Script (Tables already exist)
-- =====================================

USE hbnb_db;

-- CREATE: إضافة مستخدم جديد
INSERT INTO User (id, first_name, last_name, email, password)
VALUES ('11111111-1111-1111-1111-111111111111', 'John', 'Doe', 'john@example.com', '$2b$12$examplehash');

-- CREATE: إضافة مكان جديد
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES ('22222222-2222-2222-2222-222222222222', 'Cozy Villa', 'Nice view', 200.00, 36.5, -120.2, '11111111-1111-1111-1111-111111111111');

-- CREATE: إضافة review
INSERT INTO Review (id, text, rating, user_id, place_id)
VALUES ('33333333-3333-3333-3333-333333333333', 'Amazing!', 5, '11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222');

-- CREATE: ربط place مع amenity
INSERT INTO Place_Amenity (place_id, amenity_id)
VALUES ('22222222-2222-2222-2222-222222222222', 'a8e9d9fa-1234-4b2f-9a5d-1f2c3d4e5b6f'); -- WiFi

-- READ: عرض كل المستخدمين
SELECT * FROM User;

-- READ: عرض كل الأماكن مع اسم المالك
SELECT Place.id, Place.title, User.first_name, User.last_name
FROM Place
JOIN User ON Place.owner_id = User.id;

-- READ: عرض كل reviews مع معلومات المستخدم والمكان
SELECT Review.text, Review.rating, User.first_name, Place.title
FROM Review
JOIN User ON Review.user_id = User.id
JOIN Place ON Review.place_id = Place.id;

-- UPDATE: تعديل اسم المستخدم
UPDATE User
SET first_name = 'Jonathan'
WHERE email = 'john@example.com';

-- UPDATE: تعديل سعر المكان
UPDATE Place
SET price = 250.00
WHERE title = 'Cozy Villa';

-- DELETE: حذف review
DELETE FROM Review
WHERE id = '33333333-3333-3333-3333-333333333333';

-- DELETE: حذف المكان
DELETE FROM Place
WHERE id = '22222222-2222-2222-2222-222222222222';

-- DELETE: حذف المستخدم
DELETE FROM User
WHERE id = '11111111-1111-1111-1111-111111111111';

-- التحقق النهائي من Admin & Amenities
SELECT first_name, last_name, email, is_admin FROM User WHERE is_admin = TRUE;
SELECT * FROM Amenity;
