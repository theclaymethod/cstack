"""Local demonstration output for the reviewed native how-to input.

This candidate is not an endorsed canonical replacement or a product change.
"""
import copy
import json
import sys


def respond(payload):
    state = copy.deepcopy(payload["state"])
    return {"action": "guidance", "account": None, "state": state,
            "note": "Open your VPN client, choose your organization connection, and sign in using your account credentials."}


if __name__ == "__main__":
    print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))
