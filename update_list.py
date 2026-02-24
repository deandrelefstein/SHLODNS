import requests
import datetime

# Your sources
urls = [
    "https://raw.githubusercontent.com/deandrelefstein/FAM-DNS-1/main/MY_RULES.txt", 
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt",
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/nsfw.txt",
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/gamble.txt",
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/doh-vpn-proxy-bypass.txt",
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/popupads.txt"
]

def main():
    combined_rules = set() 
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for url in urls:
        print(f"Fetching {url}...")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for line in lines:
                    if line and not line.startswith(("!", "#", "[Adblock")):
                        combined_rules.add(line)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    # Convert to a sorted list for processing
    final_rules = sorted(list(combined_rules))

    # --- 1. GENERATE STRICT LIST (Includes YouTube Restriction) ---
    with open("master_strict.txt", "w") as f:
        f.write(f"! Title: SHLOMO-STRICT\n")
        f.write(f"! Updated: {timestamp}\n")
        f.write("! Includes: Ads, Malware, Gambling, SafeSearch, YouTube Restricted\n\n")
        for rule in final_rules:
            f.write(f"{rule}\n")

    # --- 2. GENERATE LITE LIST (Removes YouTube Restriction) ---
    # We filter out any line containing 'restrict.youtube.com'
    with open("master_lite.txt", "w") as f:
        f.write(f"! Title: SHLOMO-LITE\n")
        f.write(f"! Updated: {timestamp}\n")
        f.write("! Includes: Ads, Malware, Gambling, SafeSearch (No YouTube Restriction)\n\n")
        for rule in final_rules:
            if "restrict.youtube.com" not in rule:
                f.write(f"{rule}\n")

    print(f"Update Complete at {timestamp}")

if __name__ == "__main__":
    main()
