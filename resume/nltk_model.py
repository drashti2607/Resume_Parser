import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError
from distutils import extension
import docx2txt
# import textract
import pandas as pd
import spacy
import re
from nltk.util import ngrams
from nltk.corpus import stopwords

class resumeParser:
    
    def __init__(self, url):
        self.url = url
    
    abc = True
    def get_text(self):
        if self.abc:
            self.extract_text = ""
            for page in extract_page(self.url):
                self.extract_text = self.extract_text + '' + page
            self.abc = False
            # print(self.extract_text)
        return self.extract_text
        
    def get_cleaned_text(self):
    
        self.cleaned_text = cleanResume(self.get_text())
        return self.cleaned_text
    
    def get_cleaned_text_list(self):
        
        self.cleaned_text_list = self.get_cleaned_text().strip().split()
        return self.cleaned_text_list
    
    def get_number(self):
        
        self.number = extract_mobile_number(self.get_text())
        return self.number
    
    def get_email(self):
        
        self.email = extract_email(self.get_text())
        return self.email
    
    def get_skills(self):
        # print(self.get_text())
        self.skills = extract_skills(self.get_text())
        # print(self.skills)
        return self.skills
    
    def get_education(self):
        
        self.education = extract_education(self.get_text(), self.get_cleaned_text_list())
        return self.education
    
    def get_person_info(self):
        self.person_info = {
            "email": self.get_email() ,
            "phone_number": self.get_number(),
            "skills": self.get_skills(),
            "education" : self.get_education() , 
        }   
        return self.person_info


def extract_page(file_path):
        text = ''
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
            
        elif file_path.endswith('.docx'):
            text = extract_text_from_docx(file_path)
            # print(text)
        return text

def extract_text_from_pdf(pdf_path):
    try:
        # Open file
        with open(pdf_path, 'rb') as file:
            
            # Iterate all pages from pdf
            for page in PDFPage.get_pages(file, caching=True):
                # creating a resoure manager
                resource_manager = PDFResourceManager()
                
                # create a file handle
                fake_file_handle = io.StringIO()
                
                # creating a text converter object
                converter = TextConverter(
                                    resource_manager, 
                                    fake_file_handle, 
                                    codec='utf-8', 
                                    laparams=LAParams()              # Set parameter for anaylsis
                            )

                # creating a page interpreter
                page_interpreter = PDFPageInterpreter(
                                    resource_manager, 
                                    converter
                                )

                # process current page
                page_interpreter.process_page(page)
                
                # extract text
                text = fake_file_handle.getvalue()
                yield text

                # close open handles
                converter.close()
                fake_file_handle.close()

    except PDFSyntaxError:
        return " "

def extract_text_from_docx(doc_path):
    try:
        temp = docx2txt.process(doc_path)
        # print(temp)
        text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
        # print(text)
        text = ' '.join(i for i in text)
        return text
    except KeyError:
        return ' '

# def extract_text_from_doc(doc_path):
#     try:
#         temp = textract.process(doc_path).decode('utf-8')
#         text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
#         text = ' '.join(i for i in text)
#         return text
#     except KeyError:
#         return ' '


def cleanResume(resumeText):
    #resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    #resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    #resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    #resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""●!"#$%&'()*+,/:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    #resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText
    
def extract_mobile_number(text):
    # phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    phone = re.findall(re.compile(r'\d{12}|\d{10}'), text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number

def extract_email(email):
    email = re.findall("[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9_-]+", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

# load pre-trained model
nlp = spacy.load('en_core_web_sm')

def extract_skills(resume_text):
    nlp_text = nlp(resume_text)
    # nlp_text = nlp_text.noun_chunks
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    # print(tokens)
    # reading the csv file
    data = pd.read_csv("resume\skills.csv") 
    
    # extract skills from values
    skills = list(data.columns.values)
    skills = [skill.lower().strip() for skill in skills]
    # skills = [skill.replace(" ", "_") for skill in skills]
    # print(skills)
    skillset = []
    
    # check for one-grams (example: python)
    for token in tokens:
        token = re.sub("[^A-Za-z]", "", token.strip())
        if token.lower().strip() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        token = re.sub("[^a-zA-Z\s]", "", token)
        token = str(token)
        # token = token.replace(" ", "_") 
        if token in skills:
            skillset.append(token)
    # print(skillset)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 'B.S.', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 'M.S.',
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]

def extract_education(resume_text, cleaned_text_pdf_list):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|(|)|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index]
    degree = list(edu.keys())
    # print(degree)
    
    education = {}
    for i in range(0, len(degree)):
        degree_index = cleaned_text_pdf_list.index(degree[i])
        # print(degree_index)
        
        for j in range(degree_index, degree_index+30):
            year = None
            # print(cleaned_text_pdf_list[j])
            if(re.findall(r'(((20|19)(\d{2})))', cleaned_text_pdf_list[j])):
                year = cleaned_text_pdf_list[j]
                # print(year)
                education[degree[i]] = year
                break
  
    return education
    