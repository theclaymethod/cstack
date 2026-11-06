import subprocess
import sys
for script in ('solution.py', 'verify.py', 'reset.py'):
    subprocess.run([sys.executable, '-I', '-B', script], check=True)
