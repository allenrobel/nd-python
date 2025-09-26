#!/usr/bin/env python3
"""
# credentials_user_switch_get.py

## Description

Retrieve user switch credentials from the controller.

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
./examples/credentials_user_switch_get.py \
    --config ./examples/config/credentials_user_switch_get.yaml \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password password \
    --nd-username admin
```

## Notes

The configuration file contains the following parameter:

- filter: Optional; switch name to filter results.
  - If not set (or if set to a switch name that does not exist):
    - individual property accessors (e.g. instance.credential_store) will return "", e.g.:
        - instance.credential_store -> ""
        - instance.switch_id -> ""
    - instance.filtered_data will return a dictionary with all keys set to "" i.e.:
      - {'credentialStore': '', 'fabricName': '', 'ip': '', 'switchId': '', 'switchName': '', 'switchUsername': '', 'type': ''}
  - If set to a valid switch name:
    - individual property accessors will return values corresponding to the filtered switch name, e.g.:
        - instance.credential_store -> "local"
        - instance.switch_id -> "9WPLALSNXK6"
        - etc
    - instance.filtered_data will return a dictionary with values corresponding to the filtered switch name e.g.:
      - {'credentialStore': 'local', 'fabricName': 'SITE1', 'ip': '192.168.12.151', 'switchId': '9WPLALSNXK6', 'switchName': 'LE1', 'switchUsername': 'admin', 'type': 'custom'}

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
from nd_python.credentials.user_switch_get import CredentialsUserSwitchGet
from nd_python.parsers.parser_ansible_vault import parser_ansible_vault
from nd_python.parsers.parser_config import parser_config
from nd_python.parsers.parser_loglevel import parser_loglevel
from nd_python.parsers.parser_nd_domain import parser_nd_domain
from nd_python.parsers.parser_nd_ip4 import parser_nd_ip4
from nd_python.parsers.parser_nd_password import parser_nd_password
from nd_python.parsers.parser_nd_username import parser_nd_username
from nd_python.validators.credentials.user_switch_get import CredentialsUserSwitchGetConfigValidator
from pydantic import ValidationError


def action(cfg: CredentialsUserSwitchGetConfigValidator) -> None:
    """
    Retrieve user switch credentials.
    """
    # Prepopulate error message in case of failure
    errmsg = "Error retrieving user switch credentials. "
    try:
        instance = CredentialsUserSwitchGet()
        instance.rest_send = rest_send
        instance.commit()
    except ValueError as error:
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return
    if cfg.filter:
        instance.filter = cfg.filter

    print("User switch credentials (all switches):\n")
    print(f"data: {instance.data}")
    if not instance.data_filtered:
        return
    print("")
    print("User switch credentials (specific switch):\n")
    print(f"filtered_data: {instance.filtered_data}")
    print(f"credential_store: {instance.credential_store}")
    print(f"credential_type: {instance.credential_type}")
    print(f"ip: {instance.ip}")
    print(f"switch_id: {instance.switch_id}")
    print(f"switch_name: {instance.switch_name}")
    print(f"switch_username: {instance.switch_username}")


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
        description="DESCRIPTION: Retrieve user switch credentials from the controller.",
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
    validator = CredentialsUserSwitchGetConfigValidator(**user_config.contents)
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

action(validator)
