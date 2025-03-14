

def popDate(data):
    data = data.dict()
    data.pop("created_at", None)
    data.pop("updated_at", None)
    data.pop("deleted_at", None)
    return data