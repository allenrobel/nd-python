# nd-python

This repository contains Python classes and example scripts for interacting
with Cisco's Nexus Dashboard 4.1 REST API.

If you are more interested in Nexus Dashboard 3.x REST API, see the following repository:

[ndfc-python](https://github.com/allenrobel/ndfc-python)

A basic quick start guide to this repository follows.

## 1. Create a $HOME/repos directory into which we'll clone nd-python

```bash
mkdir $HOME/repos
```

## 2. Clone the nd-python repository

```bash
cd $HOME/repos
git clone https://github.com/allenrobel/nd-python.git
```

## 3. Install Python if it is not already installed

[python.org Downloads](https://www.python.org/downloads/)

## 4. Create a virtual environment

```bash
cd $HOME/repos/nd-python
# If python is in your path
python3 -m venv .venv --prompt nd-python
# If python is NOT in your path, and it was installed on MacOS
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m venv .venv --prompt nd-python
```

## 5. Source the virtual environment

- `source .venv/bin/activate`

```bash
source .venv/bin/activate
```

## 6. upgrade pip

```bash
pip install --upgrade pip
```

## 7. Install uv

```bash
pip install uv
```

## 8. Use uv to install the other dependencies

```bash
uv sync
```

## 9. Set required environment variables

```bash
# Edit $HOME/repos/nd-python/env/02-nd
# Change the following to match your environment
# ND_IP4=<your Nexus Dashboard IPv4 address>
# ND_USERNAME=<your Nexus Dashboard username, typically admin>
# ND_PASSWORD=<your Nexus Dashboard password for ND_USERNAME>
# NXOS_USERNAME=<The username of your Nexus switches, typically admin>
# NXOS_PASSWORD=<The password of your Nexus switches associated with NXOS_USERNAME>
#
# NOTE: For better security, follow the steps at Github Pages link at the top of this file.
#
# Once 02-nd is edited, source the following file (it, in turn, sources the other files)
```

```bash
source $HOME/repos/nd-python/env/env
```

## 10. Optionally, enable logging

```bash
export ND_LOGGING_CONFIG=$HOME/repos/nd-python/lib/nd_python/logging_config.json
```

## 11. Run a script that does not take any arguments

Let's try the login script since it does not require any arguments.

```bash
cd $HOME/repos/nd-python
source .venv/bin/activate
source env/env
cd examples
./login.py
```

## 12. Potential Ansible locale error

We support the optional use of Ansible Vault for credentials. Because of this,
you may see the following error.

```bash
ERROR: Ansible requires the locale encoding to be UTF-8; Detected ISO8859-1
```

You can fix it by updating a couple environment variables.

On macOS

```bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

On Ubuntu

Check if the locales are installed.

```bash
locale -a | grep -i utf
```

Example

```bash
(nd-python) arobel@glide:~/repos/nd-python$ locale -a | grep -i utf
C.utf8
en_US.utf8
(nd-python) arobel@glide:~/repos/nd-python$
```

If not, generate them.

```bash
sudo locale-gen en_US.UTF-8
```

Verify your locale is set.  If any of the following environment variables are set to something else,
change them with `export VAR="en_US.UTF-8"`

```bash
locale
```

Example

```bash
(nd-python) arobel@glide:~/repos/nd-python$ locale
LANG=en_US.UTF-8
LANGUAGE=
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC="en_US.UTF-8"
LC_TIME="en_US.UTF-8"
LC_COLLATE="en_US.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="en_US.UTF-8"
LC_PAPER="en_US.UTF-8"
LC_NAME="en_US.UTF-8"
LC_ADDRESS="en_US.UTF-8"
LC_TELEPHONE="en_US.UTF-8"
LC_MEASUREMENT="en_US.UTF-8"
LC_IDENTIFICATION="en_US.UTF-8"
LC_ALL=
(nd-python) arobel@glide:~/repos/nd-python$
```

## 13. Run a script that requires a config file

Many of the scripts take a config file.

Example config files are located in `$HOME/repos/nd-python/examples/config/*.yaml`

Let's edit a config that saves default switch credentials.

```bash
cd $HOME/repos/nd-python
source .venv/bin/activate
source env/env
cd examples
vi $HOME/repos/nd-python/examples/config/credentials_default_switch_save.yaml
```

Below is the content of this file.

```yaml
---
switch_password: mySwitchPassword
switch_username: admin
```

Modify this to match your environment by changing each item's parameters.

Save the file and then execute the associated script.

First, we'll have a look at the help facility that all scripts provide.

```bash
cd $HOME/repos/nd-python/examples
./credentials_default_switch_save.py --help
```

Example

```bash
cd $HOME/repos/nd-python/examples
(nd-python) arobel@Allen-M4 examples % ./credentials_default_switch_save.py --help
usage: credentials_default_switch_save.py [-h] [-v ANSIBLE_VAULT] -c CONFIG [-l {INFO,WARNING,ERROR,DEBUG}] [--nd-domain ND_DOMAIN] [--nd-ip4 ND_IP4] [--nd-password ND_PASSWORD] [--nd-username ND_USERNAME]

DESCRIPTION: Save default switch credentials to the controller.

options:
  -h, --help            show this help message and exit

OPTIONAL ARGS:
  -v, --ansible-vault ANSIBLE_VAULT
                        Absolute path to an Ansible Vault. e.g. /home/myself/.ansible/vault.
  --nd-domain ND_DOMAIN
                        Login domain for the Nexus Dashboard controller. If missing, the environment variable ND_DOMAIN or Ansible Vault is used.
  --nd-ip4 ND_IP4       IPv4 address for the Nexus Dashboard controller. If missing, the environment variable ND_IP4 or Ansible Vault is used.
  --nd-password ND_PASSWORD
                        Password for the Nexus Dashboard controller. If missing, the environment variable ND_PASSWORD or Ansible Vault is used.
  --nd-username ND_USERNAME
                        Username for the Nexus Dashboard controller. If missing, the environment variable ND_USERNAME or Ansible Vault is used.

MANDATORY ARGS:
  -c, --config CONFIG   Absolute path to a YAML configuration file. e.g. /home/myself/myfile.yaml

DEFAULT ARGS:
  -l, --loglevel {INFO,WARNING,ERROR,DEBUG}
                        Logging level
(nd-python) arobel@Allen-M4 examples %
```

From above, we see that we can override, on a script-by-script basis, the environment variables we configured earlier.

We also see that the `--config` argument is mandatory.  This points to the config file we just edited.  Let's use our
existing environment variables and provide only the `--config` argument.

Let's first disable debugging for shorter output.

```bash
unset ND_LOGGING_CONFIG
```

Now let's run the script.

```bash
./credentials_default_switch_save.py --config $HOME/repos/nd-python/examples/config/credentials_default_switch_save.yaml
```

Example

```bash
(nd-python) arobel@Allen-M4 examples % ./credentials_default_switch_save.py --config config/credentials_default_switch_save.yaml
Default switch credentials saved for user admin
(nd-python) arobel@Allen-M4 examples %
```

## 14. Script Documentation

Documentation is currently under construction.  We'll add a link here once it's ready.
