# Problem
The problem is to print **Top 10 Occupations** and **Top 10 States** for **certified** H1B visa applications as output files. The dataset is coming from the Office of Foreign Labor Certification Performance Data. And the output files should have three columns:
- Name of the top occupations/states
- Number of certified applications
- The ratio of the number of certified applications in an occupation/state to the total number of certified applications

The top-10 list should be sorted by number_of_certified applications and name respectively. 
# Approach
**Definition: I define every attribute of the dataset as a feature. For example, occupation_name is a feature, the state is another feature, and status (CERTIFIED or not) is another one. In other words, a feature is every column of the dataset.**

My approach in writing the code was to write it in a way to be easily generalized to potential future needs. For this reason, I considered three things:
- By changing the variable TOP_K_TO_PRINT in the main function, the user can change the number of lines printed in the output file
- Although this challenge only asks for the output files for features 'occupation' and 'state', my code can print the output for any custom number of features as will be explained below.
- I kept the number of certified applicants in two classes to be easy to change/add variables in the future. More explanation below.

One thing I wanted in my code was to be able to have top-k for any custom number of features (meaning more than only occupation and state). Therefore, I needed a 1-d variable to keep the list of features that the user wants the code to run over. And for every feature (for example state), I needed to keep the number of certified applicants in every instance of that feature (in case of state, instances are California, Florida, NewYork, Texas, ...) which means that I needed another 1-d variable to keep the instances of every feature. Therefore, I needed a 2-d variable to keep all features and all instances of every feature. I could have used several 2-d variables (for example a 2-d list). However, I decided to use two classes (an inner class inside another class) because it would make it easier to add/change variables later. In other words, if I used a 2-d list and in case we also wanted some more statistics (for example about WITHDRAWN applications) we would need to define a new 2-d list and change the code accordingly. However, with classes, we simply add another variable to the classes and the generalization is cleaner (although a 2-d classs is a little slower than a 2-d list). In my code, I called the outer class 'Feature' which contains an inner class called 'FeatureInstance'.

After deciding on the format, the next step would be to read the input file(s). In the explanation of the challenge, it is mentioned only to use basic data structures. Therefore, I did not use Panda or even CSV reader and instead used a simple Open() command. My code reads the file line by line and creates a list of the values in every line using the command split(';'). Every line has the data for an application, and if the application is not certified, the code will ignore the line and continue to the next line. As the code is reading the file line by line, it creates instances of the class FeatureInstances. For example, if the first four lines of a file are:

```bash
1 CASE_STATUS; SOC_NAME; WORKSITE_STATE
2 CERTIFIED; SOFTWARE DEVELOPERS; FL
3 CERTIFIED; DATABASE ADMINISTRATORS; CA
4 CERTIFIED; SOFTWARE DEVELOPERS; CA
```

After reading line 2, it creates an instance of the class FeatureInstance for SOFTWARE DEVELOPERS in the OCCUPATIONS Feature class and also another instance of the class FeatureInstance, FL in the STATES Feature class. Then it increments the number_of_certified_application in 'SOFTWARE DEVELOPERS' and 'FL' inner classes. Reading the third line, it creates two new instances of FeatureInstance for DATABASE ADMINISTRATORS (in OCCUPATIONS Feature class) and CA (in STATES Feature class) and does the incrementation. However, in the fourth line, no new instance of FeatureInstance is created as both SOFTWARE DEVELOPERS and CA FeatureInstances exist, and the code only increments the number_of_certified_application variable inside the class. 

Finally, after all the lines in the dataset are read, the FeatureInstances are sorted using the function sorted() of python, and the first top10 are printed in the output file. 

A few things about my code:
- As explained above, my code can run over any custom number of features. Right now, it only runs over features 'occupation' and 'state'. However, the user can add features to the variable feature_names in the main function of the code. For example, by adding this line to the main function:
```bash
feature_names['CITIES']={'LCA_CASE_WORKLOC2_CITY', 'WORKSITE_CITY'}
```
The code will automatically create 'top_10_cities.txt' in addition to the previous outputs. Here, CITIES is the name we give to the feature and 'LCA_CASE_WORKLOC2_CITY' and 'WORKSITE_CITY' are what is used in the dataset header. I have noticed that H1B_FY_2014.csv header has a different header titles than newer datasets. If the Office of Foreign Labor Certification Performance Data decides to change the format again, the user can easily update the code by adding the new titles to variable feature_names.
- The code reads all the files in the input directory and combines them. For example, if we put two input files for 2014 and 2015 in the input directory, it will combine the input files and create an overall output. To have the top10 for a single year, only the corresponding input file should be put in the input directory.
## Platform
The code is written with python 3.7
# Run instructions
If you haven't installed git yet, first install git. Then, in a linux or mac terminal, do: 
```bash
git clone https://github.com/aminghiasi/h1b_statistics 
cd h1b_statistics/input
```
Put your input file(s) here in this directory . Then do: 
```bash
cd ..
. ./run.sh
```
The output files will be in ./output/

