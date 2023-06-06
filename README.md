# Custom testnet

This repository is a minimal set of playbooks and inventories required to set up an eth2 testnet.

## Assumption

- This setup assumes you already have provisioned virtual machines that will act as nodes with docker and docker compose installed already and have an ansible.ini inventory with their details
- [Checkout this repo for terraform project that can create virtual machines using linode provider and create inventory.ini automatically.](https://github.com/gathecageorge/eth-testnet)
- This setup is ideally aimed at public testnets and helps quickly provision validators

## Initial configuration

- Install required python modules

```bash
    # Preparation libraries required
    pip3 install beautifulsoup4 ansible
```

- Ensure this repo is cloned locally

- Ensure ansible has been installed `ansible --version`

- Copy secrets config to `testnets/efoundation/inventory/group_vars/secrets.yml`

    ```text
    A sample secrets file can be found at
    testnets/efoundation/inventory/secrets_sample.yml 
    ```

- Copy inventory file to `testnets/efoundation/inventory/inventory.ini`

    ```text
    A sample inventory can be found at
    testnets/efoundation/inventory/inventory_sample.ini
    ```

- Ensure SSH access to all servers. Check by command
`ansible -i testnets/efoundation/inventory/inventory.ini -m ping all`

## Playbooks setup for each action

1. Setup eth1 execution client/geth `(Needed to run premerge testnet. This will be shared by all CL nodes)`

    ```bash
    # Setup first time only
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/setup_geth.yml

    # Setup geth firewall each time inventory changes
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/firewall/firewall_geth.yml
    ```

2. Setup logging nodes

    ```bash
    # Setup global logging first time only
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/setup_logging_global.yml

    # Setup dclocal logging and firewall each time inventory changes
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/setup_logging_dclocal.yml

    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/firewall/firewall_dclocal.yml
    ```

3. Start up bootnodes, validators and beacon nodes `#NB: Variable runningTest="test1" needs to be same name used with terraform for the test and also same in secrets.yml`

    ```bash
    # Prepare data for testnet. You need to setup some values in `testnets/efoundation/inventory/group_vars/secrets.yml` to configure how testnet will look like, eg Number of validators per node, Genesis time etc
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/prepare_custom_conf_data.yml --extra-vars "runningTest=test1"

    # Full setup the first time
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/setup_beacon_and_validators_full.yml --extra-vars "runningTest=test1"

    # Setup testnet network firewall each time inventory changes or Enable/Disable peering
    # To change peering update value in secrets.yml and rerun this
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/firewall/firewall_testnet.yml --extra-vars "runningTest=test1"

    # Reset testnet network firewall
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/firewall/firewall_testnet_reset.yml --extra-vars "runningTest=test1"
    ```

## Updating testnet with new configs/images

You can update the testnet beacon/bootnodes/validators by running

```bash
ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/update_beacon_and_validator.yml --extra-vars "runningTest=test1"
```

This will stop existing bootnode, beacon and validator containers and re-start them with the new config or versions.

### `OR`

```bash
ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/update_beacon_and_validator_and_keys.yml --extra-vars "runningTest=test1"
```

This will do the same as above and also remove existing keys and regenerate new ones. This means you must have ran `prepare_custom_conf_data.yml` playbook with new testnet configuration.

```text
If any other configuration is supposed to be changed, then run the specific playbook from number 1 - 4
```

## Other playbooks

1. Clear the testnet by stopping beacon/validator and wiping their data

    ```bash
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/clear_testnet.yml --extra-vars "runningTest=test1"
    ```

2. Restart testnet containers in bootnode/beacon/validator nodes

    ```bash
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/restart_testnet.yml --extra-vars "runningTest=test1"
    ```

3. Remove all containers and data in all nodes. `NB: Use with caution though will prompt for confirm.`

    ```bash
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/wipe_all.yml  --extra-vars "runningTest=test1"
    ```

4. Enable packet loss feature

    ```bash
    # Need to update secrets.yml with percentage or delay to be setup on network
    ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/setup_tc.yml  --extra-vars "runningTest=test1"
    ```
