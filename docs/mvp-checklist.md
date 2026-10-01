# MVP Feature Acceptance Checklist

This checklist defines the public functional scope of the Business Management System MVP.

## Products

- [x] Add product
- [x] List products
- [x] Get product by ID
- [x] Delete product
- [x] Persist product data in SQLite

## Customers

- [x] Add customer
- [x] List customers
- [x] Get customer by ID
- [x] Delete customer
- [x] Persist customer data in SQLite

## Suppliers

- [x] Add supplier
- [x] List suppliers
- [x] Get supplier by ID
- [x] Delete supplier
- [x] Persist supplier data in SQLite

## Inventory

- [x] View current stock
- [x] Stock in
- [x] Adjust stock
- [x] Stock out
- [x] View stock movement history
- [x] Persist stock movements
- [x] Reject invalid stock operations
- [x] Prevent insufficient-stock operations

## Sales

- [x] Create sale
- [x] Add products and quantities to a sale
- [x] Calculate sale totals
- [x] Deduct inventory after sale
- [x] List sales
- [x] Persist sale data in SQLite

## Invoices

- [x] Create invoice from sale
- [x] Generate invoice number
- [x] Show invoice details
- [x] Persist invoice data in SQLite

## Reports

- [x] Business summary report
- [x] Sales report
- [x] Inventory report
- [x] Customer report
- [x] Supplier report
- [x] Low-stock reporting

## Integrated Business Workflow

- [x] Product creation
- [x] Customer creation
- [x] Sale creation
- [x] Automatic stock deduction
- [x] Invoice creation from sale
- [x] Invoice presentation
- [x] Business reporting
- [x] Shared CLI application context
- [x] End-to-end workflow verified with SQLite

## Acceptance Verification

- [x] CLI feature tests pass
- [x] Application service integration tests pass
- [x] CLI integration tests pass
- [x] Full project test suite passes

## MVP Status

The public functional MVP workflows are implemented and covered by the current automated tests.

This checklist is used as the acceptance reference for v0.9.1 functional completion.
