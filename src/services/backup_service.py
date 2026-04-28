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
