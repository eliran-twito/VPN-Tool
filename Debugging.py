import socket
import time
from datetime import datetime,timedelta

import paramiko


class DebugSSH(object):
    def __init__(self, IP, username, password, F_date, F_time, T_date, T_time):
        self.IP = IP
        self.username = str(username)
        self.password = str(password)
        full_f_date = datetime.strptime(F_date, "%Y-%m-%d")
        formatted_date1 = full_f_date.strftime("%b %d").strip()
        self.F_date = str(formatted_date1)
        full_t_date = datetime.strptime(T_date, "%Y-%m-%d")
        formatted_date2 = full_t_date.strftime("%b %d ").strip()
        self.T_date = str(formatted_date2)
        full_f_time = datetime.strptime(F_time, "%H:%M:%S")
        formatted_time1 = full_f_time.strftime("%H:%M")
        self.F_time = str(formatted_time1)
        full_t_time = datetime.strptime(T_time, "%H:%M:%S")
        formatted_time2 = full_t_time.strftime("%H:%M")
        self.T_time = str(formatted_time2)

    def generate_date_range(self):
        start_date = datetime.strptime(self.F_date, "%b %d")
        end_date = datetime.strptime(self.T_date, "%b %d")

        date_range = [(start_date + timedelta(days=i)).strftime("%d %b") for i in
                      range((end_date - start_date).days + 1)]
        return "|".join(date_range)

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
            ssh_client.exec_command('cat $FWDIR/log/iked* | grep -E -i "Dropping packet|error|fail|Could not get SAs|failed to find SA|internal error|dropped|tunnel is not yet established|MEP_chosen_gw_g: failed to get entry" > /var/log/VPN_Tool/DB/iked_DB.txt')
            ssh_client.exec_command('cat /var/log/messages* | grep -E -i "Dropping packet|error|fail|Could not get SAs|failed to find SA|internal error|dropped|tunnel is not yet established|MEP_chosen_gw_g: failed to get entry" > /var/log/VPN_Tool/DB/messages_errors_DB.txt; sort -M /var/log/VPN_Tool/DB/messages_errors_DB.txt -o /var/log/VPN_Tool/DB/messages_errors_DB.txt')
            ssh_client.exec_command('cat $FWDIR/log/fwk.elg* | grep -E -i "Dropping packet|error|fail|Could not get SAs|failed to find SA|internal error|dropped|tunnel is not yet established|MEP_chosen_gw_g: failed to get entry" > /var/log/VPN_Tool/DB/fwk_failures_DB.txt; sort -k2M /var/log/VPN_Tool/DB/fwk_failures_DB.txt -o /var/log/VPN_Tool/DB/fwk_failures_DB.txt')

            time.sleep(5)

            date_range_pattern = self.generate_date_range()
            print(date_range_pattern)


            ssh_client.exec_command(f'cat /var/log/VPN_Tool/DB/fwk_failures_DB.txt | grep -E -i "{date_range_pattern}" > /var/log/VPN_Tool/Filtered_fwk_failures.txt')
            ssh_client.exec_command(f'cat /var/log/VPN_Tool/DB/iked_failures_DB.txt | grep -E -i "{date_range_pattern}" > /var/log/VPN_Tool/Filtered_iked_failures.txt')
            ssh_client.exec_command(f'cat /var/log/VPN_Tool/DB/messages_errors_DB.txt | grep -E -i "{date_range_pattern}" > /var/log/VPN_Tool/Filtered_messages_errors.txt')
            ssh_client.exec_command('cat /var/log/VPN_Tool/Filtered_fwk_failures.txt /var/log/VPN_Tool/Filtered_iked_failures.txt /var/log/VPN_Tool/Filtered_messages_errors.txt | grep -i \'Ipv6\|ip6\' > /var/log/VPN_Tool/IPv6_logs.txt')

            print(self.F_date,self.F_time)

            ssh_client.exec_command('vpn debug truncoff')


            stdin, stdout, stderr = ssh_client.exec_command('grep -E -c "outSPI_to_instance_g: failed to get entry, -1|inSPI_to_instance_g: failed to get entry, -1" /var/log/VPN_Tool/Filtered_fwk_failures.txt')
            result = stdout.read().decode('utf-8').strip()
            print(result)

            count = int(result) if result.isdigit() else 0

            if count >= 10:
                additional_output = (
                    "<br><b>Issues found:</b><br><br>"
                    "# There are a lot of 'inSPI / outSPI failed to get entry -1' messages inside fwk.elg during the time you searched for.<br>"
                    "This could be just cosmetic. For more info, please use the Solution repository.<br>"
                )
            else:
                additional_output = ""

            output = stdout.read().decode('utf-8')
            lines = output.split('\n')[1:-1]
            filtered_output = '</br>'.join(lines)

            ssh_client.close()

            return additional_output+filtered_output

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
            ssh_client.exec_command('mkdir /var/log/VPN_Tool/DB')
            ssh_client.exec_command('cd /var/log/VPN_Tool/DB')
            ssh_client.exec_command('fw ctl debug 0;fw ctl debug -buf 32000;fw ctl debug -m fw + conn drop packet;fw ctl debug -m VPN + all;fwaccel dbg -m vpn all;fw ctl debug -m fg + all;fw ctl kdebug -T -f > /var/log/VPN_Tool/DB/kern_debug.txt')
            time.sleep(10)
            ssh_client.exec_command('fw ctl debug 0;fw ctl debug 0')
            ssh_client.exec_command('cat /var/log/VPN_Tool/DB/kern_debug.txt | grep -E -i "Dropping packet|error|fail|Could not get SAs|failed to find SA|internal error|dropped|tunnel is not yet established|MEP_chosen_gw_g: failed to get entry" > /var/log/VPN_Tool/DB/kern_debug_errors.txt')
            ssh_client.exec_command('cat $FWDIR/log/iked* | grep -E -i "Dropping packet|error|fail|Could not get SAs|failed to find SA|internal error|dropped|tunnel is not yet established|MEP_chosen_gw_g: failed to get entry" > /var/log/VPN_Tool/DB/Advanced_iked_DB.txt')
            ssh_client.exec_command('vpn debug truncoff')

            date_range_pattern = self.generate_date_range()
            ssh_client.exec_command(f'cat /var/log/VPN_Tool/DB/Advanced_iked_DB.txt | grep -E -i "{date_range_pattern}" > /var/log/VPN_Tool/Filtered_Advanced_iked_DB.txt')

            # Count specific error messages
            stdin, stdout, stderr = ssh_client.exec_command('grep -c "0.0.0.0:8116" /var/log/VPN_Tool/DB/kern_debug_errors.txt')
            result = stdout.read().decode('utf-8').strip()
            print(result)


            count = int(result) if result.isdigit() else 0

            if count >= 10:
                additional_output = (
                    "<br><b>Issues found:</b><br><br>"
                    "#I detected a lot of CCP connections '0.0.0.0:8116' are being dropped,<br>"
                    "please check if your GW is associated with another VSX being on the same VLAN.<br>"
                )
            else:
                additional_output = ""



            output = stdout.read().decode('utf-8')
            lines = output.split('\n')[1:-1]
            filtered_output = '</br>'.join(lines)

            ssh_client.close()

            return additional_output+filtered_output

        except paramiko.AuthenticationException as e:
            return f"Authentication failed: {e}"
        except paramiko.SSHException as e:
            return f"Unable to establish SSH connection: {e}"
        except Exception as e:
            return f"Hostname could not be resolved: {e}"

        print(formatted_date1)
