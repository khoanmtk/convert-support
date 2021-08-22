# Converts md to enex for Evernote importing
# From VS roam or Obsidian to Evernote

import os
import glob
import re
import base64
import pathlib
from datetime import datetime
import markdown

# Data to change before run the tool

# You may need to change to author to you
author = "Khoan"
# if empty then export all file, if set as format %Y/%m/%d then export file >= that day
export_from_date = ""
# export_from_date = "2021/08/22"

def convert_note(file_name, lines):
    create_date = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    updated_date = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    tags = "MarkdownBackup"
    content = ""
    # create markdown object
    md = markdown.Markdown()

    for i,line in enumerate(lines):
        if i == 0:
            title = line
        else:
            match = re.search("(!\[.*\]\()(.*)(\))", line)
            if match:
              paragraphs = handle_for_image(match.group(2))
            else:
              paragraphs = md.convert(line)
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
    write_enex("./Output/", file_name, xml)

# Write file to output folder
def write_enex(output_folder, file_name, output_string):
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    file_output = output_folder + file_name.replace(".md", ".enex")
    with open(file_output, "w", encoding='utf-8') as f:
        f.write(output_string)

# Loop all md file in current folder, convert and write it to /Output/
def convert_file_in_folder():
  for input_file in glob.glob("./*.md"):
    export_flag = True
    if export_from_date != "":
      export_threshold = datetime.strptime(export_from_date, "%Y/%m/%d")
      fname = pathlib.Path(input_file)
      modify_time = datetime.fromtimestamp(fname.stat().st_mtime)
      if modify_time < export_threshold:
        export_flag = False
      
    if export_flag:
      with open(input_file, "r", encoding='utf-8') as f:
          lines = f.readlines()
          convert_note(os.path.basename(input_file), lines)

def handle_for_image(path):
  base64_image_string = ""
  with open(path, "rb") as binary_file:
    base64_encoded_data = base64.b64encode(binary_file.read())
    base64_image_string = base64_encoded_data.decode("utf-8")

  file_type = os.path.splitext(path)[1][1:].strip().lower()
  # png is image/png, gif is image/gif, but jpg is image/jpeg
  # therefore we need to update it in case jpg
  file_type.replace("jpg","jpeg")

  image_string = f'<img src="data:image/{file_type};base64,{base64_image_string}" />\n'
  return image_string

# main call
if __name__ == "__main__":
    convert_file_in_folder()