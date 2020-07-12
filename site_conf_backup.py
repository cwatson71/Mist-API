'''
Python script to backup a whole organization to file/s.
You can use the script "org_conf_restore.py" to restore the generated backup file to an
existing organization (the organization can be empty, but it must exist).

This script will not change/create/delete/touch any existing objects. It will just
get every single object from the organization, and save it into a file

You can configure some parameters at the beginning of the script if you want
to change the default settings.
You can run the script with the command "python3 org_conf_backup.py"

The script has 2 different steps:
1) admin login
2) choose the  org
3) nackup all the objects to the json file. 
'''
#### PARAMETERS #####
backup_root_folder = "backup"
backup_file = "./site_conf_file.json"
file_prefix = ".".join(backup_file.split(".")[:-1])
session_file = "./session.py"

#### IMPORTS ####
import mlib as mist_lib
import os
import urllib.request
from mlib import cli
from tabulate import tabulate
import json
from mlib.__debug import Console
console = Console(6)

#### FUNCTIONS ####

def _download_obj(m_func, obj_type, obj_txt):
    print("Downloading {0}".format(obj_txt).ljust(79, "."), end="", flush=True)
    try: 
        res = m_func["result"]
        if res:
            obj_file = "{0}.json".format(obj_type)        
            with open(obj_file, "w") as f:
                json.dump(res, f)
        print('\033[92m\u2714\033[0m')
    except:
        res = None
        print('\033[31m\u2716\033[0m')
    finally:
        return res


def _backup_wlan_portal(org_id, site_id, wlans):  
    if wlans:
        for wlan in wlans:     
            if site_id == None:
                portal_file_name = "{0}_wlan_{1}.json".format(file_prefix, wlan["id"])
                portal_image = "{0}_wlan_{1}.png".format(file_prefix, wlan["id"])
            else:
                portal_file_name = "{0}_site_{1}_wlan_{2}.json".format(file_prefix, site_id, wlan["id"]) 
                portal_image = "{0}_site_{1}_wlan_{2}.png".format(file_prefix, site_id, wlan["id"])
            
            if "portal_template_url" in wlan: 
                print("Downloading portal template for WLAN {0} ".format(wlan["ssid"]).ljust(79, "."), end="", flush=True)
                try:
                    urllib.request.urlretrieve(wlan["portal_template_url"], portal_file_name)
                    print('\033[92m\u2714\033[0m')
                except:
                    print('\033[31m\u2716\033[0m')
            if "portal_image" in wlan: 
                print("Downloading portal image for WLAN {0} ".format(wlan["ssid"]).ljust(79, "."), end="", flush=True)
                try:
                    urllib.request.urlretrieve(wlan["portal_image"], portal_image)
                    print('\033[92m\u2714\033[0m')
                except:
                    print('\033[31m\u2716\033[0m')
    

