## -------------------------------------------------------------------------------------------------------------
## 
##
##      Description: Creator functions
##
## DISCLAIMER
## The sample scripts are not supported under any HP standard support program or service.
## The sample scripts are provided AS IS without warranty of any kind. 
## HP further disclaims all implied warranties including, without limitation, any implied 
## warranties of merchantability or of fitness for a particular purpose. 
##
##    
## Scenario
##     	Create the baremteal.csv forHelion installation
##		
##
## Input parameters:
##         iLOCSV             = path to the CSV file containing iLO Ip address and credentials
##
## Output : 
##      a file called baremetal.csv is created in the current folder.
## 
## Pre-requisite:
##      Requires the python library called hpilo
##      https://pypi.python.org/pypi/python-hpilo/2.8
##
## History: 
##         October 2014 : First release
##
## -------------------------------------------------------------------------------------------------------------


def createbaremetal(iLOCSV):

    # Open the file
    fo = open('baremetal.csv', 'w')
    
    print("Creating baremetal.csv in the current folder...")

    reader = csv.reader(iLOCSV)
    next(reader) # skip first line
   

    for row in reader:
        a = ','.join(row)
        if not re.match('^,,,,,', a) and not re.match('^,,,#', a) and not re.match('^#', a):
            iLOIP          = row[0]
            username       = row[1]
            password       = row[2]

            ThisiLO       = hpilo.Ilo(iLOIP,username,password,60,443,'',False)
            iLOhealth     = ThisiLO.get_embedded_health()
            PwrStatus     = ThisiLO.get_host_power_status()
            iLOVersion    = ThisiLO.get_fw_version()
            iLOType       = iLOVersion['management_processor'] 

            a= "\t Writing iLO info for IP address %s" % iLOIP
            print(a) 
            
            # 
            #    Get physical Nics information
            #

            AllNics        = iLOhealth['nic_information']

            portindex      = '1'                # First NIC
            ThisPortNumber = '' 

            KeyList = AllNics.keys()
            for key in KeyList:
                if portindex in key:
                    ThisPortNumber = key
                    break

            if len(ThisPortNumber) > 0:
                ThisNicInfo    = AllNics[ThisPortNumber]
                ThisMac        = ThisNicInfo['mac_address']
            else:
                print("\t\tCannot find MAC address on port " + portindex + " on iLO " + iLOIP)
                ThisMac = "No-MAC-info"

            #
            #     Get memory information
            #
            mem = iLOhealth['memory']
            TotalMem= 0

            if 'OFF' in PwrStatus:
                components = mem['memory_components']
                for i in range(len(components)):
                    Dimm = components[i]
                    for j in range(len(Dimm)):
                        Value = Dimm[j][1]['value']
                        if 'MB'in Value:
                            OneDimm = Value.split(' ')[0]
                            TotalMem += int(OneDimm) 
            else:
                mem_details = mem['memory_details_summary'] 
                for key in mem_details.keys():
                    MemoryperCPU = mem_details[key]['total_memory_size']
                    MemoryperCPU = MemoryperCPU.split(' ')[0]
                    TotalMem    += int(MemoryperCPU) * 1024
                    

            # 
            #    Get Processors information
            #

            Procs = iLOhealth['processors']
            TotalCores = 0
            for key in Procs.keys():
                Cores = Procs[key]['execution_technology'].split('/')[0]
                TotalCores += int(Cores)
            
             
            # 
            #    Get Storage information
            #
            #    Note: Disk size is calculated as 80% of the raw size.
            #
            if iLOType == 'iLO4':
                Storage = iLOhealth['storage']
                Controller = Storage['Controller on System Board'] 
                LogicalDrives = Controller['logical_drives'] 
                for ld in LogicalDrives:
                    if '01' in ld['label']:
                        disksize = ld['capacity'].split(' ')[0]
                        disksize = int(int(disksize) * 0.8)
                        disksize = str(disksize).strip()
            else:
                print('\t\t Server has iLO3 , so cannot extract storage information...')  
                disksize = 'Disk-Size-to-be-filled-out'.strip()
                
        Line = ThisMac.strip() + "," + username.strip() + "," + password.strip() + "," + iLOIP.strip() + "," 
        Line +=  str(TotalCores).strip() + "," + str(TotalMem).strip() + "," + disksize + "\n"
        

        fo.write(Line)
    
    fo.close()
    print("\n...Check out the file baremetal.csv file created in the current folder")
    
# -----------------------------------------------------------------------------------
# 
#  Function: main
#
#  Description: Main entry point
# -----------------------------------------------------------------------------------
def main():
    
    # Define parameters 
    parser = argparse.ArgumentParser(add_help=True, description='Usage')
    parser.add_argument('-ilo', '--iLOCSV', dest='iLOCSV', required=False, type=argparse.FileType('r'),  
                        help='CSV file containing iLO credentials and IPs')

    args = parser.parse_args()
    iLOCSV = args.iLOCSV
    if iLOCSV != None:
        createbaremetal(iLOCSV)
        
    else:
        print("Please specify a CSV file with iLO IP address and credentials")
    
if __name__ == '__main__':
    import sys
    import argparse
    import hpilo
    import re
    import csv
    import tempfile
    sys.exit(main())
