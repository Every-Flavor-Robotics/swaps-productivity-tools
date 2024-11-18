

# Setting Up mDNS on a Raspberry Pi (Ubuntu 24.04)

This guide explains how to configure your Raspberry Pi running Ubuntu 24.04 to be accessible on the local network via `pi4.local` using mDNS.

---

1. Install Avahi

Avahi provides mDNS support for Ubuntu.

```bash
sudo apt update
sudo apt install avahi-daemon avahi-utils -y
```

2. Verify the Avahi Service

Ensure that the avahi-daemon is running and starts on boot.

```bash
sudo systemctl start avahi-daemon
sudo systemctl enable avahi-daemon
sudo systemctl status avahi-daemon
```

3. Set the Hostname

Change the hostname to identify the device

```bash
sudo hostnamectl set-hostname <HOSTNAME?
```

Verify the hostname:
```bash
hostname
```

4. Edit the hosts File

Update the /etc/hosts file to include the new hostname.

```bash
sudo nano /etc/hosts
```

Ensure it contains the following:

```
127.0.1.1    pi4
```

Save and close the file.

5. Restart Avahi

Restart the Avahi service to apply changes.

```bash
sudo systemctl restart avahi-daemon
```

6. Test mDNS

From another device on the same network, test the setup:

```bash
ping pi4.local
```

You should receive a response from the Raspberry Pi.

Troubleshooting

	•	Make sure all devices are on the same local network.
	•	Check for firewall rules that might block UDP port 5353.

Your Raspberry Pi is now accessible at pi4.local!

