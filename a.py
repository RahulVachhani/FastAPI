
def User(id,signup_ts,friends,name='Rahul'):
    print(f'id={id}, signup_ts = {signup_ts},friends = {friends}')
    

external_data = {
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
    "id": 123
}

User(**external_data)