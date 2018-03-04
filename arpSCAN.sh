#!/bin/bash

fout() {
	if nmcli d | grep -w "wireless"
	then
		(sudo arp-scan --interface=wlan0 --localnet) > arpRESULTS.txt
	else
		(sudo arp-scan -l) > arpRESULTS.txt
	fi
	sleep 0.5
}

fout

SCAN_RESULTS=$(grep 192 < arpRESULTS.txt | awk '{printf ("%5s\t%s\n", $1, $2)}' | sort -u)
echo ""
echo "-----------------------[SCAN RESULTS]---------------------------"
echo ""
echo "$SCAN_RESULTS"
echo ""
