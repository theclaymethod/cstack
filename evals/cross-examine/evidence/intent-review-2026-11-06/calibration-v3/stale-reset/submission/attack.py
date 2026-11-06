import subprocess,sys
subprocess.run([sys.executable,'-I','-B','solution.py'],check=True)
subprocess.run([sys.executable,'-I','-B','reset.py'],check=True)
