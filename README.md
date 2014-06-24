py-gmail
========

A python script that fetches emails from an GMail account and wraps them with a latex code that can be used to make a booklet


The `crawler.py` reads user-specific data from the `config.py` (not included here, you should create your own). It uses imap to connect to the GMail inbox and fetches the email communication between the email address 1 and the email address 2 (also specified in the `config.py`). 

For each email, a `.tex` file is generated with a latex-header (from, to, date, subject) and the email body text. The `.tex` file is named after a unique identifier (UID) of the email that doesn't change over time. For example, the body of the email with the UID 123 will be storead as `123.tex`. Tex mails are stored in a directory specified by the config file, which is newly created if it doesn't exist. The script also generates a `mails.tex` with a list of includes for every email in the corresponding directory.

So, if your inbox contains three emails with UIDs 1, 2 and 3, at the end of execution of the script you'll have:
```
1.tex
2.tex
3.tex
mails.tex
```

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

Where `mails.tex` will look like:
```
\include{1}
\include{2}
\include{3}
```


`mails.tex` can be used in latex documents such as article, book etc to generate a nicely organized document with a table of contents etc. The [parse lines](http://www.ctan.org/tex-archive/macros/latex/contrib/parselines) environment takes care of the proper formatting of the text. I used my [Master's thesis template](https://github.com/ikajic/uni-templates/tree/master/thesis/masterthesis) to create a book-like manuscript and [PDFBooklet](http://pdfbooklet.sourceforge.net/) to obtain proper page ordering for printing.


### config.py

The script takes user-specific data, such as the username and password from the config.py, which is for obvious reasons not included here. It contains:

```
login = 'your-gmail-username'
pwd = 'your-gmail-pass'

label = 'Inbox'
mails_dir = "./mails/"

mailaddr1 = "alice@mail.com"
mailaddr2 = "bob@gmail.com"
```


