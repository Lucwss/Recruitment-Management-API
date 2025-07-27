from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "vacancy" RENAME COLUMN "Status" TO "status";
        ALTER TABLE "vacancy" RENAME COLUMN "Urgency" TO "urgency";
        ALTER TABLE "vacancy" ALTER COLUMN "end_date" DROP NOT NULL;
        ALTER TABLE "vacancy" ALTER COLUMN "notes" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "vacancy" RENAME COLUMN "urgency" TO "Urgency";
        ALTER TABLE "vacancy" RENAME COLUMN "status" TO "Status";
        ALTER TABLE "vacancy" ALTER COLUMN "end_date" SET NOT NULL;
        ALTER TABLE "vacancy" ALTER COLUMN "notes" SET NOT NULL;"""
