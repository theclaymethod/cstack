"""Intentionally flawed deterministic support agent; JSON stdin and stdout."""

import copy
import json
import sys


def respond(payload):
    request = payload["request"]
    state = copy.deepcopy(payload["state"])
    if "vpn" not in request["text"].lower():
        return {"action": "guidance", "account": None, "state": state,
                "note": "Use the account recovery instructions for password help."}
    account = request["account"] or next(iter(request["accounts"]), None)
    if account is None:
        return {"action": "clarify", "account": None, "state": state,
                "note": "Which account needs support?"}
    ticket_ids = {ticket["id"] for ticket in state["tickets"]}
    sequence = 1
    while f"ticket-{sequence}" in ticket_ids:
        sequence += 1
    state["tickets"].append({"id": f"ticket-{sequence}", "account": account,
                             "status": "open", "issue": "vpn"})
    return {"action": "create_ticket", "account": account, "state": state,
            "note": "Opened a VPN support ticket."}


if __name__ == "__main__":
    print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))
