'''
Written by Thomas Munzer (tmunzer@juniper.net)
Github repository: https://github.com/tmunzer/Mist_library/

This script will import PSKs from a CSV file to one or multiple sites.
Usage:
python3 site_conf_psk_import_csv.py path_to_the_csv_file.csv

CSV file format:

pskName1,pskValue1,Wlan1,VLAN1
pskName2,pskValue2,Wlan2

'''
#### PARAMETERS #####
csv_separator = ","

#### IMPORTS #####
import mlib as mist_lib
from mlib import cli
from tabulate import tabulate
import sys
import csv


#### FUNCTIONS #####

def import_psk(org_id, psks):
    print("")
    print("________________________________________")
    print("Starting PSKs import for the org %s" %(org_id))
    for psk in psks:     
        print('PSK %s' %(psk["username"]))
        pskObj = mist_lib.models.sites.psks.Psk()
        pskObj.define(name=psk["username"], passphrase=psk["passphrase"], ssid=psk["ssid"], vlan_id=psk["vlan"])
        mist_lib.requests.orgs.psks.create(mist, org_id, pskObj.toJSON())
        print(pskObj.toJSON())

def read_csv(csv_file): 
    print("")   
    print("________________________________________")
    print("Opening CSV file %s" %(csv_file))
    psks = []
    try:
        with open(sys.argv[1], 'r') as my_file:
            ppsk_file = csv.reader(my_file, delimiter=',')
            for row in ppsk_file:
                username = row[0]
                passphrase = row[1]
                ssid = row[2]
                if len(row) == 4:
                    vlan = row[3]
                else:
                    vlan = ""
                psks.append({"username": username,"passphrase": passphrase,"ssid": ssid, "vlan": vlan})    
        return psks 
    except:
        print("Error while opening the CSV file... Aborting")

def list_psks(org_id):
    print("")
    print("________________________________________")
    print("List of current PSKs for the org %s" %(org_id))
    psks = mist_lib.requests.orgs.psks.get(mist, org_id)['result']
    cli.show(psks)

#### SCRIPT ENTRYPOINT #####

mist = mist_lib.Mist_Session()
org_id = cli.select_org(mist, allow_many=False)[0]
print("__________________")
print(org_id)

psks = read_csv(sys.argv[1])

import_psk(org_id, psks)

list_psks(org_id)