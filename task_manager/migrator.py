from peewee import PostgresqlDatabase, SqliteDatabase, MySQLDatabase
from playhouse.cockroachdb import CockroachDatabase
from typing import Union, Optional
from pathlib import Path


class SqlMigrator:
    MIGRATION_SEPARATOR = "-- Downgrade --"
    CREATE_MIGRATION_TABLE = """
        CREATE TABLE IF NOT EXISTS MigrationHistory(
            nr SERIAL PRIMARY KEY,
            id INTEGER NOT NULL,
            name VARCHAR(256) NOT NULL,
            upgrade TEXT NOT NULL,
            downgrade TEXT NOT NULL
        );
    """
    SELECT_LAST_MIGRATION = """
        SELECT *
        FROM MigrationHistory
        ORDER BY nr DESC
        LIMIT 1;
    """
    INSERT_NEW_MIGRATION = """
        INSERT INTO MigrationHistory
        VALUES(?, ?, ?, ?, ?);
    """

    def __init__(
        self,
        database: Union[
            PostgresqlDatabase,
            SqliteDatabase,
            MySQLDatabase,
            CockroachDatabase,
        ],
        migrations_dir: str="migrations"
    ):
        # Create connection with database
        self.db = database
        self.db.connect()
        self.db.execute_sql(
            SqlMigrator.CREATE_MIGRATION_TABLE
        )
        # Get migrations files
        self.migrations_dir = Path(migrations_dir)

        if not self.migrations_dir.exists():
            self.migrations_dir.mkdir()

        self.migrations = self.migrations_dir.glob("*.sql")

    @property
    def last_migration(self) -> Optional[dict]:
        record = self.db.execute_sql(SqlMigrator.SELECT_LAST_MIGRATION).fetchone()

        if record:
            return {
                "nr": record[0],
                "id": record[1],
                "name": record[2],
                "upgrade": record[3],
                "downgrade": record[4]
            }

    def get_migration(self, name_or_id: Union[str, int]) -> Optional[dict]:
        for migration_file in self.migrations:
            migration_id, migration_name = migration_file.stem.split("-", 1)

            if (isinstance(name_or_id, int) and int(migration_id) == name_or_id) or (migration_name == name_or_id):
                upgrade, downgrade = migration_file.read_text().split(SqlMigrator.MIGRATION_SEPARATOR, 1)

                return {
                    "id": int(migration_id),
                    "name": migration_name,
                    "upgrade": upgrade,
                    "downgrade": SqlMigrator.MIGRATION_SEPARATOR + downgrade
                }

    def migrate(self, name_or_id: Union[str, int]):
        migration = self.get_migration(name_or_id)

        if migration:
            self.db.execute_sql(migration["upgrade"])
            self.db.execute_sql(
                SqlMigrator.INSERT_NEW_MIGRATION,
                [
                    self.last_migration["nr"] + 1,
                    migration["id"],
                    migration["name"],
                    migration["upgrade"],
                    migration["downgrade"]
                ]
            )

    def rollback(self, name_or_id: Union[str, int]):
        migration = self.get_migration(name_or_id)

        if migration:
            previous_migration = self.get_migration(migration["id"] - 1)

            if not previous_migration:
                previous_migration = {
                    "id": 0,
                    "name": "EMPTY",
                    "upgrade": "",
                    "downgrade": ""
                }

            nr = self.last_migration["nr"] if self.last_migration else 0
            self.db.execute_sql(migration["downgrade"])
            self.db.execute_sql(
                SqlMigrator.INSERT_NEW_MIGRATION,
                [
                    nr + 1,
                    previous_migration["id"],
                    previous_migration["name"],
                    previous_migration["upgrade"],
                    previous_migration["downgrade"]
                ]
            )


if __name__ == "__main__":
    db = SqliteDatabase("sqlite.db")
    migrator = SqlMigrator(db)
    migrator.rollback(1)