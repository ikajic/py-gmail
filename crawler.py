import imaplib
import email
import os
import sys
import codecs
import config as cf

import numpy as np

def attempt_from_email(adr):
    name = adr[:adr.rfind("@")]
    return name.replace(".", " ").title()

def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        # several payloads (plaintext/html), parse each instance separately
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload(decode=True)
     # one payload
    elif maintype == 'text':
        return email_message_instance.get_payload(decode=True)   

def escape_latex(word):
    CHARS = {
        '&':  '\&',
        '%':  '\%', 
        '$':  '\$', 
        '#':  '\#', 
        '_':  '\_', 
        '{':  '\{', 
        '}':  '\}',
        '~':  '\\textasciitilde{}', 
        '^':  '\^'
    }
    
    for ch, esch in CHARS.items():
        word = word.replace(ch, esch) 
        
    return word

# connect to gmail and select the inbox
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(cf.login, cf.pwd)
mail.select(cf.label)

# obtain emails, use person 1 as a sender
_, tm_id = mail.uid('search', 'charset', '"UTF8"', 'FROM', '"' + cf.mailaddr1 + '"', 'TO', '"' + cf.mailaddr2 + '"')
tm_id_arr = tm_id[0].split(' ')

# and person 2 as a sender  
_, im_id = mail.uid('search', 'charset', '"UTF8"', 'FROM', '"' + cf.mailaddr2 + '"', 'TO', '"' + cf.mailaddr1 + '"')
im_id_arr = im_id[0].split(' ')

mid = np.sort(np.array(tm_id_arr+im_id_arr, dtype='int'))

# no copies of emails
assert len(set(mid))==len(mid)

subjects = []
dates = []

# create a directory to store downloaded mails
if not os.path.exists(cf.mails_dir):
    os.makedirs(cf.mails_dir)

f_ids = open(cf.mails_dir + 'ids', 'w+')
np.savetxt(f_ids, mid, fmt='%d')
f_ids.close()

# either save xor display mails
save_mails = True 
stream = sys.stdout

for mail_id in mid:
    print mail_id
    if save_mails:
        stream = codecs.open(cf.mails_dir + str(mail_id) + '.tex', 'w+', 'utf-8')
        
    # fetch email
    _, raw_email = mail.uid('fetch', int(mail_id), '(RFC822)')
    parsed_email = email.message_from_string(raw_email[0][1])   
  
    # handle sender's name
    from_name, from_email = email.utils.parseaddr(parsed_email['From'])
    from_bytes, from_encoding = email.Header.decode_header(from_name)[0]
    
    # handle recipients, possibly more than 1
    tos = parsed_email.get_all('to', [])
    ccs = parsed_email.get_all('cc', [])
    to_tuples = email.utils.getaddresses(tos+ccs)

    to_names = []

    for person_name, person_mail in to_tuples:
        if person_name == '':
            name = attempt_from_email(person_mail)
        else:
            dec_name = email.Header.decode_header(person_name)               
            name = []
            for name_part, enc in dec_name: 
                name.append(name_part.decode(enc or 'utf-8'))
            name = " ".join(name)
        to_names.append(name)
    
    to_names = ", ".join(to_names)
    
    # resolve encodings in the subject
    subj, enc = email.Header.decode_header(parsed_email['subject'])[0]
    subj = escape_latex(subj)
    
    # reslove encodings in the body
    mail_text = get_first_text_block(parsed_email)
    mail_payload, mail_enc = email.Header.decode_header(mail_text)[0]
        
    # genreate latex code for each email
    stream.write('\section{' + subj.decode(enc or 'utf-8') + '}' + '\n')
    stream.write('\\textbf{DATE: ' + parsed_email['Date'] + '} \\\\' + '\n')
    stream.write('\\textbf{FROM: ' + from_bytes.decode(from_encoding or 'utf-8') + '} \\\\' + '\n')
    stream.write('\\textbf{TO: ' + to_names +  '} \\\\' + '\n \n')  
    stream.write('\\begin{parse lines}[\\noindent]{#1\\\\} \n')   
    
    encodings_all = set(parsed_email.get_charsets())-set([None])
    encoding = list(encodings_all)[0]
    
    mail_txt = mail_payload.decode(encoding)
    mail_txt = escape_latex(mail_txt)
    
    stream.write(mail_txt + '\n')
    stream.write('\end{parse lines} \n')    
        
    if save_mails:
        stream.close()

# generate index-tex file with all mailids, used to generate content table
# here mails split in two files

mail1_tex = open(cf.mails_dir + 'mails_1.tex', 'w+')
mail2_tex = open(cf.mails_dir + 'mails_2.tex', 'w+')

half = int(len(mid)/2.)

for m_id in mid[:half]:
    mail1_tex.write('\include{' + str(m_id) + '}\n')
    
for m_id in mid[half:]:
    mail2_tex.write('\include{' + str(m_id) + '}\n')
    
mail1_tex.close()
mail2_tex.close()



        
