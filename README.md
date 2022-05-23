# Convert Support

Multiple tool for convert file


## Install requirement

Need to install requirement before using the script
```console
pip install -r requirements.txt
```
See the requirements.txt file to know which module need to be used

## md-to-enex.py

Convert from markdown to Evernote format.

I use vscode foam and obsidian to manage my knowledge. But I have problem when fast access it by phone.
Evernote is good at searching and support multi platform. 
Therefore I convert the md to enex, and import it to Evernote to backup, fast access and searching.
This script use for that.

Time creation will be the time that run script, the author was default as me, you need customize below code before use it.
To filter the exported md, you could filter by setting export_from_date, Then program will only export file that have modified day >=  that date.
``` python
# You may need to change to author to you
author = "Khoan"
# if empty then export all file, if set as format %Y/%m/%d then export file with modified date >= that day
export_from_date = ""
# export_from_date = "2021/08/22"
```
