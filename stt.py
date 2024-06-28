import requests

class STTModel():
    """
    explanation: STTModel 클래스는 네이버 음성인식 API를 사용하여 음성을 텍스트로 변환하는 클래스입니다.
    
    >>> input data 형식: mp3, aac, ac3, ogg, flac, wav
    
    >>> output data 형식: json({text: 변환된 텍스트})
    """
    
    def __init__(self, client_id, client_secret, lang="Kor"):
        
        """
        client_id: 네이버 음성인식 API의 client_id
        
        client_secret: 네이버 음성인식 API의 client_secret
        
        """
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.lang = lang
        self.url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
        self.headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret,
            "Content-Type": "application/octet-stream"
        }
        self.response = None
        self.rescode = None
        self.text = None
        
    def request(self, data):
        
        '''
        data: 음성 데이터(형식: mp3, aac, ac3, ogg, flac, wav)
        
        '''
        
        self.response = requests.post(self.url,  data=data, headers=self.headers)
        self.rescode = self.response.status_code
        if(self.rescode == 200):
            self.text = self.response.text
        else:
            self.text = "Error : " + self.response.text
        
        return self.text
    
