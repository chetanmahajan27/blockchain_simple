import os
import paramiko
import sys

def get_transfer_id(tf_id):
    # write code to read from the MSTransferID.txt file and get the values in variables
    # MSTransferID.txt is expected to be in the same directory as this script
    # The file contains a single line with the transfer ID
    # and line is pipe delimited, get all variables from the line
    transfer_id = None
    try:
        with open('MSTransferID.txt', 'r') as file:
            line = file.readline().strip()
            transfer_id = line.split('|')[0]  # Assuming the first value is the transfer ID
            remote_user = line.split('|')[1]  # Assuming the second value is the remote user
            remote_host = line.split('|')[2]
            remote_path = line.split('|')[3]
        except FileNotFoundError:
            print("Error: MSTransferID.txt file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None
    if(transfer_id == tf_id):
        print("Transfer ID found.")
        return transfer_id, remote_user, remote_host, remote_path
    else:
        print("Transfer ID not found.")
        return None, None, None, None

def sftp_to_ecg(transfer_id, local_file, remote_file):
    """
    Transfer a file from local to remote using SFTP.
    
    Args:
        transfer_id (str): The ID for the transfer session.
        local_file (str): The path to the local file to be transferred.
        remote_file (str): The path on the remote server where the file will be stored.
    
    Returns:
        bool: True if the transfer was successful, False otherwise.
    """
    # Check if local file exists
    if not os.path.exists(local_file):
        print(f"Error: Local file {local_file} does not exist.")
        return False  
        
    print(f"Transfer ID: {transfer_id}")
    print(f"Transferring {local_file} to {remote_file}...")

    transfer_params = get_transfer_id(transfer_id)
    if transfer_params is None:
        print("Transfer parameters not found.")
        return False
    else:
        transfer_id, remote_user, remote_host, remote_path = transfer_params
        print(f"Remote User: {remote_user}")
        print(f"Remote Host: {remote_host}")
        print(f"Remote Path: {remote_path}")
        #write paramiko commands to send the file
        try:
            # Create an SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Connect to the remote server
            ssh.connect(remote_host, username=remote_user)
            
            # Create an SFTP session
            sftp = ssh.open_sftp()
            
            # Transfer the file
            sftp.put(local_file, os.path.join(remote_path, remote_file))
            
            # Close the SFTP session and SSH connection
            sftp.close()
            ssh.close()
            
            print(f"Successfully transferred {local_file} to {remote_file}.")
            return True
        
        except Exception as e:
            print(f"An error occurred during SFTP transfer: {e}")
            return False