
[![Build Status](https://travis-ci.org/ISISScientificComputing/autoreduce.svg?branch=master)](https://travis-ci.org/ISISScientificComputing/autoreduce) [![Master Coverage Status](https://coveralls.io/repos/github/ISISScientificComputing/autoreduce/badge.svg?branch=master)](https://coveralls.io/github/ISISScientificComputing/autoreduce?branch=master) 

# Autoreduction v20.1
A service for automated batch processing of jobs specifically design for use at [ISIS Neutron and Muon Facility](https://www.isis.stfc.ac.uk). For further documentation see also [Wiki](https://github.com/ISISScientificComputing/autoreduce/wiki). 

In one (not complete) picture the Autoreduction service is:

![Example Table](documentation/assets/main_components/Autoreduction_main_components.png)

The code for monitors of experiments, i.e. that send messages to the Messenging server when experiments are ready to be reduced (processed) is in monitors folder. The code for processors which consume/subscribe to Messenging queues and run jobs on the compute nodes are in the QueueProcessors folder. Finally, the code for the WebApp, which is used to monitor the system by both users and those who support the service is located in the WebApp folder. 

This service discovers raw data automatically, reduces it (performs some processing on them) and stores the result. The results are rendered by the web application which allows the user and support staff to monitor the system and rerun jobs manually as needed.

####################
