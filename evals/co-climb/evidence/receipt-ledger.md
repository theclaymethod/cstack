# Receipt campaign ledger

The user owns the arithmetic and display criteria. Keep the existing "Total: " prefix. The printed numeric amount must equal quantity × positive whole-dollar unit price. The user explicitly accepts 6, 6.0 and 6.00. Reviewer suggestions are hypotheses. Inputs below are synthetic integer examples. Expected judgments follow the user's contract. All observed judgments come from the local deterministic evaluator.

Two cycles, 80 local example judgments maximum, zero final reserve, no sealed set, no promotion or adoption decision. Only generator.py and evaluator.py are candidate code. One candidate per side. Use local Python 3.14.9 with no model, cache, retries, network or paid calls. Both functions receive the actual quantity and price. The judge also sees the exact output, with no label or rationale. It runs after generation. All rows below record these payloads verbatim using Python repr.

## Frozen identities and plan

G0 (generator.py SHA-256 8c345085f84de63e1703063005f26d0eac3d78486e4dec364c8fccc124913b6d) returns f'Total: {price:.2f}'. J0 (evaluator.py SHA-256 2700f468290fd910b3e760ad03c864f78495c3b4914904cf15c054e885857498) returns output.startswith('Total: '). Neither imports a dependency.

Cycle 1 challenges J0 on the display suggestion (D1) and on the wrong unit price at quantity three (A1). Keep G0 frozen. Select a judge repair only if it catches the wrong total and retains all legitimate controls, including a quantity-one receipt where the unit price is correct. Replay the identical corpus and execute G0 against the repaired judge. Reserve 16 judgments.

Cycle 2 carries forward any confirmed arithmetic failure. Freeze the repaired judge. Use climb cases C1 (3,2) and C2 (1,2) and fresh working cases F1 (4,7) and F2 (2,11), a multi-unit family outside the reported quantity-three example. Working sets are adaptive. Execute two identical baseline controls and two candidate runs on each set. Compare passed counts per set against the observed baseline range (max minus min). Require replicated improvement beyond spread on both sets and retention of the single-unit control to report a gain. Reserve 16 judgments. Unused allowance stays unspent.

## Execution receipts

Each numbered line is one actual call to accepts(qty, price, output). In the target runs the output is from a fresh answer(qty, price) call. G1 and J1 denote the uncommitted candidates identified below.
    01 probe J0 D1.two | 3, 2, 'Total: 6.00' | True
    02 probe J0 D1.one | 3, 2, 'Total: 6.0' | True
    03 probe J0 D1.zero | 3, 2, 'Total: 6' | True
    04 probe J0 A1.wrong | 3, 2, 'Total: 2.00' | True
    05 probe J0 A1.valid | 3, 2, 'Total: 6.00' | True
    06 probe J0 A1.single | 1, 2, 'Total: 2.00' | True

Cycle 1 experiment E1. Reject D1 as a proposed two-decimal requirement. It would fail two explicitly valid receipts without changing the amount. Keep those spellings as valid calibration controls. Admit A1. Charging $2 for three $2 items understates the total by $4. J0 missed it. The identical $2.00 text is valid for one item. The duplicate correct $6.00 links the two challenges and is not a separate coverage gain. No uncertain labels.

E2 changes only the judge, preserving the prefix and parsing the full ordinary decimal amount for exact numeric comparison. No archived candidates or promotions existed to regrade. Replay both challenge pairs before drawing conclusions about G0.

    07 replay J1 D1.two | 3, 2, 'Total: 6.00' | True
    08 replay J1 D1.one | 3, 2, 'Total: 6.0' | True
    09 replay J1 D1.zero | 3, 2, 'Total: 6' | True
    10 replay J1 A1.wrong | 3, 2, 'Total: 2.00' | False
    11 replay J1 A1.valid | 3, 2, 'Total: 6.00' | True
    12 replay J1 A1.single | 1, 2, 'Total: 2.00' | True
    13 cycle1 G0/J1 A1.wrong | 3, 2, 'Total: 2.00' | False
    14 cycle1 G0/J1 A1.single | 1, 2, 'Total: 2.00' | True
    15 cycle2 G0/J1 run1 C1 | 3, 2, 'Total: 2.00' | False
    16 cycle2 G0/J1 run1 C2 | 1, 2, 'Total: 2.00' | True
    17 cycle2 G0/J1 run1 F1 | 4, 7, 'Total: 7.00' | False
    18 cycle2 G0/J1 run1 F2 | 2, 11, 'Total: 11.00' | False
    19 cycle2 G0/J1 run2 C1 | 3, 2, 'Total: 2.00' | False
    20 cycle2 G0/J1 run2 C2 | 1, 2, 'Total: 2.00' | True
    21 cycle2 G0/J1 run2 F1 | 4, 7, 'Total: 7.00' | False
    22 cycle2 G0/J1 run2 F2 | 2, 11, 'Total: 11.00' | False

