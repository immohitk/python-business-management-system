# Invoice Numbering

## MVP Numbering Format

Invoices use a predictable sequential public number:

- INV-000001
- INV-000002
- INV-000003

## Numbering Rules

- Numbering starts at INV-000001.
- Each newly generated invoice receives the next sequence number.
- The invoice number is persisted with the invoice.
- Invoice numbers must remain unique.
- The application layer is responsible for generating invoice numbers.
- The infrastructure layer is responsible for persistence.
- SQLite provides the final uniqueness constraint through the invoice_number column.

## MVP Limitations

The numbering approach is designed for the current single-database SQLite MVP.

It does not attempt to provide distributed sequence coordination or a production-grade numbering service for multiple application instances.

Future versions may replace or extend this approach if the system requires more advanced concurrency or deployment support.
