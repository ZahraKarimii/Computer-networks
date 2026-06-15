
from Filter import filter_manager
import os

def show_menu():
    print("Proxy blacklist manager")
    print("=======================")
    print("1) Show blacklist")
    print("2) Add domain")
    print("3) Remove domain")
    print("4) Reload from file")
    print("0) Exit")

def main():
    while True:
        show_menu()
        choice = input("Choice: ").strip()
        if choice == "1":
            for d in sorted(filter_manager.blacklist):
                print(" -", d)
            print()
        elif choice == "2":
            dom = input("Domain to add (e.g. badsite.com): ").strip()
            if dom:
                filter_manager.add(dom)
                print("Added.")
        elif choice == "3":
            dom = input("Domain to remove: ").strip()
            if dom:
                filter_manager.remove(dom)
                print("Removed (if existed).")
        elif choice == "4":
            filter_manager.load()
            print("Reloaded.")
        elif choice == "0":
            break
        else:
            print("Unknown option.")
        input("return to menu")
        os.system('cls')

if __name__ == "__main__":
    main()
