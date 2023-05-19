from PyPDF2 import PdfReader
import pytesseract
import re
from PIL import Image

file_path = 'DCEO1_-_UE_2.1_-_CC_n1_du_13112019.pdf'

reader = PdfReader(file_path)
text = reader.pages[1].extract_text()
    

def get_question_number(line):
    # Utiliser une expression régulière pour trouver le numéro de question
    match = re.search(r'Q\s*(\d+)', line)
    if match:
        numero_question = match.group(1)
    else:
        numero_question = None
    return numero_question

def get_correct_answer(line):
    match = re.search(r'Q\s*\d+\.\s*([A-Z\s]+)', line)
    if match:
        groupement_lettres = match.group(1).strip().split()[1]
        return groupement_lettres
    else:
        return None