def status_success(show, msg, data):
    status = {
        "status": "successful",
        "message": {
            "show": show,
            "text": msg
        },
        "info": data,
        "error": None
    }
    return status


def status_unsuccessful(show, msg, e):
    status = {
        "status": "unsuccessful",
        "message": {
            "show": show,
            "text": msg
        },
        "info": None,
        "error": e
    }
    return status