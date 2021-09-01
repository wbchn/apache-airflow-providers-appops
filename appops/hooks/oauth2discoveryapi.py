
import json
from typing import Dict, Optional, Tuple

import google.auth.credentials
from airflow.exceptions import AirflowException
from airflow.providers.google.common.hooks.discovery_api import \
    GoogleDiscoveryApiHook
from googleapiclient.discovery import build


class GoogleOauth2DiscoveryApiHook(GoogleDiscoveryApiHook):

    def _get_credentials_and_project_id(self) -> Tuple[google.auth.credentials.Credentials, Optional[str]]:
        """Returns the Credentials object for Google API and the associated project_id"""
        if self._cached_credentials is not None:
            return self._cached_credentials, self._cached_project_id

        try:
            keyfile_dict: Optional[str] = self._get_field('keyfile_dict', None)
            keyfile_dict_json: Optional[Dict[str, str]] = None
            if keyfile_dict:
                keyfile_dict_json = json.loads(keyfile_dict)
        except json.decoder.JSONDecodeError:
            raise AirflowException('Invalid key JSON.')

        import google.oauth2.credentials
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
            keyfile_dict_json, scopes=self.scopes
        )

        project_id = self._get_field('project')

        self._cached_credentials = credentials
        self._cached_project_id = project_id

        return credentials, project_id
