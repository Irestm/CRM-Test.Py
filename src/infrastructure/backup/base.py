from typing import Protocol

class BackupStorage(Protocol):
    async def save_backup(self, db_path: str, backup_name: str) -> None:
        ...
        
    async def restore_backup(self, db_path: str, backup_name: str) -> None:
        ...