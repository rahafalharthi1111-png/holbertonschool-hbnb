# HBnB – Part 3: Enhanced Backend with Authentication and Database Integration

## Overview

This repository contains **Part 3 of the HBnB project**, where the backend is enhanced with **authentication, authorization, and persistent database storage**.  
In this phase, the application transitions from **in-memory storage** to a **relational database** using **SQLAlchemy** with **SQLite for development** and prepares for **MySQL in production**.

Additionally, **JWT-based authentication** and **role-based access control** are introduced to secure API endpoints and enforce user permissions.

---

## Project Objectives

By completing this part, the backend achieves the following:

- 🔐 **Authentication & Authorization**
  - Implement JWT-based authentication using **Flask-JWT-Extended**
  - Enforce role-based access control using the `is_admin` attribute

- 🗄️ **Database Integration**
  - Replace in-memory repositories with **SQLite** for development
  - Prepare configuration for **MySQL** in production
  - Use **SQLAlchemy ORM** for database interaction

- ♻️ **Persistent CRUD Operations**
  - Refactor all CRUD logic to work with a relational database
  - Ensure data persists across application restarts

- 🧩 **Database Design & Visualization**
  - Design a relational schema for Users, Places, Reviews, and Amenities
  - Visualize relationships using **Mermaid.js ER diagrams**

- ✅ **Data Consistency & Validation**
  - Enforce constraints (foreign keys, unique constraints, validations)
  - Ensure integrity and reliability of stored data

---

## Learning Outcomes

By the end of Part 3, you will be able to:

- Secure APIs using JWT authentication
- Implement authorization rules for different user roles
- Use SQLAlchemy to map Python models to relational tables
- Design scalable database schemas
- Transition seamlessly between development and production databases
- Apply real-world backend best practices

---

## Project Context

Earlier parts of the HBnB project relied on **in-memory storage**, which is useful for prototyping but unsuitable for production systems.

In **Part 3**, the backend evolves into a **production-ready system** by:

- Introducing persistent storage with SQLite
- Preparing MySQL for real-world deployment
- Securing endpoints with authentication and authorization
- Structuring the application to scale reliably

This mirrors how modern backend systems are built in real-world applications.

---

## Technologies Used

- **Python**
- **Flask**
- **Flask-JWT-Extended**
- **SQLAlchemy**
- **SQLite** (development)
- **MySQL** (production-ready)
- **bcrypt2** (password hashing)
- **Mermaid.js** (ER diagrams)

---

## Database Design

The database schema includes the following entities:

- **users**
- **places**
- **reviews**
- **amenity**
- **place_amenity** (many-to-many relationship)

All relationships are enforced using **foreign keys** and **constraints**, ensuring data integrity.

📊 ER diagrams are created using **Mermaid.js** to visualize entity relationships clearly.

---



