def success(data=None, message="success"):
    return {
        "status": "ok",
        "message": message,
        "data": data
    }