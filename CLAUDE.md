# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Python library for interacting with Cisco's Nexus Dashboard 4.1 REST API. The repository uses a three-layer architecture pattern: high-level business logic classes, low-level REST endpoint definitions with Pydantic validation, and validator classes for type safety.

## Development Setup

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv .venv --prompt nd-python
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install uv
uv sync

# Set PYTHONPATH (required)
export PYTHONPATH=$PYTHONPATH:$HOME/repos/nd-python/lib

# Source environment variables
source env/env

# Optional: Enable logging
export ND_LOGGING_CONFIG=$HOME/repos/nd-python/lib/nd_python/logging_config.json
```

### Required Environment Variables
- `ND_IP4`: Nexus Dashboard IPv4 address
- `ND_USERNAME`: Nexus Dashboard username (typically admin)
- `ND_PASSWORD`: Nexus Dashboard password
- `NXOS_USERNAME`: Switch username (typically admin)
- `NXOS_PASSWORD`: Switch password
- `ND_DOMAIN`: Optional login domain (can be set via command line)

## Code Quality Commands

```bash
# Format code (line-length: 180)
black --line-length 180 <file>

# Sort imports
isort <file>

# Type checking
mypy <file>

# Linting
pylint <file>
```

## Running Scripts

```bash
# From examples directory
cd examples

# Run script without arguments
./login.py

# Run script with config file
./credentials_default_switch_save.py --config config/credentials_default_switch_save.yaml

# Override environment variables via command line
./credentials_default_switch_save.py \
    --config config/credentials_default_switch_save.yaml \
    --nd-domain local \
    --nd-ip4 10.1.1.1 \
    --nd-password password \
    --nd-username admin

# Get help for any script
./credentials_default_switch_save.py --help
```

## Architecture

### Directory Structure

```
lib/nd_python/
├── common/           # Shared utilities (logging, HTTP sender, credentials, response handling)
├── credentials/      # High-level credential management operations
├── endpoints/        # Low-level REST endpoint definitions
│   ├── base/        # Base endpoint paths (e.g., /api/v1/manage)
│   ├── fabrics/     # Fabric-related endpoints
│   └── switches/    # Switch-related endpoints
├── fabric/          # High-level fabric operations
├── parsers/         # Reusable argument parsers for CLI scripts
├── switches/        # High-level switch operations
└── validators/      # Pydantic models for validation
    ├── credentials/ # Credential-related validators
    ├── endpoints/   # Endpoint payload validators
    ├── fabric/      # Fabric-related validators
    └── switches/    # Switch-related validators

examples/            # Example scripts demonstrating usage
├── config/         # YAML configuration templates
└── *.py           # Executable scripts using nd-python library
```

### Three-Layer Architecture Pattern

Every API operation follows this pattern:

1. **High-level class** (e.g., `credentials/default_switch_save.py`)
   - Business logic and orchestration
   - Uses `RestSend` for HTTP operations
   - Requires config set via Pydantic validator
   - Must call `.commit()` before use

2. **Endpoint class** (e.g., `endpoints/manage.py`)
   - REST API definition (verb, path, body)
   - Has own Pydantic validator for payloads
   - Must call `.commit()` to validate before accessing `.body`
   - Example: `EpCredentialsDefaultSwitchSave`

3. **Validator classes** (e.g., `validators/credentials/default_switch_save.py`)
   - Pydantic models for config files
   - Validates YAML config structure
   - Example: `CredentialsDefaultSwitchSaveConfigValidator`

### Key Components

**NdPythonSender**: Handles authentication and credential selection
- Reads credentials from: command line args → environment variables → Ansible Vault
- Must call `.commit()` to perform login
- Provides logged-in `Sender` instance to `RestSend`

**RestSend**: Sends REST requests with retry logic
- Requires `sender` (from `NdPythonSender`) and `response_handler`
- Accepts endpoint class with `verb`, `path`, and `body`
- Handles timeouts and intervals between requests

**ResponseHandler**: Processes controller responses
- Abstracts response handling logic
- Returns structured result dictionaries

**Parsers**: Reusable argument parsers in `parsers/`
- `parser_config`: Required config file argument
- `parser_nd_*`: Nexus Dashboard credentials (optional, override env vars)
- `parser_nxos_*`: Switch credentials (optional)
- `parser_ansible_vault`: Ansible Vault support
- `parser_loglevel`: Logging level control

### Endpoint Path Structure

Base paths defined in `endpoints/base/endpoint.py`:
```python
base = "/api/v1/manage"
credentials = f"{base}/credentials"
fabrics = f"{base}/fabrics"
inventory = f"{base}/inventory"
switches = f"{inventory}/switches"
```

## Adding New API Operations

1. **Create endpoint class** in `endpoints/`:
```python
class EpMyNewEndpoint:
    def __init__(self):
        self.verb = "POST"
        self.path = f"{credentials}/myEndpoint"
        self.validator = EpMyNewEndpointValidator
        self._body = {}

    def commit(self):
        self.validator(**self._body)
