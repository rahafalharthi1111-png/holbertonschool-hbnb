HBnB Database ER Diagram
Task 10: Generate Database Diagrams
This document contains the Entity-Relationship (ER) diagram for the HBnB project database schema, created using Mermaid.js.
ER Diagram
<img width="1121" height="849" alt="Screenshot (354)" src="https://github.com/user-attachments/assets/609ed81c-5b23-4541-b193-cc6e68602479" />

Relationships Explanation
USER → PLACE (One-to-Many) 
A User can own many Places.

A Place belongs to one User (via owner_id foreign key).

Relationship notation: USER ||--o{ PLACE : "owns"

USER → REVIEW (One-to-Many)
A User can write many Reviews.

A Review is written by one User (via user_id foreign key).

Relationship notation: USER ||--o{ REVIEW : "writes"

PLACE → REVIEW (One-to-Many)
A Place can have many Reviews.

A Review belongs to one Place (via place_id foreign key).

Relationship notation: PLACE ||--o{ REVIEW : "has"

PLACE ↔ AMENITY (Many-to-Many)
A Place can have many Amenities.

An Amenity can be associated with many Places.

Implemented through the PLACE_AMENITY association table.

Relationship notation: PLACE }o--o{ AMENITY : "has"

Entity Details
USER

Primary Key: id (UUID, CHAR(36))

Unique: email

Attributes: first_name, last_name, email, password, is_admin, created_at, updated_at

PLACE

Primary Key: id (UUID)

Foreign Key: owner_id → USER.id

Attributes: title, description, price, latitude, longitude, owner_id, created_at, updated_at

REVIEW

Primary Key: id (UUID)

Foreign Keys:

user_id → USER.id

place_id → PLACE.id

Unique Constraint: (user_id, place_id) ensures one review per user per place

Attributes: text, rating, user_id, place_id, created_at, updated_at

AMENITY

Primary Key: id (UUID)

Unique: name

Attributes: name, created_at, updated_at

PLACE_AMENITY

Composite Primary Key: (place_id, amenity_id)

Foreign Keys:

place_id → PLACE.id

amenity_id → AMENITY.id

Purpose: Association table for the many-to-many relationship between Place and Amenity

Notes

All entities inherit id, created_at, and updated_at from BaseModelDB.

UUID format is used for all primary keys (CHAR(36) in SQL).

Foreign key constraints ensure referential integrity.

The unique constraint on (user_id, place_id) in REVIEW prevents duplicate reviews by the same user for the same place.





