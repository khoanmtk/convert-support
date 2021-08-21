# Converts md to enex for Evernote importing
# From VS roam or Obsidian to Evernote

import os
import glob
from datetime import datetime

def convert_note(file_name, lines):
    create_date = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    updated_date = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    tags = "MarkdownBackup"
    # You may need to change to author to you
    author = "Khoan"
    content = ""
    for i,line in enumerate(lines):
        if i == 0:
            title = line
        else:
            paragraphs = '<p>' + line + '</p>'
            content = content + paragraphs
    xml_note = f"""
  <note>
    <title>{title}</title>
    <tag>{tags}</tag>
    <created>{create_date}</created>
    <updated>{updated_date}</updated>
    <note-attributes>
      <author>{author}</author>
    </note-attributes>
    <content>
      <![CDATA[<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
        <en-note>
        <div>
        {content}
        </div>
        </en-note>]]>
    </content>
  </note>
    """

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="{create_date}" application="Evernote" version="Evernote Mac 7.14 (458265)">
    {xml_note}
    </en-export>
    """
    write_enex("./Output", file_name, xml)

# Write file to output folder
def write_enex(output_folder, file_name, output_string):
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    file_output = output_folder + file_name.replace(".md", ".enex")
    with open(file_output, "w") as f:
        f.write(output_string)

# Loop all md file in current folder, convert and write it to /Output/
def convert_file_in_folder():
  for input_file in glob.glob("./*.md"):
    with open(input_file, "r") as f:
        lines = f.readlines()
        convert_note(os.path.basename(input_file), lines)

# main call
if __name__ == "__main__":
    convert_file_in_folder()