```

2. **Create Pydantic validator** in `validators/endpoints/`:
```python
class EpMyNewEndpointValidator(BaseModel):
    field1: str
    field2: int
```

3. **Create high-level wrapper** in appropriate module:
```python
class MyNewOperation:
    def __init__(self):
        self.endpoint = EpMyNewEndpoint()
        self.rest_send = None

    def commit(self):
        self._final_verification()
        # Business logic here
```

4. **Create config validator** in `validators/`:
```python
class MyNewOperationConfigValidator(BaseModel):
    config_field1: str
    config_field2: int
```

5. **Create example script** in `examples/`:
- Use reusable parsers from `parsers/`
- Create YAML config template in `examples/config/`
- Follow standard script pattern (see below)

## Standard Script Pattern

All example scripts follow this structure:

```python
#!/usr/bin/env python3
import argparse
import logging
import sys

from nd_python.common.nd_python_logger import NdPythonLogger
from nd_python.common.nd_python_sender import NdPythonSender
from nd_python.common.read_config import ReadConfig
from nd_python.common.response_handler import ResponseHandler
from nd_python.common.rest_send_v2 import RestSend
from nd_python.parsers.parser_config import parser_config
# Import other parsers as needed
from pydantic import ValidationError

def action(cfg: MyConfigValidator) -> None:
    """Given validated config, perform the operation."""
    try:
        instance = MyOperation()
        instance.rest_send = rest_send
        instance.config = cfg
        instance.commit()
    except ValueError as error:
        log.error(f"Error: {error}")
        return
    log.info(instance.result)
    print(instance.result)

def setup_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        parents=[
            parser_config,
            parser_nd_ip4,
            parser_nd_username,
            parser_nd_password,
            # Add other parsers
        ],
        description="DESCRIPTION: What this script does.",
    )
    return parser.parse_args()

# Main execution
args = setup_parser()
NdPythonLogger()
log = logging.getLogger("nd_python.main")
log.setLevel(args.loglevel)

# Read and validate config
try:
    user_config = ReadConfig()
    user_config.filename = args.config
    user_config.commit()
    validator = MyConfigValidator(**user_config.contents)
except (ValueError, ValidationError) as error:
    log.error(f"Exiting: {error}")
    sys.exit(1)

# Setup sender and login
try:
    nd_sender = NdPythonSender()
    nd_sender.args = args
    nd_sender.commit()  # Performs login
except ValueError as error:
    log.error(f"Exiting: {error}")
    sys.exit(1)

# Setup RestSend
rest_send = RestSend({})
rest_send.sender = nd_sender.sender
rest_send.response_handler = ResponseHandler()
rest_send.timeout = 2
rest_send.send_interval = 5

action(validator)
```

## Important Patterns

### Commit Pattern
Most classes require calling `.commit()` before use:
- Performs validation (Pydantic)
- Performs login (NdPythonSender)
- Prepares object for use

### Property Verification
High-level classes use `_verify_property()` pattern:
```python
def _final_verification(self):
    self._verify_property(method_name, "config")
    self._verify_property(method_name, "rest_send")
```

### Error Handling
- Raise `ValueError` with detailed messages
- Use class-based loggers: `logging.getLogger(f"nd_python.{self.class_name}")`
- Always log errors before raising

### Credential Precedence
1. Command line arguments (highest priority)
2. Environment variables
3. Ansible Vault (lowest priority)

## Code Style

- **Line length**: 180 characters
- **Type hints**: Use extensively with Pydantic
- **Import sorting**: Uses isort with `multi_line_output = 7`
- **Docstrings**: Use triple-quoted strings with markdown formatting
- **Properties**: Use `@property` decorators for getters/setters
- **Logging**: Always include class name in logger path

## Testing

No formal test suite exists. Test by running example scripts:
```bash
cd examples
./script_name.py --config config/config_file.yaml
```

## Common Pitfalls

1. **Forgetting PYTHONPATH**: Must include `$HOME/repos/nd-python/lib`
2. **Missing commit()**: Objects must call `.commit()` before use
3. **Config file mismatch**: YAML configs must exactly match Pydantic validator schemas
4. **Ansible locale error**: Set `LC_ALL=en_US.UTF-8` and `LANG=en_US.UTF-8` if using Ansible Vault