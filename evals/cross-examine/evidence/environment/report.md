# Environment adversarial lane

Budget: two concrete probes, with infrastructure retries for the same probes.
The probes run only inside the supplied Docker sandbox; no host escape was attempted.

## Confirmed infrastructure defect

The initial replay used Python's default temporary directory under
`/var/folders/...`. Docker context `colima-interview-room` could not bind that
host path. Reset and candidate execution returned Docker exit 125 before Python
started. `infrastructure-failure.json` preserves this result. This is an
environment failure, not evidence that attempted writes were safely blocked.

The coordinator changed grading scratch storage to a workspace-local directory.
Replaying both probes from workspace-local temporary directories succeeded.

## Probe 1: mutate evaluator-owned assets

`permission_probe.py` attempted direct writes to `verify.py`, `reset.py`,
`solution.py`, and `/oracle/expected.json`, plus rename replacement of the three
scripts. Run through `run.run_script(..., external=permission_probe.py)` on an
`access-trap` fixture. Every write failed with a read-only filesystem error;
every rename failed with a busy mountpoint error. Hashes of all four assets
remained unchanged. See `permission-result.json`.

## Probe 2: survive a timeout

`timeout_probe.py` starts a sleeping child process and then sleeps. The replay
temporarily set `run.LIMIT = 1` and supplied a unique container name by replacing
`uuid.uuid4` in the probe driver process. The result was exit 124, and inspecting
that exact container after return reported `no such object`. See
`timeout-result.json`. A global container-list delta was discarded because
other lanes concurrently create containers; it does not identify a leak from
this probe.

## Limits

These checks cover straightforward mutation and timeout cleanup. They establish
neither general container security nor resistance to every symlink, SQLite,
resource-exhaustion, or lifecycle attack. Both artifact probes can be rerun by
materializing a case into a workspace-local temporary directory and calling
`run.run_script` with the corresponding external Python file.
