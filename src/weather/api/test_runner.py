from types import MethodType

from django.db import connections
from django.test.runner import DiscoverRunner


def prepare_database(db):
    """
    Creates the `weather` schema.
    """
    db.connect()
    db.connection.cursor().execute("CREATE SCHEMA weather")


class CustomTestRunner(DiscoverRunner):
    """
    This creates the `weather` schema after the test database is created.
    Needed because the default test runner doesn't create the schema.
    """

    def setup_databases(self, **kwargs):
        for connection_name in connections:
            connection = connections[connection_name]
            connection.prepare_database = MethodType(prepare_database, connection)
        db = super().setup_databases(**kwargs)
        return db
