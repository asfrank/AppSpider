from mitmproxy import ctx

def request(flow):
    # print(flow.request.headers)
    ctx.log.info(str(flow.request.headers))
    ctx.log.warn(str(flow.request.headers))
    ctx.log.error(str(flow.request.headers))

def response(flow):
    ctx.log.error(str(flow.response.status_code))