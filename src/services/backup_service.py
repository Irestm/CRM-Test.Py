import os
from datetime import datetime
from src.infrastructure.backup.base import BackupStorage

class BackupService:
    def __init__(self, storage: BackupStorage, db_path: str):
        self.storage = storage
        self.db_path = db_path

    async def create_backup(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}.sqlite3"
        await self.storage.save_backup(self.db_path, backup_name)
        return backup_name

    async def restore_latest_backup(self) -> str:
        backup_dir = getattr(self.storage, 'backup_dir', None)
        if not backup_dir:
            raise ValueError("Storage does not support local directory inspection")
            
        if not os.path.exists(backup_dir):
            raise FileNotFoundError("Backup directory does not exist")
            
        files = [f for f in os.listdir(backup_dir) if f.endswith('.sqlite3')]
        if not files:
            raise FileNotFoundError("No backups found")
            
        files.sort(reverse=True)
        latest_backup = files[0]
        
        await self.storage.restore_backup(self.db_path, latest_backup)
        return latest_backup