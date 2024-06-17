def individual_serial(task)->dict:
    return {
        "id":str(task["_id"]),
        "name":task["name"],
    }

def list_serail(tasks):
    print(tasks)
    return [individual_serial(task) for task in tasks]