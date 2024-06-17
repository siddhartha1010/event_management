# def individual_serial(user)->dict:
#     return {
#         "id":str(user["_id"]),
#         "name":user["name"],
#         "email":user["email"],
#         "password":user["password"],
#         "passwordConfirm":user["passwordConfirm"],
#     }
def individual_serial(user_cursor):
    return [{
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "password": user["password"],
        # "passwordConfirm": user["passwordConfirm"],
    } for user in user_cursor]


def list_serail(users):
    print(users)
    return [individual_serial(user) for user in users]