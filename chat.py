from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
 
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from django.conf import settings
 
 
class Chatbot:
    def __init__(self,
                api_key=settings.OPENAI_API_KEY,
                db_path=settings.DB_PATH,
                category=None,
                model_id='gpt-3.5-turbo',
                behavior_policy=None,
                THRESHOLD=0.4
                ):
        """
        explanation: Chatbot 클래스는 OpenAI GPT-3.5-turbo 모델을 사용하여 사용자의 질문에 답변을 해주는 클래스입니다.
                    chroma를 사용하여 사용자의 질문과 연관된 정보를 제공합니다.
                    ChatMessageHistory를 사용하여 사용자의 질문과 답변을 기록합니다.
 
        Args:
            model_id (str): model id
            api_key (_type_): openai api key
            db_path (str, optional): chroma db path
            behavior_policy (str): systemMessage
        """
       
        self.chat_model = ChatOpenAI(model=model_id, api_key=api_key)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=api_key)
        self.database = Chroma(persist_directory=db_path, embedding_function=self.embeddings)
 
        self.category = category
        self.THRESHOLD = THRESHOLD
       
        self.memory = ChatMessageHistory()
        self.behavior_policy = behavior_policy

        if self.behavior_policy != None:
            self.messages = [
                SystemMessage(self.behavior_policy) 
            ]
       
       
    def chat(self, query):
        sim_docs = self.search(query)
       
        prompt = self.prompting(query, sim_docs)
       
        output = self.chat_model.invoke(prompt).content
       
        self.memory.add_message(HumanMessage(content=query))
        self.memory.add_message(AIMessage(content=output))
       
        return output
   
   
    def search(self, query, k=3):
        sim_docs = self.database.similarity_search_with_score(query, k=k, filter={"category":self.category}) if self.category else self.database.similarity_search_with_score(query, k=k)
       
        return sim_docs
   
    def prompting(self, query, similarity_docs):
        prompt = query
        if similarity_docs:
            num = 1
            for doc, score in similarity_docs:
                if score > self.THRESHOLD:
                    continue
                prompt += f"\n\n 참고자료 {num}: " + doc.page_content
                num += 1
        
        if self.behavior_policy != None:
            prompt = self.messages + [HumanMessage(content=prompt, history=self.memory.messages)]
            
        else:
            prompt = [HumanMessage(content=prompt, history=self.memory.messages)]
       
        return prompt