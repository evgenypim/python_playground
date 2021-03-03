#!/usr/bin/env python3

import json as json_mod
from sanic import Sanic
from sanic.response import json
from sanic_jwt import exceptions
from sanic_jwt import initialize
from sanic_jwt.decorators import protected

user0 = {"username": "user1", "password": "pass1"}
users = [user0]
username_table = {u["username"]: u for u in users}


async def authenticate(request, *args, **kwargs):

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user["password"]:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user

app = Sanic("API app")
initialize(app, authenticate=authenticate)


# assume value endswith 'Val'
# def norm(_jsn):
#     r = {}
#     for e in _jsn:
#         name = e['name']
#         v_key = [k for k in e.keys() if k.endswith('Val')][0]
#         r[name] = e[v_key]
#     return r

#onle-liners
# def norm(_jsn):
#     return dict(((e['name'], e[[k for k in e.keys() if k.endswith('Val')][0]]) for e in _jsn))


def norm(_jsn):
    return {name: val for name, val in ((e['name'], e[[k for k in e.keys() if k.endswith('Val')][0]]) for e in _jsn)}


@app.route('/norm', methods=["POST"])
@protected()
async def ep_norm(request):
    return json(norm(request.json))



def for_serverless(event, context):
    req_body = json_mod.loads(event['body'])

    response = {
        "statusCode": 200,
        "body": json_mod.dumps(norm(req_body))
    }

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
