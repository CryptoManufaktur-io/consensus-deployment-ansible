from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

import requests
import ipaddress
import re
import sys

pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)')
reader = requests.get('https://geoip.linode.com/', stream=True)

def getSubnets():
  subnets = []
  for line in reader.iter_lines(decode_unicode=True):
    if line: 
      items = line.split(',')

      if pattern.match(items[0]):
        subnets.append(items[0])
  
  subnets.sort()
  return subnets

if __name__ == '__main__':
    inventory_file_name = sys.argv[1]
    data_loader = DataLoader()
    inventory = InventoryManager(loader = data_loader, sources=[inventory_file_name])

    subnets = getSubnets()

    ips_list = {}
    hostsList = inventory.get_hosts()
    for host in hostsList:
      if 'grp' in host.vars:
        grp = host.vars['grp']
        test = host.vars['test']
        key = grp + '_' + test
        ip = host.vars['ansible_host']

        for subnet in subnets:
          if ipaddress.ip_address(ip) in ipaddress.ip_network(subnet):
            if key not in ips_list:
              ips_list[key] = {}

            ips_list[key][subnet] = subnet
            break
    
    # get lists
    data = {}
    for key in ips_list:
      data[key] = list(ips_list[key].values())

    print(data)
