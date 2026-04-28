import os
import shutil
import asyncio
from src.infrastructure.backup.base import BackupStorage

class LocalHDDStorage(BackupStorage):
    def __init__(self, backup_dir: str):
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    async def save_backup(self, db_path: str, backup_name: str) -> None:
        dest_path = os.path.join(self.backup_dir, backup_name)
        await asyncio.to_thread(shutil.copy2, db_path, dest_path)
