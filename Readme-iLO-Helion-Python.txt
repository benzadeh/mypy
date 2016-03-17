Overview
	Helion installation requires an input file called baremetal.csv that describes the undercloud and overcloud server infrastructure 
	to deploy OpenStack using TripleO.
	The baremetal.csv contains the following fields: 
		<mac_address>,<ipmi_user>,<ipmi_password>,<ipmi_address>,<no_of_cpus>,<memory_MB>,<diskspace_GB>
	Filling out those values using the iLO management tool is a very time-consuming task as the environment may contain hundred of servers.
	As such, an automation script is required to query the iLO interface and collect the information

Description
	The create-baremetal.py Python script fullfills this purpose. It reads an input file called Helion-ILO.CSV that contains basic information
		<ipmi_address>,<ipmi_user>,<ipmi_password>
	and remotely connects to teh ILO interface using RIBCL to collect necessary information and creates the baremetal.csv for you.

	The syntax of the script is the following:
		python3 create-baremetal.py --iLOCSV Helion-iLO.CSV
	The output is the baremetal.csv file.

Prerequisites
	a) iLO4 with the latest firmware
	b) Requires the python library called hpilo : https://pypi.python.org/pypi/python-hpilo/2.8
