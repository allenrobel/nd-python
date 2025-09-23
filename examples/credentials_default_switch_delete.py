#!/usr/bin/env python3
"""
# credentials_default_switch_delete.py

## Description

Delete default switch credentials from the controller.

This script does not take any arguments beyond those needed to connect
to the controller, so does not require a configuration file.

## Usage

1.  Modify PYTHONPATH appropriately for your setup before running this script

``` bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/nd-python/lib:$HOME/repos/ansible/collections/ansible_collections/cisco/dcnm
```

2. Optional, to enable logging.

``` bash
export ND_LOGGING_CONFIG=$HOME/repos/nd-python/lib/nd_python/logging_config.json
```

3. Set credentials via script command line, environment variables, or Ansible Vault

4. Run the script (below we're using command line for credentials)

``` bash
./examples/credentials_default_switch_delete.py \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password password \
    --nd-username admin
```

"""
# pylint: disable=duplicate-code
import argparse
import logging
import sys

from nd_python.common.nd_python_logger import NdPythonLogger
from nd_python.common.nd_python_sender import NdPythonSender
from nd_python.common.response_handler import ResponseHandler
from nd_python.credentials.default_switch_delete import CredentialsDefaultSwitchDelete
from nd_python.parsers.parser_ansible_vault import parser_ansible_vault
from nd_python.parsers.parser_loglevel import parser_loglevel
from nd_python.parsers.parser_nd_domain import parser_nd_domain
from nd_python.parsers.parser_nd_ip4 import parser_nd_ip4
from nd_python.parsers.parser_nd_password import parser_nd_password
from nd_python.parsers.parser_nd_username import parser_nd_username
from plugins.module_utils.common.rest_send_v2 import RestSend


def action() -> None:
    """
    Delete the default switch credentials.
    """
    # Prepopulate error message in case of failure
    errmsg = "Error deleting default switch credentials"
    try:
        instance = CredentialsDefaultSwitchDelete()
        instance.rest_send = rest_send
        instance.commit()
    except ValueError as error:
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    result_msg = "Default switch credentials deleted."
    log.info(result_msg)
    print(result_msg)


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
            parser_loglevel,
            parser_nd_domain,
            parser_nd_ip4,
            parser_nd_password,
            parser_nd_username,
        ],
        description="DESCRIPTION: Delete default switch credentials from the controller.",
    )
    return parser.parse_args()


args = setup_parser()
NdPythonLogger()
log = logging.getLogger("nd_python.main")
log.setLevel = args.loglevel

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

action()
