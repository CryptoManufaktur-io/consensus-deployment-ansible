# Custom testnet

This repository is a minimal set of playbooks and inventories required to set up an eth2 testnet.

## Assumption

- This setup assumes you already have provisioned virtual machines that will act as nodes and have an ansible.ini inventory with their details
- [Checkout this repo for terraform project that can create virtual machines using linode provider and create inventory.ini automatically.](https://github.com/gathecageorge/eth-testnet)
- This setup is ideally aimed at public testnets and helps quickly provision validators

## Initial configuration

- Ensure this repo is cloned locally

- Ensure ansible has been installed `ansible --version`

- Copy secrets config to `testnets/<testnet>/inventory/group_vars/secrets.yml`

    ```text
    A sample secrets file can be found at
    testnets/<testnet>/inventory/secrets_sample.yml 
    ```

- Copy inventory file to `testnets/<testnet>/inventory/inventory.ini`

    ```text
    A sample inventory can be found at
    testnets/<testnet>/inventory/inventory_sample.ini
    ```

- Ensure SSH access to all servers. Check by command
`ansible -i testnets/<testnet>/inventory/inventory.ini -m ping all`

## Playbooks setup for each action

1. Prepare data for testnet. You need to setup some values in `testnets/<testnet>/inventory/group_vars/secrets.yml` to configure how testnet will look like, eg Number of validators per node, Genesis time etc

    ```text
    ansible-playbook -i testnets/<testnet>/inventory/inventory.ini playbooks/prepare_custom_conf_data.yml
    ```

2. Setup eth1 execution client/geth

    ```text
    ansible-playbook -i testnets/<testnet>/inventory/inventory.ini playbooks/setup_geth.yml
    ```

3. Setup logging nodes

    ```text
    ansible-playbook -i testnets/<testnet>/inventory/inventory.ini playbooks/setup_logging.yml
    ```

4. Start up bootnodes, validators and beacon nodes

    ```text
    ansible-playbook -i testnets/<testnet>/inventory/inventory.ini playbooks/setup_beacon_and_validators_full.yml --extra-vars "runningTest=test1"
    ```

## Updating testnet with new configs/images

You can update the testnet beacon/bootnodes/validators by running

```text
ansible-playbook -i testnets/<testnet>/inventory/inventory.ini playbooks/update_beacon_and_validator.yml --extra-vars "runningTest=test1"
```

This will stop existing bootnode, beacon and validator containers and re-start them with the new config or versions.

### `OR`

```text
ansible-playbook -i testnets/<testnet>/inventory/inventory.ini playbooks/update_beacon_and_validator_and_keys.yml --extra-vars "runningTest=test1"
```

This will do the same as above and also remove existing keys and regenerate new ones. This means you must have ran `prepare_custom_conf_data.yml` playbook with new testnet configuration.

```text
If any other configuration is supposed to be changed, then run the specific playbook from number 1 - 4
```

## Other playbooks

1. Clear the testnet by stopping beacon/validator and wiping their data

    ```text
    ansible-playbook -i testnets/<testnet>/inventory/inventory.ini playbooks/clear_testnet.yml --extra-vars "runningTest=test1"
    ```

2. Restart testnet containers in bootnode/beacon/validator nodes

    ```text
    ansible-playbook -i testnets/<testnet>/inventory/inventory.ini playbooks/restart_testnet.yml --extra-vars "runningTest=test1"
    ```

3. Remove all containers and data in all nodes. `NB: Use with caution though will prompt for confirm.`

    ```text
    ansible-playbook -i testnets/<testnet>/inventory/inventory.ini playbooks/wipe_all.yml
    ```
