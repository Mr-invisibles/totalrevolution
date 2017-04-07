﻿# -*- coding: utf-8 -*-

# script.module.python.koding.aio
# Python Koding AIO (c) by whufclee (info@totalrevolution.tv)

# Python Koding AIO is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.

# You should have received a copy of the license along with this
# work. If not, see http://creativecommons.org/licenses/by-nc-nd/4.0.

# IMPORTANT: If you choose to use the special noobsandnerds features which hook into their server
# please make sure you give approptiate credit in your add-on description (noobsandnerds.com)
# 
# Please make sure you've read and understood the license, this code can NOT be used commercially
# and it can NOT be modified and redistributed. Thank you.

import os
import shutil
import sys
import xbmc
import xbmcgui

# from __init__ import dolog
from systemtools import Last_Error

dp       = xbmcgui.DialogProgress()
dialog   = xbmcgui.Dialog()
HOME     = xbmc.translatePath('special://home')
PROFILE  = xbmc.translatePath('special://profile')
DATABASE = os.path.join(PROFILE,'Database')
#----------------------------------------------------------------    
# TUTORIAL #
def Archive_Tree(sourcefile, destfile, exclude_dirs=['temp'], exclude_files=['kodi.log','kodi.old.log','xbmc.log','xbmc.old.log','spmc.log','spmc.old.log'], message_header = 'ARCHIVING', message = 'Creating archive'):
    """
Archive a folder path including all sub-folders.
Optional exclude_dirs and exclude_files lists can be sent through and these will be skipped

IMPORTANT: There is a known bug where some certain compressed tar.gz files
can cause the system to hang and a bad zipfile will continue to be made until
it runs out of space on your storage device. In the unlikely event you encounter
this issue just add the file(s) to your exclude list.

CODE: Archive_Tree(sourcefile, destfile, [exclude_dirs, exclude_files, message_header, message]):

AVAILABLE PARAMS:

    (*) sourcefile   - This is the source folder of where you want to start the archive process

    (*) destfile     - This is the file path you want to save the archive as (don't forget to
    add the actual filename at end of path)

    exclude_dirs   - This is optional, if you have folder names you want to exclude just
    add them here as a list item

    exclude_files  - This is optional, if you have specific file names you want to
    exclude just add them here as a list item

    message_header - This is optional, you can give the dialog progress window a title.
    The default is "ARCHIVING"

    message        - This is optional, the default text in the dialog progress window
    will be "Creating archive" unless changed here.

EXAMPLE CODE:
HOME = xbmc.translatePath('special://home')
DST = os.path.join(HOME,'test.zip')
koding.Archive_Tree(HOME, DST)
~"""
    import zipfile
    import time
    import xbmcaddon
    xbmc.log('ARCHIVE IN PROGRESS',2)
    module_id        =  'script.module.python.koding.aio'
    this_module      =  xbmcaddon.Addon(id=module_id)
    folder_size      =  Folder_Size(sourcefile,'mb')
    available_space  =  Free_Space(HOME,'mb')
    if os.path.exists(sourcefile):
        choice = True
        if float(available_space) < float(folder_size):
            choice = dialog.yesno(this_module.getLocalizedString(30809), this_module.getLocalizedString(30810), this_module.getLocalizedString(30811) % folder_size, this_module.getLocalizedString(30812) % available_space, yeslabel = this_module.getLocalizedString(30813), nolabel = this_module.getLocalizedString(30814))
        if choice:
            zipobj       = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
            rootlen      = len(sourcefile)
            for_progress = []
            contents     = []
            
            dp.create(message_header, message)

            for base, dirs, files in os.walk(sourcefile):
                for file in files:
                    contents.append(file)
            total_items =len(contents)
            xbmc.log(str(contents),2)
            
            for base, dirs, files in os.walk(sourcefile):
                dirs[:] = [d for d in dirs if d not in exclude_dirs]
                files[:] = [f for f in files if f not in exclude_files and not 'crashlog' in f and not 'stacktrace' in f]
                
                for file in files:
                    try:
                        for_progress.append(file) 
                        progress = len(for_progress) / float(total_items) * 100  
                        dp.update(0,"Backing Up",'[COLOR yellow]%s[/COLOR]'%d, 'Please Wait')
                        file_path = os.path.join(base, file)
                    except:
                        pass
                    try:
                        timestamp_1980 = 315532800
                        file_date = os.path.getmtime(file_path)                    
                        if file_date < timestamp_1980:
                            xbmc.log('OLD File date: %s'%file_date, 2)
                            os.utime(file_path,(315536400, 315536400))
                        zipobj.write(file_path, file_path[rootlen:])  
                    except:
                        xbmc.log('Failed to backup: %s'%file_path, 2)

                    if dp.iscanceled():
                        sys.exit()
            zipobj.close()
            dp.close()
    else:
        dialog.ok(this_module.getLocalizedString(30965),this_module.getLocalizedString(30815) % sourcefile)
