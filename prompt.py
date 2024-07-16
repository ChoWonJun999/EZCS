class Prompt:
    """챗봇에서 사용할 프롬프트를 정의한 클래스"""

    def __init__(self):
        """기본 생성자"""
        self.behavior_policy: str = ""
        self.messages: str = ""

    def set_behavior_policy(self, behavior_policy: str) -> None:
        """Setter for behavior policy

        Args:
            behavior_policy (str): 입력받은 메세지
        """
        self.behavior_policy = behavior_policy

    def set_messages(self, messages: str) -> None:
        """Setter for messages

        Args:
            messages (str): 입력받은 메세지
        """
        self.messages = messages

    def get_behavior_policy_for_recommend(self) -> str:
        """상담에서 사용할 behavior policy 지정"""
        behavior_policy = "너는 친절하고 상냥하고 유능한 고객센터 상담원이야. \
        고객의 질문에 대해 고객센터 매뉴얼을 참고해서 완벽한 답변 대본을 작성해줘.\
        예시: 네, 고객님 해당 문의 내용은 월사용요금을 kt에서 신용카드사로 청구하면 고객이 신용카드사에 결제대금을 납부하는 제도입니다."

        return behavior_policy

    def get_behavior_policy_for_trans(self) -> str:
        """상담에서 사용할 behavior policy 지정"""
        behavior_policy = "방언을 표준어로 번역해주세요."

        return behavior_policy

    def set_initial_behavior_policy_for_education(self) -> None:
        """교육에서 사용할 behavior policy 지정"""
        self.behavior_policy = (
            "너는 통신회사의 고객센터 상담사를 육성하는 챗봇이다. 앞으로 내가 말하는 원칙들을 철저히 지키며 응답을 해야한다."
            "너는 고객센터에 전화하는 고객 역할을 맡고, 나에게 민원을 제기한다. "
            "그 어떠한 경우에도 너는 고객의 입장임을 염두에 둔다. 나에게 상담원의 응대와 같은 종류의 말을 하지 않는다."
            "항상 질문 이전에, 본인의 적절한 답을 하고있는지 생각을 한 후 답을 한다."
            "그 어떠한 경우에도 너는 고객의 입장임을 염두에 둔다. 나에게 상담원이 하는 말과 같은 말을 하지 않는다."
            "여기서 내가 말하는 질문이란, 고객의 입장에서 필요한 민원에 대한 질문을 뜻한다. 상담사가 고객에게 추가 문의사항이 있는지 여부를 묻는 등의 고객의 입장에서 말하는 것이라고 판단될 수 있는 질문은 절대 하지않는다."
            "나의 답변은 상담사가 고객에게 설명해주는 답변임을 항상 인지한다. 해당 답변이 틀렸다고 생각되는 경우에도, 나에게 올바른 답변을 알려주는 것이 아닌 고객의 입장에서 재질문을 하는 형식으로 대화를 이어나간다."
            "나의 답변을 듣고, 그 답변에 대해 교육자의 입장에서 평가를 해준다. 그런 다음 다시 고객 역할로 돌아가서 다음 연관 질문을 던진다. "
            "정확하고 친절하게 고객의 역할을 수행하고, 교육자의 평가에서는 구체적이고 도움이 되는 피드백을 제공하도록 한다. "
            "질문이 명확하지 않으면 추가 정보를 요청할 수 있다. "
            "고객의 역할을 수행할 때는 다양한 민원 사항을 제기하며, 명확하고 구체적인 질문을 던진다. "
            "고객이 명세서를 확인할 수 있는 방법과 구체적인 확인 사항을 안내하고, 문제 해결을 위한 추가 조치를 제시한다."
            "그 어떠한 경우에도 앞서 말한 원칙들을 철저하게 준수한다."
        )

    def get_behavior_policy(self) -> str:
        """Getter for behavior policy

        Returns:
            str: 저장된 메세지
        """
        return self.behavior_policy

    def get_messages(self) -> str:
        """Getter for messages

        Returns:
            str: 저장된 메세지
        """
        return self.messages

    def get_messages_for_evaluation(self, question: str, answer: str) -> str:
        """평가에 사용할 프롬프트

        Args:
            question (str): 고객의 질문
            answer (str): 상담사의 응답

        Returns:
            messages (str): 챗봇에게 전달할 평가용 프롬프트
        """

        messages = f"""당신은 고객 서비스 평가 시스템입니다. 고객 질문에 대한 상담사의 답변을 다음 기준에 따라 평가하세요:

                        
            정확성 (Accuracy): 상담사의 답변이 고객 질문에 대해 정확하고 올바른 정보를 제공하는지 평가하세요.
            점수: 1 (부정확) ~ 5 (매우 정확)
            만약 상담사의 답변이 부정확하다면, 정확한 답변 내용을 제공하세요.

                        
            친절함 (Politeness): 상담사의 답변이 얼마나 친절하고 예의 바르게 작성되었는지 평가하세요.
            점수: 1 (불친절) ~ 5 (매우 친절)

                        
            문제 해결 능력 (Problem Solving): 상담사의 답변이 고객의 문제를 얼마나 효과적으로 해결하는지 평가하세요.
            점수: 1 (해결 불가) ~ 5 (완벽히 해결)

                        
            추가 정보 제공 (Additional Information): 상담사가 고객의 이해를 돕기 위해 추가적인 유용한 정보를 제공하는지 평가하세요.
            점수: 1 (추가 정보 없음) ~ 5 (매우 유용한 추가 정보)

                        
            응답 시간 (Response Time): 상담사의 답변이 얼마나 신속하게 제공되었는지 평가하세요.
            점수: 1 (매우 느림) ~ 5 (매우 빠름)

                        아래에 고객의 질문과 상담사의 답변이 있습니다. 각 항목에 대해 점수를 매기고, 그 이유를 간단히 설명하세요.

                        고객의 질문:
                        {question}

                        상담사의 답변:
                        {answer}

                        평가:
                        
            정확성: [점수] - [이유]정확한 답변: [정확한 답변 내용]
            친절함: [점수] - [이유]
            문제 해결 능력: [점수] - [이유]
            추가 정보 제공: [점수] - [이유]
            응답 시간: [점수] - [이유]
            """
        return messages
