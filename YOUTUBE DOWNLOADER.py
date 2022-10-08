import os
import pytube
from sys import exit
# from sys import platform
# PLATFORM:str = platform.lower()

class YouTube:
    def __init__(self, defaultSavePath:str = "Downloads", fileExtension:str = "mp4") -> None:
        self.defaultSavePath:str = defaultSavePath
        self.fileExtension:str = fileExtension


        if(os.path.isdir(self.defaultSavePath) == False):
            os.mkdir(self.defaultSavePath)
        
    # List the videos downloaded in the default directory
    def list(self):
        try:
            videos = os.listdir("Downloads")
            print("\nVideos in Default Directory are: ")
            for vid in videos:
                print(vid)
        except Exception as e:
            print("No Videos in Default Directory")
        finally:
            print()

    def open(self):
        pass

    # Downloads a single file
    def download(self, url:str, fileName:str = None, savePath:str = None) -> None:
        if(savePath is None):
            savePath = self.defaultSavePath
        if(not os.path.isdir(savePath)):
            os.mkdir(savePath)
        if(fileName is None):
            fileName = url.split("/")[-1]
        try:
            yt = pytube.YouTube(url)
            yt.streams.filter(progressive=True, file_extension=self.fileExtension).order_by('resolution').desc().first().download(savePath, filename=f"{fileName}.{self.fileExtension}")
        except Exception as e:
            print(e)

    # Downloads multiple file
    # Need path for the list of file links
    def downloadMultiple(self, filePath:str, savePath:str = None) -> None:
        if(savePath is None):
            savePath = self.defaultSavePath
        try:
            if(not os.path.isdir(savePath)):
                os.mkdir(savePath)
        except Exception as e:
            print(e)
        with open(filePath, "r") as f:
            for line in f:
                try:
                    fileName = line.split("=")[0]
                    if(fileName == " " or fileName == "" or fileName == line):
                        fileName = line.split("/")[-1]
                except:
                    fileName = line.split("/")[-1]
                try:
                    url = line.split("=")[1]
                except:
                    url = line
                print(f"Url: {url} \t FileName: {fileName} \t savePath: {savePath}")
                self.download(url, fileName, savePath)
    
    def menu(self):
        print("\n0. Exit")
        print("1. List Downloaded Videos in Default Directory")
        print("2. Download Single File")
        print("3. Download Multiple Files")
        print("99. Show this Menu\n")

    def CLI(self):
        self.menu()
        while((user_input:=int(input(">> ")))):
            if(user_input == 0): exit(0)
            elif(user_input == 1): self.list()
            elif(user_input == 2):
                url = input("Enter URL for the Youtube video: ")
                fileName = input("Enter FileName to save Video as(Default=None): ")
                fileName = None if fileName == "" else fileName
                savePath = input("Enter Save Path for the video(Default=None): ")
                savePath = None if savePath == "" else savePath
                print("Downloading...")
                self.download(url, fileName, savePath)
                print("Downloaded Successfully...")
            elif(user_input == 3):
                filePath = input("Enter File path for the list: ")
                if(filePath == ""):
                    print("File Path Cannot be None")
                    return 0
                savePath = input("Enter The Save Path for the file: ")
                savePath = None if savePath=="" else savePath
                self.downloadMultiple(filePath, savePath)
            elif(user_input == 99): self.menu()

if __name__ == '__main__':
    y = YouTube()
    y.CLI()
    # link = str(input('Enter Youtube Video Link: '))
    # print("Downloading...")
    # y.download(link)
    # y.list()
    # print("Download Successful !")
    # # y.downloadMultiple("/tmp/test.txt")