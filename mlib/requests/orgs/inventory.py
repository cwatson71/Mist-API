########## INVENTORY ############

def get(mist_session, org_id, page=1, limit=100):
    uri = "/api/v1/orgs/%s/inventory" % org_id
    resp = mist_session.mist_get(uri, page=page, limit=limit)
    return resp

def add(mist_session, org_id, serials):
    uri = "/api/v1/orgs/%s/inventory" % org_id
    body = serials
    resp = mist_session.mist_post(uri, body=body)
    return resp

def delete_multiple(mist_session, org_id, serials=[], macs=[]):
    uri = "/api/v1/orgs/%s/inventory" % org_id
    body = {
        "op": "delete",
        "serials": serials,
        "macs": macs
    }
    resp = mist_session.mist_put(uri, body=body)
    return resp

def unassign(mist_session, org_id, macs):
    uri = "/api/v1/orgs/%s/inventory" % org_id
    body = {
        "op": "unassign",
        "macs": macs,
    }
    resp = mist_session.mist_put(uri, body=body)
    return resp

def assign_macs_to_site(mist_session, org_id, site_id, macs):
    uri = "/api/v1/orgs/%s/inventory" % org_id
    if type(macs) == str:
        macs = [macs]
    body = {
        "op": "assign",
        "site_id": site_id,
        "macs": macs,
        "no_reassign": False
    }
    resp = mist_session.mist_put(uri, body=body)
    return resp
