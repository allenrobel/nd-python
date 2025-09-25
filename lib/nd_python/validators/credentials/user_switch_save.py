from pydantic import BaseModel, Field


class CredentialsUserSwitchSaveConfigItem(BaseModel):
    """
    # Summary

    Validate config parameters for saving user switch credentials.
    """

    fabric_name: str = Field(..., min_length=1, max_length=64, description="Fabric Name")
    switch_name: str = Field(..., min_length=1, description="Switch Name")
    switch_username: str = Field(..., min_length=1, description="Switch Username")
    switch_password: str = Field(..., min_length=1, description="Switch Password")


class CredentialsUserSwitchSaveConfigValidator(BaseModel):
    """
    # Summary

    Validate config parameters for saving user switch credentials.
    """

    config: list[CredentialsUserSwitchSaveConfigItem]
