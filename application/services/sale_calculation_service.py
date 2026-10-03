from dataclasses import dataclass

from domain.entities.sale import Sale
from domain.entities.tax_charge import TaxCharge
from application.services.tax_charge_calculator import TaxChargeCalculator


@dataclass(frozen=True)
class SaleCalculationResult:
    subtotal: float
    tax_total: float
    charge_total: float
    final_total: float


class SaleCalculationService:
    """Calculates sale subtotal, taxes, charges, and final total."""

    def __init__(self, tax_charge_calculator: TaxChargeCalculator) -> None:
        self.tax_charge_calculator = tax_charge_calculator

    def calculate(
        self,
        sale: Sale,
        tax_charges: list[TaxCharge],
    ) -> SaleCalculationResult:
        subtotal = sum(line.subtotal for line in sale.lines)

        tax_total = 0.0
        charge_total = 0.0

        for tax_charge in tax_charges:
            if tax_charge.scope == "Overall":
                amount = self.tax_charge_calculator.calculate(
                    tax_charge=tax_charge,
                    base_amount=subtotal,
                )

                if tax_charge.type == "Tax":
                    tax_total += amount
                else:
                    charge_total += amount

        for line in sale.lines:
            for tax_charge in tax_charges:
                if tax_charge.scope != "Product":
                    continue

                amount = self.tax_charge_calculator.calculate(
                    tax_charge=tax_charge,
                    base_amount=line.subtotal,
                    product_id=line.product_id,
                )

                if tax_charge.type == "Tax":
                    tax_total += amount
                else:
                    charge_total += amount

        final_total = subtotal + tax_total + charge_total

        return SaleCalculationResult(
            subtotal=subtotal,
            tax_total=tax_total,
            charge_total=charge_total,
            final_total=final_total,
        )
