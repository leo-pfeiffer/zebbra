from datetime import datetime

from pydantic import BaseModel

from core.schemas.integrations import IntegrationProvider
from core.schemas.models import Employee
from core.schemas.utils import DateString


class EmployeeListCache(BaseModel):
    integration: IntegrationProvider
    workspace_id: str
    created_at: datetime
    from_date: int
    employees: list[Employee]


TimeSeriesDict = dict[DateString, float | None]


class DataBatch(BaseModel):
    dates: list[DateString]
    data: dict[str, TimeSeriesDict]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "dates": [
                    "2020-31-01",
                    "2020-31-02",
                    "2020-31-03",
                ],
                "data": {
                    "Sales": {
                        "2020-31-01": 111,
                        "2020-31-02": 222,
                        "2020-31-03": 333,
                    },
                    "Total Income": {
                        "2020-31-01": 111,
                        "2020-31-02": 222,
                        "2020-31-03": 333,
                    },
                },
            }
        }


class DataBatchCache(DataBatch):
    integration: IntegrationProvider
    workspace_id: str
    created_at: datetime
    from_date: int

    def to_data_batch(self) -> DataBatch:
        return DataBatch(dates=self.dates, data=self.data)
