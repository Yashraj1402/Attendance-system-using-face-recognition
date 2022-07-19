The program uses pre-uploaded images to recognize faces.
In a folder upload the images of people you want the program to recognize and name those images as the name you want for that person to be associated with in the attendance file.
Input the folder name.
After the program is run, it uses webcam to detect faces.
If a face that was loaded in the program is detected, it marks attendance in a csv file called 'Attendance.csv'
The attendance is marked in the following format:
Name,Time
Here 'Name' is the name by which the image is saved and 'Time' is the time when the program recognized the person.
Some necessary dependencies are: cmake, face-recognition, dlib, numpy, opencv-python
