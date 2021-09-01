
import os

from airflow import models
from airflow.utils import dates
from airflow.operators.python import PythonOperator
from appops.hooks.admob import AdmobHook


def admob_test(*args, **kwargs):
    hook = AdmobHook(admob_conn_id='admob_default')
    accounts = hook.list_accounts()
    hook.log.info(accounts)

    # for acc in accounts['account']:
    #     response = hook.query(
    #         endpoint='admob.accounts.mediationReport.generate',
    #         data={
    #             "parent": acc['name'],
    #             "body": {
    #                 "report_spec": {
    #                     "dateRange": { "startDate": {"year": 2021, "month": 8, "day": 26}, "endDate": {"year": 2021, "month": 8, "day": 26} },
    #                     "dimensions": ["DATE","AD_UNIT","COUNTRY","APP_VERSION_NAME","FORMAT"], # 
    #                     "metrics": ["AD_REQUESTS","MATCH_RATE","MATCHED_REQUESTS","IMPRESSIONS","CLICKS"], # "ESTIMATED_EARNINGS", Requested metrics and dimensions are incompatible
    #                     "sortConditions": [
    #                         {"metric":"AD_REQUESTS", "order": "ASCENDING"}
    #                     ],
    #                     "dimensionFilters": { "dimension": "COUNTRY", "matchesAny": {"values": ["PH"]} },
    #                     "localizationSettings": { "currencyCode": "USD", "languageCode": "en-US" }
    #                 }
    #             }
    #         },
    #         paginate=False,
    #         num_retries=1,
    #     )
    #     hook.log.info(response)

def admob_report(report_spec, *args, **kwargs):
    hook = AdmobHook(admob_conn_id='admob_default')

    response = hook.mediationreport_json(
        report_spec=report_spec,
        accounts=None,
        num_retries=1,
    )
    hook.log.info(response)


with models.DAG(
    "example_google_admob",
    schedule_interval=None,  # Override to match your needs
    start_date=dates.days_ago(1),
) as dag:
    admob_test = PythonOperator(
        task_id='admob_test',
        python_callable=admob_test,
    )

    report = PythonOperator(
        task_id='report',
        python_callable=admob_report,
        op_kwargs={
            "report_spec": {
                    "dateRange": { "startDate": {"year": "{{execution_date.year}}", "month": "{{execution_date.month}}", "day": "{{execution_date.day}}"}, "endDate": {"year": "{{execution_date.year}}", "month": "{{execution_date.month}}", "day": "{{execution_date.day}}"} },
                    "dimensions": ["DATE",], # 
                    "metrics": ["AD_REQUESTS","MATCH_RATE","MATCHED_REQUESTS","IMPRESSIONS","CLICKS"], # "ESTIMATED_EARNINGS", Requested metrics and dimensions are incompatible
                    "sortConditions": [
                        {"metric":"AD_REQUESTS", "order": "ASCENDING"}
                    ],
                    "localizationSettings": { "currencyCode": "USD", "languageCode": "en-US" }
                }
            }
    )
