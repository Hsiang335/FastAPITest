from fastapi import HTTPException


def unauthorized():
    raise HTTPException(status_code=401, detail="Unauthorized")


def bad_request(msg="Bad request"):
    raise HTTPException(status_code=400, detail=msg)