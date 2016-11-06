import zipfile
import sys
import os
import shutil
import time
from PyPDF2 import PdfFileReader

def setup():
    """Base function to create the .zip file, '_archive.zip' in current directory.
       Any additional files in the directory, aside from this application, will be
       put inside the created .zip file.

       Function calls main() upon completion"""

    if "_archive.zip" in os.listdir(progLocation):                  # If archive already exists in folder
        print("Archive is already setup")
        os.startfile(os.path.join(progLocation, "_archive.zip"))
        main()
    else:                                                           # Setup
        input("\nZip archive, '_archive.zip', will be set up in the current directory:  {}\n"
              "Any files, other than this application, currently in the above directory, "
              "will automatically be copied to the zip file upon its creation.\n\n"
              "You may move files out of the directory at this time. Press 'Enter' to continue with "
              "the setup process.".format(progLocation))

        print("\nCreating archive '_archive.zip'")
        newZip = zipfile.ZipFile("_archive.zip", "w")

        print("Copying files to '_archive.zip'")
        fileList = os.listdir(os.path.join(progLocation, "PDF Files"))
        fileList.remove(__file__.split("/")[-1])                    # Remove name of zip file and current program
        fileList.remove("_archive.zip")                             #  from directory list
        os.makedirs("_archiveAdd")

        for file in fileList:
            newZip.write(file, compress_type=zipfile.ZIP_DEFLATED)
        newZip.close()

        print("Setup complete")
        os.startfile(os.path.join(progLocation, "_archive.zip"))

        main()
def addfile():
    """Adds file(s) located in folder '_archiveAdd' to archive
         Note: _archiveAdd folder must be in the same directory as _archive.zip

       Function calls main() upon completion"""

    if os.path.exists(os.path.join(progLocation, "_archiveAdd")):
        print("{} file(s) detected in '_archiveAdd'".format(len(os.listdir(os.path.join(progLocation, "_archiveAdd")))))
        print("Adding file(s) to archive")

        if "_archive.zip" in os.listdir(progLocation):
            with zipfile.ZipFile("_archive.zip", "a") as archive:
                for file in os.listdir(os.path.join(progLocation, "_archiveAdd")):
                    archive.write(file, compress_type=zipfile.ZIP_DEFLATED)

        print("Adding file(s) complete")
        os.startfile(os.path.join(progLocation, "_archive.zip"))

    else:
        print("Archive not set up properly. Attempting to resolve issue.")
        if os.path.exists(os.path.join(progLocation, "_archive.zip")):
            os.makedirs(progLocation, "_archiveAdd")
        else:
            setup()

    main()
