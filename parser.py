import requests
import PyPDF2
from io import BytesIO
import nltk
from nltk.tokenize import sent_tokenize

url = 'https://www.cadc.uscourts.gov/internet/opinions.nsf/3AF8B4D938CDEEA685257C6000532062/$file/11-1355-1474943.pdf'
r = requests.get(url)

full_text = ''

with BytesIO(r.content) as pdf_file:
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    for p in read_pdf.pages:
        full_text += p.extractText()


full_text = full_text.replace('\n',' ')

sents = sent_tokenize(full_text)

ref_sents = [x for x in sents if x.startswith('See')]

sents = [x for x in sents if x not in ref_sents]

short_sents = [x for x in sents if len(x) < 4]

sents = [x for x in sents if x not in short_sents]

[x for x in sents if x.startswith(chr(167))]
