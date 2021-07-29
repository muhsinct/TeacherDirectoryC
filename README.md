# TeacherDirectoryC
 
 Steps to run the App
 
 1) Download the repository and navigate to the folder where requirements.txt located, and run below commands to setup the environment dependencies.
 		
		pip install -r requirements.txt
		
2) Run below commandds to setup the App (from folder containing manage.py)
		
		python manage.py makemigrations
		python manage.py migrate
		
3) Run app using below command
		
		python manage.py runserver
		open the url in browser
		use the credentials (usesrname=test_1, password=pass.123) to login
		
4) Use Teachers.csv and teachers.zip for bulk upload. For any other csv files, follow the same format of the given Teachers.csv file.
		
 
