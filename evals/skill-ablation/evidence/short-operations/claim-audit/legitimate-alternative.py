"""Standalone support candidate respecting authorization and duplicate scope."""

import copy
import json
import re
import sys


def respond(payload):
    request = payload["request"]
    state = copy.deepcopy(payload["state"])
    text = request["text"].lower()

    def reply(action, note, account=None):
        return {"action": action, "account": account, "state": state, "note": note}

    authorized = re.search(r"\b(open|create|file|submit|raise)\b[^.!?]*\b(ticket|support request)\b", text)
    denied = re.search(r"\b(do not|don't|never)\s+(open|create|file|submit|raise)\b", text)
    if "vpn" not in text or not authorized or denied:
        return reply("guidance", "Check connection settings; use account recovery for password help.")
    account = request["account"]
    if account is None and len(request["accounts"]) == 1:
        account = request["accounts"][0]
    if account is None or account not in request["accounts"]:
        return reply("clarify", "Which listed account needs the VPN support ticket?")
    if any(ticket["account"] == account and ticket["status"] == "open"
           and ticket["issue"] == "vpn" for ticket in state["tickets"]):
        return reply("guidance", "An open VPN ticket already covers this account; use that ticket.")
    ticket_ids = {ticket["id"] for ticket in state["tickets"]}
    sequence = 1
    while f"alternative-{sequence}" in ticket_ids:
        sequence += 1
    state["tickets"].append({"id": f"alternative-{sequence}", "account": account,
                             "status": "open", "issue": "vpn"})
    return reply("create_ticket", "Your selected account now has a VPN support request.", account)


if __name__ == "__main__":
    print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))
