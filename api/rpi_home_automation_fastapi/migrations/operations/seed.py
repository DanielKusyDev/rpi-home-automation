from typing import Any, Dict, List, Optional

from alembic.operations import MigrateOperation, Operations
from migrations.helpers import reflect_sqlalchemy_table
from sqlalchemy import Column, column
from sqlalchemy import table as sa_table


@Operations.register_operation("seed")
class SeedOperation(MigrateOperation):
    def __init__(
        self,
        table_name: str,
        rows: List[Dict],
        schema: Optional[str],
    ):
        self.table_name = table_name
        self.rows = rows
        self.schema = schema

    @classmethod
    def seed(cls, operations: Operations, table_name: str, rows: List[Dict], schema: Optional[str]) -> Any:
        """
        Merge given data rows into a DB table.
        * Items matched by comparing id_columns will be updated
        * Items not found in DB will be inserted
        * If delete_unmatched is set, any items in the DB not in given data will be deleted
        """
        op = cls(table_name, rows, schema)
        return operations.invoke(op)


@Operations.implementation_for(SeedOperation)
def seed(operations: Operations, op: SeedOperation) -> None:
    _source_alias = "SOURCE"
    f = operations.migration_context.dialect.identifier_preparer

    target_table = reflect_sqlalchemy_table(op.table_name, op.schema, operations)

    def _source_col(c: Column) -> str:
        return f"{_source_alias}.{f.quote(c.name)}"

    temp_table = sa_table(f"##temp_{target_table.name}", *[column(c.name, c.type) for c in target_table.columns])
    formatted_target_table = f.format_table(target_table)

    insert_col_names = ", ".join(f.quote(c.name) for c in target_table.columns)
    insert_col_values = ", ".join(_source_col(c) for c in target_table.columns)

    operations.create_table(
        temp_table.name,
        *[Column(c.name, c.type) for c in target_table.columns],
    )
    operations.bulk_insert(temp_table, op.rows)
    if op.identity_insert:
        operations.execute(f"SET IDENTITY_INSERT {formatted_target_table} ON;")
    operations.execute(f"INSERT INTO {target_table.name} ({insert_col_names}) VALUES({insert_col_values})")
    if op.identity_insert:
        operations.execute(f"SET IDENTITY_INSERT {formatted_target_table} OFF;")
    operations.drop_table(temp_table.name)
