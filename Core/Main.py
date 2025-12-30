#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main Application Controller
"""

import os
import sys
import json
import platform
from pathlib import Path

class MainApplication:
    """Main application controller for AppleOSINT"""
    
    def __init__(self):
        """Initialize the main application"""
        self.base_path = Path(__file__).parent.parent
        self.config_path = self.base_path / "Configuration" / "Configuration.ini"
        self.load_config()
        self.check_platform()
        
    def check_platform(self):
        """Verify we're running on macOS/iOS"""
        if platform.system() != "Darwin":
            raise SystemError("This tool is designed exclusively for Apple devices")
        
        print("DetectMe - [SYSTEM_ACTIVE]")
        print("=" * 50)
        print(f"Running on: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version.split()[0]}")
        print("=" * 50)
        print()
    
    def load_config(self):
        """Load configuration from file"""
        config_file = self.base_path / "Configuration" / "Configuration.ini"
        if not config_file.exists():
            self.create_default_config()
        # Configuration loading logic here
    
    def create_default_config(self):
        """Create default configuration file"""
        config_dir = self.base_path / "Configuration"
        config_dir.mkdir(exist_ok=True)
        
        default_config = {
            "API": {
                "WhoIS_API_Key": "",
                "Shodan_API_Key": ""
            },
            "Proxy": {
                "Enabled": "False",
                "Type": "http",
                "Host": "",
                "Port": "",
                "Username": "",
                "Password": ""
            },
            "Settings": {
                "Timeout": "30",
                "User_Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        }
        
        # Save as INI format (simplified)
        config_file = config_dir / "Configuration.ini"
        with open(config_file, 'w') as f:
            f.write("[API]\n")
            f.write(f"WhoIS_API_Key = {default_config['API']['WhoIS_API_Key']}\n")
            f.write(f"Shodan_API_Key = {default_config['API']['Shodan_API_Key']}\n\n")
            f.write("[Proxy]\n")
            for key, value in default_config['Proxy'].items():
                f.write(f"{key} = {value}\n")
            f.write("\n[Settings]\n")
            for key, value in default_config['Settings'].items():
                f.write(f"{key} = {value}\n")
    
    def run(self):
        """Run the main application"""
        print("\n" + "=" * 60)
        print(" " * 20 + "DetectMe")
        print(" " * 15 + "[SYSTEM_ACTIVE]")
        print("=" * 60)
        print()
        print("Available options:")
        print("  [1] Username Lookup")
        print("  [2] Domain Information")
        print("  [3] Phone Number Lookup")
        print("  [4] Email Lookup")
        print("  [5] Google Dorks")
        print("  [6] Interactive Map")
        print("  [7] Generate Graph")
        print("  [8] GUI Mode")
        print("  [9] Exit")
        print()
        print("-" * 60)
        print()
        
        while True:
            try:
                choice = input("Select an option (1-9): ").strip()
                
                if choice == "1":
                    self.username_lookup()
                elif choice == "2":
                    self.domain_lookup()
                elif choice == "3":
                    self.phone_lookup()
                elif choice == "4":
                    self.email_lookup()
                elif choice == "5":
                    self.google_dorks()
                elif choice == "6":
                    self.interactive_map()
                elif choice == "7":
                    self.generate_graph()
                elif choice == "8":
                    self.launch_gui()
                elif choice == "9":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again.")
                    print()
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                print()
    
    def username_lookup(self):
        """Username lookup functionality"""
        print("\nUsername Lookup")
        print("-" * 30)
        from Core.UsernameLookup import UsernameLookup
        username = input("Enter username to search: ").strip()
        if username:
            lookup = UsernameLookup()
            lookup.search(username)
    
    def domain_lookup(self):
        """Domain lookup functionality"""
        print("\nDomain Information")
        print("-" * 30)
        from Core.DomainLookup import DomainLookup
        domain = input("Enter domain to analyze: ").strip()
        if domain:
            lookup = DomainLookup()
            lookup.analyze(domain)
    
    def phone_lookup(self):
        """Phone number lookup functionality"""
        print("\nPhone Number Lookup")
        print("-" * 30)
        from Core.PhoneLookup import PhoneLookup
        phone = input("Enter phone number: ").strip()
        if phone:
            lookup = PhoneLookup()
            lookup.search(phone)
    
    def email_lookup(self):
        """Email lookup functionality"""
        print("\nEmail Lookup")
        print("-" * 30)
        from Core.EmailLookup import EmailLookup
        email = input("Enter email address: ").strip()
        if email:
            lookup = EmailLookup()
            lookup.search(email)
    
    def google_dorks(self):
        """Google dorks search"""
        print("\nGoogle Dorks")
        print("-" * 30)
        from Core.GoogleDorks import GoogleDorks
        query = input("Enter search query: ").strip()
        if query:
            dorks = GoogleDorks()
            dorks.search(query)
    
    def interactive_map(self):
        """Create interactive map"""
        print("\nInteractive Map")
        print("-" * 30)
        from Core.MapGenerator import MapGenerator
        generator = MapGenerator()
        generator.create_map()
    
    def generate_graph(self):
        """Generate information graph"""
        print("\nGenerate Graph")
        print("-" * 30)
        from Core.GraphGenerator import GraphGenerator
        generator = GraphGenerator()
        generator.create_graph()
    
    def launch_gui(self):
        """Launch GUI mode"""
        print("\nLaunching GUI...")
        try:
            import tkinter
        except ImportError:
            print("Error: tkinter is not available.")
            print("   On macOS, tkinter should be included with Python.")
            print("   Try: brew install python-tk")
            return
        
        try:
            from GUI.App import GUIApplication
            app = GUIApplication()
            app.run()
        except ImportError as e:
            print(f"❌ GUI module import failed: {str(e)}")
            print("   Missing dependencies. Please install requirements:")
            print("   pip3 install -r requirements.txt")
            print("   Or run: ./install.sh")
        except Exception as e:
            print(f"❌ Error launching GUI: {str(e)}")
            import traceback
            traceback.print_exc()

