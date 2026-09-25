from application.invoice.presentation import InvoicePresentation


class InvoiceFormatter:
    """Formats invoice presentation data as readable text."""

    def format(self, invoice: InvoicePresentation) -> str:
        lines = [
            "=" * 60,
            "                         TAX INVOICE",
            "=" * 60,
            "",
            f"Invoice No. : {invoice.invoice_number}",
            f"Invoice Date: {invoice.invoice_date}",
            f"Sale ID     : {invoice.sale_id}",
            "",
            "-" * 60,
            "BILL TO",
            "-" * 60,
            f"Customer: {invoice.customer.name}",
            f"Address : {invoice.customer.address or '-'}",
            f"Phone   : {invoice.customer.phone or '-'}",
            f"Email   : {invoice.customer.email or '-'}",
            "",
            "-" * 60,
            "ITEM DETAILS",
            "-" * 60,
            f"{'S.No':<5}{'Product':<18}{'SKU':<12}"
            f"{'Qty':>5}{'Rate':>12}{'Amount':>13}",
            "-" * 60,
        ]

        for index, line in enumerate(invoice.lines, start=1):
            lines.append(
                f"{index:<5}"
                f"{line.product_name:<18}"
                f"{line.sku:<12}"
                f"{line.quantity:>5}"
                f"{line.unit_price:>12.2f}"
                f"{line.amount:>13.2f}"
            )

        lines.extend(
            [
                "-" * 60,
                f"{'TOTAL:':>47} {invoice.total_amount:>10.2f}",
                "",
                "-" * 60,
            ]
        )

        return "\n".join(lines)
