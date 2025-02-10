# CS361-main_program
## Version: v1.0.2
## Last Update: 02/10/2025

## Author: Shengwei Zhu

## Language/Components: HTML, CSS, Javascript, Flask, Python

This is the main program (web application) developed for course CS 361 Software Engineering taught at Oregon State University. The purpose of this web app is to display an photo gallery consisting various unique images. Users navigating through the gallery will have the option to upload images and view them in full size. It is made up mostly HTML with CSS for styling and Javascript for functionality of app features. Python and Flask are mainly used for storing images and fetching the images to be displayed on the gallery. 

## Important Notice
The Python portion, specifically Flask, requires a secret Python key. At the current moment, the program has no way to automatically fetch the key (environment path and variable aren't set up yet). This feature will likely be implemented in later versions. In the current app.py, you may notice that secret key isn't actually a key, but a placeholder. To generate the secret key, open your Terminal on your IDE. Then input the **python** command (Make sure you have Python setup on your IDE!). After this, you will see a special python terminal which will allow you to input python specific commands. Input **import secrets** and enter. Then input **secrets.token_hex(16)** and enter. This will generate a secret key which you need to copy and paste onto Line 6 or 7 in the app.py file. 

## How to Run this Web App
To run this web app, you must download the files and store them in a directory or folder where you can find them. After downloading, locate the downloaded content and have a terminal or complier open. Make sure the terminal/complier knows the path to the downloaded content, otherwise it will not run. 

For example, if you store the downloaded files and folder in a directory called **test_folder**, then your file path would be something like **C:\Source\test_folder**. After you are in the right path, then simply run **python app.py** and it will start up the local host and open it on your browser.
