# import bluetooth, subprocess
# nearby_devices = bluetooth.discover_devices(duration=4,lookup_names=True,flush_cache=True, lookup_class=False)
# for x in nearby_devices:
#     print("bt "+str(x))

# '''
# Created on Nov 16, 2011
# @author: Radu
# '''
# import time
# import bluetooth
#
# def search():
#     devices = bluetooth.discover_devices(duration=20, lookup_names = True)
#     return devices
#
# if __name__=="__main__":
#     while True:
#         results = search()
#         if (results!=None):
#             for addr, name in results:
#                 print "{0} - {1}".format(addr, name)
#             #endfor
#         #endif
#         time.sleep(60)
#     #endwhile

#
# import bluetooth
# print "looking for nearby devices..."
# nearby_devices = bluetooth.discover_devices(lookup_names = True, flush_cache = True, duration = 20)
# print "found %d devices" % len(nearby_devices)
import subprocess
import obd
import time

def run_command(command):
    p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

cmd = 'bt-device -l'.split()
notfound = True
mac = ""
for line in run_command(cmd):
    print(line)
    parse = line.split()
    if "OBDII" in parse:
        mac = line[line.find("(")+1:line.find(")")] #between parentheses
        notfound = False
        print ("obdii found at "+mac)
        break;

#if it's not already a device, scan to pair
if (notfound):
    cmd = 'bt-adapter -d'.split()
    for line in run_command(cmd):
        print(line)
        parse = line.split()
        if "OBDII" in parse:
            print ("obdii found")
            break;
    print('done with scan')
else:
    cmd = 'sudo rfcomm connect hci0 '.split()
    cmd.append(mac)
    #cmd.append('&')
    print 'serial setup'
    subprocess.Popen(cmd)
    time.sleep(2)
    ports = obd.scan_serial()
    print ports
    connection = obd.OBD("/dev/rfcomm0")
    print '----'
    while True:
        cmd = obd.commands.RPM # select an OBD command (sensor)
        response = connection.query(cmd) # send the command
        print(response) # "2410 RPM"
