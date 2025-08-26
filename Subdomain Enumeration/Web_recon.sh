#!/bin/bash

baseDir="/root/BugBounty/Recon/targets"  # Base directory for your target programs // we'll need to craete: a directory with target name and "roots.txt" file containing the target domain (e.g hackerone.com)

if [[ -d "$baseDir" ]]; then
    for dir in "$baseDir"/*/; do
        if [[ -f "${dir}/roots.txt" ]]; then
            programName=$(basename "$dir")
            echo -e "\n--> Grabbing subdomains for $programName...\n"

            rootDomains="${dir}/roots.txt"
            
            # files for each tool
            subfinderOutput="${dir}/subfinder.txt"
            assetfinderOutput="${dir}/assetfinder.txt"
            amassOutput="${dir}/amass.txt"
            finalOutput="${dir}/unique_domains.txt"
            resolvedOutput="${dir}/resolved.txt"
            liveHostsOutput="${dir}/live_hosts.txt"

            ####### ------------------------------ Subfinder -----------------------------------------
            echo "-> Running subfinder..."
            subfinder -dL "$rootDomains" -silent | tee "$subfinderOutput"

            ####### ------------------------------ Assetfinder ---------------------------------------
            echo "-> Running assetfinder..."
            while read domain; do
                assetfinder --subs-only "$domain"
            done < "$rootDomains" | tee "$assetfinderOutput"

            ####### ------------------------------ Amass ---------------------------------------------
            echo "-> Running amass..."
            while read domain; do
                amass enum -passive -d "$domain"
            done < "$rootDomains" | tee "$amassOutput"

            ####### ------------------------------ Final Merge ----------------------------------------
            echo "-> Merging all subdomains and removing duplicates..."
            cat "$subfinderOutput" "$assetfinderOutput" "$amassOutput" | sort -u > "$finalOutput"

            total=$(wc -l < "$finalOutput")
            echo "-> Total unique subdomains found for $programName: $total"
            
            ###### ------------------------------ DNSX Resolution -------------------------------------
            echo "-> Resolving subdomains with dnsx..."
            cat "$finalOutput" | dnsx -silent -resp-only > "$resolvedOutput"
            resolvedCount=$(wc -l < "$resolvedOutput")
            echo "-> Total resolving subdomains for $programName: $resolvedCount"

            ####### ------------------------------ HTTPX Live Check & Telegram Notification ------------------------------------
            echo "Probing live HTTP/S subdomains with httpx..."
            cat "$finalOutput" | httpx -silent -status-code -title -content-length -threads 50 | tee "$liveHostsOutput" |  notify --silent        
            
            liveCount=$(wc -l < "$liveHostsOutput")
            echo "-> Total live HTTP(S) domains for $programName: $liveCount" 
            
        fi
    done
fi
