import datetime, json, pathlib, subprocess, sys, time
root = pathlib.Path(__file__).resolve().parent
args = sys.argv[1:]
label = args.pop(0)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
tick = time.monotonic()
p = subprocess.run(args, text=True, capture_output=True)
(root/'commands'/f'{label}.stdout').write_text(p.stdout)
(root/'commands'/f'{label}.stderr').write_text(p.stderr)
record = dict(label=label, argv=args, cwd=str(pathlib.Path.cwd()), started=started, elapsed_seconds=time.monotonic()-tick, exit_code=p.returncode, stdout=f'commands/{label}.stdout', stderr=f'commands/{label}.stderr')
with (root/'commands.jsonl').open('a') as f: f.write(json.dumps(record)+'\n')
print(json.dumps(record))
print(p.stdout[:1500])
sys.exit(p.returncode)
