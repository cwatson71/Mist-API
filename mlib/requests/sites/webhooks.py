
def get(mist_session, site_id, page=1, limit=100):
    uri = "/api/v1/sites/%s/webhooks" % site_id
    resp = mist_session.mist_get(uri, page=page, limit=limit)
    return resp

def get_details(mist_session, site_id, webhook_id):
    uri = "/api/v1/sites/%s/webhooks/%s" % (site_id, webhook_id)
    resp = mist_session.mist_get(uri)
    return resp

def create(mist_session, site_id, webhook):
    uri = "/api/v1/sites/%s/webhooks" % site_id
    resp = mist_session.mist_post(uri, body=webhook)
    return resp


def update(mist_session, site_id, webhook_id, webhook_settings):
    uri = "/api/v1/sites/%s/webhooks/%s" % (site_id, webhook_id)
    resp = mist_session.mist_put(uri, body=webhook_settings)
    return resp


def delete(mist_session, site_id, webhook_id):
    uri = "/api/v1/sites/%s/webhooks/%s" % (site_id, webhook_id)
    resp = mist_session.mist_delete(uri)
    return resp
