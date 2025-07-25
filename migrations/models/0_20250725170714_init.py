from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "vacancy" (
    "id" UUID NOT NULL PRIMARY KEY,
    "description" VARCHAR(255) NOT NULL,
    "sector" VARCHAR(255) NOT NULL,
    "manager" VARCHAR(255) NOT NULL,
    "salary_expectation" VARCHAR(255) NOT NULL,
    "Urgency" SMALLINT NOT NULL,
    "Status" VARCHAR(11) NOT NULL,
    "start_date" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "end_date" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "notes" VARCHAR(255) NOT NULL
);
COMMENT ON COLUMN "vacancy"."Urgency" IS 'Urgency options';
COMMENT ON COLUMN "vacancy"."Status" IS 'Status options';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
