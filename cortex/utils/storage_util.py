from pathlib import Path

storage_dir = Path('/cortex-storage')  # docker volume
if not storage_dir.is_dir():
    storage_dir = None  # for testing

