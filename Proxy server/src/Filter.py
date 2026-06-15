
import os
from Config import BLACKLIST_FILE

class Filter:
    def __init__(self, filename=BLACKLIST_FILE):
        self.filename = filename
        self.blacklist = set()
        self.load()


    def load(self):
        self.blacklist.clear()
        if not os.path.exists(self.filename):
            try:
                open(self.filename, "a", encoding="utf-8").close()
            except:
                pass
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                for line in f:
                    domain = line.strip().lower()
                    if domain:
                        self.blacklist.add(domain)
        except Exception:
            pass


    def save(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                for domain in sorted(self.blacklist):
                    f.write(domain + "\n")
        except Exception:
            pass


    def add(self, domain: str):
        domain = domain.strip().lower()
        if domain:
            self.blacklist.add(domain)
            self.save()


    def remove(self, domain: str):
        domain = domain.strip().lower()
        if domain in self.blacklist:
            self.blacklist.remove(domain)
            self.save()


    def is_blocked(self, url: str) -> bool:
        try:
            domain = url.split("://")[-1].split("/")[0].split(":")[0].lower()
            for b in self.blacklist:
                if domain == b or domain.endswith("." + b):
                    return True
        except Exception:
            pass
        return False


filter_manager = Filter()
