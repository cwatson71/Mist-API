
def get(mist_session, org_id, page=1, limit=100):
    uri = "/api/v1/orgs/%s/templates" % org_id
    resp = mist_session.mist_get(uri, page=page, limit=limit)
    return resp

def get_details(mist_session, org_id, template_id):
    uri = "/api/v1/orgs/%s/templates/%s" %(org_id, template_id)
    resp = mist_session.mist_get(uri)
    return resp

def create(mist_session, org_id, template_settings):
    uri = "/api/v1/orgs/%s/templates" % org_id
    resp = mist_session.mist_post(uri, body=template_settings)
    return resp

def delete(mist_session, org_id, template_id):
    uri = "/api/v1/orgs/%s/templates/%s" % (org_id, template_id)
    resp = mist_session.mist_delete(uri)
    return resp

