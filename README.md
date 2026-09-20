# 🧾 Python Business Management System

> A Python-based business management system for managing everyday business operations through a structured and maintainable application.

**🚧 Status:** In Development

---

## 📌 About

The **Python Business Management System** is a software project focused on building a practical solution for managing core business operations such as products, inventory, sales, customers, suppliers, and invoicing.

The project is being developed incrementally with an emphasis on:

- Clean and maintainable Python code
- Object-oriented design
- SQL and database management
- Business logic
- Modular architecture
- Practical application development
- Automated testing
- Database reliability

The goal is to build something that is not only technically sound, but also useful in a real business environment.

---

## ✨ What It Offers

The system is currently being developed around the following business-management areas:

- 📦 Product management
- 📊 Inventory management
- 🛒 Sales management
- 👥 Customer management
- 🚚 Supplier management
- 🧾 Invoicing

The current implementation also includes a SQLite-based persistence layer with database initialization, schema management, repository-based persistence, application services for master data and inventory operations, product-linked stock movement history, timestamped inventory movement records, and automated unit and integration testing.

Functionality is being introduced progressively as the application develops.

---

## 🖥️ Preview

The application interface and major workflows will be showcased here as the project becomes functionally usable.

### Application Preview

> Screenshots will be added as the corresponding features and interfaces are completed.

### Planned Screenshots

- Dashboard
- Product management
- Inventory
- Sales
- Invoice creation
- Customer management
- Reports

---

## 🏗️ Architecture

The project follows a layered architecture to keep different responsibilities separated.

```text
Presentation
     │
     ▼
Application
     │
     ▼
Domain
     │
     ▼
Infrastructure
     │
     ▼
Database
```

### Presentation

Handles user interaction with the application.

### Application

Coordinates application workflows and services.

### Domain

Contains the core business entities and business rules.

### Infrastructure

Handles database access and other implementation details.

This separation helps keep the core application logic independent from the interface and infrastructure.

---

## 📁 Project Structure

```text
python-business-management-system/

│
├── application/
│   ├── services/
│   └── __init__.py
│
├── domain/
│   ├── entities/
│   ├── rules/
│   └── __init__.py
│
├── infrastructure/
│   ├── database/
│   ├── repositories/
│   └── __init__.py
│
├── presentation/
│   ├── cli/
│   └── __init__.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── __init__.py
│
├── docs/
│
├── pyproject.toml
├── README.md
└── .gitignore
```

The structure will evolve naturally as new functionality is introduced.

---

## 🗄️ Database

The project currently uses **SQLite** as its database.

The database foundation includes:

- Centralized database configuration
- SQLite connection management
- Repeatable database initialization
- Versioned database schema
- Eight core database tables
- Defined table relationships
- Repository-based persistence
- Persistent stock movement history
- Product-linked stock movement records
- Timestamped stock movement records
- Integration testing with temporary databases
- Clean-environment database verification

The current database tables are:

```text
schema_version
products
customers
suppliers
sales
sale_items
invoices
stock_movements
```

The `stock_movements` table stores inventory movement history associated with products, including:

- Stock additions
- Stock adjustments
- Stock deductions
- Movement timestamp
- Resulting stock quantity

Each persisted stock movement records when the change occurred, allowing inventory changes to be traced over time.

Stock movement persistence is handled through the repository layer, keeping database operations separate from the domain model.

Detailed database documentation is available in:

```text
docs/database.md
```

---

## 🛠️ Technology Stack

| Technology | Purpose                                  |
| ---------- | ---------------------------------------- |
| Python     | Application development                  |
| SQL        | Database operations                      |
| SQLite     | Local database                           |
| Pytest     | Automated testing                        |
| Git        | Version control                          |
| GitHub     | Source control and project collaboration |

---

## 🚀 Getting Started

### Requirements

- Python 3.12+
- Git

### Clone

