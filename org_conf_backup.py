import mlib as mist_lib
import urllib.request
from mlib import cli
from tabulate import tabulate
import json

backup_file = "./org_conf_file.json"
session_file = "./session.py"

file_prefix = ".".join(backup_file.split(".")[:-1])

mist_session = mist_lib.Mist_Session(session_file)
org_id = cli.select_org(mist_session)


def backup_wlan_portal(site_id, wlans):  
    for wlan in wlans:     
        if site_id == None:
            portal_file_name = "%s_org_%s_wlan_%s.json" %(file_prefix, org_id, wlan["id"])
            portal_image = "%s_org_%s_wlan_%s.png" %(file_prefix, org_id, wlan["id"])
        else:
            portal_file_name = "%s_org_%s_site_%s_wlan_%s.json" %(file_prefix, org_id, site_id, wlan["id"]) 
            portal_image = "%s_org_%s_site_%s_wlan_%s.png" %(file_prefix, org_id, site_id, wlan["id"])
        urllib.request.urlretrieve(wlan["portal_template_url"], portal_file_name)
        if "portal_image" in wlan: urllib.request.urlretrieve(wlan["portal_image"], portal_image)
    



backup = {}

backup["org"] = {}
backup["org"]["data"] = mist_lib.requests.orgs.info.get(mist_session, org_id)["result"]
backup["org"]["settings"] = mist_lib.requests.orgs.settings.get(mist_session, org_id)["result"]
backup["org"]["webhooks"] = mist_lib.requests.orgs.webhooks.get(mist_session, org_id)["result"]
backup["org"]["assetfilters"] = mist_lib.requests.orgs.assetfilters.get(mist_session, org_id)["result"]
backup["org"]["alarmtemplates"] = mist_lib.requests.orgs.alarmtemplates.get(mist_session, org_id)["result"]
backup["org"]["deviceprofiles"] = mist_lib.requests.orgs.deviceprofiles.get(mist_session, org_id)["result"]
backup["org"]["mxclusters"] = mist_lib.requests.orgs.mxclusters.get(mist_session, org_id)["result"]
backup["org"]["mxtunnels"] = mist_lib.requests.orgs.mxtunnels.get(mist_session, org_id)["result"]
backup["org"]["psks"] = mist_lib.requests.orgs.psks.get(mist_session, org_id)["result"]
backup["org"]["rftemplates"] = mist_lib.requests.orgs.rftemplates.get(mist_session, org_id)["result"]
backup["org"]["secpolicies"] = mist_lib.requests.orgs.secpolicies.get(mist_session, org_id)["result"]
backup["org"]["sitegroups"] = mist_lib.requests.orgs.sitegroups.get(mist_session, org_id)["result"]
backup["org"]["ssos"] = mist_lib.requests.orgs.ssos.get(mist_session, org_id)["result"]
backup["org"]["ssoroles"] = mist_lib.requests.orgs.ssoroles.get(mist_session, org_id)["result"]
backup["org"]["templates"] = mist_lib.requests.orgs.templates.get(mist_session, org_id)["result"]
backup["org"]["wlans"] = mist_lib.requests.orgs.wlans.get(mist_session, org_id)["result"]
backup_wlan_portal(None, backup["org"]["wlans"])
backup["org"]["wxrules"] = mist_lib.requests.orgs.wxrules.get(mist_session, org_id)["result"]
backup["org"]["wxtags"] = mist_lib.requests.orgs.wxtags.get(mist_session, org_id)["result"]
backup["org"]["wxtunnels"] = mist_lib.requests.orgs.wxtunnels.get(mist_session, org_id)["result"]

backup["org"]["sites"] = []

sites = mist_lib.requests.orgs.sites.get(mist_session, org_id)['result']
for site in sites:
    assets = mist_lib.requests.sites.assets.get(mist_session, site["id"])["result"]
    assetfilters = mist_lib.requests.sites.assetfilters.get(mist_session, site["id"])["result"]
    beacons = mist_lib.requests.sites.beacons.get(mist_session, site["id"])["result"]
    maps = mist_lib.requests.sites.maps.get(mist_session, site["id"])["result"]
    psks = mist_lib.requests.sites.psks.get(mist_session, site["id"])["result"]
    rssizones = mist_lib.requests.sites.rssizones.get(mist_session, site["id"])["result"]
    settings = mist_lib.requests.sites.settings.get(mist_session, site["id"])["result"]
    vbeacons = mist_lib.requests.sites.vbeacons.get(mist_session, site["id"])["result"]
    webhooks = mist_lib.requests.sites.webhooks.get(mist_session, site["id"])["result"]
    wlans = mist_lib.requests.sites.wlans.get(mist_session, site["id"])["result"]
    backup_wlan_portal(site["id"], wlans)
    wxrules = mist_lib.requests.sites.wxrules.get(mist_session, site["id"])["result"]
    wxtags = mist_lib.requests.sites.wxtags.get(mist_session, site["id"])["result"]
    wxtunnels = mist_lib.requests.sites.wxtunnels.get(mist_session, site["id"])["result"]
    zones = mist_lib.requests.sites.zones.get(mist_session, site["id"])["result"]
    backup["org"]["sites"].append({
        "data": site, 
        "assetfilters": assetfilters,
        "assets": assets,
        "beacons": beacons, 
        "maps": maps, 
        "psks": psks, 
        "rssizones":rssizones,
        "settings": settings,
        "vbeacons": vbeacons, 
        "webhooks": webhooks,
        "wlans": wlans, 
        "wxrules": wxrules, 
        "wxtags": wxtags, 
        "wxtunnels": wxtunnels,
        "zones": zones
        })
    for xmap in maps:
        if 'url' in xmap:
            url = xmap["url"]
            image_name = "%s_org_%s_site_%s_map_%s.png" %(file_prefix, org_id, site["id"], xmap["id"])
            urllib.request.urlretrieve(url, image_name)





cli.show(backup)
print("saving to file...")
with open(backup_file, "w") as f:
    json.dump(backup, f)