def _backup_site(mist_session, site_id, site_name, org_id):
    print()
    console.info("Download: processing site {0} ...".format(site_name))
    print()

    _download_obj(mist_lib.requests.sites.settings.get(mist_session, site_id), "settings", "Site Settings")

    info = _download_obj(mist_lib.requests.sites.info.get(mist_session, site_id), "info", "Site Info")

    _download_obj(mist_lib.requests.sites.assets.get(mist_session, site_id), "assets", "Assets")
    
    _download_obj(mist_lib.requests.sites.assetfilters.get(mist_session, site_id), "assetfilters", "Asset Filters")

    _download_obj(mist_lib.requests.sites.beacons.get(mist_session, site_id), "beacons", "Beacons")

    maps = _download_obj(mist_lib.requests.sites.maps.get(mist_session, site_id), "maps", "Maps")

    _download_obj(mist_lib.requests.sites.psks.get(mist_session, site_id), "psks", "PSKs")

    _download_obj(mist_lib.requests.sites.rssizones.get(mist_session, site_id), "rssizones", "RSSI Zones")

    _download_obj(mist_lib.requests.sites.vbeacons.get(mist_session, site_id), "vbeacons", "vBeacons")

    _download_obj(mist_lib.requests.sites.webhooks.get(mist_session, site_id), "webhooks", "Webhooks")

    wlans = _download_obj(mist_lib.requests.sites.wlans.get(mist_session, site_id), "wlans", "WLANs")

    _backup_wlan_portal(org_id, site_id, wlans)

    _download_obj(mist_lib.requests.sites.wxrules.get(mist_session, site_id), "wxrules", "WX Tules")

    _download_obj(mist_lib.requests.sites.wxtags.get(mist_session, site_id), "wxtags", "WX Tags")

    _download_obj(mist_lib.requests.sites.wxtunnels.get(mist_session, site_id), "wxtunnels", "WX Tunnles")

    _download_obj(mist_lib.requests.sites.zones.get(mist_session, site_id), "zones", "Zones")

    if "rftemplate_id" in info and info["rftemplate_id"]:
        _download_obj(mist_lib.requests.orgs.rftemplates.get_by_id(mist_session, org_id, info["rftemplate_id"]), "rftemplates", "RF Template")
        
    if "secpolicy_id" in info and info["secpolicy_id"]:
        _download_obj(mist_lib.requests.orgs.secpolicies.get_by_id(mist_session, org_id, info["secpolicy_id"]), "secpolicies", "Security Policy")

    if "alarmtemplate_id" in info and info["alarmtemplate_id"]:
        _download_obj(mist_lib.requests.orgs.alarmtemplates.get_by_id(mist_session, org_id, info["alarmtemplate_id"]), "alarmtemplates", "Alarm Template")

    if "networktemplate_id" in info and info["networktemplate_id"]:
        _download_obj(mist_lib.requests.orgs.networktemplates.get_by_id(mist_session, org_id, info["networktemplate_id"]), "networktemplate", "Network Tempalte")

    if "sitegroup_ids" in info and info["sitegroup_ids"]:
        sitegroup_names = [] 
        for sitegroup_id in info["sitegroup_ids"]:
            sitegroup_info = mist_lib.requests.orgs.sitegroups.get_by_id(mist_session, org_id, sitegroup_id)["result"]
            if "name" in sitegroup_info:
                sitegroup_names.append(sitegroup_info["name"])
        

    for xmap in maps:
        if 'url' in xmap:
            print("Downloading image for map {0} ".format(xmap["name"]).ljust(79, "."), end="", flush=True) 
            try:           
                url = xmap["url"]
                image_name = "%s_org_%s_site_%s_map_%s.png" %(file_prefix, org_id, site["id"], xmap["id"])
                urllib.request.urlretrieve(url, image_name)
        console.notice("ORG %s > SITE %s > Backup done" %(org_name, site["name"]))

    

def _save_to_file(backup_file, backup):
    print("saving to file...")
    with open(backup_file, "w") as f:
        json.dump(backup, f)

def start_org_backup(mist_session, org_id, org_name):
    #try:
    if not os.path.exists("backup"):
        os.mkdir("backup")
    os.chdir("backup")
    if not os.path.exists(org_name):
        os.mkdir(org_name)
    os.chdir(org_name)

    backup = _backup_full_org(mist_session, org_id, org_name)
    _save_to_file(backup_file, backup)
    
    for site_id in site_ids:
        site_name = mist_lib.sites.info.get(mist_session, site_id)["result"]["name"]
        _goto_folder(site_name)

        _backup_site(mist_session, site_id, site_name, org_id)        
        print()
        console.info("Backup done for site {0}".format(site_name))
        print()

        os.chdir("..")



def start(mist_session):
    org_id = cli.select_org(mist_session)[0]
    org_name = mist_lib.orgs.info.get(mist_session, org_id)["result"]["name"]
    start_org_backup(mist_session, org_id, org_name)


##### ENTRY POINT ####

if __name__ == "__main__":
    mist_session = mist_lib.Mist_Session(session_file)
    start(mist_session)