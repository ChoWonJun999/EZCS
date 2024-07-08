class AbuseFilter:
    """
    explanation: A class that filters abusive words from the text

    abusefilepath: str
            path to the file that contains abusive words

    """
    def __init__(self, abuse_file_path="./abuse.txt"):
        self.abuses = []
        with open(abuse_file_path, "r", encoding='UTF-8') as f:
            for line in f:
                self.abuses.append(line.strip())

    def abuse_clean(self, text):
        for abuse in self.abuses:
            text = text.replace(abuse, "*"*len(abuse))
        
        return text


if __name__ == "__main__":
    abuse_filter = AbuseFilter()
    print(abuse_filter.abuse_clean("안녕하세요. 나는 바보입니다."))