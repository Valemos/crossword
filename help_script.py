from pathlib import Path

file = Path('./categories/.txt')
file_out = Path('./categories/default.txt')

with file.open('r') as fin:
    with file_out.open('w') as fout:
        for line in fin.readlines():
            if len(line) > 2:
                fout.write(line.lower())
