# Mapping-Occupancy-Dynamics

This project uses machine learning techniques to infer data
collected from “simple” sensors placed strategically in rooms
within an apartment such that they have the best field of vision of
the rooms to automatically recognize human presence. Existing
sensor networks and infrastructures that are used for mapping
room occupancy employ models based on security systems.
However these systems can be very intrusive and comes at a
privacy, computational, and monetary cost and hence are not
really suitable for the regular home. With this project we examine
the use of PIR sensors primarily and capacitive bed sensor as a
second cross validation sensor to show that such sensors are
enough to tell us which rooms are occupied and which rooms are
not.

# Goals 

A focus of the project was to use a central processing
computer, and simple sensor nodes. By placing the heavy lifting
on the central processing computer, we could use identical
inexpensive BLE chips, with sufficient onboard processing to
analyze the output from the sensor at each node, and alert the
central computer that the occupancy had changed. A main goal
was to avoid the use of any system that would require a user to
carry a smartphone or any similar hardware, but it would be
possible to naturally navigate the home and have the home
intelligently adjust based on where people are located.

# System

The system is comprised of hardware and software components.
The hardware deals with collection of sensor data and enabling
the processing and storage of the data. The software is made up of
several different parts which are broken into different sections, codes
of which are contained in the different subfolders.
The first part is the software running on the sensors and central
processor (Code in subfolder '' ) . The second part is
the user interface and software behind it that allowed for
recording training data and comparison data for the system( Code in subfolder '').
Finally, there is the machine learning code that powered the occupancy detection technique 
(Code in Subfolder '').
