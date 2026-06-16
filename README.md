<<<<<<< HEAD
# Traffic_Crash_Analytics_and_Safety_Intelligence_Platform
=======   
Download “Traffic_CrashesData.csv” from this link https://drive.google.com/file/d/1jAFsxF8ri--wYC1A-8k_Otdlf8xfcODN/view?usp=sharing and save in your PC.  

Requirement:  
- VS Code  
- MySQL Server  
- Python 3.13.9  
- pandas  
- streamlit  
- matplotlib  
   Install these in your PC.   

Open "Traffic_Crash_Analysis_project.ipynb" file in VSCode  
- Replace your MySQL server password in "Connection to MySQL Server" code cell then run the cell. It will establish the connection to your MySQL Server.  
- Run "Creating Database 'Traffic_Crashes_Data'" code cell. It will create 'Traffic_Crashes_Data' database in your MySQL Server.  
- Replace your “Traffic_CrashesData.csv” file path in "Reading the CSV file and convert as DataFrame" code cell then run the cell. It will read the csv file and covert as DataFrame. It will take few seconds, wait until complete running.  
- Run "Function to make Connection to Traffic_Crashes_Data Database" code cell. It will establish the connection to your 'Traffic_Crashes_Data' database.  
- Run "Creating the Table" code cell. It will create 'Traffic_Crashes_Analysis' table in your 'Traffic_Crashes_Data' database.  
- Run "Inserting the Data from DataFrame to MySQL" code cell. It will insert the data from DataFrame to 'Traffic_Crashes_Analysis' table.  
- Run "Function to read SQLQuery output, assign column name of database table to dataframe column and rearrange index starts from 1" code cell. Then run the below code cells one by one the see the Query results there.  

Open "Traffic_Crash_Analysis.py" file  
- Replace your MySQL server password in line 11 and save.  
- Copy "home_img.webp" file from data/raw/input_images to your PC and copy the path, then replace it in line 68 and save.  
- Open New Terminal in VS Code.  
- Go to your file path of "Traffic_Crash_Analysis.py" in terminal.  
- Enter this command "streamlit run Traffic_Crash_Analysis.py" and press Enter key. Streamlit app will open in your browser.  
>>>>>>> f3eff27 (Created Traffic Crash Analytics project)
