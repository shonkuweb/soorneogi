import glob

html_files = glob.glob('*.html')
old_logo_url = "https://lh3.googleusercontent.com/aida-public/AB6AXuAF-XiQmcThBlT4IfVz-N2XrE1vE-m06Avgnz9149xtN-HUFEXWQ52qVnPxJR2ARytAErB7XGtlaXAqVsWovV8qCDr6U5Zu1F5qEu7fzfXWEm1iog_QbFicXOc2Rd-WwbQt0ojC2L9pcHVIKuQwdQF2gbxgrBdWfFgclSRLlx-UBCpLScDO3xNaY14MF9l5hiMqVy64nLFKfoS-LKm4nku3vN3mJVrm9pCBHNKSBYlBJLGYyYAzhighE4HJLtA4qqPMy0L7xDnBRVb3"

for file in html_files:
    with open(file, 'r') as f:
        content = f.read()

    # If it was admin.html, it had an illustrations link. We can just replace all instances of soor_neogi_logo.png
    content = content.replace('images/soor_neogi_logo.png', old_logo_url)

    with open(file, 'w') as f:
        f.write(content)
        
    print(f"Restored logo in {file}")

