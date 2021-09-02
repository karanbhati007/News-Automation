# Text Summarization using NLP

import bs4 as bs
import requests
import re
import nltk
nltk.download('stopwords')
import heapq
from newspaper import Article


def summarizeText(newsUrl,newsDescp,itr):
    print('News Link :: '+ newsUrl)
    summarized_text=""
    try:
        """
        # Gettings the data source
        agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

        source = requests.get(newsUrl,headers = agent)
        # Parsing the data/ creating BeautifulSoup object
        soup = bs.BeautifulSoup(source.text,'html.parser')

        # Fetching the data
        text = ""
        # for paragraph in soup.find_all('p'):
        #     text += paragraph.text
        text = soup.text
        """
        article = Article(newsUrl)
        article.download()
        article.parse()

        text = article.text


        # Clear Unwanted Symbols
        text = re.sub(r'\[[0-9]*\]',' ',text)
        text = re.sub(r'\s+',' ',text)
        clean_text = text.lower()
        clean_text = re.sub(r'\W',' ',clean_text)
        clean_text = re.sub(r'\d',' ',clean_text)
        clean_text = re.sub(r'\s+',' ',clean_text)

        # Tokenize sentences
        sentences = nltk.sent_tokenize(text)

        stop_words = nltk.corpus.stopwords.words('english')

    
        word2count = {}
        for word in nltk.word_tokenize(clean_text):
            if word not in stop_words:
                if word not in word2count.keys():
                    word2count[word] = 0
                
                word2count[word] += 1

        max_count = max(word2count.values())
        for key in word2count.keys():
            word2count[key] = word2count[key]/max_count
            
    
        sent2score = {}
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence.lower()):
                if word in word2count.keys():
                    if len(sentence.split(' ')) < 35:
                        if sentence not in sent2score.keys():
                            sent2score[sentence] = 0
                        
                        sent2score[sentence] += word2count[word]
                            
        # Gettings best 2 lines             
        best_sentences = heapq.nlargest(2, sent2score, key=sent2score.get)
        
        for sentence in best_sentences:
            summarized_text+=sentence

        
    except Exception as e:
        print(str(e))
        print('ERROR !!')
        # If any error occured then use news summary given by API
        if summarized_text=="":
            summarized_text = newsDescp[itr]

    print('Summary : ' + summarized_text)

    return summarized_text



if __name__ == '__main__':
    summarizeText(newsUrl="",newsDescp=[],itr=0)