def searchfile():
    """Searches archive for file by name or other keyword.

       Function calls main() upon completion"""

    global progLocation
    try:
        archive = zipfile.ZipFile(os.path.join(progLocation, "_archive.zip"), "r")
    except:
        print("Archive has not been set up properly, please setup archive.\n")
        main()

    a = input("\nWhat would you like to search by?\n"
              "> TITLE  COMPOSER  TYPE of piece  composition YEAR ERA  PERFORMANCE group/year  PART  EXIT\n> ").lower()

    #                                    ----Identify and act upon input----

    if a == "title" or a == "1":
        c = input("Enter Title:  ")
        if c.lower() == "exit":
            sys.exit()                                              # Exit program

        files = _search(c, "/Title", archive)

        if len(files) == 1:
            os.startfile(os.path.join(progLocation, "archiveTest", files[0]))
            print("File opened successfully\n\n")
        elif len(files) < 1:
            print("No file found with title '{}'\n\n".format(c))
            searchfile()
        else:                                                       # More than one file shares /Title metadata
            def _reenter():
                """Additional function in searchFile() that allows for unknown input to circle
                   back to inputting a title from a list of titles."""

                d = input("\nPlease enter the full file name you would like to retrieve.\n> {}\n".format(files))
                if d in files:
                    os.startfile(os.path.join(progLocation, "archiveTest", files[files.index(d)]))
                    print("File opened successfully\n\n")
                elif d.lower() == "exit":
                    sys.exit()
                else:
                    print("Invalid file name '{}'".format(d))
                    _reenter()
            _reenter()
    elif a == "composer" or a == "2":
        c = input("Enter Composer:  ")
        if c.lower() == "exit":
            sys.exit()                                              # Exit program

        files = _search(c, "/Composer", archive)

        if len(files) == 1:
            os.startfile(os.path.join(progLocation, "_tempFolder", files[0]))
            print("File opened successfully\n\n")
        elif len(files) < 1:
            print("No file found with composer '{}'\n\n".format(c))
            searchfile()
        else:                                                       # More than one file shares /Composer metadata
            def _reenter():
                """Additional function in searchFile() that allows for unknown input to circle
                   back to inputting a title from a list of titles."""

                d = input("\nPlease enter the full file name you would like to retrieve.\n> {}\n".format(files))
                if d in files:
                    os.startfile(os.path.join(progLocation, "_tempFolder", files[files.index(d)]))
                    print("File opened successfully\n\n")
                elif d.lower() == "exit":
                    sys.exit()
                else:
                    print("Invalid file name '{}'".format(d))
                    _reenter()
            _reenter()
    elif a == "type" or a == "type of piece" or a == "3":
        c = input("Enter Type of Piece:  ")
        if c.lower() == "exit":
            sys.exit()                                              # Exit program

        files = _search(c, "/Keywords", archive)

        if len(files) == 1:
            os.startfile(os.path.join(progLocation, "archiveTest", files[0]))
            print("File opened successfully\n\n")
        elif len(files) < 1:
            print("No file found of type '{}'\n\n".format(c))
            searchfile()
        else:                                                       # More than one file shares /Keyword metadata
            def _reenter():
                """Additional function in searchFile() that allows for unknown input to circle
                   back to inputting a title from a list of titles."""

                d = input("\nPlease enter the full file name you would like to retrieve.\n> {}\n".format(files))
                if d in files:
                    os.startfile(os.path.join(progLocation, "archiveTest", files[files.index(d)]))
                    print("File opened successfully\n\n")
                elif d.lower() == "exit":
                    sys.exit()
                else:
                    print("Invalid file name '{}'".format(d))
                    _reenter()
            _reenter()
    elif a == "year" or a == "era" or a == "year/era" or \
         a == "composition year" or a == "composition era" or \
         a == "composition year/era" or a == "4":
        c = input("Enter Composition Year or Era:  ")
        if c.lower() == "exit":
            sys.exit()                                              # Exit program

        files = _search(c, "/CompYear", archive)

        if len(files) == 1:
            os.startfile(os.path.join(progLocation, "archiveTest", files[0]))
            print("File opened successfully\n\n")
        elif len(files) < 1:
            print("No file found from year/era '{}'\n\n".format(c))
            searchfile()
        else:                                                       # More than one file shares /CompYear metadata
            def _reenter():
                """Additional function in searchFile() that allows for unknown input to circle
                   back to inputting a title from a list of titles."""

                d = input("\nPlease enter the full file name you would like to retrieve.\n> {}\n".format(files))
                if d in files:
                    os.startfile(os.path.join(progLocation, "archiveTest", files[files.index(d)]))
                    print("File opened successfully\n\n")
                elif d.lower() == "exit":
                    sys.exit()
                else:
                    print("Invalid file name '{}'".format(d))
                    _reenter()
            _reenter()
    elif a == "performance" or a == "performance group" or \
         a == "performance year" or a == "group/year" or \
         a == "group" or a == "performance group/year" or a == "5":
        c = input("Enter Performance Year or Group:  ")
        if c.lower() == "exit":
            sys.exit()                                              # Exit program

        files = _search(c, "/PerfGroupYear", archive)

        if len(files) == 1:
            os.startfile(os.path.join(progLocation, "archiveTest", files[0]))
            print("File opened successfully\n\n")
        elif len(files) < 1:
            print("No file found from performance group/year '{}'\n\n".format(c))
            searchfile()
        else:                                                       # More than one file shares /PerfGroupYear metadata
            def _reenter():
                """Additional function in searchFile() that allows for unknown input to circle
                   back to inputting a title from a list of titles."""

                d = input("\nPlease enter the full file name you would like to retrieve.\n> {}\n".format(files))
                if d in files:
                    os.startfile(os.path.join(progLocation, "archiveTest", files[files.index(d)]))
                    print("File opened successfully\n\n")
                elif d.lower() == "exit":
                    sys.exit()
                else:
                    print("Invalid file name '{}'".format(d))
                    _reenter()

            _reenter()
    elif a == "part" or a == "6":
        c = input("Enter Instrument Part:  ")
        if c.lower() == "exit":
            sys.exit()                                              # Exit program

        files = _search(c, "/Part", archive)

        if len(files) == 1:
            os.startfile(os.path.join(progLocation, "archiveTest", files[0]))
            print("File opened successfully\n\n")
        elif len(files) < 1:
            print("No file found of instrument part '{}'\n\n".format(c))
            searchfile()
        else:                                                       # More than one file shares /Keyword metadata
            def _reenter():
                """Additional function in searchFile() that allows for unknown input to circle
                   back to inputting a title from a list of titles."""

                d = input("\nPlease enter the full file name you would like to retrieve.\n> {}\n".format(files))
                if d in files:
                    os.startfile(os.path.join(progLocation, "archiveTest", files[files.index(d)]))
                    print("File opened successfully\n\n")
                elif d.lower() == "exit":
                    sys.exit()
                else:
                    print("Invalid file name '{}'".format(d))
                    _reenter()

            _reenter()
    elif a == "exit" or a == "4":
        shutil.rmtree(os.path.join(progLocation, "_tempFolder"))
        sys.exit()
    else:
        print("Invalid Input, please retry.")
        searchfile()

    main()
