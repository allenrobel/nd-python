from pydantic import BaseModel, ConfigDict, Field


class EpCredentialsDefaultSwitchSaveValidator(BaseModel):
    """Save Default Switch Credentials Endpoint Payload Model"""

    switch_username: str = Field(..., alias="switchUsername", description="Switch Username")
    switch_password: str = Field(..., alias="switchPassword", description="Switch Password")

    model_config = ConfigDict()
    model_config["validate_by_name"] = True
    model_config["populate_by_name"] = True
    model_config["str_strip_whitespace"] = True
    model_config["str_min_length"] = 1
    model_config["extra"] = "forbid"


class EpCredentialsRobotSwitchSaveValidator(BaseModel):
    """Save Robot Switch Credentials Endpoint Payload Model"""

    switch_username: str = Field(..., alias="switchUsername", description="Switch Username")
    switch_password: str = Field(..., alias="switchPassword", description="Switch Password")

    model_config = ConfigDict()
    model_config["validate_by_name"] = True
    model_config["populate_by_name"] = True
    model_config["str_strip_whitespace"] = True
    model_config["str_min_length"] = 1
    model_config["extra"] = "forbid"