#----------------------------------------------------------------    
# TUTORIAL #
def Convert_Special(filepath=xbmc.translatePath('special://home')):
    """
Convert physcial paths stored in text files to their special:// equivalent.

CODE: Convert_Special([filepath])

AVAILABLE PARAMS:

    filepath  -  This is the path you want to scan, by default it's set to the Kodi HOME directory.

EXAMPLE CODE:
koding.Convert_Special()
~"""    
    import urllib

    for root, dirs, files in os.walk(filepath):
        
        for file in files:
            
            if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies") or file.endswith(".ini"):
                contents     = Text_File(os.path.join(root,file), 'r')
                encodedpath  = urllib.quote(HOME)
                encodedpath2 = encodedpath.replace('%3A','%3a').replace('%5C','%5c')
                newfile = contents.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(encodedpath2, 'special://home/')
                Text_File(os.path.join(root, file), 'w', newfile)
#----------------------------------------------------------------    
# TUTORIAL #
def Create_Paths(path):
    """
Send through a path to a file, if the directories required do not exist this will create them.

CODE: Create_Paths(path)

AVAILABLE PARAMS:

    (*) path  -  This is the full path including the filename. The path
    sent through will be split up at every instance of '/' so if you
    only want to send through a directory you MUST include a trailing '/'

EXAMPLE CODE:
my_path = xbmc.translatePath('special://home/test/testing/readme.txt')
koding.Create_Paths(path=my_path)
dialog.ok('PATH CREATED','Check in your Kodi home folder and you should now have sub-folders of /test/testing/.','[COLOR=gold]Press ok to remove these folders.[/COLOR]')
shutil.rmtree(xbmc.translatePath('special://home/test'))
~"""
    newdirs = []
    directories = path.split('/')
    directories.pop()

# Remove any blanks in the array (eg /storage on linux creates a blank entry at start of array)
    if directories[0] == '':
        directories[1] = '/'+directories[1]
    for item in directories:
        if item != '':
            newdirs.append(item)

    rootpath = HOME
    for d in newdirs:
        rootpath = os.path.join(rootpath, d)
        if not os.path.exists(rootpath):
            try:
                os.makedirs(rootpath)
            except:
                pass
#----------------------------------------------------------------    
# TUTORIAL #
def DB_Path_Check(db_path):
    """
If you need to find out the current "real" database in use then this is the function for you.
It will scan for a specific database type (e.g. addons) and return the path to the one which was last updated.
This is particularly useful if the system has previously updated to a newer version rather than a fresh install
or if they've installed a "build" which contained old databases.

CODE: DB_Path_Check(db_path)

AVAILABLE VALUES:

    (*) db_path  -  This is the string the database starts with.
    If you want to find the path for the addons*.db you would use "addons"
    as the value, if you wanted to find the path of the MyVideos*.db you would use
    "myvideos" etc. - it is not case sensitive.

EXAMPLE CODE:
dbpath = koding.DB_Path_Check(db_path='addons')
dialog.ok('ADDONS DB','The path to the current addons database is:',dbpath)
~"""
    finalfile = 0
    databasepath = os.listdir(DATABASE)
    for item in databasepath:
        if item.lower().endswith('.db') and item.lower().startswith(db_path.lower()):
            mydb         = os.path.join(DATABASE,item)
            lastmodified = os.path.getmtime(mydb)
            if lastmodified>finalfile:
                finalfile = lastmodified
                gooddb   = mydb
    return gooddb
