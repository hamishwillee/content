#! /usr/bin/python
"""
This finds links of format /en-US/docs/Learn/HTML/Multimedia_and_embedding/Video_and_audio_content
strips the front bit and converts to lower case.
it is a tool to allow htmlproofer to be run.

"""

import re
import os # for walk
import sys
import codecs

dir_name='./files/en-us/'
exclude_list=["node_modules", "_book", "build_scripts", "zh", "ko", "kr", "ja", "ru", "tr"]

print("running")
#file_set=set()

def fixuplinks(input_text):
    print(' fix up links')
    def fixfoundlinks(matchobj):
        print('XXXXMatchobj:X%sX' % matchobj.group(0))
        fixed_up_link=matchobj.group(1).split("#")
        fixed_up_link[0]=fixed_up_link[0].lower()
        fixed_up_link="#".join(fixed_up_link)
        print('reduced:X%sX' % fixed_up_link)
        return fixed_up_link
    input_text=re.sub(r'"/en-US/docs(.*?)"', fixfoundlinks, input_text)
    return input_text

for subdir, dirs, files in os.walk(dir_name):
    #print(subdir)
    # Skip any folders in the exclude_list  
    try:
        stripped_subdir=subdir.split("\\")[1]
        if stripped_subdir in exclude_list:
            print("excluded: %s" % stripped_subdir)
            continue
    except:
        pass
        

    for file in files:
        if file[-5:]!=".html":
            print("excluded: %s" % file)
            continue

        full_file=subdir+'\\'+file
        print("files: %s" % full_file)
        contents=''
        with codecs.open(full_file, "a+", encoding='utf-8') as content_file:

            try:
                contents=content_file.read()
                #print(contents)
                contents=fixuplinks(contents)
                #print(contents)
                
                content_file.write(contents)
                
            except UnicodeDecodeError:
                print('Error read: %s' % full_file)
            except:
                print("Unexpected error:", sys.exc_info()[0])
                pass
                





        
print("COMPLETED")
#print(images_fs_but_not_text)

