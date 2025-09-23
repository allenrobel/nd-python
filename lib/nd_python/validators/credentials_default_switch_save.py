from pydantic import BaseModel, Field


class CredentialsDefaultSwitchSaveConfigValidator(BaseModel):
    """
    # Summary

    Validate config parameters for saving default switch credentials.
    """

    switch_username: str = Field(..., min_length=1, description="Switch Username")
    switch_password: str = Field(..., min_length=1, description="Switch Password")
