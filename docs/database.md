# Database Documentation

## 1. Overview

The Python Business Management System uses SQLite as its initial database.

The database is responsible for storing the persistent business data used by the application, including:

- Products
- Customers
- Suppliers
- Sales
- Sale items
- Invoices
- Database schema version

The database layer is located inside the `infrastructure/database/` package.

The current database architecture separates database operations from the rest of the application through the infrastructure layer.

```text
Presentation
     ↓
Application
     ↓
Domain
     ↓
Infrastructure
     ↓
SQLite Database
```

This separation keeps SQL and database-specific operations outside the presentation and domain layers.

---

## 2. Database Configuration

The database configuration is defined in:

```text
infrastructure/database/config.py
```

The configuration determines the project root, database directory, and database file path.

The current database location is:

```text
data/business.db
```

The database directory is created automatically when a database connection is requested.

The database file is excluded from Git using the following `.gitignore` rule:

```text
data/
```

This prevents local application data from being committed to the repository.

---

## 3. Database Connection

Database connections are handled by:

```text
infrastructure/database/connection.py
```

The main function is:

```python
get_connection()
```

This function:

1. Determines the configured database path.
2. Creates the parent directory if necessary.
3. Opens a SQLite connection.
4. Returns the connection to the caller.

A custom database path can also be supplied.

This is useful for testing because tests can create temporary SQLite databases without modifying the application's normal database.

Example:

```python
connection = get_connection(custom_database_path)
```

The connection layer therefore provides a single entry point for obtaining SQLite connections.

---

## 4. Database Initialization

Database initialization is handled by:

```text
infrastructure/database/initialization.py
```

The main function is:

```python
initialize_database()
```

Initialization performs the following operations:

1. Opens a database connection.
2. Loads the SQL schema.
3. Executes the schema.
4. Commits the changes.
5. Closes the connection.

The initialization function uses:

```text
infrastructure/database/schema.py
```

to obtain the database schema.

Database initialization is designed to be safe to run more than once.

The schema uses:

```sql
CREATE TABLE IF NOT EXISTS
```

for table creation and:

```sql
INSERT OR IGNORE
```

for the initial schema version.

Therefore, initializing an existing database does not recreate existing tables.

---

## 5. Database Schema

The current database contains seven tables:

```text
schema_version
products
customers
suppliers
sales
sale_items
invoices
```

The schema is defined in:

```text
infrastructure/database/schema.py
```

### 5.1 schema_version

The `schema_version` table stores the current database schema version.

Columns:

| Column  | Type    | Description             |
| ------- | ------- | ----------------------- |
| id      | INTEGER | Primary key             |
| version | TEXT    | Database schema version |

The initial schema version is:

```text
1
```

The table allows the database schema version to be tracked independently from the application version.

---

### 5.2 products

The `products` table stores product and inventory information.

Columns:

| Column      | Type    | Description                  |
| ----------- | ------- | ---------------------------- |
| id          | INTEGER | Primary key                  |
| name        | TEXT    | Product name                 |
| description | TEXT    | Optional product description |
| sku         | TEXT    | Unique stock keeping unit    |
| price       | REAL    | Product price                |
| quantity    | INTEGER | Current quantity             |
| created_at  | TEXT    | Creation timestamp           |

The `sku` column is unique.

This prevents multiple products from using the same SKU.

---

### 5.3 customers

The `customers` table stores customer information.

Columns:

| Column     | Type    | Description            |
| ---------- | ------- | ---------------------- |
| id         | INTEGER | Primary key            |
| name       | TEXT    | Customer name          |
| phone      | TEXT    | Optional phone number  |
| email      | TEXT    | Optional email address |
| address    | TEXT    | Optional address       |
| created_at | TEXT    | Creation timestamp     |

---

### 5.4 suppliers

The `suppliers` table stores supplier information.

Columns:

| Column     | Type    | Description            |
| ---------- | ------- | ---------------------- |
| id         | INTEGER | Primary key            |
| name       | TEXT    | Supplier name          |
| phone      | TEXT    | Optional phone number  |
| email      | TEXT    | Optional email address |
| address    | TEXT    | Optional address       |
| created_at | TEXT    | Creation timestamp     |

---

### 5.5 sales

The `sales` table stores the main information about a sale.

Columns:

| Column       | Type    | Description         |
| ------------ | ------- | ------------------- |
| id           | INTEGER | Primary key         |
| customer_id  | INTEGER | Associated customer |
| sale_date    | TEXT    | Date of sale        |
| total_amount | REAL    | Total sale amount   |
| created_at   | TEXT    | Creation timestamp  |

The `customer_id` column references the `customers` table.

Relationship:

```text
customers
    │
    └── sales
```

---

### 5.6 sale_items

