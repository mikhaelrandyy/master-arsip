import datetime
import json
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
from configs.config import settings
from typing import Dict, Any


class GCloudTaskService:
    client = tasks_v2.CloudTasksClient()

    def create_task(self, base_url:str, payload: Dict[str, Any] | None = None):
        url = base_url
        url = url.replace('http://', 'https://')

        payload = payload
        try:
            task = self._create_task(
                url=url,
                queue_name='landrope-queue',
                payload=payload
            )
        except Exception as e:
            print(e)
        return payload