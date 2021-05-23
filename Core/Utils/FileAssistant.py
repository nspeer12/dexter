import os
import win32api # if active state python is installed or install pywin32 package seperately
import subprocess

#Searches all installed apps and opens one matching the app_name
def open_application(app_name):    
    
    p = subprocess.Popen(["powershell.exe", 
              "(Get-StartApps " + app_name +").AppId"], 
              stdout=subprocess.PIPE)
    
    out, err = p.communicate()
    out = out.strip().decode('ascii')
    
    try: 
        os.system("start " + out)
    except: 
        print("Could not find " + app_name )

#Launches a file with whatever associated app is to that extension, for example Notepad++ and .txt
def open_file(filepath):
    os.startfile(filepath)
    
#Recursively searchces directory for filename 
def search_file(filename, directory):
   result = []
   
   for root, dir, files in os.walk(directory):
      if filename in files:
         result.append(os.path.join(root, filename))
   
   return result

#open_file("C:/dump/example.txt")
#open_application("spotify")
#search_file("example.txt", "C:/")