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

def splitFirewall(subnets, hostsList):
    ips_list = {}
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

    # check overlap
    for group, ips in data.items():
      for group_check, ips_check in data.items():
        test = group.split("_")[1]
        test_check = group_check.split("_")[1]

        if(group != group_check and test == test_check):
          for ip in ips:
            if(ip in ips_check):
              raise Exception("ERROR (" + group + ") checking in (" + group_check + ") " + ip + " OVERLAP")

    return data

def gethFirewall(subnets, hostsList):
    ips_list = {}
    for host in hostsList:
      if 'geth_host' in host.vars:
        geth = host.vars['geth_host']
        key = geth
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

    return data

def rWFirewall(subnets, hostsList):
    ips_list = {}
    for host in hostsList:
      if 'rw_host' in host.vars:
        rw = host.vars['rw_host']
        key = rw
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

    return data  

if __name__ == '__main__':
    inventory_file_name = sys.argv[1]
    action = sys.argv[2]

    data_loader = DataLoader()
    inventory = InventoryManager(loader = data_loader, sources=[inventory_file_name])

    subnets = getSubnets()

    hostsList = inventory.get_hosts()

    if action == 'split':
      data = splitFirewall(subnets, hostsList)
    elif action == 'geth':
      data = gethFirewall(subnets, hostsList)
    elif action == 'rw':
      data = rWFirewall(subnets, hostsList)

    print(data)
