def response(status, message, data=None):
    response_result = {
        "status": status,
        "message": message
    }
    if data:
        response_result['data'] = data
    
    return response_result