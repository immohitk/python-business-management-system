# GUI Architecture

## Framework

The project uses **Tkinter** for the desktop GUI.

Tkinter is selected because it is included with Python, requires minimal additional dependencies, and is suitable for building the project's desktop business-management interface.

## GUI Responsibility

The GUI is responsible for:

- Window and screen presentation
- User navigation
- User input collection
- Basic UI-level validation
- Displaying application results and errors

Business rules remain outside the GUI.

## Architecture Boundary

The GUI follows the existing layered architecture:

```text
GUI
 ↓
Application Services
 ↓
Domain
 ↓
Infrastructure
 ↓
Database
```

GUI screens should use application services for business operations rather than implementing business logic directly.

## Database Access

The GUI must not access the database directly.

Direct SQL, repository calls, and database connection management remain outside the presentation layer's GUI screens.

## Business Logic

Existing application services and domain rules remain the source of business behavior.

GUI code should not duplicate:

- Business validation rules
- Stock-management rules
- Sale calculations
- Invoice generation logic
- Reporting logic
- Database persistence logic

## GUI Structure

GUI code will remain inside the presentation layer:

```text
presentation/
└── gui/
```

Future GUI screens and navigation components will be added under this package while keeping the existing CLI presentation layer independent.

## Goal

The GUI should provide a real desktop interface for the existing business-management system without changing the established application and domain architecture.
