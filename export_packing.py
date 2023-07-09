import os
from pathlib import Path

try:
    os.mkdir('export-packed')
except:
    pass

for i in [f for f in os.listdir('export') if Path(os.path.join('export', f)).is_dir()]:
    source_path = os.path.join('export', i)
    destination_path = os.path.join('export-packed', f'{i}.zip')
    cmd = f'''7z a -tzip "{destination_path}" "{source_path}/*"'''
    # print(cmd)
    os.system(cmd)