#----------------------------------------------------------------
# TUTORIAL #
def Delete_Files(filepath = HOME, filetype = '*.txt', subdirectories=False):
    """
Delete all specific filetypes in a path (including sub-directories)

CODE: Delete_Files([filepath, filetype, subdirectories])

AVAILABLE PARAMS:
    
    (*) filepath  -  By default this points to the Kodi HOME folder (special://home).
    The path you send through must be a physical path and not special://

    (*) filetype  -  The type of files you want to delete, by default it's set to *.txt

    subdirectories  -  By default it will only search the folder given, if set to True
    all filetypes listed above will be deleted in the sub-directories too.

WARNING: This is an extremely powerful and dangerous tool! If you wipe your whole system
by putting in the wrong path then it's your own stupid fault!

EXAMPLE CODE:
delete_path = xbmc.translatePath('special://profile/addon_data/test')
dialog.ok('DELETE FILES','All *.txt files will be deleted from:', '', '/userdata/addon_data/test/')
koding.Delete_Files(filepath=delete_path, filetype='.txt', subdirectories=True)
~"""    
    if filepath == '/' or filepath == '.' or filepath == '' or (filepath[1]==':' and len(filepath)<4):
        dialog.ok('IDTenT ERROR!!!','You are trying to wipe your whole system!!!','Be more careful in future, not everyone puts checks like this in their code!')
        return

    if os.path.exists(filepath):
        filetype = filetype.replace('*','')

        if subdirectories:
            for parent, dirnames, filenames in os.walk(filepath):
                for fn in filenames:
                    if fn.lower().endswith(filetype):
                        os.remove(os.path.join(parent, fn))

        else:
            for delete_file in os.listdir(filepath):
                delete_path = os.path.join(filepath,delete_file)
                if delete_path.endswith(filetype):
                    try:
                        os.remove(delete_path)
                    except:
                        kodi.log(Last_Error())
    else:
        xbmc.log('### Cannot delete files as directory does not exist: %s' % filepath)
#----------------------------------------------------------------
# TUTORIAL #
def Delete_Folders(filepath=''):
    """
Completely delete a folder and all it's sub-folders

CODE: Delete_Folders(filepath)

AVAILABLE PARAMS:
    
    (*) filepath  -  Use the physical path you want to remove (not special://)

WARNING: This is an extremely powerful and dangerous tool! If you wipe your whole system
by putting in the wrong path then it's your own stupid fault!

EXAMPLE CODE:
delete_path = xbmc.translatePath('special://profile/addon_data/test')
if dialog.yesno('DELETE FOLDER','The following folder will now be removed:', '/userdata/addon_data/test/','Do you want to continue?'):
    koding.Delete_Folders(delete_path)
~"""
    if os.path.exists(filepath) and filepath != '':
        shutil.rmtree(filepath, ignore_errors=True)
        xbmc.executebuiltin('Container.Refresh')
#----------------------------------------------------------------
# TUTORIAL #
def Dummy_File(dst= xbmc.translatePath('special://home/dummy.txt'), size='10', size_format='mb'):
    """
Create a dummy file in whatever location you want and with the size you want.
Use very carefully, this is designed for testing purposes only. Accidental
useage can result in the devices storage becoming completely full in just a
few seconds. If using a cheap poor quality device (like many android units)
then you could even end up killing the device as some of them are made
with very poor components which are liable to irreversable corruption.

CODE: koding.Dummy_File(dest, [size, size_format])

AVAILABLE PARAMS:

    dst          - This is the destination folder, make sure it's a physical path and not
    "special://...". This needs to be a FULL path including the file extension. By default
    this is set to special://home/dummy.txt

    size         -  This is an optional integer, by default a file of 10 MB will be created.

    size_format  -  By default this is set to 'mb' (megabytes) but you can change this to
    'b' (bytes), 'kb' (kilobytes), 'gb' (gigabytes)

EXAMPLE CODE:
dummy = xbmc.translatePath('special://home/test_dummy.txt')
koding.Dummy_File(dst=dummy, size=100, size_format='b')
dialog.ok('DUMMY FILE CREATED','Check your Kodi home folder and you should see a 100 byte test_dummy.txt file.','[COLOR=gold]Press OK to delete this file.[/COLOR]')
os.remove(dummy)
~"""
    if size_format == 'kb':
        size = float(size*1024)
    elif size_format == 'mb':
        size = float(size*1024) * 1024
    elif size_format == 'gb':
        size = float(size*1024) * 1024 * 1024

    xbmc.log('format: %s  size: %s'%(size_format, size), 2)

    f = open(dst,"wb")
    f.seek(size-1)
    f.write("\0")
    f.close()
