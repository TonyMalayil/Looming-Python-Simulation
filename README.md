# Looming-Python-Simulation
Python 3D simulation of Time-To-Contact

## What each file does:
* TTC.py - Contains the mathematical functions used to calculate TTC when given the vectors and time between the frames.
* main.py - Runs the simulation code where a cube (representing a vehicle) approaches the viewer. Once the viewer closes the simulation, the numerical values are plotted showing the angles found and the time-to-contact in both planes.

## Activity Suggestions:
Open-source code is a powerful teaching tool as it allows student to understand the logic behind a project, how it should be structured, and gives them the opportunity to fiddle and create. By giving a simple template to build off, students are not required to know the very technical or complex side of the project and can start right away.  
With this code, students are recommended to change the values to four different variable in main.py to see how it affects TTC.
* cube_vertices (line 39-47) - This variable is an array containing the location of the vertices of the cube. Students may change the x, y, and z coordinates of each vertex to move the location of the cube. Each vertex is numbered and given with its original relative position. The fourth variable of each array (w) should not be changed.
* numFrames (line 102) - Students may increase or decrease the number of frames shown in the simulation. This variable does not represent FPS (frames per second) and students must change the time between frames to attain their desired FPS.
* time (line 114) - This variable represents the time between each frame.
* translation_matrix[2,3] (line 141) - This values in the array of the translation matrix allows us to adjust the speed of the cube. While numFrames and time can be used to adjust the FPS, how much the cube moves each frame is given in this variable. Students can multiply the current value of the variable by a factor to attain their desired speed.

Students may adjust other parts of the repository, but with the risk that the simulation may fail to run.

## Adapted from:
The projection code was adapted from an article by Skann AI (https://skannai.medium.com/projecting-3d-points-into-a-2d-screen-58db65609f24) which provided the base Python code for converting the 3D points into 2D. This article delves into the mathematical process and provides the code for a viewing an object in 3D.
