import requests

# The "Raw" links we discussed earlier
urls = [
    "https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt",
    "https://big.oisd.nl/",
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/multi.txt",
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/nsfw.txt",
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/gamble.txt",
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/doh-vpn-proxy-bypass.txt",
    "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/popupads.txt"
]

def main():
    combined_rules = set() # Using a 'set' automatically removes duplicates
    
    for url in urls:
        print(f"Fetching {url}...")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Split by line and add to our set
                lines = response.text.splitlines()
                for line in lines:
                    # Ignore comments and empty lines to keep it clean
                    if line and not line.startswith(("!", "#", "[Adblock")):
                        combined_rules.add(line)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    # Save everything to your master file
    with open("master.txt", "w") as f:
        f.write("! --- AUTOMATED MASTER LIST ---\n")
        f.write("! Updated daily via GitHub Actions\n\n")
        for rule in sorted(combined_rules):
            f.write(f"{rule}\n")

if __name__ == "__main__":
    main()
