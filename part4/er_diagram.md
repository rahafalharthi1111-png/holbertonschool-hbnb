# HBnB Database ER Diagram

## Task 10: Generate Database Diagrams

This document describes the **Entity-Relationship (ER) Diagram** for the **HBnB project database schema**, created using **Mermaid.js**.
The diagram visually represents all core entities, their attributes, and the relationships between them.

---

## ER Diagram
<img width="1121" height="849" alt="Screenshot (354)" src="https://github.com/user-attachments/assets/609ed81c-5b23-4541-b193-cc6e68602479" />

---

## Relationships Explanation

### users → places (One-to-Many)

- A **User** can own many **Places**.
- A **Place** belongs to one **User**.
- Implemented via the foreign key `owner_id` in the `places` table.
- **Notation**:
  `USER ||--o{ PLACE : "owns"`

---

### users → reviews (One-to-Many)

- A **User** can write many **Reviews**.
- A **Review** is written by one **User**.
- Implemented via the foreign key `user_id` in the `reviews` table.
- **Notation**:
  `USER ||--o{ REVIEW : "writes"`

---

### places → reviews (One-to-Many)

- A **Place** can have many **Reviews**.
- A **Review** belongs to one **Place**.
- Implemented via the foreign key `place_id` in the `reviews` table.
- **Notation**:
  `PLACE ||--o{ REVIEW : "has"`

---

### olaces ↔ amenityt (Many-to-Many)

- A **Place** can have many **Amenities**.
- An **Amenity** can be associated with many **Places**.
- Implemented through the **PLACE_AMENITY** association table.
- **Notation**:
  `PLACE }o--o{ AMENITY : "has"`

---

## Entity Details

### users

- **Primary Key**: `id` (UUID, `CHAR(36)`)
- **Unique Constraint**: `email`
- **Attributes**:
  - `first_name`
  - `last_name`
  - `email`
  - `password`
  - `is_admin`

---

### places

- **Primary Key**: `id` (UUID)
- **Foreign Key**:
  - `owner_id` → `USER.id`
- **Attributes**:
  - `title`
  - `description`
  - `price`
  - `latitude`
  - `longitude`
  - `owner_id`

---

### reviews

- **Primary Key**: `id` (UUID)
- **Foreign Keys**:
  - `user_id` → `USER.id`
  - `place_id` → `PLACE.id`
- **Unique Constraint**:
  - `(user_id, place_id)` ensures one review per user per place
- **Attributes**:
  - `text`
  - `rating`
  - `user_id`
  - `place_id`

---

### amenity

- **Primary Key**: `id` (UUID)
- **Unique Constraint**: `name`
- **Attributes**:
  - `id`
  - `name`

---

### places_amenity

- **Composite Primary Key**:
  - `(place_id, amenity_id)`
- **Foreign Keys**:
  - `place_id` → `PLACE.id`
  - `amenity_id` → `AMENITY.id`
- **Purpose**:
  - Association table representing the many-to-many relationship between **Place** and **Amenity**

---

## Notes

- All entities inherit `id`, `created_at`, and `updated_at` from `BaseModelDB`.
- UUID format (`CHAR(36)`) is used for all primary keys.
- Foreign key constraints ensure **referential integrity**.
- The unique constraint on `(user_id, place_id)` in `REVIEW` prevents duplicate reviews by the same user for the same place.
- This schema represents the **core structure of the HBnB application**.





