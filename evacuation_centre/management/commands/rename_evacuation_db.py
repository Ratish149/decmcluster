from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = (
        "Renames the evacuation centre DB table and indexes from the old typo-based "
        "names to the correct names, then fakes the related migrations. "
        "Safe to run multiple times (idempotent)."
    )

    OLD_TABLE = "evacutation_centre_evacutationcentre"
    NEW_TABLE = "evacuation_centre_evacuationcentre"

    # (old_index_name, new_index_name, column(s))
    INDEXES = [
        (
            "evacutation_compoun_59af64_idx",
            "evacuation__compoun_c0bce6_idx",
            "(compound_name)",
        ),
        (
            "evacutation_latitud_e1243a_idx",
            "evacuation__latitud_052a05_idx",
            "(latitude, longitude)",
        ),
    ]

    MIGRATIONS_TO_FAKE = [
        ("evacuation_centre", "0001_initial"),
        ("evacuation_centre", "0002"),
    ]

    def handle(self, *args, **options):
        vendor = connection.vendor  # 'sqlite', 'postgresql', 'mysql'
        self.stdout.write(f"Database backend: {vendor}")

        with connection.cursor() as cursor:
            self._rename_table(cursor, vendor)
            self._rename_indexes(cursor, vendor)

        self._fake_migrations()

        self.stdout.write(
            self.style.SUCCESS(
                "\nAll done! Run `python manage.py migrate` to confirm no pending migrations."
            )
        )

    # ------------------------------------------------------------------
    # Table rename
    # ------------------------------------------------------------------
    def _rename_table(self, cursor, vendor):
        existing_tables = self._get_tables(cursor)

        if self.NEW_TABLE in existing_tables:
            self.stdout.write(
                self.style.WARNING(
                    f"[SKIP] Table already named '{self.NEW_TABLE}' — no rename needed."
                )
            )
            return

        if self.OLD_TABLE not in existing_tables:
            self.stdout.write(
                self.style.ERROR(
                    f"[ERROR] Neither '{self.OLD_TABLE}' nor '{self.NEW_TABLE}' found in the database. "
                    "Nothing to rename."
                )
            )
            return

        self.stdout.write(f"Renaming table: {self.OLD_TABLE} → {self.NEW_TABLE}")
        cursor.execute(f"ALTER TABLE {self.OLD_TABLE} RENAME TO {self.NEW_TABLE}")
        self.stdout.write(self.style.SUCCESS("[OK] Table renamed."))

    # ------------------------------------------------------------------
    # Index rename
    # ------------------------------------------------------------------
    def _rename_indexes(self, cursor, vendor):
        existing_indexes = self._get_indexes(cursor)

        for old_name, new_name, columns in self.INDEXES:
            if new_name in existing_indexes:
                self.stdout.write(
                    self.style.WARNING(f"[SKIP] Index '{new_name}' already exists.")
                )
                continue

            if old_name in existing_indexes:
                if vendor == "postgresql":
                    # PostgreSQL supports direct rename
                    self.stdout.write(f"Renaming index: {old_name} → {new_name}")
                    cursor.execute(f"ALTER INDEX {old_name} RENAME TO {new_name}")
                    self.stdout.write(self.style.SUCCESS("[OK] Index renamed."))
                else:
                    # SQLite / MySQL: drop old + create new
                    self.stdout.write(f"Dropping old index: {old_name}")
                    cursor.execute(f"DROP INDEX IF EXISTS {old_name}")

                    self.stdout.write(f"Creating new index: {new_name} on {columns}")
                    cursor.execute(
                        f"CREATE INDEX {new_name} ON {self.NEW_TABLE} {columns}"
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"[OK] Index recreated as '{new_name}'.")
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"[SKIP] Old index '{old_name}' not found — may already be renamed."
                    )
                )

    # ------------------------------------------------------------------
    # Fake migrations
    # ------------------------------------------------------------------
    def _fake_migrations(self):
        from django.db.migrations.recorder import MigrationRecorder

        recorder = MigrationRecorder(connection)
        applied = {(r.app, r.name) for r in recorder.migration_qs.all()}

        for app, migration in self.MIGRATIONS_TO_FAKE:
            if (app, migration) in applied:
                self.stdout.write(
                    self.style.WARNING(
                        f"[SKIP] Migration '{app}.{migration}' already recorded."
                    )
                )
            else:
                recorder.record_applied(app, migration)
                self.stdout.write(
                    self.style.SUCCESS(f"[OK] Faked migration: {app}.{migration}")
                )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_tables(self, cursor):
        vendor = connection.vendor
        if vendor == "sqlite":
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        elif vendor == "postgresql":
            cursor.execute(
                "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
            )
        elif vendor == "mysql":
            cursor.execute("SHOW TABLES")
        else:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return {row[0] for row in cursor.fetchall()}

    def _get_indexes(self, cursor):
        vendor = connection.vendor
        if vendor == "sqlite":
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        elif vendor == "postgresql":
            cursor.execute(
                "SELECT indexname FROM pg_indexes WHERE schemaname = 'public'"
            )
        elif vendor == "mysql":
            cursor.execute(
                f"SELECT index_name FROM information_schema.statistics "
                f"WHERE table_schema = DATABASE() AND table_name = '{self.NEW_TABLE}'"
            )
        else:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        return {row[0] for row in cursor.fetchall()}
