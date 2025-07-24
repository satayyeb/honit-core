from core.settings import OPENAI_BASE_URL, OPENAI_API_KEY, OPENAI_MODEL_NAME
from router.models import Session, Log
from openai import OpenAI

client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)


class LLMApi:

    @staticmethod
    def chat(session: Session, message: str) -> Log:
        completion = client.chat.completions.create(
            model=OPENAI_MODEL_NAME,
            extra_body={},
            messages=[
                *session.context,
                {'role': 'user', 'content': message},
            ]
        )
        model_output = completion.choices[0].message.content
        return Log.objects.create(session=session, request=message, response=model_output)
