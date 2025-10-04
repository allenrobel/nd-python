#!/usr/bin/env python3
"""
# fabric_detail_get.py

## Description

Retrieve fabric details from the controller.

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

4. Run the script (below we're using environment variables for credentials)

``` bash
export ND_DOMAIN=local
export ND_IP4=10.1.1.1
export ND_USERNAME=admin
export ND_PASSWORD=my_password
./examples/fabric_detail_get.py --config config/fabric_detail_get.yaml
```

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
from nd_python.endpoints.manage import EpFabricDetailGet
from nd_python.fabric.fabric_detail_get import FabricDetailGet
from nd_python.parsers.parser_ansible_vault import parser_ansible_vault
from nd_python.parsers.parser_config import parser_config
from nd_python.parsers.parser_loglevel import parser_loglevel
from nd_python.parsers.parser_nd_domain import parser_nd_domain
from nd_python.parsers.parser_nd_ip4 import parser_nd_ip4
from nd_python.parsers.parser_nd_password import parser_nd_password
from nd_python.parsers.parser_nd_username import parser_nd_username
from nd_python.validators.fabric.fabric_detail_get import FabricDetailGetConfigValidator
from pydantic import ValidationError


def set_endpoint_filter(cfg: FabricDetailGetConfigValidator, endpoint: EpFabricDetailGet) -> None:
    """
    Set the filter parameters on the endpoint instance

    Args:
        cfg (FabricDetailGetConfigValidator): Config validator
        endpoint (EpFabricDetailGet): Endpoint instance on which to set parameters
    """
    if cfg.max is not None:
        endpoint.query_filter.max = cfg.max
    if cfg.filter is not None:
        endpoint.query_filter.filter = cfg.filter
    if cfg.offset is not None:
        endpoint.query_filter.offset = cfg.offset
    if cfg.sort is not None:
        endpoint.query_filter.sort = cfg.sort
    endpoint.commit()


def action(cfg: FabricDetailGetConfigValidator) -> None:
    """
    Retrieve fabric details from the controller.
    """
    # Prepopulate error message in case of failure
    errmsg = "Error retrieving fabric details. "
    endpoint = EpFabricDetailGet()
    set_endpoint_filter(cfg, endpoint)
    try:
        instance = FabricDetailGet()
        instance.endpoint = endpoint
        instance.rest_send = rest_send
        instance.commit()
    except ValueError as error:
        errmsg += f"Error detail: {error}"
        log.error(errmsg)
        print(errmsg)
        return

    print("Fabric details:\n")
    print("data:", instance.data)


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
        description="DESCRIPTION: Retrieve fabric details from the controller.",
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
    validator = FabricDetailGetConfigValidator(**user_config.contents)
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
