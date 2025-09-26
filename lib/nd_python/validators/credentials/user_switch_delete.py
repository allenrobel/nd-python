from pydantic import BaseModel, Field


class CredentialsUserSwitchDeleteConfigItem(BaseModel):
    """
    # Summary

    Validate config parameters for deleting user switch credentials.
    """

    fabric_name: str = Field(..., min_length=1, max_length=64, description="Fabric Name")
    switch_name: str = Field(..., min_length=1, description="Switch Name")


class CredentialsUserSwitchDeleteConfigValidator(BaseModel):
    """
    # Summary

    Validate config parameters for deleting user switch credentials.
    """

    config: list[CredentialsUserSwitchDeleteConfigItem]
