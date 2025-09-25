#!/usr/bin/env python3
"""
# credentials_user_switch_save.py

## Description

Save user switch credentials to the controller.

## Usage

1.  Modify PYTHONPATH appropriately for your setup before running this script

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/nd-python/lib
```

2. Optional, to enable logging.

``` bash
export ND_LOGGING_CONFIG=$HOME/repos/nd-python/lib/nd_python/logging_config.json
```

3. Set credentials via script command line, environment variables, or Ansible Vault

4. Run the script (below we're using command line for credentials)

``` bash
./examples/credentials_user_switch_save.py \
    --config ./examples/config/credentials_user_switch_save.yaml \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password password \
    --nd-username admin
```

## Notes

The configuration file contains the following parameters:

- config: Required; list of dictionaries with the following keys:
  - switch_name: Required; name of the switch.
  - switch_username: Required; username for the switch.
  - switch_password: Required; password for the switch.
"""
# pylint: disable=duplicate-code
# We are using isort for import sorting.
# pylint: disable=wrong-import-order

import argparse
import logging
import sys

from nd_python.common.nd_python_logger import NdPythonLogger
from nd_python.common.nd_python_sender import NdPythonSender
from nd_python.common.read_config import ReadConfig
from nd_python.common.response_handler import ResponseHandler
from nd_python.common.rest_send_v2 import RestSend
from nd_python.credentials.user_switch_save import CredentialsUserSwitchSave
from nd_python.parsers.parser_ansible_vault import parser_ansible_vault
from nd_python.parsers.parser_config import parser_config
from nd_python.parsers.parser_loglevel import parser_loglevel
from nd_python.parsers.parser_nd_domain import parser_nd_domain
from nd_python.parsers.parser_nd_ip4 import parser_nd_ip4
from nd_python.parsers.parser_nd_password import parser_nd_password
from nd_python.parsers.parser_nd_username import parser_nd_username
from nd_python.validators.credentials.user_switch_save import CredentialsUserSwitchSaveConfigItem, CredentialsUserSwitchSaveConfigValidator
from pydantic import ValidationError


def action(cfg: CredentialsUserSwitchSaveConfigItem) -> None:
    """
    Save user switch credentials.
    """
    # Prepopulate error message in case of failure
    errmsg = "Error saving user switch credentials. "
    try:
        instance = CredentialsUserSwitchSave()
        instance.rest_send = rest_send
        instance.fabric_name = cfg.fabric_name
        instance.switch_name = cfg.switch_name
        instance.switch_username = cfg.switch_username
        instance.switch_password = cfg.switch_password
        instance.commit()
    except ValueError as error:
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    print(f"fabric_name {cfg.fabric_name} switch_name {cfg.switch_name} switch_username {cfg.switch_username} credentials saved")


def setup_parser() -> argparse.Namespace:
    """
    ### Summary

    Setup script-specific parser

    Returns:
        argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        parents=[
            parser_ansible_vault,
            parser_config,
            parser_loglevel,
            parser_nd_domain,
            parser_nd_ip4,
            parser_nd_password,
            parser_nd_username,
        ],
        description="DESCRIPTION: Save user switch credentials to the controller.",
    )
    return parser.parse_args()


args = setup_parser()
NdPythonLogger()
log = logging.getLogger("nd_python.main")
log.setLevel(args.loglevel)

try:
    user_config = ReadConfig()
    user_config.filename = args.config
    user_config.commit()
except ValueError as error:
    msg = f"Exiting: Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

try:
    validator = CredentialsUserSwitchSaveConfigValidator(**user_config.contents)
except ValidationError as error:
    msg = f"{error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

try:
    nd_sender = NdPythonSender()
    nd_sender.args = args
    nd_sender.commit()
except ValueError as error:
    msg = f"Exiting.  Error detail: {error}"
    log.error(msg)
    print(msg)
    sys.exit(1)

rest_send = RestSend({})
rest_send.sender = nd_sender.sender
rest_send.response_handler = ResponseHandler()
rest_send.timeout = 2
rest_send.send_interval = 5

for item in validator.config:
    action(item)
