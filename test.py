cmd_file = open('obd_commands_complete.txt','r')
cmds_list = cmd_file.readlines()
for cmdline in range(0,len(cmds_list)):
    print cmds_list[cmdline]
    clean = cmds_list[cmdline].rstrip()
    cmds_list[cmdline] = clean
print(cmds_list)

str = "BLEH_EVAP_VAPOR_JUNK"
print str.find("EVAP_VAPOR")
