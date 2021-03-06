import requests
import os 
import subprocess
import nltk
from io import BytesIO
import re
import time
import tempfile
import webbrowser
from nltk.tokenize import sent_tokenize

url = 'https://www.supremecourt.gov/opinions/09pdf/08-205.pdf'

##soft_hyphen = chr(173)

# continue playing with this for cleaner case name
m = re.search(r'(?<=205\n_{17}\n).+\n?.+(?=\n\n)',a.text)
m.group(0)
# doesn't work for 'https://www.supremecourt.gov/opinions/17pdf/15-1204_f29g.pdf'
# and be sure to clean file names before inferring things!


class SCOTUSOpinion:
    
    def __init__(self, path_to_opinion_txt):
        self.url = path_to_opinion_txt
        self.filename = os.path.splitext(os.path.basename(self.url))[0]

        r = requests.get(self.url, stream=True)
        pdf_binary = BytesIO(r.content)

        pdf_binary.seek(0)
        
        
        fd, path = tempfile.mkstemp(suffix='.pdf')
        
        try:
            with os.fdopen(fd, 'wb') as tmp:

                tmp.write(pdf_binary.read())

            self.download(path)
        finally:
            os.remove(path)

        self.case_name = re.findall('UNITED STATES\n+Syllabus\n.+v.+\n',self.text)[0][:-1].split('\n')[-1]

    def download(self, pdf_destination):
        lines = []
        proc = subprocess.Popen(['pdftotext', pdf_destination, '-'], stdout=subprocess.PIPE)
        while True:
          line = proc.stdout.readline()
          if line != b'':
            lines.append(line.rstrip().decode("ISO-8859-1"))
          else:
            break

        self.text = '\n'.join(lines)

    def open_opinion(self):
        webbrowser.open(self.url)


    def syllabus(self):
        pass

a = SCOTUSOpinion(url)

##a = SCOTUSOpinion(url)

##sents = sent_tokenize(full_text)
##
##ref_sents = [x for x in sents if x.startswith('See')]
##
##sents = [x for x in sents if x not in ref_sents]
##
##short_sents = [x for x in sents if len(x) < 4]
##
##sents = [x for x in sents if x not in short_sents]
##
##remove_too_much = [x for x in sents if x.startswith(chr(167))]
##
##sents = [x for x in sents if x not in remove_too_much]
