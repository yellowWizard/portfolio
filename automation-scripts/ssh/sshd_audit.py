"""
    sshd_audit.py
    Automates the hardening of /etc/ssh/sshd_config by enforcing secure options,
    validating syntax, and safely restarting the SSH daemon.
"""

import shutil
import sys
import os
import subprocess
from datetime import datetime

def sshd_audit(sshd_tmp: str, sshd_bak: str, sshd_options: dict, sshd_config: str) -> list:
    #Parses the SSHD configuration, enforces specified options, and remove duplicates
    if os.getuid() != 0:
        print('Error: Script Must be run as Root!')
        sys.exit(1)
    processed_opt = []
    try:
        print('Creating a backup copy...')
        shutil.copy2(sshd_config, sshd_bak)
        print(f'Done.\nOpening Files...')
        with (
            open(sshd_config, 'r', encoding='UTF-8') as config_file,
            open(sshd_tmp, 'w', encoding='UTF-8') as tmp_file
        ):
            for line in config_file:
                clean_line = line.strip()
                # Strip Commented options to inspect the undlerlyin option
                if clean_line.startswith('#'):
                    clean_line = clean_line.replace('#', '', 1)
                clean_line = clean_line.split()
                # Process standard directive lines (Key Value)
                if len(clean_line) == 2:
                    for option in sshd_options.keys():
                        if option == clean_line[0]:
                            # Drop the line if the option was already configured
                            if option in processed_opt:
                                line = ''
                                break

                            processed_opt.append(option)
                            print(f'Setting: {option} {sshd_options[option]} option...')
                            
                            # Update value if it doesn't match the target configuration
                            if clean_line[1] != sshd_options[option]:
                                clean_line[1] = sshd_options[option]
                            
                            clean_line = ' '.join(clean_line)
                            line = clean_line + '\n'
                            break

                tmp_file.write(line)
    except Exception as e:
        print(f' Error during audit phase: {e}')
        if os.path.exists(sshd_tmp):
            os.remove(sshd_tmp)
        sys.exit(1)
    # Append configuration options that were completely mising from the original file
    if len(processed_opt) != len(sshd_options):
        print(f'\n\tWarning: configuration file Does not use standard format')
        print(f'Appending mising required options...')
        try:
            with open(sshd_tmp, 'a', encoding='UTF-8') as config_file:
                config_file.write('# +--------------- Added By ssh_audit.py -----------------+\n')
                for option in sshd_options.keys():
                    if not option in processed_opt:
                        config_file.write(f'{option} {sshd_options[option]}\n')
                config_file.write('# +--------------- End Of Added by ssh_audit.py conf --------------+\n')
        except Exception as e:
                print(f'Error writing missing options: {e}')
                sys.exit(1)

def check_syntax(sshd_tmp: str):
    # Validates the syntax of the generated configuration file
    cmd = ['sshd', '-t', '-f', sshd_tmp]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f'Syntax error in generated configuration: {res.stderr}')
        sys.exit(1)

def replace_file_with_perm(sshd_tmp: str, sshd_bak: str, sshd_config:str):
    # Secures file permission(0600 root:root) and moves the file atomically
    try:
        print(f'Setting Owner.')
        os.chown(sshd_tmp, 0, 0)
        os.chown(sshd_bak, 0, 0)
        print(f'Setting Permission.')
        os.chmod(sshd_tmp, 0o600)
        os.chmod(sshd_bak, 0o600)
        print(f'Replacing...')
        os.replace(sshd_tmp, sshd_config)
    except Exception as e:
        print(f'Error while replacing file: {e}')
        sys.exit(1)
# Restart sshd and print status
def restart_sshd():
    # Reloads/Restart the SSH daemon and prints its current systemd status
    cmd = ['systemctl', 'restart', 'sshd']
    try:
        print('Restarting sshd process...')
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f'Error restarting SSH daemon: {e}')
        sys.exit(1)

    print('Completed.\n\nPrinting Status:')
    cmd = ['systemctl', 'status', 'sshd']
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)

if __name__ == '__main__':
    SSHD_CONFIG = '/etc/ssh/sshd_config'
    SSHD_OPTIONS = {
            'Port': '2222',
            'PermitRootLogin': 'no', 
            'PasswordAuthentication': 'no',
            'PubkeyAuthentication': 'yes'
    }
    time = datetime.now().strftime('%Y%m%d_%H%M%S')
    sshd_tmp = f'{SSHD_CONFIG}.tmp.{time}'
    sshd_bak = f'{SSHD_CONFIG}.bak.{time}'
    sshd_audit(sshd_tmp, sshd_bak, SSHD_OPTIONS, SSHD_CONFIG)
    check_syntax(sshd_tmp)
    replace_file_with_perm(sshd_tmp, sshd_bak, SSHD_CONFIG)
    restart_sshd()


    



