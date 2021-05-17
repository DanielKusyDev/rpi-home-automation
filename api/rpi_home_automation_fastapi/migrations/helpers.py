from alembic.operations import Operations
from sqlalchemy import MetaData, Table, inspect


def reflect_sqlalchemy_table(table_name: str, schema: str, operations: Operations) -> Table:
    target_table = Table(table_name, MetaData(), schema=schema)
    inspector = inspect(operations.migration_context.connection)
    inspector.reflecttable(target_table, None, resolve_fks=False)

    return target_table