#----------------------------------------------------------------
# TUTORIAL #
def Extract(_in, _out, dp=None):
    """
This function will extract a zip or tar file and return true or false so unlike the
builtin xbmc function "Extract" this one will pause code until it's completed the action.

CODE: koding.Extract(src,dst,[dp])
dp is optional, by default it is set to false

AVAILABLE PARAMS:

    (*) src    - This is the source file, the actual zip/tar. Make sure this is a full path to
    your zip file and also make sure you're not using "special://". This extract function
    is only compatible with .zip/.tar/.tar.gz files

    (*) dst    - This is the destination folder, make sure it's a physical path and not
    "special://...". This needs to be a FULL path, if you want it to extract to the same
    location as where the zip is located you still have to enter the full path.

    dp - This is optional, if you pass through the dp function as a DialogProgress()
    then you'll get to see the status of the extraction process. If you choose not to add
    this paramater then you'll just get a busy spinning circle icon until it's completed.
    See the example below for a dp example.

EXAMPLE CODE:
dp = xbmcgui.DialogProgress()
dp.create('Extracting Zip','Please Wait')
if koding.Extract(src,dst,dp):
    dialog.ok('YAY IT WORKED!','Successful extraction complete')
else:
    dialog.ok('BAD NEWS!','UH OH SOMETHING WENT HORRIBLY WRONG')
~"""
    import zipfile
    import tarfile

    nFiles = 0
    count  = 0

    if os.path.exists(_in):
        if zipfile.is_zipfile(_in):
            zin      = zipfile.ZipFile(_in,  'r')
            nFiles   = float(len(zin.infolist()))
            contents = zin.infolist()

        elif tarfile.is_tarfile(_in):
            zin      = tarfile.open(_in)
            contents = [tarinfo for tarinfo in zin.getmembers()]
            nFiles   = float(len(contents))
       
        if nFiles > 0:
            if dp:
                try:
                    for item in contents:
                        count += 1
                        update = count / nFiles * 100
                        dp.update(int(update))
                        zin.extract(item, _out)
                    zin.close()
                    return True

                except:
                    xbmc.log(Last_Error())
                    return False
            else:
                try:
                    zin.extractall(_out)
                    return True
                except:
                    xbmc.log(Last_Error())
                    return False
        
        else:
            xbmc.log('NOT A VALID ZIP OR TAR FILE: %s' % _in)
    else:
        dialog.ok(this_module.getLocalizedString(30965),this_module.getLocalizedString(30815) % _in)

#----------------------------------------------------------------
# TUTORIAL #
def Find_In_Text(content, start, end, show_errors = True):
    """
Regex through some text and return a list of matches.
Please note this will return a LIST so even if only one item is found
you will still need to access it as a list, see example below.

CODE: koding.Find_In_Text(content, start, end, [show_errors])

AVAILABLE PARAMS:
    
    (*) content  -  This is the string to search

    (*) start    -  The start search string

    (*) end      -  The end search string

    show_errors  -  Default is True, the code will show help dialogs for bad code.
    Set to False if you want to hide these messages

EXAMPLE CODE:
textsearch = 'This is some text so lets have a look and see if we can find the words "lets have a look"'
search_result = koding.Find_In_Text(textsearch, 'text so ', ' and see')
dialog.ok('SEARCH RESULT','You searched for the start string of "text so " and the end string of " and see". Your result is: %s' % search_result[0])

# Please note: we know for a fact there is only one result which is why we're only accessing list item zero.
# If we were expecting more than one return we would probably do something more useful and loop through in a for loop.
~"""
    import re
    if content == None or content.startswith('This url could not be opened'):
        if show_errors:
            dialog.ok('ERROR WITH REGEX','No content sent through - there\'s nothing to scrape. Please check the website address is still active (details at bottom of log).')
            xbmc.log(content)
        return
    if end != '':
        links = re.findall('%s([\s\S]*?)%s' % (start, end), content)
    if len(links)>0:
        return links
    else:
        if show_errors:
            xbmc.log(content)
            dialog.ok('ERROR WITH REGEX','Please check your regex, there was content sent through to search but there are no matches for the regex supplied. The raw content has now been printed to the log')
        return None
