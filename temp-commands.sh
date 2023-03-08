docker run --rm --name ptest \
-v $PWD/testnets/efoundation/custom_config_data/test1:/custom_config_data \
prysmaticlabs/prysm-beacon-chain:latest \
--accept-terms-of-use=true \
--datadir="/beacondata" \
--genesis-state="/custom_config_data/genesis.ssz" \
--chain-config-file="/custom_config_data/config.yaml" \
--verbosity="debug" \
--min-sync-peers=1 \
--pprof \
--p2p-host-ip=127.0.0.1 \
--p2p-max-peers=2 \
--p2p-udp-port=4000 --p2p-tcp-port=4001 \
--monitoring-host=0.0.0.0 --monitoring-port=4002 \
--rpc-host=0.0.0.0 --rpc-port=4003 \
--grpc-gateway-host=0.0.0.0 \
--grpc-gateway-port=4004 \
--execution-endpoint="http://geth:8545"


docker run --rm --name ltest \
-v $PWD/testnets/efoundation/custom_config_data/test1:/custom_config_data \
sigp/lighthouse:latest \
lighthouse \
--debug-level="debug" \
--datadir "/beacondata" \
--testnet-dir="/custom_config_data" \
bn \
--disable-enr-auto-update \
--enr-address=127.0.0.1 \
--enr-tcp-port=4000  \
--enr-udp-port=4000 \
--port=4000  \
--discovery-port=4000 \
--http \
--http-address 0.0.0.0 \
--http-port "4001" \
--metrics \
--metrics-address 0.0.0.0 \
--metrics-port "4002" \
--listen-address 0.0.0.0 \
--graffiti="bbb" \
--target-peers=2 \
--eth1  \
--eth1-endpoints "http://geth:8545"


docker run --rm --name ttest \
-v $PWD/testnets/efoundation/custom_config_data/test1:/custom_config_data \
consensys/teku:latest \
--network "/custom_config_data/config.yaml" \
--initial-state "/custom_config_data/genesis.ssz" \
--data-storage-mode=PRUNE \
--p2p-enabled=true \
--p2p-advertised-ip=127.0.0.1 \
--p2p-port="4000" \
--p2p-advertised-port=4000 \
--logging="debug" \
--log-destination=CONSOLE \
--log-file="/beacondata/log_outputs" \
--p2p-peer-upper-bound=2 \
--metrics-enabled=true --metrics-interface=0.0.0.0 --metrics-port="4002" \
--p2p-discovery-enabled=true \
--p2p-peer-lower-bound=1 \
--rest-api-enabled=true \
--rest-api-docs-enabled=true \
--rest-api-interface=0.0.0.0 \
--rest-api-port="4001" \
--metrics-host-allowlist="*" \
--rest-api-host-allowlist="*" \
--ee-endpoint="http://geth:8545" \
--eth1-endpoint "http://geth:8545"


docker run --rm --name ntest \
-v $PWD/testnets/efoundation/custom_config_data/test1:/custom_config_data \
statusim/nimbus-eth2:multiarch-latest \
--non-interactive \
--status-bar=false \
--tcp-port=4000 \
--udp-port=4000 \
--max-peers="2" \
--network="/custom_config_data" \
--graffiti="bbb" \
--log-level="debug" \
--rest --rest-port=4001 --rest-address=0.0.0.0 \
--enr-auto-update=false \
--doppelganger-detection=off \
--metrics --metrics-port=4002 --metrics-address=0.0.0.0 \
--listen-address=0.0.0.0 \
--nat="extip:127.0.0.1" \
--dump:on \
--web3-url="http://geth:8545"

