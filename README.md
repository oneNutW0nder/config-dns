# config-dns
A python script that helps you configure DNS zone files. Made for CSEC 743 at RIT.

Everything you need to configure can be found in the `header.conf` and `host.conf` files. The python script `dnsconfig.py` will handle the backup and generation of both the _forward_ and _reverse_ zone files. 

## Usage

1. Configure the `header.conf` file.

    This file contains the header of a dns zone file. The script will read the `header.conf` file and use it for the zone files it will generate. Nothing in this file is custom or required for the script to execute properly. It must be complient with whatever DNS zone file format you choose to use though.

2. Configure the `host.conf` file.

    This file contains the host and domain information. You can also specify where your current _zone file_ and _reverse zone file_ are located on your file system. The script will take these paths and use them to create backups of your current configuration and write the new files to those locations.

    ### Configuration Options:

    - `ZONE_FILE:` --> This is the path to the forward zone file
    - `REVERSE_ZONE_FILE:` --> This is the path to the reverse zone file
    - `DOMAIN:` --> Specifies a record for a domain and the namerserver records for that domain.
    - `HOST:` --> Specifies a host record

    Please see the example `host.conf` file for example entries.

3. Run the script

    After you have configured the previous files you are ready to run the script. The script will use the configuration files to build your new zone files. Before creating the new files, the script will backup your current configuration to the directory you ran the script from. The backup will have the name of `zoneFile.bak` and `reverseFile.bak`. The new zone files that are created will have the same names as before.

    Please note, you should never trust a tool to perform backups for you. It is your responsibility to ensure your data is backed up prior to running this tool. 

    After running the script, you should be good to go!
