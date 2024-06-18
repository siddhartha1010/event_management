def individual_serial(employee)->dict:
    return {
        "id":str(employee["_id"]),
        "name":employee["name"],
        "email":employee["email"],
        "phone":employee["phone"],
        "address":employee["address"],
        "experience":employee["experience"],
    }

def list_serail(employees):
    print(employees)
    return [individual_serial(employee) for employee in employees]