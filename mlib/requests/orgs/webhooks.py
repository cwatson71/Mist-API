def create(mist_session, org_id, webhook_settings):
    uri = "/api/v1/orgs/%s/webhooks" % org_id
    body = webhook_settings
    resp = mist_session.mist_post(uri, body=body)
    return resp

def update(mist_session, org_id, webhook_id, body={}):
    uri = "/api/v1/orgs/%s/webhooks/%s" % (org_id, webhook_id)
    resp = mist_session.mist_put(uri, body=body)
    return resp
    
def delete(mist_session, org_id, webhook_id):
    uri = "/api/v1/orgs/%s/webhooks/%s" % (org_id, webhook_id)
    resp = mist_session.mist_delete(uri)
    return resp

def get(mist_session, org_id, page=1, limit=100):
    uri = "/api/v1/orgs/%s/webhooks" % org_id
    resp = mist_session.mist_get(uri, page=page, limit=limit)
    return resp


