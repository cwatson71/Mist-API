########## Subscriptions ############


def get(mist_session, org_id, page=1, limit=100):
    uri = "/api/v1/self/subscriptions" % org_id
    resp = mist_session.mist_get(uri, page=page, limit=limit)
    return resp

def subscribe(mist_session, org_id, subscription):
    uri = "/api/v1/orgs/%s/subscriptions" % org_id
    body = subscription
    resp = mist_session.mist_post(uri, body=body)
    return resp

def ussubscribe(mist_session, org_id, subscription_id):
    uri = "/api/v1/orgs/%s/subscriptions/%s" % (org_id, subscription_id)    
    resp = mist_session.mist_delete(uri)
    return resp

