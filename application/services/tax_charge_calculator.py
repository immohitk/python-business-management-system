from domain.entities.tax_charge import TaxCharge


class TaxChargeCalculator:
    """Calculates applicable tax or charge amounts from immutable config values."""

    def calculate(
        self,
        tax_charge: TaxCharge,
        base_amount: float,
        product_id: int | None = None,
    ) -> float:
        if not tax_charge.is_active:
            return 0.0

        if tax_charge.scope == "Product":
            if tax_charge.product_id != product_id:
                return 0.0

        if tax_charge.calculation == "Percentage":
            return base_amount * tax_charge.value / 100

        return tax_charge.value

    def calculate_override(
        self,
        tax_charge: TaxCharge,
        base_amount: float,
        *,
        value: float | None = None,
    ) -> float:
        """Calculate using a transaction-level override without mutating the configuration."""
        if value is None:
            return self.calculate(tax_charge, base_amount)
        if value < 0:
            raise ValueError("Tax or charge override cannot be negative.")
        if tax_charge.calculation == "Percentage":
            return base_amount * value / 100
        return value