```bash
git clone <repository-url>
cd python-business-management-system
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Install the Project

```bash
python -m pip install -e ".[dev]"
```

### Run the Application

```bash
python -m presentation.cli
```

### Run Tests

```bash
pytest
```

The current test suite covers database configuration, database initialization, schema behavior, repository persistence, CLI behavior, inventory rules, stock movement persistence, timestamped movement history, and integration scenarios.

---

## 🖥️ Current CLI

The current CLI provides navigation for:

- Products
- Inventory
- Sales
- Customers
- Suppliers

### Currently Available

#### Products

- Add product
- List products
- Get product
- Delete product

#### Customers

- Add customer
- List customers
- Get customer
- Delete customer

#### Suppliers

- Add supplier
- List suppliers
- Get supplier
- Delete supplier

### Inventory

The inventory domain currently supports:

- Stock quantity validation
- Stock additions
- Stock adjustments
- Stock deductions
- Stock movement tracking
- Timestamped stock movement history
- Persistent stock movement recording

Inventory operations are coordinated through the application service layer, which applies the domain rules and persists the resulting product and stock movement changes.

The inventory service currently supports:

- Stock-in operations
- Stock adjustments
- Stock-out operations
- Invalid quantity protection
- Insufficient-stock protection
- Timestamped stock movement recording
- Persistent stock movement history

The interactive inventory workflow currently supports:

- View stock
- Stock-in operations
- Stock adjustments
- Stock-out operations
- Movement history
- CLI error handling

Inventory CLI operations use the application service layer rather than accessing the database directly. Inventory changes are persisted through the repository layer and can be traced through timestamped stock movement history.

Sales and invoicing workflows will also be implemented progressively in future releases.

Inventory persistence is handled through the repository layer and is covered by automated unit and integration tests.

---

## 📦 Release History

### v0.5.2 — Sales Calculations

- Added subtotal calculation for sale lines
- Added calculated total support for sales with single and multiple sale lines
- Added explicit application of calculated totals to persisted sale totals
- Added pricing behavior without CLI coupling
- Added calculation edge-case coverage for fractional unit prices
- Added validation coverage for invalid sale-line pricing
- Verified sales calculations with 22 automated unit tests

**Release result:** Deterministic sales totals.

### v0.5.1 — Sale Domain Model

- Added the SaleLine domain entity
- Added the Sale domain entity
- Added validation for sale customers, dates, totals, and creation timestamps
- Added validation for sale line products, quantities, and unit prices
- Added domain integration coverage for sales containing multiple sale lines
- Added tests for preserving sale line data within a sale
- Verified the sale domain with 13 automated tests

**Release result:** Sales are domain concepts.

### v0.5.0 — Inventory CLI and Regression

- Added interactive inventory CLI workflows
- Added stock viewing through the CLI
- Added stock-in, stock adjustment, and stock-out operations through the CLI
- Added inventory movement history through the CLI
- Added CLI error handling for invalid input and inventory service errors
- Added end-to-end inventory CLI integration coverage
- Verified the complete application with 236 automated tests

**Release result:** Safe inventory management.

### v0.4.4 — Stock Movement History

- Added timestamps to stock movement records
- Propagated movement timestamps through product and inventory operations
- Persisted stock movement timestamps in the database
- Added repository and integration coverage for movement timestamps
- Stock additions, adjustments, and deductions can now be traced with their recorded time
- Updated persistence tests to verify timestamped movement history

**Release result:** Stock changes are explainable through timestamped movement history.

---

## 🧪 Development

The project is developed incrementally:

```text
Understand
    ↓
Design
    ↓
Implement
    ↓
Test
    ↓
Review
    ↓
Commit
```

Each feature is developed as part of the overall application rather than being added as an isolated demonstration.

The project also uses automated unit and integration tests to verify implemented functionality.

Development is organized into versioned releases, with each release introducing a focused set of improvements.

---

## 🤝 Contributing

Contributions and suggestions are welcome.

If you would like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add or update tests where appropriate
5. Verify that the project continues to work
6. Open a pull request

For larger changes, opening an issue first is recommended so the approach can be discussed before implementation.

---

## 📚 Documentation

Technical documentation and project notes are maintained in:

```text
docs/
```

Current documentation includes:

```text
docs/
└── database.md
```

Additional documentation will be added as the project grows.

---

## 👨‍💻 Author

**Mohit Kumar**

M.Tech Computer Science & Engineering

**Python • SQL • Software Development**

---

## ⭐ Support

If you find the project interesting, consider giving it a ⭐ on GitHub.

Suggestions, feedback, and contributions are always welcome.

---

> **Built for real-world problems. Developed one step at a time.**
