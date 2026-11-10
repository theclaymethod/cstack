"""Deterministic support agent for the bounded JSON command fixture."""

import copy
import json
import re
import sys


def respond(payload):
    request = payload["request"]
    state = copy.deepcopy(payload["state"])
    text = request["text"].lower()
    if not re.search(r"\bvpn\b", text):
        return {"action": "guidance", "account": None, "state": state,
                "note": "Use the account recovery instructions for password help."}
    prohibited = re.search(r"\b(?:do\s+not|don't|never)\b", text)
    creation = re.search(r"\b(?:open|create|file|submit|raise)\b", text)
    ticket_request = re.search(r"\b(?:ticket|support\s+request)\b", text)
    if prohibited or not (creation and ticket_request):
        return {"action": "guidance", "account": None, "state": state,
                "note": "Check the VPN setup and connection troubleshooting instructions."}
    accounts = request["accounts"]
    account = request["account"]
    if account is None and len(accounts) == 1:
        account = accounts[0]
    if account is None or account not in accounts:
        return {"action": "clarify", "account": None, "state": state,
                "note": "Which account needs support?"}
    if any(ticket["account"] == account and ticket["status"] == "open"
           and ticket["issue"] == "vpn" for ticket in state["tickets"]):
        return {"action": "guidance", "account": None, "state": state,
                "note": "An open VPN ticket already exists for this account."}
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
