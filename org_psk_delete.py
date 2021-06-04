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

def delete_psks(org_id, psks):
    print("")
    print("________________________________________")
    print("Starting to delete PSKs from the org %s" %(org_id))
    for psk in psks:     
        print('PSK %s' %(psk["name"]))
        psk_id = psk["id"]
        mist_lib.requests.orgs.psks.delete(mist, org_id, psk_id)       



def list_psks(org_id):
    print("")
    print("________________________________________")
    print("List of current PSKs for the org %s" %(org_id))
    psks = mist_lib.requests.orgs.psks.get(mist, org_id)['result']
    delete_psks(org_id, psks)

#### SCRIPT ENTRYPOINT #####

mist = mist_lib.Mist_Session()
org_id = cli.select_org(mist, allow_many=False)[0]
print("__________________")
print(org_id)

list_psks(org_id)