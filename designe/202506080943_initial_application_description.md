# this is initial application description

This is a completely new python application with command line interface. 
The goal of application - to contain and orchestrate RPA (via python), it should be easy to remove existing robot from daily schedule or add new one.
All credentials should be stored in .env file.
I want to store all robots in config.robots.json like robot_name, schedule info (like time to invoke, days to invoke), and also order of actions (like click, double click, keyboard input, mouse move with x,y coordinate, etc).
So likely each robot it's not module itself, it's just order of actions and one generic module that translate this data into actions in loop
I want to be able rerun tasks via command in command line and also see current status.
All current data like list of scheduled tasks, status of tasks, status of robots, logs, etc. should be stored in DB (MS SQL Server)
