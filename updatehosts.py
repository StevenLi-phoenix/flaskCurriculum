import time

import rawdnsquery

hosts_file = open("hosts","r")
before_text = hosts_file.read().split("# GitHub Start\n")
before_text, after_text = before_text[0], before_text[1].split("# GitHub End\n")
hosts, after_text = after_text[0], after_text[1]
urls = []
for host in hosts.split("\n"):
    if host:
        ip, url = host.split(" ")[0], host.split(" ")[1]
        urls.append(url)
hosts = []
for url in set(urls):
    for ip in rawdnsquery.decode_message_ip(rawdnsquery.queryAddress(url)):
        s = f"{ip} {url}"
        print(s)
        hosts.append(s)
    time.sleep(0.1)
hosts = "\n".join(hosts) + "\n"
hosts_file = open("hosts","w")
s = before_text + "# GitHub Start\n" + hosts + "# GitHub End\n" + after_text
print(s)
hosts_file.write(s)