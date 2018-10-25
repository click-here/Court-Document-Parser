import requests
import os 
import subprocess
import nltk
from io import BytesIO
import re
import time
import tempfile
from nltk.tokenize import sent_tokenize

url = 'https://www.supremecourt.gov/opinions/09pdf/08-205.pdf'

r = requests.get(url)

file_name = os.path.splitext(os.path.basename(url))[0]

pdf_destination = os.path.join('pdfs/',file_name + '.pdf')
txt_destination = os.path.join('text-outputs/',file_name + '.txt')


with open(pdf_destination, 'wb') as f:
    f.write(r.content)

##subprocess.call(['pdftotext', pdf_destination, txt_destination])

subprocess.call(['pdftotext', pdf_destination, txt_destination], stdout=subprocess.PIPE)


with open(txt_destination, 'r') as f:
    opinion_text = f.read()


full_text = opinion_text.replace('\n',' ')

class SCOTUSOpinion:
    
    def __init__(self, path_to_opinion_txt, url = url):
        self.url = url
        self.filename = os.path.splitext(os.path.basename(self.url))[0]

        r = requests.get(self.url, stream=True)
        self.t = BytesIO(r.content)

        self.t.seek(0)

        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'wb') as tmp:

                tmp.write(self.t.read())
                print(path)
                self.download(path)
        finally:
            os.remove(path)

        self.case_name = re.findall('UNITED STATES\n+Syllabus\n.+v.+\n',self.text)[0][:-1].split('\n')[-1]

    def download(self, pdf_destination):
        self.lines = []
        proc = subprocess.Popen(['pdftotext', pdf_destination, '-'], stdout=subprocess.PIPE)
        while True:
          line = proc.stdout.readline()
          if line != b'':
            self.lines.append(line.rstrip().decode("ISO-8859-1"))
          else:
            break

        self.text = '\n'.join(self.lines)
        
a = SCOTUSOpinion(url)

sents = sent_tokenize(full_text)

ref_sents = [x for x in sents if x.startswith('See')]

sents = [x for x in sents if x not in ref_sents]

short_sents = [x for x in sents if len(x) < 4]

sents = [x for x in sents if x not in short_sents]

remove_too_much = [x for x in sents if x.startswith(chr(167))]

sents = [x for x in sents if x not in remove_too_much]