#----------------------------------------------------------------
# TUTORIAL #
def Free_Space(dirname = HOME, filesize = 'b'):
    """
Show the amount of available free space in a path, this can be returned in a number of different formats.

CODE: Free_Space([dirname, filesize])

AVAILABLE PARAMS:

    dirname  - This optional, by default it will tell you how much space is available in your special://home
    folder. If you require information for another path (such as a different partition or storage device)
    then enter the physical path. This currently only works for local paths and not networked drives.

    filesize - By default you'll get a return of total bytes, however you can get the value as bytes,
    kilobytes, megabytes, gigabytes and terabytes..

        VALUES:
        'b'  = bytes (integer)
        'kb' = kilobytes (float to 1 decimal place)
        'mb' = kilobytes (float to 2 decimal places)
        'gb' = kilobytes (float to 3 decimal places)
        'tb' = terabytes (float to 4 decimal places)

EXAMPLE CODE:
HOME = xbmc.translatePath('special://home')
my_space = koding.Free_Space(HOME, 'gb')
dialog.ok('Free Space','Available space in HOME: %s GB' % my_space)
~"""
    import ctypes
    filesize = filesize.lower()
    if xbmc.getCondVisibility('system.platform.windows'):
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        finalsize = free_bytes.value
    else:
        st = os.statvfs(dirname)
        finalsize =  st.f_bavail * st.f_frsize
    if filesize == 'b':
        return finalsize
    elif filesize == 'kb':
        return "%.1f" % (float(finalsize / 1024))
    elif filesize == 'mb':
        return "%.2f" % (float(finalsize / 1024) / 1024)
    elif filesize == 'gb':
        return "%.3f" % (float(finalsize / 1024) / 1024 / 1024)
    elif filesize == 'tb':
        return "%.4f" % (float(finalsize / 1024) / 1024 / 1024 / 1024)
#----------------------------------------------------------------
# TUTORIAL #
def Folder_Size(dirname = HOME, filesize = 'b'):
    """
Return the size of a folder path including sub-directories,
this can be returned in a number of different formats.

CODE: koding.Folder_Size([dirname, filesize])

AVAILABLE PARAMS:

    dirname  - This optional, by default it will tell you how much space is available in your
    special://home folder. If you require information for another path (such as a different
    partition or storage device) then enter the physical path. This currently only works for
    local paths and not networked drives.

    filesize - By default you'll get a return of total bytes, however you can get the value as
    bytes, kilobytes, megabytes, gigabytes and terabytes..

        VALUES:
        'b'  = bytes (integer)
        'kb' = kilobytes (float to 1 decimal place)
        'mb' = kilobytes (float to 2 decimal places)
        'gb' = kilobytes (float to 3 decimal places)
        'tb' = terabytes (float to 4 decimal places)

EXAMPLE CODE:
HOME = xbmc.translatePath('special://home')
home_size = Folder_Size(HOME, 'mb')
dialog.ok('Folder Size','KODI HOME: %s MB' % home_size)
~"""
    finalsize = 0
    for dirpath, dirnames, filenames in os.walk(dirname):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            finalsize += os.path.getsize(fp)
    if filesize == 'b':
        return finalsize
    elif filesize == 'kb':
        return "%.1f" % (float(finalsize / 1024))
    elif filesize == 'mb':
        return "%.2f" % (float(finalsize / 1024) / 1024)
    elif filesize == 'gb':
        return "%.3f" % (float(finalsize / 1024) / 1024 / 1024)
    elif filesize == 'tb':
        return "%.4f" % (float(finalsize / 1024) / 1024 / 1024 / 1024)
