import json
from operator import attrgetter
from tempfile import NamedTemporaryFile
from typing import List, Optional, Dict, Sequence, Union

from airflow.models import BaseOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from appops.hooks.admob import AdmobHook


class AdmobToPostgresOperator(BaseOperator):

    template_fields = ('postgres_table', 'report_spec')
    ui_color = '#fba000'

    def __init__(
        self,
        *,
        report_spec: Union[Dict, str],
        accounts: Optional[Sequence[str]] = None,
        replace_index: str = None,
        postgres_table: str,
        admob_conn_id: str = 'admob_default',
        postgres_conn_id: str = 'postgres_default',
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.postgres_table = postgres_table
        self.postgres_conn_id = postgres_conn_id

        if isinstance(report_spec, str):
            self.report_spec = json.loads(report_spec)
        else:
            self.report_spec = report_spec
        self.accounts = accounts
        self.admob_conn_id = admob_conn_id

        self.replace_index = replace_index

    def execute(self, context: Dict) -> None:
        admob = AdmobHook(admob_conn_id=self.admob_conn_id)
        self.log.info(
            f"Extracting data from Google Admob: {self.admob_conn_id}.")

        records = admob.mediationreport_json(
            self.report_spec,
            self.accounts,
        )

        target_fields = list(records[0].keys())
        rows = [tuple(r[k] for k in target_fields) for r in records]
        self.log.info(f"Inserting {len(rows)} rows into Postgres.")

        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        hook.insert_rows(table=self.postgres_table, rows=rows,
                         target_fields=target_fields,
                         replace=True if self.replace_index else False,
                         replace_index=self.replace_index)
