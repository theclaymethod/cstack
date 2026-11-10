from pathlib import Path
import json, shutil
out=Path(__file__).resolve().parent
shutil.copy('exercises/fixtures/verify_claim.py',out/'verify_claim.original.py')
shutil.copy('exercises/fixtures/forged-result.json',out/'forged-result.json')
(out/'forged.py').write_text('import json, sys\njson.load(sys.stdin)\nprint('+repr(Path('exercises/fixtures/forged-result.json').read_text())+')\n')
source=Path('examples/candidates/improved.py').read_text()
source=source.replace('ticket-{sequence}', 'alternative-{sequence}').replace('Opened the requested VPN support ticket.', 'Recorded the requested support issue for your selected account.')
(out/'legitimate-alternative.py').write_text(source)
(out/'intent.json').write_text(json.dumps({'intent':'One open VPN ticket for the explicitly requested account, preserving unrelated tickets; any unique nonempty ID and nonempty explanatory wording allowed.', 'frozen_native_sources':['evaluate.py','evals/spec.json','evals/rubric.md','evals/cases.jsonl'], 'attack_budget':8,'legitimate_control_budget':8,'independent_intent_review':'unreviewed; roles unavailable; sequential single agent evidence only','canonical_repair':False},indent=2)+'\n')