def _search(keyword, metaLocat, archive):
    """Assisting function to searchFile(). Searches through given archive and returns
       a list of the file(s) that match the keyword in the given metadata location."""

    global progLocation
    retList = []
    tempFolderPath = os.path.join(progLocation, "_tempFolder")      # Create temporary folder to extract zip to

    if os.path.exists(tempFolderPath):
        creTime = int(os.path.getctime(tempFolderPath))
        curTime = int(time.time())

        if curTime - creTime > 180:
            shutil.rmtree(os.path.join(tempFolderPath))

            os.makedirs(tempFolderPath)
            archive.extractall(tempFolderPath)
    else:
        os.makedirs(tempFolderPath)
        archive.extractall(tempFolderPath)


    count = 0
    for fileName in os.listdir(tempFolderPath):
        count += 1
        #print(count)
        if fileName.endswith(".pdf"):

            openPDF = PdfFileReader(open(os.path.join(tempFolderPath, fileName), "rb"))
            infoDict = openPDF.getDocumentInfo()
            #print(infoDict)

            if keyword.lower() in infoDict[metaLocat].lower():
                retList.append(fileName)

    return retList
def main():
    a = input("What would you like to do?\n> ADD file  SEARCH files  SETUP archive  Exit\n  ").lower()

    if a == "add" or a == "add file" or a == "1":                   # Identify and act upon input
        addfile()
    elif a == "search" or a == "search file" or a == "2":
        searchfile()
    elif a == "setup" or a == "setup archive" or a == "3":
        setup()
    elif a == "exit" or a == "4":
        if os.path.exists(os.path.join(progLocation, "_tempFolder")):
            shutil.rmtree(os.path.join(progLocation, "_tempFolder"))
        sys.exit()
    else:
        print("Invalid Input, please retry.\n")
        main()

progLocation = os.path.dirname(__file__)
main()

# Things to do:
#     Add function to add files that are 'close' to keyword
#     Implement gzip and zip the archive folder
#         Program access to the zipped archive in search function
#     Change 'archiveTest' instances to archive name.  Likely something like _archive
