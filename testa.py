from PyPDF2 import PdfReader

def extract_information(pdf_path):
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text = page.extract_text()
        print(text)
        # lines = text.splitlines()
        # for index, line in enumerate(lines):
        #     if line.startswith("Question") and line.endswith(('1','2','3','4','5','6','7','8','9','10')):
        #         print(line)
        #     if line in ['A','B','C','D','E']:
        #         print(line)
        #         if lines[index+4] == "(+1)":
        #             print(lines[index+5])
        #         else:
        #             print(lines[index+4])
if __name__ == '__main__':
    path = 'a.pdf'
    extract_information(path)