
def get(mist_session, site_id, device_id):
    uri = "/api/v1/sites/%s/devices/%s/iot" % (site_id, device_id)
    resp = mist_session.mist_get(uri)
    return resp


def set(mist_session, site_id, device_id):
    uri = "/api/v1/sites/%s/devices/%s/iot" % (site_id, device_id)
    resp = mist_session.mist_put(uri)
    return resp
