
import json
from operator import attrgetter
from typing import (Any, Dict, Optional, Sequence)


from appops.hooks.oauth2discoveryapi import GoogleOauth2DiscoveryApiHook


class AdmobHook(GoogleOauth2DiscoveryApiHook):
    conn_name_attr = 'admob_conn_id'
    default_conn_name = 'admob_default'

    conn_type = 'admob'
    hook_name = 'Admob'

    @staticmethod
    def get_connection_form_widgets() -> Dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3PasswordFieldWidget, BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import IntegerField, PasswordField, StringField
        from wtforms.validators import NumberRange

        return {
            f"extra__{AdmobHook.conn_type}__keyfile_dict": PasswordField(
                lazy_gettext('Keyfile JSON'), widget=BS3PasswordFieldWidget()
            ),
            f"extra__{AdmobHook.conn_type}__scope": StringField(
                lazy_gettext('Scopes (comma separated)'), widget=BS3TextFieldWidget(),
                default='https://www.googleapis.com/auth/admob.report'
            ),
            f"extra__{AdmobHook.conn_type}__num_retries": IntegerField(
                lazy_gettext('Number of Retries'),
                validators=[NumberRange(min=0)],
                widget=BS3TextFieldWidget(),
                default=3,
            ),
            f"extra__{AdmobHook.conn_type}__accounts": StringField(
                lazy_gettext('Account Ids(comma separated)'), widget=BS3TextFieldWidget()
            ),
        }

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns custom field behaviour"""
        return {
            "hidden_fields": ['host', 'schema', 'login', 'password', 'port', 'extra'],
            "relabeling": {},
        }

    def __init__(
        self,
        api_version: str = 'v1',
        admob_conn_id: str = 'admob_default',
        **kwargs
    ) -> None:
        super().__init__(
            api_service_name='admob',
            api_version=api_version,
            gcp_conn_id=admob_conn_id,
            **kwargs,
        )
        self.admob_conn_id = admob_conn_id

    def _get_field(self, f: str, default: Any = None) -> Any:
        """
        Fetches a field from extras, and returns it. This is some Airflow
        magic. The {conn_type} hook type adds custom UI elements
        to the hook page, which allow admins to specify service_account,
        key_path, etc. They get formatted as shown below.
        """
        long_f = f'extra__{AdmobHook.conn_type}__{f}'
        if hasattr(self, 'extras') and long_f in self.extras:
            return self.extras[long_f]
        else:
            return default

    @property
    def accounts(self) -> Optional[str]:
        field_value = self._get_field('accounts', default='')
        if field_value:
            return field_value.split(',')
        else:
            return []

    def list_accounts(self) -> Optional[str]:
        accounts = self.query(
            endpoint='admob.accounts.list',
            data={},
        )
        return accounts

    def _admob_flat_dimentions(self, dimensions: Dict) -> Dict:
        # https://developers.google.com/admob/api/v1/reference/rest/v1/ReportRow#DimensionValue
        output = {}
        for prefix, value in dimensions.items():
            # print(prefix, value)
            output[prefix] = value.get("value")
            if 'displayLabel' in value:
                output[f'{prefix}_NAME'] = value["displayLabel"]
        return output

    def _admob_flat_metrics(self, metrics: Dict) -> Dict:
        # https://developers.google.com/admob/api/v1/reference/rest/v1/ReportRow#metricvalue
        output = {}
        for metric, value in metrics.items():
            if "integerValue" in value:
                output[metric] = value["integerValue"]
            elif "doubleValue" in value:
                output[metric] = value["doubleValue"]
            elif "microsValue" in value:
                output[metric] = value["microsValue"]
        return output

    def _admob_plain_api_response(self, api_response, account):
        row = []
        header = api_response[0]["header"]
        sdate = header["dateRange"]["startDate"]
        footer = api_response[-1]["footer"]
        self.log.info(f"Api response rows: {footer['matchingRowCount']}")

        for line in api_response[1:-1]:
            dimensions = line["row"]["dimensionValues"]
            metrics = line["row"]["metricValues"]
            formated = {
                "account": account,
            }
            formated.update(
                self._admob_flat_dimentions(dimensions)
            )
            formated.update(
                self._admob_flat_metrics(metrics)
            )
            row.append(formated)

        return row

    def mediationreport_json(self, report_spec: Dict, accounts: Optional[Sequence[str]] = None, num_retries: int = None) -> Dict:
        if not accounts:
            accounts = self.accounts
        if num_retries is None:
            num_retries = self.num_retries

        reports = []
        for account in accounts:
            self.log.info(
                f"mediationReport.generate: {account}, with query: {report_spec}")
            response = self.query(
                endpoint='admob.accounts.mediationReport.generate',
                data={
                    "parent": f'accounts/{account}',
                    "body": {"report_spec": report_spec},
                },
                paginate=False,
                num_retries=num_retries,
            )
            rows = self._admob_plain_api_response(response, account)
            self.log.info(f'report fetch with {len(rows)} records.')
            reports.extend(rows)

        self.log.info(f"Total report {len(reports)} records.")
        return reports
