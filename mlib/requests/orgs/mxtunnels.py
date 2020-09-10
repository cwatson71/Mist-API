def create(mist_session, org_id, mxtunnel_settings):
    uri = "/api/v1/orgs/%s/mxtunnels" % org_id
    body = mxtunnel_settings
    resp = mist_session.mist_post(uri, body=body)
    return resp

def update(mist_session, org_id, mxtunnel_id, body={}):
    uri = "/api/v1/orgs/%s/mxtunnels/%s" % (org_id, mxtunnel_id)
    resp = mist_session.mist_put(uri, body=body)
    return resp
    
def delete(mist_session, org_id, mxtunnel_id):
    uri = "/api/v1/orgs/%s/mxtunnels/%s" % (org_id, mxtunnel_id)
    resp = mist_session.mist_delete(uri)
    return resp

def get(mist_session, org_id, page=1, limit=100):
    uri = "/api/v1/orgs/%s/mxtunnels" % org_id
    resp = mist_session.mist_get(uri, page=page, limit=limit)
    return resp



