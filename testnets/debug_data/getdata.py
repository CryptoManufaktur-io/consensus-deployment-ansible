import requests, sys, pathlib, calendar, time, os
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

gmt = time.gmtime()
ts = calendar.timegm(gmt)
dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
  append = sys.argv[1] if len(sys.argv) == 2 else ''
  dir_name = dir_path + "/data/" + str(ts) + append
  pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)

  inventory_file_name = dir_path + "/../efoundation/inventory/inventory.ini"
  data_loader = DataLoader()
  inventory = InventoryManager(loader = data_loader, sources=[inventory_file_name])
  hostsList = inventory.get_hosts()

  for host in hostsList:
    label = str(host)
    ip = host.vars['ansible_host']

    if(label.__contains__('prysm')):
      url = "http://" + ip + ":4000/eth/v1/debug/beacon/forkchoice"
    elif(label.__contains__('teku')):
      url = "http://" + ip + ":4000/teku/v1/debug/beacon/protoarray"
    elif(label.__contains__('lighthouse')):
      url = "http://" + ip + ":4000/lighthouse/proto_array"
    else:
      continue

    solditems = requests.get(url)
    pathlib.Path(dir_name + '/' + label + '.json').write_bytes(solditems.content)

