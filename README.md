# Custom testnet

This repository is a minimal set of playbooks and inventories required to set up an eth2 node or an eth2 testnet.

## Assumption

- This setup expects that you already have deposits made and config data generated
- This setup is ideally aimed at public testnets and helps quickly provision validators

## Initial configuration

- Ensure this repo is cloned locally and that the submodules have been pulled
`git submodule update --init --recursive`

- Ensure ansible has been installed
`ansible --version`

- Copy secrets config to `<testnet>/inventory/secrets.yml` A sample secrets file can be found at `<testnet>/inventory/secrets_sample.yml`

- Copy inventory file to `<testnet>/inventory/inventory.ini` A sample inventory can be found at `<testnet>/inventory/inventory_sample.ini`

- Ensure SSH access to all servers. Check by command
`ansible -i testnets/efoundation/inventory/inventory.ini -m ping all`

## Playbooks setup for each action

`1. ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/setup_geth.yml`

`2. ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/setup_beacon_and_validators_full.yml`

`3. ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/setup_logging.yml`

## Usage

- Replace the `testnets/efoundation/inventory/inventory.ini`
- Generate the keys from the mnemonic by running the `generate_keys.sh` file (after exporting the mnemonic)
- Modify the client distribution in `select_keys_for_clients.sh` and run the script to get keys in the needed format
- If needed, modify the `testnets/efoundation/custom_config_data/` folder with the `genesis.ssz` and `config.yaml`
- Modify the `testnets/efoundation/inventory/group_vars/eth2client_<client_name>.yml` if required
- Check the inventory with `ansible-inventory -i testnets/efoundation/inventory/inventory.ini --list`
- Run the playbook to run all beacon nodes and validators with `ansible-playbook -i testnets/efoundation/inventory/inventory.ini playbooks/setup_beacon_and_validators_full.yml`

## Updating example nodes with new configs/images

Note!!: Assumptions made for the updating process:  
    - Please do not change the volume maps, container names or key locations unless you know what you are doing
    - Please do not change the `client_type`(lighthouse/teku/etc), the playbook `update-beacon-and-validator.yml` doesn't
touch the keys: it will lead to format errors!

- Update `testnets/efoundation/inventory/inventory.ini` if needed
- Make the required changes in the `inventory/group_vars` folder, the flags and image names are organized as `eth2client_<client-name>`
- There are flags separately listed for beacon node and validator, make changes as needed. All clients work as separate
beacon node/validator except for nimbus (runs both in one container).
- Run `ansible-inventory -i testnets/efoundation/inventory/inventory.ini --list` to confirm the inventory is loaded as expected,
check if the change shows up in the inventory variables
- Run `ansible-playbook -i testnets/efoundation/inventory/inventory.ini consensus-deployment-ansible/playbooks/update_beacon_and_validator.yml`.
This will stop existing beacon and validator containers and re-start them with the new config or versions. No key or beacon db is changed.
- If you wish to change the client distribution or want to fully wipe and re-deploy the entire node, then please run
`ansible-playbook -i testnets/efoundation/inventory/inventory.ini consensus-deployment-ansible/playbooks/setup_beacon_and_validators_full.yml`
- Manually check the grafana dashboards or ssh into the instance and confirm changes.
