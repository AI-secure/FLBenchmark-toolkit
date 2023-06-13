#! /usr/bin/env python3

import os
import json
import colink as CL


with open('server_list.json', 'r') as outfile:
    servers=json.load(outfile)


# in this example script, we will create one new user on each server (if the user already exists, the script will do nothing)
def main():
    # create a folder to store user credentials
    if not os.path.exists("users"):
        os.makedirs("users")
    for (server_nickname, (server_url, host_jwt)) in servers.items():
        if os.path.exists(f"users/{server_nickname}.json"):
            print(f"User already exists on {server_nickname}")
            continue
        cl = CL.CoLink(server_url, host_jwt)
        expiration_timestamp = CL.decode_jwt_without_validation(cl.jwt).exp
        pk, sk = CL.generate_user()
        core_pub_key = cl.request_info().core_public_key
        signature_timestamp, sig = CL.prepare_import_user_signature(
            pk, sk, core_pub_key, expiration_timestamp
        )
        user_jwt = cl.import_user(pk, signature_timestamp, expiration_timestamp, sig)
        cl.update_jwt(user_jwt)
        cl.wait_user_init()
        with open(f"users/{server_nickname}.json", "w") as f:
            f.write(json.dumps({
                "user_jwt": user_jwt,
                "server_url": server_url,
                "user_id": CL.decode_jwt_without_validation(user_jwt).user_id,
                "sk_hex": sk.to_hex(),
            }, indent=4))
        print(f"User created on {server_nickname}: {CL.decode_jwt_without_validation(user_jwt).user_id}")

if __name__ == "__main__":
    main()
