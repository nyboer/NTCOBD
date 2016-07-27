# Script to look for ODBII device on bluetooth.
# first checks if it is already paired and trusted, then setup the rfcomm0 port

import subprocess
import obd
import time


# request all diagnostic trouble codes from the vehicle's engine.
def getdtc(connection):
    troublecodes = connection.query(obd.commands.GET_DTC)
    dtc_log = open("obd_dtc_errors.txt", "w")
    dtc_log.write(troublecodes)
    dtc_log.close()
    print troublecodes

def run_command(command):
    p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

cmd = 'bt-device -l'.split()
notfound = True
mac = ""
isserial = False

for line in run_command(cmd):
    print(line)
    parse = line.split()
    if "OBDII" in parse:
        mac = line[line.find("(")+1:line.find(")")] #between parentheses
        notfound = False
        print ("-- obdii trusted at "+mac)
        break;

#if it's not already a device, scan to pair
if (notfound):
    cmd = 'bt-adapter -d'.split()
    for line in run_command(cmd):
        print(line)
        parse = line.split()
        if "OBDII" in parse:
            mac = line[line.find("(")+1:line.find(")")] #between parentheses
            print ("-- obdii is @ "+mac)
            break;
    print('done with scan')
    # connect and pair to device
    cmd = 'bt-device -c'.split()
    cmd.append(mac)
    run_command(cmd)
        ##need to get data back about the cnxn attempt and then continue with pair, pin, and trust.

#otherwise, setup the rfcomm0 serial device
else:
    getdata = False;
    print '-- begin serial device setup --'
    cmd = 'sudo rfcomm connect hci0 '.split()
    cmd.append(mac)
    subprocess.Popen(cmd)
    ports = []
    cmds_list = []
    trycount = 0
    trymax = 15
    while trycount<trymax:
        print("-- Looking for a serial port, attempt: "+str(trycount))
        time.sleep(.1)
        ports = obd.scan_serial()
        trycount = trycount + 1
        if ports:
            trycount = trymax
    if ports:
        connection = obd.OBD("/dev/rfcomm0")
        getdata = (connection.status() == 'Car Connected')
        print('connection to Car: '+str(getdata))
        if connection:
            print('protocol: '+connection.protocol_name())
            print('supported commands:')
            cmds_text = open("obd_commands.txt", "w")
            for command in connection.supported_commands:
                print(command.name)
                cmds_text.write('{0}\n'.format(command.name) )
                cmds_list.append(command.name)
            cmds_text.close()
    else:
        print("-- no serial connection was made. --")

    #instead of using all available, use a curated selection of commands:
    cmd_file = open('obd_commands_complete.txt','r')
    cmds_list = cmd_file.readlines()
    #get rid of the trailing newline at the end of each line:
    for cmdline in range(0,len(cmds_list)):
        clean = cmds_list[cmdline].rstrip()
        cmds_list[cmdline] = clean
    print(cmds_list)

    ## main loop
    try:
        cmds_log = open("obd_log.txt", "w")
        while getdata:
            time.sleep(0.5)
            for cmdname in cmds_list:
                cmd = obd.commands[cmdname] # select an OBD command (sensor)
                #exclude EVAP_VAPOR and OBD_COMPLIANCE commands - seems to be a bug in obd python
                vape = cmdname.find("EVAP_VAPOR")
                clear_dtc = cmdname.find("OBD_COMPLIANCE")
                # these are not realtime relevant
                get_dtc = cmdname.find("GET_DTC")
                get_freeze = cmdname.find("GET_FREEZE_DTC")
                if vape < 0 and clear_dtc < 0 and get_dtc < 0 and get_freeze < 0:
                    response = connection.query(cmd) # send the command
                    csv = cmdname+', '+str(response)
                    cmds_log.write(csv+'\n')
                    print(csv)
    except KeyboardInterrupt:
        cmds_log.close()
        print 'interrupted!'
