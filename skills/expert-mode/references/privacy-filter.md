# Local PII filtering before export

Use [OpenAI Privacy Filter](https://huggingface.co/openai/privacy-filter) as an optional local redaction aid for the [export workflow](export.md). It detects text spans across eight categories, including names, contact details, account numbers, dates, URLs, and secrets. Its model card describes missed identifiers, excess masking, and domain variation; it does not guarantee anonymization. Review clinical identifiers and potentially identifying combinations separately. [Model card](https://huggingface.co/openai/privacy-filter#bias-risks-and-limitations)

## Set up once in the working project

Use Python 3.10 or newer. The optional runtime installs PyTorch and other dependencies; ordinary capture and manual exports keep using standard-library Python. Keep the tool checkout, environment, model cache, and private packet outside version control. The following uses the [official local package](https://github.com/openai/privacy-filter#how-to-use), not a hosted inference service. [Package requirements](https://github.com/openai/privacy-filter/blob/main/pyproject.toml)

```bash
python3 -m venv .venv-privacy-filter
git clone https://github.com/openai/privacy-filter.git .tools/privacy-filter
.venv-privacy-filter/bin/python -m pip install -e .tools/privacy-filter
git -C .tools/privacy-filter rev-parse HEAD > .tools/privacy-filter.commit
```

Download only the native checkpoint, pin its resolved revision, and warm the tokenizer cache with no private input:

```bash
TIKTOKEN_CACHE_DIR=.models/tiktoken .venv-privacy-filter/bin/python - <<'PY'
import json
from pathlib import Path
from huggingface_hub import HfApi, snapshot_download
import tiktoken

model_id = "openai/privacy-filter"
revision = HfApi().model_info(model_id).sha
snapshot_download(
    repo_id=model_id, revision=revision,
    local_dir=".models/privacy-filter", allow_patterns=["original/*"],
)
Path(".models/privacy-filter.revision").write_text(revision + "\n")
config = json.loads(Path(".models/privacy-filter/original/config.json").read_text())
tiktoken.get_encoding(config["encoding"])
PY
```

The native checkpoint is under `original/`; the upstream downloader uses that subtree too. The runtime reads its tokenizer name from `config.json`. [Checkpoint downloader](https://github.com/openai/privacy-filter/blob/main/opf/_common/checkpoint_download.py), [runtime](https://github.com/openai/privacy-filter/blob/main/opf/_core/runtime.py)

Run a synthetic smoke check on CPU before processing source records:

```bash
TIKTOKEN_CACHE_DIR=.models/tiktoken HF_HUB_OFFLINE=1 \
  .venv-privacy-filter/bin/python - <<'PY'
from opf import OPF
model = OPF(model=".models/privacy-filter/original", device="cpu")
result = model.redact("Fictional contact: Avery Lane, avery@example.invalid.")
print(result.redacted_text)
PY
```

The [public API](https://github.com/openai/privacy-filter/blob/main/opf/_api.py) supports CPU or CUDA and structured results with span offsets. The export helper uses those offsets on parsed values and stops on tokenizer round-trip warnings. Use the same `TIKTOKEN_CACHE_DIR=.models/tiktoken` setting when invoking the helper. Downloads happen during setup; inference uses the local checkpoint. Offline flags are not a network sandbox.

## Export only sanitized content

The CLI and structured API results include original text and the detected spans' original text in addition to redacted output. Those reports are private working data, not sanitized exports. The helper copies neither raw field into the bundle. [Official output schema](https://github.com/openai/privacy-filter/blob/main/OUTPUT_SCHEMAS.md)

The helper scans individual JSON keys and string/numeric values with field-name context. This preserves JSON syntax but does not provide the whole document's context to every call. Numeric masking can change a value's type; generic placeholders can also erase important distinctions. Review these effects and task meaning before using a row in an eval. Schema preservation and a successful model call do not prove de-identification.

Record the model revision and installed package/code version with the local processing receipt. Keep `.tools/privacy-filter.commit` and dependency details privately for reproducibility. If the model or policy changes, recheck representative synthetic or authorized local examples before exporting new sensitive records. No Docker, SQLite, or remote inference endpoint is needed for this path.
