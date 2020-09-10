def get(mist_session, org_id):
    uri = "/api/v1/orgs/%s" % org_id
    resp = mist_session.mist_get(uri)
    return resp

def create(mist_session, org_id, org_settings):
    uri = "/api/v1/orgs/%s" % org_id
    body = org_settings
    resp = mist_session.mist_post(uri, body=body)
    return resp

def update(mist_session, org_id, org_settings):
    uri = "/api/v1/orgs/%s" % org_id
    body = org_settings
    resp = mist_session.mist_put(uri, body=body)
    return resp