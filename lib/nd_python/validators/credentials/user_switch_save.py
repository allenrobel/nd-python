from pydantic import BaseModel, Field


class Switches(BaseModel):
    """
    # Summary

    Information needed to target specific switches.
    """

    fabric_name: str = Field(..., min_length=1, max_length=64, description="Fabric Name")
    switch_name: str = Field(..., min_length=1, description="Switch Name")


class CredentialsUserSwitchSaveConfigValidator(BaseModel):
    """
    # Summary

    Validate config parameters for saving user switch credentials.
    """

    switch_username: str = Field(..., min_length=1, description="Switch Username")
    switch_password: str = Field(..., min_length=1, description="Switch Password")
    switches: list[Switches]
