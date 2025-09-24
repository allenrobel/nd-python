from pydantic import BaseModel, Field


class CredentialsUserSwitchGetConfigValidator(BaseModel):
    """
    # Summary

    Validate config parameters for retrieving user switch credentials.
    """

    filter: str = Field(default="", min_length=0, description="Optional filter to retrieve specific switch credentials.  A switch name e.g. myLeafSwitch1")
