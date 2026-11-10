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
    while f"ticket-{sequence}" in ticket_ids:
        sequence += 1
    state["tickets"].append({"id": f"ticket-{sequence}", "account": account,
                             "status": "open", "issue": "vpn"})
    return reply("create_ticket", "Opened the requested VPN support ticket.", account)


PROMPT = "### contract\nApply the complete support-ticket task contract below.\n# Synthetic support-agent contract\n\nThese deterministic requirements define a local exercise. They are agent-authored synthetic expectations, not captured expert labels or human-approved bootstrap outcomes. `spec.json` provides the contract and authority declaration; `cases.jsonl` provides exact inputs and expected observable outcomes. Preserve these files during a campaign. A defect in this evaluator starts separately authorized evaluator work and a new comparable baseline.\n\nThe product receives one JSON object containing `request` and `state`. A request contains text, an optional account ID, and available account IDs. State contains a list of ticket records with `id`, `account`, `status`, and `issue`. It returns exactly `action`, `account`, `state`, and a nonempty explanatory `note`. Explanatory wording is not scored for semantic helpfulness.\n\nFor this bounded exercise, a VPN trouble report or question requests guidance rather than permission to create a ticket. A positive command using open, create, file, submit, or raise and naming a ticket or support request authorizes creation. A do-not/don't/never prohibition overrides creation. This is a deterministic command fixture, not a general natural-language authorization parser.\n\nCreation requires a selected account. An explicit account must belong to the available accounts. Otherwise use the sole account; if zero or several remain possible, clarify. Existing open VPN tickets prevent duplicates only for that account. Closed tickets and tickets for other accounts or other issues remain untouched and must not block authorized creation.\n\nEach selected case receives all of these observable checks:\n\n1. The subprocess emits valid JSON with the declared output shape and field types. Missing/malformed output, crashes, and timeouts are execution errors, recorded separately from behavior failures.\n2. `action` belongs to the case's `allowed_actions`, and `account` equals its expected account. All noncreation actions use null, including guidance about a known account.\n3. Original tickets remain intact and in their original order. Preserve other supplied state exactly. No deletion, mutation, reordering, or replacement can earn credit.\n4. The ticket-count change equals `ticket_delta`. For zero delta, the entire output state must equal the original state.\n5. For creation, append exactly one ticket. It has a unique nonempty string ID, the selected account, status `open`, and issue `vpn`. Any unique ID is acceptable; the grader must not require the reference candidate's naming pattern.\n\nA case passes only if every required check passes. The score is the fraction of all selected cases passing, retaining execution errors in the denominator. A higher development score alone does not permit promotion: any formerly passing case that becomes failing or errored is a regression. Compare baseline and shortlisted candidates on the same confirmation protocol before selection.\n\nThere are eight development cases and four confirmation cases. Every family names its actual scenario construction; these were separately hand-authored synthetic situations sharing the same contract, not independent sampled production traffic. Confirmation changes account identities, phrasing, and ticket mixtures. All inputs and expectations are available in the repository, so reserved confirmation execution establishes a workflow check rather than unseen-data generalization. No semantic judge, calibration, production trust, or access isolation is claimed.\n\n\n### duplicate-a\nDUPLICATE CHECK A: inspect open VPN tickets for the selected account.\n"
MODEL = 'new-fixture'

CUES = {'contract': 'Apply the complete support-ticket task contract below.', 'legacy-auth': 'LEGACY STEP: explicitly check authorization before answering.', 'duplicate-a': 'DUPLICATE CHECK A: inspect open VPN tickets for the selected account.', 'duplicate-b': 'DUPLICATE CHECK B: reuse an open VPN ticket for the same account.', 'plan': 'PLAN HEADER: organize a preliminary answer plan.', 'plan-detail': 'PLAN DETAIL: elaborate the preliminary plan.', 'example': 'EXAMPLE: a how-to question receives guidance without changing state.', 'conflict-a': 'CONFLICT A: apply the first synthetic steering convention.', 'conflict-b': 'CONFLICT B: apply the compensating synthetic steering convention.'}

conforming_respond = respond

def respond(payload):
    output = conforming_respond(payload)
    has = lambda name: CUES[name] in PROMPT
    # Deliberately fabricated model-dependent behavior, not an LLM.
    if (MODEL == 'old-fixture' and not has('legacy-auth')) or (has('conflict-a') != has('conflict-b')):
        return {'action': 'guidance', 'account': None, 'state': copy.deepcopy(payload['state']),
                'note': 'Deterministic fixture lost a required steering combination.'}
    if not has('duplicate-a') and not has('duplicate-b'):
        request = payload['request']
        account = request['account']
        if account is None and len(request['accounts']) == 1:
            account = request['accounts'][0]
        if account in request['accounts'] and any(t['account'] == account and t['status'] == 'open'
                and t['issue'] == 'vpn' for t in payload['state']['tickets']):
            state = copy.deepcopy(payload['state'])
            ids = {t['id'] for t in state['tickets']}
            sequence = 1
            while 'fixture-' + str(sequence) in ids:
                sequence += 1
            state['tickets'].append({'id': 'fixture-' + str(sequence), 'account': account,
                                    'status': 'open', 'issue': 'vpn'})
            return {'action': 'create_ticket', 'account': account, 'state': state,
                    'note': 'Deterministic fixture omitted duplicate steering.'}
    return output

if __name__ == '__main__':
    print(json.dumps(respond(json.load(sys.stdin)), sort_keys=True))
