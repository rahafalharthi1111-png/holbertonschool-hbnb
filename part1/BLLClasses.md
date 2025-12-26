# Class Diagram for Business Logic Layer


## Explanatory Notes

Detailed class diagram for the Business Logic layer of the HBnB application. This diagram will depict the entities within this layer, their attributes, methods, and the relationships between them. The primary goal is to provide a clear and detailed visual representation of the core business logic, focusing on the key entities: User, Place, Review, and Amenity.

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'darkMode': true,
    'primaryColor': '#161b22',
    'primaryTextColor': '#c9d1d9',
    'primaryBorderColor': '#30363d',
    'lineColor': '#58a6ff',
    'secondaryColor': '#0d1117',
    'tertiaryColor': '#21262d',
    'mainBkg': '#0d1117'
  }
}}%%

classDiagram
    class BaseModel {
        <<abstract>>
        -UUID id
        -DateTime created_at
        -DateTime updated_at
        +save() None
        #create() None
        #update() None
        #delete() None
    }

    class User {
        -String first_name
        -String last_name
        -String email
        -String password
        -bool is_admin
        +register(data dict) bool
        +update(data dict) bool
        +delete() bool
    }

    class Place {
        +String title
        +String description
        -float price
        -float latitude
        -float longitude
        +create(owner_id UUID, data dict) bool
        +update(data dict) bool
        +delete() bool
        +get_amenities() List~Amenity~
    }

    class Review {
        -User user
        -Place place
        -int rating
        -String comment
        +create(user_id UUID, place_id UUID, data dict) bool
        +update(data dict) bool
        +delete() bool
        +list_by_place(place_id UUID)
    }

    class Amenity {
        +String name
        +String description
        +create(data dict) bool
        +update(data dict) bool
        +delete() bool
        +get_amenities() List~Amenity~
    }

    %% Inheritance Relationships
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    %% Associations and Multiplicities
    User "1" -- "0..*" Place : owns
    User "1" -- "0..*" Review : writes
    Place "1" -- "0..*" Review : has
    Place "0..*" *-- "0..*" Amenity : features


    %% Notes Attachments
    note for User "email and password are private with validation
    password is write-only and hashed" 
    note for Place "price, latitude, longitude are validated in setters"
    note for Review "rating must be 1-5"
    note for Amenity "many-to-many relationship with Place"
