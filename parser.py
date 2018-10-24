import requests
import os 
import subprocess
import nltk
from nltk.tokenize import sent_tokenize

url = 'https://www.supremecourt.gov/opinions/09pdf/08-205.pdf'

r = requests.get(url)

file_name = os.path.splitext(os.path.basename(url))[0]

pdf_destination = os.path.join('pdfs/',file_name + '.pdf')
txt_destination = os.path.join('text-outputs/',file_name + '.txt')


with open(pdf_destination, 'wb') as f:
    f.write(r.content)

subprocess.call(['pdftotext', pdf_destination, txt_destination])


with open(txt_destination, 'r') as f:
    opinion_text = f.read()


full_text = opinion_text.replace('\n',' ')

class SCOTUSOpinion:
    
    def __init__(self, path_to_opinion_txt):
        self.filepath = path_to_opinion_txt
        self.filename = os.path.splitext(os.path.basename(path_to_opinion_txt))[0]

        try:
            with open(self.filepath, 'r') as f:
                self.text = f.read()
        except IOError:
            raise IOError("{} not found".format(self.filename))


sents = sent_tokenize(full_text)

ref_sents = [x for x in sents if x.startswith('See')]

sents = [x for x in sents if x not in ref_sents]

short_sents = [x for x in sents if len(x) < 4]

sents = [x for x in sents if x not in short_sents]

remove_too_much = [x for x in sents if x.startswith(chr(167))]

sents = [x for x in sents if x not in remove_too_much]
