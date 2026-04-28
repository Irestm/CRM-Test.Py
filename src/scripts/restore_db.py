import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.api.dependencies import get_backup_service

async def main():
    try:
        print("Starting disaster recovery process...")
        service = get_backup_service()
        restored_file = await service.restore_latest_backup()
        print(f"Successfully restored database from backup: {restored_file}")
    except Exception as e:
        print(f"Error during restore: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())