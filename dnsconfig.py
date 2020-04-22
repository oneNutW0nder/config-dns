def readHeader():
    """
    This function reads the "header.conf" file which is where the
    dns options for the zone file
    
    :return: (string)the contents of the "header.conf" file
    """
    with open("./header.conf", "r") as fd:
        header = fd.readlines()
    return header


def backup(zoneFile, reverseZoneFile):
    """
    This function backs up the current zoneFile and reverseZoneFile
    if they exist so you can restore a previous version
    
    :param zoneFile:        The path that was specified for the forward zone 
                            in the "host.conf" file
    :param reverseZoneFile: The path that was specified for the reverse zone
                            in the "host.conf" file
    """
    # Backup the forward zone file if it exists
    if zoneFile is not None:
        with open(zoneFile, "r") as fd:
            zoneBackup = fd.readlines()

        with open("./zoneFile.bak", "w") as fd:
            fd.writelines(zoneBackup)

    # Backup the reverse zone file if it exists
    if reverseZoneFile is not None:
        with open(reverseZoneFile, "r") as fd:
            reverseZoneBackup = fd.readlines()

        with open("./reverseFile.bak", "w") as fd:
            fd.writelines(reverseZoneBackup)


def readConfig():
    """
    This function reads the provided "host.conf" file and parses
    the information contained in it. It will parse out Hosts,
    Zone file, and Reverse zone file locations.
    
    :return: (4)tuple of a (string)zoneFile location, 
                (string)reverseZoneFile location,
                (list of (3)tuple)Hosts,
                (list of (3)tuple)Domains
    """
    hosts = []
    domains = []
    with open("./host.conf", "r") as fd:
        for line in fd.readlines():
            line = line.strip().split()
            if line != []:
                # Parse config for zone files and hosts
                if line[0] == "ZONE_FILE:":
                    zoneFile = line[1]
                if line[0] == "REVERSE_ZONE_FILE:":
                    reverseZoneFile = line[1]
                if line[0] == "HOST:":
                    hosts.append((line[1], line[2], line[3]))
                if line[0] == "DOMAIN:":
                    domains.append((line[1], line[2], line[3]))

    return zoneFile, reverseZoneFile, hosts, domains


def createZoneFile(zoneFile, header, hosts, domains):
    """
    This function creates the forward zone file configuration based on
    the configuration provided in "host.conf"
    
    :param zoneFile: (string) The path to the zonefile that you want to create
    :param header: (string) The header to use from "./header.conf"
    :param hosts: (list of (3)tuples) Contains the information for each host
    :param domains: (list of (3)tuples) Contains information for each domain
    """
    # Overwrite the old zoneFile with the header and host information
    with open(zoneFile, "w") as fd:
        fd.writelines(header)
        fd.write("\n")

        # Domains and Hosts should have the same number in the config
        for x in range(len(domains)):
            # Format for forward zone file:
            # example.com. IN NS ns.example.com.
            # ns.example.com. IN A 192.168.1.1
            try:
                lineToWrite = (
                    f"{domains[x][0]}\t\tIN\t{domains[x][1]}\t{domains[x][2]}\n"
                )
                fd.write(lineToWrite)

                lineToWrite = f"{hosts[x][0]}  \tIN\t{hosts[x][1]}\t{hosts[x][2]}\n"
                fd.write(lineToWrite)
            except IndexError as e:
                print(e)
                print(
                    "[!] Make sure HOST and DOMAIN entries are 1:1 in the 'host.conf'"
                )
                exit()


def createReverseZoneFile(reverseZoneFile, header, hosts, domains):
    """
    This function creates the reverse zone file from the "host.conf" info
    
    :param reverseZoneFile: (string) path to reverse zonefile to create
    :param header: (string) The header to use from "./header.conf"
    :param hosts: (list of (3)tuples) Contains the information for each host
    :param domains: (list of (3)tuples) Contains information for each domain
    """
    # Overwrite the old reverseZoneFile with the header and host information
    with open(reverseZoneFile, "w") as fd:
        fd.writelines(header)
        fd.write("\n")

        for x in range(len(hosts)):
            # Format for reverse zone file:
            # 1.168.192.in-addr.arpa. IN NS ns.example.com
            # 1.168.192.in-addr.arpa. IN NS ns2.example.com
            try:
                ip = hosts[x][2].split(".")
                arpa = ip[2] + "." + ip[1] + "." + ip[0] + ".in-addr.arpa."

                lineToWrite = f"{arpa} \tIN \tNS \t{hosts[x][0]}\n"
                fd.write(lineToWrite)
            except IndexError as e:
                print(e)
                print(
                    "[!] If this error occurs please look at the \
                    'createReverseZoneFile()' function because this should never happen"
                )
                exit()


if __name__ == "__main__":

    # Read the config file for the information about hosts and the current zone file
    zoneFile, reverseZoneFile, hosts, domains = readConfig()
    header = readHeader()

    # backup the current zone files
    backup(zoneFile, reverseZoneFile)

    # Create new zone files
    createZoneFile(zoneFile, header, hosts, domains)
    createReverseZoneFile(reverseZoneFile, header, hosts, domains)