#----------------------------------------------------------------
# TUTORIAL #
def Move_Tree(src, dst, dp=None):
    """
Move a directory including all sub-directories to a new location.
This will automatically create the new location if it doesn't already
exist and it wierwrite any existing entries if they exist.

CODE: koding.Move_Tree(src, dst)

AVAILABLE PARAMS:

    (*) src  -  This is source directory that you want to copy

    (*) dst  -  This is the destination location you want to copy a directory to.

    dp - This is optional, if you pass through the dp function as a DialogProgress()
    then you'll get to see the status of the move process. See the example below for a dp example.

EXAMPLE CODE:
dp = xbmcgui.DialogProgress()
source = xbmc.translatePath('special://profile/move_test')

# Lets create a 500MB dummy file so we can move and see dialog progress
dummy = os.path.join(source,'dummy')
if not os.path.exists(source):
    os.makedirs(source)
koding.Dummy_File(dst=dummy+'1.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'2.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'3.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'4.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'5.txt', size=10, size_format='mb')
koding.Dummy_File(dst=dummy+'6.txt', size=10, size_format='mb')
dialog.ok('DUMMY FILE CREATED','If you want to check in your userdata folder you should have a new folder called "move_test" which has 6x 10MB dummy files.')

# This is optional but if you want to see a dialog progress then you'll need this
dp.create('MOVING FILES','Please Wait')

destination = xbmc.translatePath('special://home/My MOVED Dummy File')
koding.Move_Tree(source, destination, dp)
dialog.ok('CHECK YOUR KODI HOME FOLDER','Please check your Kodi home folder, the dummy file should now have moved in there. When you press OK it will be removed')
shutil.rmtree(destination)
~"""
    if dp:
        totalfiles = 0
        for root, dirs, files in os.walk(src):
            totalfiles += len(files)
        count = 0

    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)
            if dp:
                try:
                    count += 1
                    update = count / totalfiles * 100
                    dp.update(int(update))
                except:
                    pass
    try:
        shutil.rmtree(src)
    except:
        pass

    if dp:
        dp.close()
#----------------------------------------------------------------
# TUTORIAL #
def Split_Lines(raw_string, size):
    """
Splits up a piece of text into a list of lines x amount of chars in length.

CODE: koding.Split_Lines(raw_string, size)

AVAILABLE PARAMS:

    (*) raw_string  -  This is the text you want split up into lines

    (*) size        -  This is the maximum size you want the line length to be (in characters)

EXAMPLE CODE:
raw_string = 'This is some test code, let\'s take a look and see what happens if we split this up into lines of 20 chars per line'
my_list = koding.Split_Lines(raw_string,20)
koding.Text_Box('List of lines',str(my_list))
~"""    
    final_list=[""]
    for i in raw_string:
        length = len(final_list)-1
        if len(final_list[length]) < size:
            final_list[length]+=i
        else:
            final_list += [i]
    return final_list
#----------------------------------------------------------------
# TUTORIAL #
def Text_File(path, mode, text = ''):
    """
Open/create a text file and read/write to it.

CODE: koding.Text_File(path, mode, [text])

AVAILABLE PARAMS:
    
    (*) path  -  This is the path to the text file

    (*) mode  -  This can be 'r' (for reading) or 'w' (for writing)

    text  -  This is only required if you're writing to a file, this
    is the text you want to enter. This will completely overwrite any
    text already in the file.

EXAMPLE CODE:
HOME = xbmc.translatePath('special://home')
koding_test = os.path.join(HOME, 'koding_test.txt')
koding.Text_File(path=koding_test, mode='w', text='Well done, you\'ve created a text file containing this text!')
dialog.ok('CREATE TEXT FILE','If you check your home Kodi folder and you should now have a new koding_test.txt file in there.','[COLOR=gold]DO NOT DELETE IT YET![/COLOR]')
mytext = koding.Text_File(path=koding_test, mode='r')
dialog.ok('TEXT FILE CONTENTS','The text in the file created is:','[COLOR=dodgerblue]%s[/COLOR]'%mytext,'[COLOR=gold]CLICK OK TO DELETE THE FILE[/COLOR]')
try:
    os.remove(koding_test)
except:
    dialog.ok('FAILED TO REMOVE','Could not remove the file, looks like you might have it open in a text editor. Please manually remove yourself')
~"""
    try:
        textfile = open(path, mode)

        if mode == 'r':
            content  = textfile.read()
            textfile.close()
            return content

        if mode == 'w':
            textfile.write(text)
            textfile.close()
            return True

    except:
        xbmc.log(Last_Error())
        return False
#----------------------------------------------------------------