The `sale_items` table stores the individual products included in a sale.

Columns:

| Column     | Type    | Description        |
| ---------- | ------- | ------------------ |
| id         | INTEGER | Primary key        |
| sale_id    | INTEGER | Associated sale    |
| product_id | INTEGER | Associated product |
| quantity   | INTEGER | Quantity sold      |
| unit_price | REAL    | Price per unit     |

The table connects sales with products.

Relationships:

```text
sales
   │
   └── sale_items ─── products
```

A sale can therefore contain multiple sale items.

---

### 5.7 invoices

The `invoices` table stores invoice information associated with sales.

Columns:

| Column         | Type    | Description           |
| -------------- | ------- | --------------------- |
| id             | INTEGER | Primary key           |
| sale_id        | INTEGER | Associated sale       |
| invoice_number | TEXT    | Unique invoice number |
| invoice_date   | TEXT    | Invoice date          |
| total_amount   | REAL    | Invoice total         |
| created_at     | TEXT    | Creation timestamp    |

The `sale_id` column references the `sales` table.

The `invoice_number` column is unique.

Relationship:

```text
sales
   │
   └── invoices
```

---

## 6. Database Relationships

The current database relationships can be represented as follows:

```text
customers
    │
    │ customer_id
    ▼
  sales
    │
    ├───────────────┐
    │               │
    │ sale_id       │
    ▼               ▼
sale_items       invoices
    │
    │ product_id
    ▼
products
```

The main relationships are:

### Customer → Sales

A sale references a customer through:

```text
sales.customer_id
```

which references:

```text
customers.id
```

### Sale → Sale Items

A sale item references its sale through:

```text
sale_items.sale_id
```

which references:

```text
sales.id
```

### Product → Sale Items

A sale item references the product being sold through:

```text
sale_items.product_id
```

which references:

```text
products.id
```

### Sale → Invoice

An invoice references its associated sale through:

```text
invoices.sale_id
```

which references:

```text
sales.id
```

---

## 7. Repository Persistence

The application uses repositories to separate persistence logic from the domain and application layers.

Repository implementations are located in:

```text
infrastructure/repositories/
```

The repository layer currently provides persistence for:

- Products
- Customers
- Suppliers
- Sales
- Sale items
- Invoices

The base repository contract is defined in:

```text
infrastructure/repositories/base.py
```

The repository contract provides common operations such as:

```text
add()
get_by_id()
get_all()
delete()
```

The sale repository additionally supports sale-item persistence.

The invoice repository provides invoice persistence.

This structure prevents higher application layers from directly depending on SQL statements.

---

## 8. Database Testing

Database behavior is tested using `pytest`.

The database tests cover:

- Database configuration
- Database connection creation
- Custom database paths
- Database initialization
- Schema creation
- Schema version
- Table structure
- Column definitions
- Constraints
- Foreign-key relationships
- Repository persistence
- Master-data persistence
- Sale and invoice persistence

Unit-level database tests are located under:

```text
tests/unit/
```

Integration tests are located under:

```text
tests/integration/
```

The integration tests use temporary SQLite database files.

This prevents test execution from modifying the normal application database.

---

## 9. Clean Environment Verification

The database foundation should work correctly from a clean environment.

A clean database initialization should:

1. Create the database directory when necessary.
2. Create the SQLite database file.
3. Create all required tables.
4. Insert the initial schema version.
5. Allow repositories to persist and retrieve data.
6. Allow initialization to be executed repeatedly without breaking the database.

The expected database tables are:

```text
customers
invoices
products
sale_items
sales
schema_version
suppliers
```

---

## 10. Current Database Scope

This document describes the database implementation currently present in the project.

It intentionally documents only the implemented database functionality.

Future business functionality is not considered part of the current database design unless it has been implemented and tested in the project.

The database can be extended in future versions as new application requirements are implemented.

---

## 11. Related Source Files

The main database-related source files are:

```text
infrastructure/
├── database/
│   ├── config.py
│   ├── connection.py
│   ├── initialization.py
│   └── schema.py
│
└── repositories/
    ├── base.py
    ├── product.py
    ├── customer.py
    ├── supplier.py
    ├── sale.py
    └── invoice.py
```

Database tests are located in:

```text
tests/
├── unit/
└── integration/
```

---

## 12. Summary

The current database foundation provides a SQLite-based persistence layer for the Python Business Management System.

It includes:

- Centralized database configuration
- Reusable database connections
- Repeatable database initialization
- Versioned schema
- Seven core database tables
- Defined table relationships
- Repository-based persistence
- Unit-level database testing
- Integration-level persistence testing
- Temporary databases for isolated integration tests

This database foundation provides the persistence layer required for the current version of the application while keeping database-specific logic separated from the rest of the system.
