import socket
import time
from datetime import datetime

import paramiko


class DebugSSH(object):
    def __init__(self, IP, username, password, F_date, F_time, T_date, T_time):
        self.IP = IP
        self.username = str(username)
        self.password = str(password)
        full_f_date = datetime.strptime(F_date, "%Y-%m-%d")
        formatted_date1 = full_f_date.strftime("%b %d ")
        self.F_date = str(formatted_date1)
        full_t_date = datetime.strptime(T_date, "%Y-%m-%d")
        formatted_date2 = full_t_date.strftime("%b %d ")
        self.T_date = str(formatted_date2)
        full_f_time = datetime.strptime(F_time, "%H:%M:%S")
        formatted_time1 = full_f_time.strftime("%H:%M")
        self.F_time = str(formatted_time1)
        full_t_time = datetime.strptime(T_time, "%H:%M:%S")
        formatted_time2 = full_t_time.strftime("%H:%M")
        self.T_time = str(formatted_time2)

    def general_debug(self):
        ssh_client = paramiko.SSHClient()

        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_client.connect(hostname=self.IP, username=self.username, password=self.password)

            if ssh_client.get_transport().is_active():
                print("Connected to the remote server")
            else:
                print("Failed to connect to the remote server")

            ssh_client.exec_command('vpn debug trunc ALL=5')

            time.sleep(5)
            stdin, stdout, stderr = ssh_client.exec_command('vpn tu tlist -y')
            ssh_client.exec_command('mkdir /var/log/VPN_Tool')
            ssh_client.exec_command('mkdir /var/log/VPN_Tool/DB')
            ssh_client.exec_command('cd /var/log/VPN_Tool/DB')
            ssh_client.exec_command('cat $FWDIR/log/iked* | grep -i "fail" > /var/log/VPN_Tool/DB/iked_failures_DB.txt')
            ssh_client.exec_command('cat $FWDIR/log/iked* | grep -i "error" > /var/log/VPN_Tool/DB/iked_errors_DB.txt')
            ssh_client.exec_command('cat /var/log/messages* | grep -i "error" > /var/log/VPN_Tool/DB/messages_errors_DB.txt; sort -M /var/log/VPN_Tool/DB/messages_errors_DB.txt -o /var/log/VPN_Tool/DB/messages_errors_DB.txt')
            ssh_client.exec_command('cat /var/log/messages /var/log/messages.1 /var/log/messages.2 /var/log/messages.3 /var/log/messages.4 | grep -i "fail"  > /var/log/VPN_Tool/DB/messages_failures_DB.txt; sort -M /var/log/VPN_Tool/DB/messages_failures_DB.txt -o /var/log/VPN_Tool/DB/messages_failures_DB.txt')
            ssh_client.exec_command('cat /opt/CPsuite-R81.20/fw1/log/fwk.elg /opt/CPsuite-R81.20/fw1/log/fwk.elg.0 /opt/CPsuite-R81.20/fw1/log/fwk.elg.1 | grep -i "fail" > /var/log/VPN_Tool/DB/fwk_failures_DB.txt; sort -k2M /var/log/VPN_Tool/DB/fwk_failures_DB.txt -o /var/log/VPN_Tool/last_fwk_failures_DB.txt')
            ssh_client.exec_command('cat /opt/CPsuite-R81.20/fw1/log/fwk.elg /opt/CPsuite-R81.20/fw1/log/fwk.elg.0 /opt/CPsuite-R81.20/fw1/log/fwk.elg.1 | grep -i "error" > /var/log/VPN_Tool/DB/fwk_error_DB.txt; sort -k2M /var/log/VPN_Tool/DB/fwk_error_DB.txt -o /var/log/VPN_Tool/last_fwk_error_DB.txt')

            ssh_client.exec_command('cat /var/log/VPN_Tool/DB/iked_failures_DB.txt /var/log/VPN_Tool/DB/iked_errors_DB.txt | grep -i \'Ipv6\|ip6\' > /var/log/VPN_Tool/VPN_IPv6_logs.txt')
            ssh_client.exec_command('cat $FWDIR/log/iked* | grep -i \'error\|fail\'" > /var/log/VPN_Tool/iked_errors.txt')

            time.sleep(5)
            ssh_client.exec_command(
                'start_time=$(date -d \"'+ self.F_date +''+self.F_time+'\" \"+%s\"); end_time=$(date -d \"'+ self.T_date +''+self.T_time+'\" \"+%s\");while '
                'read -r line; do timestamp=$(echo \"$line\" | awk \'{print $1\" \"$2\" \"$3\" \"$4}\');'
                'epoch_time=$('
                'date -d \"$timestamp\" \"+%s\"); if [[ \"$epoch_time\" -ge \"$start_time\" && \"$epoch_time\" -le '
                '\"$end_time\" ]]; then echo \"$line\"; fi; done < \"/var/log/VPN_Tool/DB/messages_errors_DB.txt\"> '
                '/var/log/VPN_Tool/messages_errors.txt')
            ssh_client.exec_command(
                'start_time=$(date -d \"'+ self.F_date +''+self.F_time+'\" \"+%s\"); end_time=$(date -d \"'+ self.T_date +''+self.T_time+'\" \"+%s\");while '
                'read -r line; do timestamp=$(echo \"$line\" | awk \'{print $1\" \"$2\" \"$3\" \"$4}\');'
                'epoch_time=$('
                'date -d \"$timestamp\" \"+%s\"); if [[ \"$epoch_time\" -ge \"$start_time\" && \"$epoch_time\" -le '
                '\"$end_time\" ]]; then echo \"$line\"; fi; done < \"/var/log/VPN_Tool/DB/messages_failures_DB.txt\"> '
                '/var/log/VPN_Tool/messages_failures.txt')

            ssh_client.exec_command('vpn debug truncoff')

            output = stdout.read().decode('utf-8')
            lines = output.split('\n')[1:-1]
            filtered_output = '</br>'.join(lines)

            ssh_client.close()

            return filtered_output

        except paramiko.AuthenticationException as e:
            return f"Authentication failed: {e}"
        except paramiko.SSHException as e:
            return f"Unable to establish SSH connection: {e}"
        except Exception as e:
            return f"Hostname could not be resolved: {e}"

    def vpn_debug(self):
        ssh_client = paramiko.SSHClient()

        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh_client.connect(hostname=self.IP, username=self.username, password=self.password)

            if ssh_client.get_transport().is_active():
                print("Connected to the remote server")
            else:
                print("Failed to connect to the remote server")

            ssh_client.exec_command('vpn debug trunc ALL=5')

            time.sleep(5)
            stdin, stdout, stderr = ssh_client.exec_command('vpn tu tlist -y')
            ssh_client.exec_command('mkdir /var/log/VPN_Tool')
            ssh_client.exec_command('cat $FWDIR/log/iked* | grep -i fail -> /var/log/VPN_Tool/IKED_failures.txt')
            ssh_client.exec_command('cat $FWDIR/log/iked* | grep -i error -> /var/log/VPN_Tool/IKED_errors.txt')
            ssh_client.exec_command('vpn debug truncoff')

            output = stdout.read().decode('utf-8')
            lines = output.split('\n')[1:-1]
            filtered_output = '</br>'.join(lines)

            ssh_client.close()

            return filtered_output

        except paramiko.AuthenticationException as e:
            return f"Authentication failed: {e}"
        except paramiko.SSHException as e:
            return f"Unable to establish SSH connection: {e}"
        except Exception as e:
            return f"Hostname could not be resolved: {e}"
