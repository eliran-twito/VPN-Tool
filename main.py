import eel
import threading
import os
import ScriptGen
import Debugging
import paramiko


@eel.expose
def bgp_get_script_to_html(S_AS, P_AS, S_IP, P_IP, P_Name):
    bgp_script = ScriptGen.Generator(S_AS, P_AS, S_IP, P_IP, P_Name)
    return ScriptGen.Generator.bgp_get_script(bgp_script)


@eel.expose
def ospf_get_script_to_html(S_IP, P_IP, P_Name):
    return ScriptGen.Generator.ospf_get_script(S_IP, P_IP, P_Name)


@eel.expose
def general_debug_ssh(IP, username, password, F_date, F_time, T_date, T_time):
    debug = Debugging.DebugSSH(IP, username, password, F_date, F_time, T_date, T_time)
    return Debugging.DebugSSH.general_debug(debug)


@eel.expose
def vpn_debug_ssh(IP, username, password, F_date, F_time, T_date, T_time):
    debug = Debugging.DebugSSH(IP, username, password, F_date, F_time, T_date, T_time)
    return Debugging.DebugSSH.vpn_debug(debug)


eel.init('web')
eel.start('VPN_Tool_Test.html', size=(1000, 700), port=0)
