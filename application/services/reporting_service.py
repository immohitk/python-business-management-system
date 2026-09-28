from infrastructure.repositories.reporting_repository import ReportingRepository


class ReportingService:
    """Application service for reporting operations."""

    def __init__(self, repository: ReportingRepository) -> None:
        self.repository = repository

    def get_business_summary(self) -> dict[str, int]:
        return self.repository.get_business_summary()

    def get_sales_total(self) -> float:
        return self.repository.get_sales_total()

    def get_sales_by_date(self) -> list[dict[str, object]]:
        return self.repository.get_sales_by_date()

    def get_sales_by_product(self) -> list[dict[str, object]]:
        return self.repository.get_sales_by_product()
