# AppOps

App 投放运营工具集

## Admob

### Hooks

```python
from appops.hooks.admob import AdmobHook
h = AdmobHook()

h.accounts
Out[3]: ['pub-xxxx']

h.mediationreport_json(
    query_body={
        "report_spec": {
            "dateRange": { "startDate": {"year": 2021, "month": 8, "day": 30}, "endDate": {"year": 2021, "month": 8, "day": 30} },
            "dimensions": ["DATE","FORMAT"], # 
            "metrics": ["ESTIMATED_EARNINGS","AD_REQUESTS","MATCH_RATE","MATCHED_REQUESTS","IMPRESSIONS","CLICKS"],
            "sortConditions": [
                {"metric":"ESTIMATED_EARNINGS", "order": "ASCENDING"}
            ],
            "localizationSettings": { "currencyCode": "USD", "languageCode": "en-US" }
        }
    },
    accounts=None, # using accounts from connection
)
```

### Operator

ignore


## Ads