# Sequence Diagrams for API Calls

## Explanatory Notes

The following sequence diagrams describe how the different layers of the HBnB Evolution system collaborate to process common API requests.  
Each diagram highlights the interaction between the **Client**, **Presentation Layer (API)**, **Business Logic Layer**, and **Persistence Layer (Database)**, showing the step-by-step flow required to complete each operation.

---

### 1. **User Registration**

### Description

This sequence illustrates the process of creating a new user account. The system validates the submitted data, secures the password, stores the user information, and returns a safe response excluding sensitive fields.

```mermaid
sequenceDiagram
    autonumber
    participant Client as User (Frontend)
    participant API as API (Presentation Layer)
    participant Logic as Business Logic Layer
    participant DB as Persistence Layer (Database)

    Note over Client: The user fills out the registration form
    Client->>API: POST /api/users {first_name, last_name, email, password}

    Note over API: Validate input data (presence, format, email uniqueness)
    API->>Logic: register_user(data: dict)

    Note over Logic: Hash password, generate UUID, timestamps
    Logic->>DB: INSERT INTO users (uuid, first_name, last_name, email, hashed_password, is_admin, created_at, updated_at)

    DB-->>Logic: Return new user ID and confirmation
    Logic-->>API: Return user object (without password)
    API-->>Client: 201 Created + JSON {id, first_name, last_name, email, is_admin, created_at}
```

---

### 2. **Place Creation**

### Description

This diagram represents the workflow for adding a new place. The system validates the provided information, links the place to its owner, and persists the data.

```mermaid
sequenceDiagram
    autonumber
    participant Client as User (Frontend)
    participant API as API (Presentation Layer)
    participant Logic as Business Logic Layer
    participant DB as Persistence Layer (Database)

    Note over Client: User submits a new place listing form
    Client->>API: POST /api/places {title, description, price, lat, long}

    Note right of API: Validates input data (types, required fields)
    API->>Logic: create_place(data)

    Note right of Logic: Validate data, associate current user as owner<br>Generate UUID, set created_at/updated_at<br>Sanitize fields if necessary
    Logic->>DB: INSERT INTO places (id, user_id, title, description, price, latitude, longitude, created_at, updated_at)

    Note right of DB: Save the new place entry<br>Return newly created place ID
    DB-->>Logic: Return place_id
    Logic-->>API: Return created place object (JSON, no internal fields)
    API-->>Client: 201 Created + JSON {id, title, description, price, lat, long}

    Note right of Client: Displays success message and new place

```

---

### 3. **Review Submission**

### Description

This sequence shows how a user submits a review for a place. The system ensures the user is authenticated, validates the review content, and saves it.

```mermaid
sequenceDiagram
    autonumber
    participant Client as User (Frontend)
    participant API as API (Presentation Layer)
    participant Logic as Business Logic Layer
    participant DB as Persistence Layer (Database)

    Client->>API: POST /api/reviews {place_id, rating, comment}
    Note right of Client: Authenticated user

    API->>Logic: create_review(data: dict, user_id: str)
    Note right of API: Extract user ID from auth token

    Logic->>DB: INSERT INTO reviews (user_id, place_id, rating, comment, created_at, updated_at)
    Note right of Logic: Business logic validates data and creates review

    DB-->>Logic: Return review ID and confirmation
    Logic-->>API: Return review object as dict
    API-->>Client: 201 Created + JSON {id, user_id, place_id, rating, comment, created_at, updated_at}

```

---

### 4. **Fetching a List of Places**

### Description

This diagram illustrates how the system retrieves a list of places based on optional filtering criteria and enriches the response with related data.

```mermaid
sequenceDiagram
    autonumber
    participant Client as User (Frontend)
    participant API as API (Presentation Layer)
    participant Logic as Business Logic Layer
    participant DB as Persistence Layer (Database)
    Client->>API: GET /api/places?min_price=50&max_price=200&lat=45.5&long=3.2
    API->>Logic: fetch_places(filters: dict)
    Logic->>DB: SELECT * FROM places WHERE price BETWEEN 50 AND 200 AND location NEAR (lat, long)
    DB-->>Logic: Return matching places
    loop For each place
        Logic->>DB: SELECT * FROM reviews WHERE place_id = place.id
        Logic->>DB: SELECT * FROM amenities WHERE place_id = place.id
    end
    Logic-->>API: Return list of place objects with reviews and amenities
    API-->>Client: 200 OK + JSON [\n  {id, title, price, lat, long, reviews[], amenities[]},\n  {...}\n]
    
```
