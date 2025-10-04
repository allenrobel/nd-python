from pydantic import BaseModel, Field


class FabricDetailGetConfigValidator(BaseModel):
    """
    # Summary

    Validate config parameters for retrieving fabric details.
    """

    max: int | None = Field(default=0, description="Maximum number of records to return")
    filter: str | None = Field(default="", min_length=1, description="Filter for fabric details e.g. name:my_fabric")
    offset: int | None = Field(default=0, description="Number of records to offset into the result set")
    sort: str | None = Field(default=None, min_length=1, description="Sort order of the results e.g. name:asc")
