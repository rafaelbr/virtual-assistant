from watson_developer_cloud import AssistantV1
import config

class AssistantService:

    def __init__(self):
        self.service = AssistantV1(
            iam_apikey=config.ASSISTANT_APIKEY,
            url=config.ASSISTANT_URL,
            version='2018-07-10'
        )

    def message(self, message, context):
        content = self.service.message(
            workspace_id=config.ASSISTANT_WORKSPACEID,
            input={
                'text': message
            },
            context=context
        ).get_result()
        return content

