# How to create a post-merge testnet:

This information is compiled as of end Oct 22, a lot could change in the future. 

Disclaimer: Post merge testnets currently do not work with [Nimbus](https://github.com/status-im/nimbus-eth2/issues/4193) 
and [Prysm](https://github.com/prysmaticlabs/prysm/issues/11508). Once the linked issues are closed,
we will be able to start post-merge testnets with them.

## Generic Post-Merge information:

![testnet](images/merge-testnet.png)

A post-merge testnet has two components, the Execution Layer(EL) and the Consensus Layer(CL). We set all forks to be 
active at genesis (`value: 0`) and Total Terminal Difficulty(Trigger for the merge) to 0 (`TTD: 0`). This would mean that the merge happens at genesis
and we do not go through the PoW -> PoS transition, instead we start from a merged state. 

Below are some general notes about post-merge testnets:
- The CL node handles consensus, the EL node handles teh state, transactions and RPC. The CL requests block information from the
EL via the Engine API (specific API port), the information is placed as an `Execution Payload` in the Slots proposed by the
CL.
- A CL node depends on the EL to propose slots. Without a EL, it will only be able to follow the chain in an unverified 
state. This is considered unhealthy. Without a CL, the EL will not progress at all and it will stall. 
- There exists a close coupling between the EL-CL, We recommend a 1:1 mapping. While 1-many and many-1 might work, they
are not recommended and are untested. 
- The Engine API port is exposed in a different port than the JSON-RPC port (user port), the Engine API port requires a 
JWT token that is shared between the EL and CL to authenticate the communication.

## Testnet considerations:
- The beaconchain we will spin up requires validators. But since we are starting the chain merged from genesis, we will not
get an oportunity to perform a deployment of deposit contract/deposits. Therefore, we will need to embed the deposit contract
in the genesis state of the EL chain. This is done by specifying the contract data in the `alloc` field of the `genesis.json`
for the EL chain. 
- Once the deposit contract has been embedded in the EL genesis state, we will also need to embed the deposits in the genesis
state of the CL. These deposits represent the active validators at genesis. To achieve this, we use the tool `eth2-testnet-genesis`
and it will output a `genesis.ssz` for us with the embedded deposits. 
- The CL beaconchain changes its `BeaconBody` to have different fields based on which `phase` its in. Since we are starting
a post-merge testnet, we will need to ensure that the `genesis.ssz` is of `merge` type. This will contain an 
`ExecutionPayload` field with all 0's to represent the post-merged state. 

## Steps to setup post-merge testnet:

### Genesis data:
We have a tool called the `ethereum-genesis-generator` that packages all the required dependencies into one convenient docker 
image. The required configs are specified in a `values.env` file and are passed to the container. The container will then
generate the required information in a `/data` director as well as expose it via a proxy listening on `localhost:8000`(useful for automation).

The tool can be found [here](https://github.com/skylenet/ethereum-genesis-generator/pull/10).

The rest of the guide assumes you will use the above mentioned tool. The steps to create a testnet are:
- [ ] Clone the `ethereum-genesis-generator` repo, create a folder and copy the contents of `config-example` into your folder
- [ ] Open the `values.env` file
- [ ] Configure the values as needed. It's best practice to set the `mnemonic` to a new value (You can generate one with `eth2-val-tools mnemonic`)
- [ ] Ensure that the value set as `MIN_GENESIS_ACTIVE_VALIDATOR_COUNT` is the number of validators you want at genesis
- [ ] Modify the `GENESIS_TIMESTAMP` to be the time you want the chain to start (Minus the `GENESIS_DELAY` in the `cl/config.yaml` file).
(You need the UNIX epoch time, (e.g with [epochconverter](https://www.epochconverter.com/)).

Once the changes have been made, you can run the following command to generate the genesis files:
```shell
docker run -it -u $UID -v $PWD/data:/data -v $PWD/<ENTER-FOLDERNAME-HERE>:/config -p 127.0.0.1:8000:8000 parithoshj/ethereum-gene
sis-generator:merged-genesis all
```

Once done, the genesis data will be accessible via `localhost:8000` or in the folder `$PWD/data`. 

### Deploy bootnodes:
- [ ] Deploy the bootnode with the genesis data from the previous step
- [ ] Copy the `enode` from the EL, obtain it via the startup logs or the JSON-RPC
- [ ] Copy the `enr` from the CL, obtain it via the JSON-RPC `curl localhost:5052/eth/v1/node/identity`

### Deploy the testnet:
- [ ] Create the validator keys, e.g: with `eth2-val-tools` or `ethereal` 
- [ ] Once the bootnode information has been obtained, deploy the rest of the testnet and await genesis

### Explanation of variables:
- A unique `chainID` should be used, this value is used for finding peers and reusing widespread values (1,5..) 
will lead to peering issues. Refer to [this](https://chainid.network/chains_mini.json) list for publically taken
`chainID`s
- The Beaconchain deposit contract address with its `code` and `storage` being specified in the alloc(allocations) section of the `genesis.json`. 
For an example of how this should look, refer to [this](https://github.com/eth-clients/merge-testnets/blob/main/kintsugi/genesis.json#L786).
The `code` and `storage` doesn’t change per testnet, You can always reuse the same values and change the address field as needed.
- The `mnemonics.yaml` specifies the mnemonics from which the genesis validators are derived from. The format of the file is defined below. 
The sum of the count fields should be equal to `MIN_GENESIS_ACTIVE_VALIDATOR_COUNT` in order to start the network in a simple manner. 
The yaml file allows for multiple mnemonics purely for organization/sharing purposes. You can of course use a single mnemonic for all validators:
```yaml
- mnemonic: ""  # a 24 word BIP 39 mnemonic
  count: 1234
- mnemonic: ""  # a 24 word BIP 39 mnemonic
  count: 1234  
```

### Debug advice:
- Parse the `genesis.ssz` into a readable format with `zcli pretty merge BeaconState genesis.ssz > parsedBeaconState.json`