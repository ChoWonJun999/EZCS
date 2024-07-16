from django.conf import settings
from openai import OpenAI

class Chatbot_trans:
    def __init__(self,
                api_key=settings.OPENAI_API_KEY,
                model_id='ft:gpt-3.5-turbo-0125:personal::9god26fK',
                behavior_policy=None,
                ):
        """
        explanation: Chatbot_trans 클래스는 OpenAI GPT-3.5-turbo Fine_tuning 모델을 사용하여 방언을 표준어로 번역해주는 클래스입니다.
 
        Args:
            model_id (str): model id
            api_key (_type_): openai api key
            behavior_policy (str): systemMessage
        """
        self.api_key = api_key
        self.model_id = model_id
        self.behavior_policy = behavior_policy
        
    def ask(self, question, message_history=[]):
        client = OpenAI(api_key = self.api_key)

        # 최초 질문 생성
        initial_message = {
            "role": "system",
            "content": self.behavior_policy,
        }

        # 사용자 질문 추가
        user_question = {
            "role": "user",
            "content": question,
        }

        # 메시지 리스트 생성
        message_history = [initial_message, user_question]
        
        # GPT에 질문을 전달하여 답변을 생성
        completion = client.chat.completions.create(
            model=self.model_id,
            messages=message_history,
        )

        return completion.choices[0].message.content
                    
    