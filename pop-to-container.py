import fabric
import time
import getpass
import sys

PROFILES = {
    'factchecking': {
        'container_ip': '10.179.127.25',
        'user': 'np278'
    },
    'brat': {
        'container_ip': '10.179.127.60',
        'user': 'np278'
    },
    'bratd': {
        'container_ip': '10.179.127.60',
        'user': 'db57'
    },
    'qhs': {
        'container_ip': '10.179.127.216',
        'user': 'db57'
    },
    'intek': {
        'container_ip': '10.179.127.160',
        'user': 'ca296'
    }
}


if len(sys.argv) < 2:
    raise Exception('use a profile name as the first argument')

profile_name = sys.argv[1]
profile = PROFILES[profile_name]

user = profile['user']

print("Loaded profile for user {}.".format(user))

# Establish contact with perimeter host
print("I will now prompt you for your password for unix.uscs.susx.ac.uk.")
password = getpass.getpass()
options = {
    'password': password,
    'banner_timeout': 200,
    'timeout': 200,
    'auth_timeout': 200
}
c = fabric.Connection('unix.uscs.susx.ac.uk', user=user, connect_kwargs=options)

## xx handle case where local port is busy
local_port = 49152
remote_host = 'shl1.inf.susx.ac.uk'
remote_port = 22

with c.forward_local(
        local_port,
        remote_port=remote_port,
        remote_host=remote_host,
        local_host='localhost'
): 
    print("Set up tunnel successfully.")

    # Note that user spec is *required* here because it may differ.  Note that we
    # assume you use the same pass for both hosts.  May not be valid assumption.
    c2 = fabric.Connection('localhost', user=user, port=local_port, connect_kwargs=options)

    print("Running a test command on shl1.")
    c2.run("/bin/true")
    print("Test command succeeded.")

    print("Now use your root password for the container; wait for the prompt.")
    print("You might receive a prompt about an unknown key fingerprint; if so, enter 'yes' to continue connecting.")
    container_ssh_command = "ssh root@{}".format(profile['container_ip'])
    c2.run(container_ssh_command, pty=True)

    print("SSH session to container terminated.")

print("Tunnel has been stopped.")
