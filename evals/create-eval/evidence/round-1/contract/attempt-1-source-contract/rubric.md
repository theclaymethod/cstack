# Source naming in imported synthetic items

Decide only whether an imported item names a source. This requirement is grounded in criterion-0002 version 2 of the supplied synthetic packet. It does not establish probability correctness, source reliability, clinical correctness, or actual product execution.

The `source-named` question applies to imported items. Pass when the output identifies a source with a nonempty name, whether in a structured field, prose, a citation, or another unambiguous representation. A literal `source` key is not required. A blank source field or no identified source fails. Unclear applicability or insufficient output evidence is UNKNOWN. Check questions are independent; there is only one configured question.

The stored output is a JSON serialization of artifact-0001's original structured output. Private provenance retains its source, scoped synthetic judgment, and origin. Numerical probability 0.9 is preserved without assessing it. Criterion-0001 is a preference without a settled task-specific length bound and is not scored. Criterion-0002 version 1 is superseded by version 2.

Handwritten structured and prose controls name Synthetic Reference A; the empty-name control does not. They exercise the naming rule only and are development evidence, not independent expert labels or a verified external source. All case `gold` values are null. The active audit context has already read the packet's annotations; no blind calibration claim is available.

The source-naming observation can be retained without supplying a replacement probability. The numerical concern remains in the incomplete queue. No rate from this package estimates production failure prevalence or authorizes a release.
