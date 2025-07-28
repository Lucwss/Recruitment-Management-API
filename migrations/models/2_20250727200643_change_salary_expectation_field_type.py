from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "vacancy" ALTER COLUMN "salary_expectation" TYPE DOUBLE PRECISION USING "salary_expectation"::DOUBLE PRECISION;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "vacancy" ALTER COLUMN "salary_expectation" TYPE VARCHAR(255) USING "salary_expectation"::VARCHAR(255);"""
