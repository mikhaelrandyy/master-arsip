# Publish to Pub/Sub
import base64
import json

from google.cloud import pubsub_v1
from fastapi import Request

from configs.config import settings
class PubSubService:
    __projectId:str
    def __init__(self, projectId:str = settings.PROJECT_NAME):
        self.__projectId = projectId

    def publish_to_pubsub(self, topic_name, message, action):
        try:
            message_dict = message.dict(
                exclude_unset=True
            )
            message_dict['action'] = action
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(self.__projectId, topic_name + settings.PUBSUB_PUBLISHER_SUFFIX)
            
            message_data = json.dumps(message_dict, indent=4, sort_keys=True, default=str).encode("utf-8")
            future = publisher.publish(topic_path, data=message_data)
            print(f"Published message ID: {future.result()}")
            return True
        except Exception as e:
            print(e)
            return False
            
    async def process_message(self,  message):
        data = message.data.decode("utf-8")
        print(f"Received pushed message: {data}")
        # Your message processing logic here
        message.ack()

    async def subscribe(self, subscriptionName: str):
        #publisher_client = pubsub_v1.PublisherClient()
        #topic_path = publisher_client.topic_path(self.__projectId, topik)
        #publisher_client.create_topic(topic_path)

        # 2. create subscription (test_push with push_config)
        # subscriber_client = pubsub_v1.SubscriberClient(credentials=self.credentials)
        subscriber_client = pubsub_v1.SubscriberClient()
        pubsubSubscriptionName = settings.PUBSUB_SUBCRIBER_PREFIX + subscriptionName
        pubsubPublisherName = subscriptionName + settings.PUBSUB_PUBLISHER_SUFFIX
        subscription_path = subscriber_client.subscription_path(
            self.__projectId, pubsubSubscriptionName
        )
        
        # push_endpoint_url = settings.SELF_URL + "/" + subscriptionName
        # push_config = pubsub_v1.types.PushConfig(push_endpoint=push_endpoint_url)

        # subscription = pubsub_v1.types.Subscription(
        #     name=subscription_path, topic=topik, push_config=push_config
        # )
        # update_mask = {"paths": {"push_config"}}

        # with subscriber_client:
        #     result = subscriber_client.update_subscription(
        #         request={"subscription": subscription, "update_mask": update_mask}
        #     )
        print(f"Listening for pushed messages from subcriber {pubsubSubscriptionName} to topic {pubsubPublisherName}")

        # Start the subscription in the background
        subscriber_client.subscribe(subscription_path, callback=self.process_message)
        
    async def generatePublisherMessage(self, request: Request, base64Str: str|None):
        base64_data = ""
        if base64Str and base64Str != "" :
            #decodedata =  json.loads(base64Str)
            base64_data =  base64Str #decodedata['message']['data']
        else:      
            data = await request.body()
            print(data.decode('utf-8'))
            decodedata =  json.loads((data.decode('utf-8')))    
            base64_data = decodedata['message']['data']
        decoded_data = base64.b64decode(base64_data).decode('utf-8')
        message_object = json.loads(decoded_data)
        print(message_object)
        return  message_object
    
pubsub_service = PubSubService()