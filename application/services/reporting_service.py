from infrastructure.repositories.reporting_repository import ReportingRepository


class ReportingService:
    """Application service for reporting operations."""

    def __init__(self, repository: ReportingRepository) -> None:
        self.repository = repository

    def get_business_summary(self) -> dict[str, int]:
        return self.repository.get_business_summary()
