from PyPDF2 import PdfReader
import re
import pandas as pd
import plotly.graph_objects as go
def get_full_text(reader):
    full_text = ""
    for page in reader.pages[3:10]:
        text = page.extract_text()
        full_text += "\n"+text
    return full_text

def init_questions_df(questions):
    reps = ['Q','a','b','c','d','e']
    df = pd.DataFrame(dict.fromkeys(reps,[]))
    for index, question in enumerate(questions):
            df.loc[index,'Q'] = question[0]
    return df

def delete_percent_useless_text(full_text):
    lines = full_text.split("\n")
    new_text = ""
    for index, line in enumerate(lines):
        if(line.startswith("Non réponse") or "DCEO1" in line):
            lines[index] = ""
        # On supprime les lignes commençant par W (vrai) ou U (faux)
        if(line.startswith(('W', 'U'))):
            lines[index] = lines[index][1:]
        ligne_no_percent = re.sub(r'[0-9]*\s*%', '', lines[index-1])
        ligne_no_percent = ligne_no_percent.lstrip()
        new_text += ligne_no_percent + "\n"
        new_text = new_text.replace('\n\n','\n')
    return (new_text)

def add_space_before_q(full_text):
    lines = full_text.split("\n")
    new_text = ""
    for index, line in enumerate(lines):
        if line.startswith("Q"):
            lines[index] = "\n" + lines[index]
        new_text += lines[index] + "\n"
    return new_text
        
def get_questions_blocks(full_text):
    questions = full_text.split("\n\n")[1:]
    for i_q,question in enumerate(questions):
        lines = question.split("\n")
        for i_l,line in enumerate(lines):
            if not line.startswith(('Q','a)','b)','c)','d)','e)')):
                lines[i_l] = lines[i_l-1] + " " + line
                lines[i_l-1] = ""
        questions[i_q] = list(filter(lambda x: x != '', lines))
    questions = list(filter(lambda x: x != [], questions))
    return questions
    
    
def assemble_lines(full_text):
    lines = full_text.split("\n")
    for index, line in enumerate(lines):
        if(index - 1 > 0 and not line.startswith(('Q','a)','b)','c)','d)','e)')) and line != ""):
            lines[index - 1] = lines[index - 1] + " " + line
            pass
        
def init_answers_df(questions, dataframe):
    df = dataframe
    for index, question in enumerate(questions):
        for i_l, letter in enumerate(['a', 'b', 'c', 'd','e']):
            if i_l + 1 < len(question):
                df.loc[index, letter] = question[i_l+1]
    return df
    
        
        
def extract_information(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = get_full_text(reader)
    full_text = delete_percent_useless_text(full_text) 
    full_text = add_space_before_q(full_text)
    questions = get_questions_blocks(full_text)
    df = init_questions_df(questions)
    df = init_answers_df(questions, df)
    print(df)
    with open('sample_b.txt','w') as file:
        file.write(full_text)
    fig = go.Figure(data=[
        go.Table(
        header=dict(values=list(df.columns)),
        cells=dict(values=[df[k].tolist() for k in df.columns])
    )])
    
    return fig