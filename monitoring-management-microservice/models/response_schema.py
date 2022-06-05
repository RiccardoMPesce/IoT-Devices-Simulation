
def Response(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }
