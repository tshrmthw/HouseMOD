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

Machine Learning Implementation was in Google TensorFlow

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
processor (Code in subfolder 'Hardware/Adafruit_code' ) . The second part is
the user interface and software behind it that allowed for
recording training data and comparison data for the system( Code in subfolder 'Hardware/PIR').
Finally, there is the machine learning code that powered the occupancy detection technique 
(Code in Subfolder 'SourceCode').

Added to this to aid us in collecting training and verification data, an android app was created called "WheresEthan"
 for real time data collection by manual entry of the persons position in the room that is under opbservation in order to train the Machine Learning ALgorithm (Code in Subfolder 'WheresEthan')
 
 
# Contributors:

Tushar Mathew, Ethan Glassman , Mark Kurtz

# Machine Learning INSTALL

An installation of python 2.7 was used on a mac os computer. The installation steps for installing
tensorflow in a virtual environment are followed. More can be found at this link:
https://www.tensorflow.org/versions/r0.8/get_started/os_setup.html#virtualenv­installation

# Install pip and Virtualenv:

"# Ubuntu/Linux 64­bit"
$ sudo apt­get install python­pip python­dev python­virtualenv
"# Mac OS X"
$ sudo easy_install pip
$ sudo pip install ­­upgrade virtualenv
Create a Virtualenv environment in the directory ~/tensorflow:
$ virtualenv ­­system­site­packages ~/tensorflow
Activate the environment and use pip to install TensorFlow inside it:
$ source ~/tensorflow/bin/activate # If using bash
$ source ~/tensorflow/bin/activate.csh # If using csh
(tensorflow)$ # Your prompt should change
"# Ubuntu/Linux 64­bit, CPU only:"
(tensorflow)$ pip install ­­upgrade
https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow­
0.8.0­cp27­none­linux_x86_64.whl
"# Ubuntu/Linux 64­bit, GPU enabled. Requires CUDA toolkit 7.5
and CuDNN v4. For"
"# other versions, see "Install from sources" below."
(tensorflow)$ pip install ­­upgrade
https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow­
0.8.0­cp27­none­linux_x86_64.whl
"# Mac OS X, CPU only:"
(tensorflow)$ pip install ­­upgrade
https://storage.googleapis.com/tensorflow/mac/tensorflow­
0.8.0­py2­none­any.whl

# Machine Learning HOW­to­RUN

Generate labels and features:

open terminal
cd into the machine learning folder
run the following command:
be created>
An example is given below:
python generator.py ­r 1 ­s DataSetTwo/sensor_data_4_20­22.txt ­l
DataSetTwo/label_data_4_20­22.txt ­g DataSetTwo/room_1_generated.txt

Run the k­nn:

open terminal
cd into the machine learning folder

run the following command:
python kmeans.py ­t <test train generated file> ­v <validation generated file>

An example is given below:
python kmeans.py ­t DataSetTwo/room_1_generated.txt ­v
DataSetThree/room_1_generated.txt

Run the neural network:

Follow the install instructions first.
Follow the commands to setup tensor flow:
python generator.py ­r 1 ­s <sensor data file> ­l <label data file> ­g <generated file — to
$ source ~/tensorflow/bin/activate # If using bash.
$ source ~/tensorflow/bin/activate.csh # If using csh.
(tensorflow)$ # Your prompt should change.
"# Run Python programs that use TensorFlow.
...
"# When you are done using TensorFlow, deactivate the
(tensorflow)$ deactivate
python <path_to_machine_learning_folder>/hidden_nn.py ­­test_train <test
environment.

run the following command:
train generated file> ­­validation <validation generated file> ­­num_hidden 16 ­­num_epochs 20

An example is given below:
python ../LearningCode/hidden_nn.py ­­test_train
../LearningCode/DataSetTwo/room_2_generated.txt ­­
validation
../LearningCode/DataSetThree/room_2_generated.txt ­­
num_hidden 16 ­­num_epochs 20
