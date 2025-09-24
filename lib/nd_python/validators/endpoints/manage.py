from pydantic import BaseModel, Field


class EpCredentialsDefaultSwitchSaveValidator(BaseModel):
    """Save Default Switch Credentials Endpoint Payload Model"""

    switch_username: str = Field(..., alias="switchUsername", description="Switch Username")
    switch_password: str = Field(..., alias="switchPassword", description="Switch Password")

    class Config:
        """Pydantic configuration."""

        validate_by_name = True
        populate_by_alias = True
        str_strip_whitespace = True
        str_min_length = 1
        extra = "forbid"
