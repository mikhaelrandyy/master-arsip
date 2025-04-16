from typing import Tuple
from schemas.workflow_sch import WorkflowCreateResponseSch
from configs.config import settings
import requests


class WorkflowService:
    WF_BASE_URL = settings.WF_BASE_URL
    WF_CLIENT_ID = settings.WF_CLIENT_ID
    OAUTH2_TOKEN = settings.OAUTH2_TOKEN
    CONNECTION_FAILED = "Cannot create connection to authentication server."

    async def create_workflow(self, body:dict) -> Tuple[WorkflowCreateResponseSch|None, str]:

        url_create_workflow = self.WF_BASE_URL + '/approval-workflow-system/client/api/workflow'

        headers = {
            'Authorization': 'Bearer ' + self.OAUTH2_TOKEN,
            'Content-Type': 'Application/Json'
        }

        try:
            response = requests.post(url_create_workflow, json=body, headers=headers)
            if response.status_code == 200:
                data = response.json()['data']
                return WorkflowCreateResponseSch(**data), "OK"
            else:
                print(f'{response.status_code}:{response.reason}')
                return None, response.reason
        except Exception as e:
            return None, self.CONNECTION_FAILED
        
    async def reject_workflow(self, body:dict) -> Tuple[dict, str]:

        url_rejected_workflow = self.WF_BASE_URL + '/approval-workflow-system/client/api/workflow/reject-by-client'

        headers = {
            'Authorization': 'Bearer ' + self.OAUTH2_TOKEN,
            'Content-Type': 'Application/Json'
        }

        body["client_id"] = self.WF_CLIENT_ID

        try:

            response = requests.post(url_rejected_workflow, json=body, headers=headers)
            if response.status_code == 200:
                data = response.json()['data']
                return WorkflowCreateResponseSch(**data), "OK"
            else:
                print(f'{response.status_code}:{response.reason}')
                return None, response.reason
        except Exception as e:
            return None, self.CONNECTION_FAILED