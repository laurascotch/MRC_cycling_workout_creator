# .mrc cycling workout creator
A simple software that takes a .csv files and generates a .mrc to be used with indoor cycling training apps.

## How to prepare the .csv
Use the gsheet/xlsx file attached to this repo (assets folder) to generate the .csv file. The format of each row is as follows:
|      Duration      | %FTP start | %FTP end | Duration (decimal) |
|:-:|:-:|:-:|:-:|
| Interval duration expressed in gsheet time format | %FTP at the start of the interval | %FTP at the end of the interval | Decimal duration of the interval, computed by gsheet formula |
The first three columns are the ones that need to be edited.
#### Example
Consider the following workout from [whatsonzwift.com](https://whatsonzwift.com/workouts/le-col-training-with-legends)

 ![Example workout](/assets/images/example_workout.png)
 
The gsheet will appear as follows:

 ![Example GSheet](/assets/images/example_gsheet.png)
 
You just need to download the sheet as a .csv file.

## Script usage
You can run the .py script or use the .exe in dist.

You will be prompted with the following window:

 ![Main window](/assets/images/mainwindow.png)
 
You can now load the .csv and its graphic preview will appear:

 ![Loaded csv](/assets/images/loaded.png)
 
Enter the workout name, its description (all optional) and hit save: you are now ready to import the .mrc file on the app of your choice and ***smash those pedals!***