Cycle 1 closed with the judge repaired and a confirmed generator failure at row 13. Cycle 2 experiment E3 uses G0 as parent with J1 frozen. Rows 15–22 are the two controls. Test multiplication while retaining the existing two-decimal output style for the whole-dollar integer examples.

    23 cycle2 G1/J1 run1 C1 | 3, 2, 'Total: 6.00' | True
    24 cycle2 G1/J1 run1 C2 | 1, 2, 'Total: 2.00' | True
    25 cycle2 G1/J1 run1 F1 | 4, 7, 'Total: 28.00' | True
    26 cycle2 G1/J1 run1 F2 | 2, 11, 'Total: 22.00' | True
    27 cycle2 G1/J1 run2 C1 | 3, 2, 'Total: 6.00' | True
    28 cycle2 G1/J1 run2 C2 | 1, 2, 'Total: 2.00' | True
    29 cycle2 G1/J1 run2 F1 | 4, 7, 'Total: 28.00' | True
    30 cycle2 G1/J1 run2 F2 | 2, 11, 'Total: 22.00' | True

    31 cycle2 G1/J1 precision check P1 | 3, 3002399751580331, 'Total: 9007199254740992.00' | False

E4, still within cycle 2. Source inspection identified an integer-to-float conversion in the inherited .2f formatter. The contract has no stated price maximum. Row 31 confirms a one-dollar understatement. Admit P1 as a distinct precision regression. Working-set wins from E3 apply only to those examples. Prune G1 (692c95fc313a5cbeab8bc2212b844492af92d555983ecf80cd924fc95e9eb43f). Keep one active candidate. Reserve 18 additional judgments including row 31 for the boundary check, a nearby valid receipt, and replicated runs on the extended sets. Re-execute both generators against the identical J1 and cases. Use the permitted integer spelling in G2.
    32 cycle2 J1 P1.valid | 3, 3002399751580331, 'Total: 9007199254740993' | True
    33 cycle2 G0/J1 run1 C1 | 3, 2, 'Total: 2.00' | False
    34 cycle2 G0/J1 run1 C2 | 1, 2, 'Total: 2.00' | True
    35 cycle2 G0/J1 run1 P1 | 3, 3002399751580331, 'Total: 3002399751580331.00' | False
    36 cycle2 G0/J1 run1 F1 | 4, 7, 'Total: 7.00' | False
    37 cycle2 G0/J1 run1 F2 | 2, 11, 'Total: 11.00' | False
    38 cycle2 G0/J1 run2 C1 | 3, 2, 'Total: 2.00' | False
    39 cycle2 G0/J1 run2 C2 | 1, 2, 'Total: 2.00' | True
    40 cycle2 G0/J1 run2 P1 | 3, 3002399751580331, 'Total: 3002399751580331.00' | False
    41 cycle2 G0/J1 run2 F1 | 4, 7, 'Total: 7.00' | False
    42 cycle2 G0/J1 run2 F2 | 2, 11, 'Total: 11.00' | False
    43 cycle2 G2/J1 run1 C1 | 3, 2, 'Total: 6' | True
    44 cycle2 G2/J1 run1 C2 | 1, 2, 'Total: 2' | True
    45 cycle2 G2/J1 run1 P1 | 3, 3002399751580331, 'Total: 9007199254740993' | True
    46 cycle2 G2/J1 run1 F1 | 4, 7, 'Total: 28' | True
    47 cycle2 G2/J1 run1 F2 | 2, 11, 'Total: 22' | True
    48 cycle2 G2/J1 run2 C1 | 3, 2, 'Total: 6' | True
    49 cycle2 G2/J1 run2 C2 | 1, 2, 'Total: 2' | True
    50 cycle2 G2/J1 run2 P1 | 3, 3002399751580331, 'Total: 9007199254740993' | True
    51 cycle2 G2/J1 run2 F1 | 4, 7, 'Total: 28' | True
    52 cycle2 G2/J1 run2 F2 | 2, 11, 'Total: 22' | True

## Closeout

Budget reconciliation: E4 required 22 judgments including row 31, four more than its 18-judgment estimate. Total spend was 14 in cycle 1 and 38 in cycle 2, or 52/80. No paid calls, retries, errors or sealed consumption. Wall latency was not measured.

Under frozen J1 (5ef265c8f411156476f9fe9cf7d45ae8ad7dd4e44328fcce6e861076169ae941), G0 passed 1/3 extended climb examples and 0/2 fresh working examples in each run. G2 (6f73b85910638ce114736f2400aa9a829bde6a085921e38a9bab0d327e4328cd) passed 3/3 and 2/2 respectively in each run. Observed baseline spread was zero on each set. Replication is deterministic repeatability on synthetic examples. G0 in rows 33–42 was executed from its original function body reproduced inline. For reproduction, invoke the identified answer function on each recorded pair and pass the returned string to the indicated accepts function. For judge-only challenges, pass the recorded string directly.

Two cycles exhausted. G2 and J1 remain working candidates for review, with no promotion or holdout claim. No unresolved reviewer disagreement requires owner adjudication.
