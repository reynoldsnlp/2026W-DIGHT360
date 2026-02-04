from pathlib import Path


poetry_dir = Path('corpora/poems')
all_files = poetry_dir.glob('*.txt')
for path in all_files:
    with path.open() as f:
        txt = f.read()
    ...

print(list(all_files))
