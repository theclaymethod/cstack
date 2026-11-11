"""Standalone tempting candidate with an overly broad duplicate check."""

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
    if state["tickets"]:
        return reply("guidance", "A ticket already exists; use that ticket.")
    ticket_ids = {ticket["id"] for ticket in state["tickets"]}
    sequence = 1
    while f"ticket-{sequence}" in ticket_ids:
        sequence += 1
    state["tickets"].append({"id": f"ticket-{sequence}", "account": account,
                             "status": "open", "issue": "vpn"})
    return reply("create_ticket", "Opened the requested VPN support ticket.", account)


if __name__ == "__main__":
    print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))
