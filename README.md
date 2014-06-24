py-gmail
========

A python script that fetches emails from the gmail account and wraps them with a latex code that can be used in various documents


The `crawler.py` reads the user-specific data from the `config.py` (not included here, you should create your own). It uses imap to connect to the gmail inbox and fetches the email communication between the email address 1 and the email address 2 (also specified in the `config.py`). 

For each email, a `.tex` file is generated with a latex-header (from, to, date, subject) and the email body text. The .tex file is named after the UID of the email. For example, the body of an email with the UID 123 will be storead as `123.tex`. Tex mails are stored in a directory specified by the config file, which is newly created unless it already exists. The script also generates a tex file which has an include command for every email in the corresponding directory.
So, if your inbox contains 3 emails with UIDs 1, 2 and 3, at the end of execution of the script you'll have:
'''
1.tex
2.tex
3.tex
mails.tex
'''

`1.tex` might look like:
```
\section{Drinks}
\textbf{DATE: Tue, 17 Sep 2013 21:32:22 +0200 (CEST)} \\
\textbf{FROM: Bob} \\
\textbf{TO: Alice} \\
 
\begin{parse lines}[\noindent]{#1\\} 
Hi Alice,

up for the drinks tonight?

Bye
Bob

\end{parse lines} 

```

Where mails.tex will look like:
'''
\include{1}
\include{2}
\include{3}
'''


`mails.tex` can be used in latex documents such as article, book etc to generate a nicely organized manuscript. The `parse lines` environment takes care of the proper formatting of the text.

