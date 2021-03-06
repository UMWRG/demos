# A worked example running the pywr model through Hydra Platform 
This is a step-by-step set of instructions for running the water allocation model
in pywr through Hydra Platform.

## Disclaimer
This example is broken into multiple scripts for illustration, and does not necessarily reflect
how a cliient interaction should be performed.

For example,a single connection would normally be used for all communiucation with Hydra Platform. 

The code is kept as short as possible for clarity, so there is a minimum of error
checking in place! 

#Prerequisites

These examples assume a unix-based shell environment. Windows users should be able
to use powershell or other

1. You have Python 3.6 installed
2. You have Docker installed

# Step 1
Get Hydra and some dependencies

```bash
    >>> pip install hydra-base
    >>>
    >>> pip install hydra-client-python
    >>> pip install click
    >>> pip install matplotlib
```

# Step 2
Create a project in Hydra. This will output a project ID to the terminal.

```bash
    >>> python create_project.py -u 1
    Project <project_id> created
```

# Step 3
Get the pywr app

```bash
    >>> docker pull pywr/hydra-pywr
```

# Step 4
Register pywr template

```bash
    >>> docker run -it hydra-pywr register
```

# Step 5
Using the pywr app, upload the network to Hydra

```bash
    >>> docker run -it hydra-pywr upload ../wad.json -p <project_id>
    Network <network_id> created 
    >>> python get_network_details.py -n <network_id>
    Name: 'Water Allocation Demo', 'ID': <network_id> 'Scenario ID': <scenario_id>     
```

# Step 6
Run the model

```bash
    >>> docker run -it hydra-pywr run  -n <network_id> -s <scenario_id>
```

# Step 7
Create a second user

```bash
    >>> python create_user.py 
    User <user_id> created
```

# Step 8
Share the network with user A, keeping 'costs' hidden.

```bash
    >>> python share_network.py -u <user_id> --hidden-attribute 'cost'
```

# Step 9
Posing as the shared user, Inspect results (in this case, simulated_volume) with a simple graph.

```bash
    >>> python plot_result.py -u <user_id> -p <password> -s <scenario_id> -a simulated_volume
```

