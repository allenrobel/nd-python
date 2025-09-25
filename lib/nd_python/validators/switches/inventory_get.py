from pydantic import BaseModel, Field


class InventoryGetConfigItem(BaseModel):
    """
    # Summary

    Validate config parameters for retrieving switches inventory.
    """

    fabric_name: str = Field(min_length=1, description="Fabric Name")


class InventoryGetConfigValidator(BaseModel):
    """
    # Summary

    Validate config parameters for retrieving switches inventory.
    """

    config: list[InventoryGetConfigItem]
