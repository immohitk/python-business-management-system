from domain.entities.tax_charge import TaxCharge


class TaxChargeCalculator:
    """Calculates applicable tax or charge amounts."""

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