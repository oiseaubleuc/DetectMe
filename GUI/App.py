#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modern GUI Application for AppleOSINT
Professional, discreet design for macOS
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
from pathlib import Path
import sys
import os
import threading

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Core modules with error handling
try:
    from Core.UsernameLookup import UsernameLookup
except ImportError as e:
    UsernameLookup = None

try:
    from Core.DomainLookup import DomainLookup
except ImportError as e:
    DomainLookup = None

try:
    from Core.PhoneLookup import PhoneLookup
except ImportError as e:
    PhoneLookup = None

try:
    from Core.EmailLookup import EmailLookup
except ImportError as e:
    EmailLookup = None

try:
    from Core.GoogleDorks import GoogleDorks
except ImportError as e:
    GoogleDorks = None

try:
    from Core.MapGenerator import MapGenerator
except ImportError as e:
    MapGenerator = None

try:
    from Core.GraphGenerator import GraphGenerator
except ImportError as e:
    GraphGenerator = None

class ModernGUI:
    """Modern, professional GUI application"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.load_theme()
        self.root = tk.Tk()
        self.setup_window()
        self.create_modern_ui()
    
    def load_theme(self):
        """Load theme from configuration"""
        theme_file = self.base_path / "GUI" / "Theme" / "Mode.json"
        try:
            if theme_file.exists():
                with open(theme_file, 'r') as f:
                    theme_data = json.load(f)
                    self.theme = theme_data.get("Color", {}).get("Background", "Dark")
            else:
                self.theme = "Dark"
        except:
            self.theme = "Dark"
        
        # Zwart-wit-groen spy kleurenschema
        self.colors = {
            "Dark": {
                "bg": "#000000",
                "fg": "#ffffff",
                "secondary_bg": "#0a0a0a",
                "tertiary_bg": "#1a1a1a",
                "accent": "#00ff00",
                "accent_hover": "#00dd00",
                "button_bg": "#0a0a0a",
                "button_fg": "#00ff00",
                "button_hover": "#1a1a1a",
                "entry_bg": "#0a0a0a",
                "entry_fg": "#ffffff",
                "border": "#00ff00",
                "success": "#00ff00",
                "warning": "#ffff00",
                "error": "#ff0000",
                "text_muted": "#888888",
            },
            "Light": {
                "bg": "#000000",
                "fg": "#ffffff",
                "secondary_bg": "#0a0a0a",
                "tertiary_bg": "#1a1a1a",
                "accent": "#00ff00",
                "accent_hover": "#00dd00",
                "button_bg": "#0a0a0a",
                "button_fg": "#00ff00",
                "button_hover": "#1a1a1a",
                "entry_bg": "#0a0a0a",
                "entry_fg": "#ffffff",
                "border": "#00ff00",
                "success": "#00ff00",
                "warning": "#ffff00",
                "error": "#ff0000",
                "text_muted": "#888888",
            }
        }
        
        self.color = self.colors.get(self.theme, self.colors["Dark"])
    
    def setup_window(self):
        """Setup main window with discrete spy styling"""
        self.root.title("DetectMe")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.color["bg"])
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Modern macOS styling
        try:
            self.root.tk.call('tk', 'scaling', 2.0)
        except:
            pass
    
    def create_modern_button(self, parent, text, command, **kwargs):
        """Create discrete spy-styled button - groene achtergrond met witte tekst"""
        btn = tk.Button(
            parent,
            text=f"[{text.upper()}]",
            command=command,
            bg=self.color["accent"],
            fg="#ffffff",
            activebackground=self.color["accent_hover"],
            activeforeground="#ffffff",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            padx=15,
            pady=8,
            font=("SF Mono", 10, "bold"),
            cursor="hand2",
            **kwargs
        )
        
        # Hover effect - iets donkerder groen
        def on_enter(e):
            btn.config(bg=self.color["accent_hover"])
        def on_leave(e):
            btn.config(bg=self.color["accent"])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def create_modern_entry(self, parent, **kwargs):
        """Create modern styled entry"""
        entry = tk.Entry(
            parent,
            bg=self.color["entry_bg"],
            fg=self.color["entry_fg"],
            insertbackground=self.color["fg"],
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.color["border"],
            highlightcolor=self.color["accent"],
            font=("SF Mono", 11),
            **kwargs
        )
        return entry
    
    def create_modern_text(self, parent, **kwargs):
        """Create modern styled text widget"""
        text = scrolledtext.ScrolledText(
            parent,
            bg=self.color["entry_bg"],
            fg=self.color["entry_fg"],
            insertbackground=self.color["fg"],
            relief="flat",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.color["border"],
            highlightcolor=self.color["accent"],
            font=("SF Mono", 11),
            wrap=tk.WORD,
            **kwargs
        )
        return text
    
    def create_modern_ui(self):
        """Create modern UI layout"""
        # Header
        header = tk.Frame(self.root, bg=self.color["secondary_bg"], height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Logo/Title
        title_frame = tk.Frame(header, bg=self.color["secondary_bg"])
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        title_label = tk.Label(
            title_frame,
            text="DetectMe",
            font=("SF Mono", 18, "bold"),
            bg=self.color["secondary_bg"],
            fg=self.color["accent"]
        )
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(
            title_frame,
            text="[SYSTEM_ACTIVE]",
            font=("SF Mono", 9),
            bg=self.color["secondary_bg"],
            fg=self.color["accent"]
        )
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.color["bg"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sidebar - verbeterde navbar
        sidebar = tk.Frame(main_container, bg=self.color["bg"], width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar.pack_propagate(False)
        
        # Navigation buttons - moderne discrete stijl
        nav_buttons = [
            ("USERNAME", self.show_username_tab),
            ("DOMAIN", self.show_domain_tab),
            ("PHONE", self.show_phone_tab),
            ("EMAIL", self.show_email_tab),
            ("DORKS", self.show_dorks_tab),
            ("MAPS", self.show_maps_tab),
            ("GRAPHS", self.show_graphs_tab),
        ]
        
        self.nav_buttons = []
        self.active_nav_index = 0
        
        # Container voor nav buttons
        nav_container = tk.Frame(sidebar, bg=self.color["bg"])
        nav_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        for i, (text, command) in enumerate(nav_buttons):
            btn = tk.Button(
                nav_container,
                text=text,
                command=command,
                bg=self.color["secondary_bg"],
                fg=self.color["fg"],
                activebackground=self.color["tertiary_bg"],
                activeforeground=self.color["accent"],
                relief="flat",
                borderwidth=1,
                highlightthickness=1,
                highlightbackground=self.color["border"],
                highlightcolor=self.color["accent"],
                anchor="w",
                padx=20,
                pady=12,
                font=("SF Mono", 11, "bold"),
                cursor="hand2"
            )
            btn.pack(fill=tk.X, padx=5, pady=3)
            
            # Hover effecten
            def make_hover(index):
                def on_enter(e):
                    if index != self.active_nav_index:
                        btn.config(bg=self.color["tertiary_bg"])
                def on_leave(e):
                    if index != self.active_nav_index:
                        btn.config(bg=self.color["secondary_bg"])
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
            
            make_hover(i)
            self.nav_buttons.append(btn)
        
        # Content area
        self.content_frame = tk.Frame(main_container, bg=self.color["bg"])
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_tabs()
        
        # Show first tab
        self.show_username_tab()
    
    def create_tabs(self):
        """Create all tab content"""
        self.tabs = {}
        
        # Username tab
        self.tabs["username"] = self.create_username_tab()
        
        # Domain tab
        self.tabs["domain"] = self.create_domain_tab()
        
        # Phone tab
        self.tabs["phone"] = self.create_phone_tab()
        
        # Email tab
        self.tabs["email"] = self.create_email_tab()
        
        # Dorks tab
        self.tabs["dorks"] = self.create_dorks_tab()
        
        # Maps tab
        self.tabs["maps"] = self.create_maps_tab()
        
        # Graphs tab
        self.tabs["graphs"] = self.create_graphs_tab()
    
    def show_tab(self, tab_name):
        """Show specific tab"""
        for tab in self.tabs.values():
            tab.pack_forget()
        self.tabs[tab_name].pack(fill=tk.BOTH, expand=True)
    
    def highlight_nav_button(self, index):
        """Highlight active navigation button - groen accent"""
        self.active_nav_index = index
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.config(
                    bg=self.color["accent"],
                    fg="#000000",
                    highlightbackground=self.color["accent"],
                    highlightcolor=self.color["accent"]
                )
            else:
                btn.config(
                    bg=self.color["secondary_bg"],
                    fg=self.color["fg"],
                    highlightbackground=self.color["border"],
                    highlightcolor=self.color["border"]
                )
    
    def show_username_tab(self):
        self.show_tab("username")
        self.highlight_nav_button(0)
    
    def show_domain_tab(self):
        self.show_tab("domain")
        self.highlight_nav_button(1)
    
    def show_phone_tab(self):
        self.show_tab("phone")
        self.highlight_nav_button(2)
    
    def show_email_tab(self):
        self.show_tab("email")
        self.highlight_nav_button(3)
    
    def show_dorks_tab(self):
        self.show_tab("dorks")
        self.highlight_nav_button(4)
    
    def show_maps_tab(self):
        self.show_tab("maps")
        self.highlight_nav_button(5)
    
    def show_graphs_tab(self):
        self.show_tab("graphs")
        self.highlight_nav_button(6)
    
    def create_username_tab(self):
        """Create username lookup tab"""
        frame = tk.Frame(self.content_frame, bg=self.color["bg"])
        
        # Title - discrete style
        title = tk.Label(
            frame,
            text="[USERNAME_LOOKUP]",
            font=("SF Mono", 12, "bold"),
            bg=self.color["bg"],
            fg=self.color["accent"]
        )
        title.pack(pady=(0, 15))
        
        # Input section
        input_frame = tk.Frame(frame, bg=self.color["bg"])
        input_frame.pack(fill=tk.X, pady=20)
        
        label = tk.Label(
            input_frame,
            text="TARGET:",
            font=("SF Mono", 10),
            bg=self.color["bg"],
            fg=self.color["accent"]
        )
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        entry = self.create_modern_entry(input_frame, width=40)
        entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        results_text = self.create_modern_text(frame, height=25)
        results_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        def search():
            username = entry.get().strip()
            if not username:
                messagebox.showwarning("Warning", "Please enter a username")
                return
            
            if UsernameLookup is None:
                messagebox.showerror("Error", "UsernameLookup module not available")
                return
            
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, f"Searching for username: {username}\n")
            results_text.update()
            
            def do_search():
                try:
                    lookup = UsernameLookup()
                    lookup.search(username)
                    results_text.insert(tk.END, "\nSearch completed. Check Reports folder for detailed results.\n")
                except Exception as e:
                    results_text.insert(tk.END, f"\nError: {str(e)}\n")
            
            threading.Thread(target=do_search, daemon=True).start()
        
        btn = self.create_modern_button(input_frame, "SCAN", search)
        btn.pack(side=tk.LEFT)
        
        frame.entry = entry
        frame.results = results_text
        
        return frame
    
    def create_domain_tab(self):
        """Create domain lookup tab"""
        frame = tk.Frame(self.content_frame, bg=self.color["bg"])
        
        title = tk.Label(
            frame,
            text="[DOMAIN_ANALYSIS]",
            font=("SF Mono", 16, "bold"),
            bg=self.color["bg"],
            fg=self.color["fg"]
        )
        title.pack(pady=(0, 10))
        
        input_frame = tk.Frame(frame, bg=self.color["bg"])
        input_frame.pack(fill=tk.X, pady=20)
        
        label = tk.Label(
            input_frame,
            text="TARGET:",
            font=("SF Mono", 11),
            bg=self.color["bg"],
            fg=self.color["fg"]
        )
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        entry = self.create_modern_entry(input_frame, width=40)
        entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        results_text = self.create_modern_text(frame, height=25)
        results_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        def analyze():
            domain = entry.get().strip()
            if not domain:
                messagebox.showwarning("Warning", "Please enter a domain")
                return
            
            if DomainLookup is None:
                messagebox.showerror("Error", "DomainLookup module not available")
                return
            
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, f"Analyzing domain: {domain}\n")
            results_text.update()
            
            def do_analyze():
                try:
                    lookup = DomainLookup()
                    lookup.analyze(domain)
                    results_text.insert(tk.END, "\nAnalysis completed. Check Reports folder.\n")
                except Exception as e:
                    results_text.insert(tk.END, f"\nError: {str(e)}\n")
            
            threading.Thread(target=do_analyze, daemon=True).start()
        
        btn = self.create_modern_button(input_frame, "ANALYZE", analyze)
        btn.pack(side=tk.LEFT)
        
        return frame
    
    def create_phone_tab(self):
        """Create phone lookup tab"""
        frame = tk.Frame(self.content_frame, bg=self.color["bg"])
        
        title = tk.Label(
            frame,
            text="[PHONE_TRACE]",
            font=("SF Mono", 16, "bold"),
            bg=self.color["bg"],
            fg=self.color["fg"]
        )
        title.pack(pady=(0, 10))
        
        input_frame = tk.Frame(frame, bg=self.color["bg"])
        input_frame.pack(fill=tk.X, pady=20)
        
        label = tk.Label(
            input_frame,
            text="TARGET:",
            font=("SF Mono", 11),
            bg=self.color["bg"],
            fg=self.color["fg"]
        )
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        entry = self.create_modern_entry(input_frame, width=40)
        entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        results_text = self.create_modern_text(frame, height=25)
        results_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        def search():
            phone = entry.get().strip()
            if not phone:
                messagebox.showwarning("Warning", "Please enter a phone number")
                return
            
            if PhoneLookup is None:
                messagebox.showerror("Error", "PhoneLookup module not available")
                return
            
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, f"Analyzing phone: {phone}\n")
            results_text.update()
            
            def do_search():
                try:
                    lookup = PhoneLookup()
                    lookup.search(phone)
                    results_text.insert(tk.END, "\nAnalysis completed. Map generated in Reports folder.\n")
                except Exception as e:
                    results_text.insert(tk.END, f"\nError: {str(e)}\n")
            
            threading.Thread(target=do_search, daemon=True).start()
        
        btn = self.create_modern_button(input_frame, "SCAN", search)
        btn.pack(side=tk.LEFT)
        
        return frame
    
    def create_email_tab(self):
        """Create email lookup tab"""
        frame = tk.Frame(self.content_frame, bg=self.color["bg"])
        
        title = tk.Label(
            frame,
            text="[EMAIL_SCAN]",
            font=("SF Mono", 16, "bold"),
            bg=self.color["bg"],
            fg=self.color["fg"]
        )
        title.pack(pady=(0, 10))
        
        input_frame = tk.Frame(frame, bg=self.color["bg"])
        input_frame.pack(fill=tk.X, pady=20)
        
        label = tk.Label(
            input_frame,
            text="TARGET:",
            font=("SF Mono", 11),
            bg=self.color["bg"],
            fg=self.color["fg"]
        )
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        entry = self.create_modern_entry(input_frame, width=40)
        entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        results_text = self.create_modern_text(frame, height=25)
        results_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        def search():
            email = entry.get().strip()
            if not email:
                messagebox.showwarning("Warning", "Please enter an email address")
                return
            
            if EmailLookup is None:
                messagebox.showerror("Error", "EmailLookup module not available")
                return
            
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, f"Analyzing email: {email}\n")
            results_text.update()
            
            def do_search():
                try:
                    lookup = EmailLookup()
                    lookup.search(email)
                    results_text.insert(tk.END, "\nAnalysis completed. Check Reports folder.\n")
                except Exception as e:
                    results_text.insert(tk.END, f"\nError: {str(e)}\n")
            
            threading.Thread(target=do_search, daemon=True).start()
        
        btn = self.create_modern_button(input_frame, "SCAN", search)
        btn.pack(side=tk.LEFT)
        
        return frame
    
    def create_dorks_tab(self):
        """Create Google dorks tab"""
        frame = tk.Frame(self.content_frame, bg=self.color["bg"])
        
        title = tk.Label(
            frame,
            text="[DORK_QUERY]",
            font=("SF Mono", 16, "bold"),
            bg=self.color["bg"],
            fg=self.color["fg"]
        )
        title.pack(pady=(0, 10))
        
        input_frame = tk.Frame(frame, bg=self.color["bg"])
        input_frame.pack(fill=tk.X, pady=20)
        
        label = tk.Label(
            input_frame,
            text="QUERY:",
            font=("SF Mono", 11),
            bg=self.color["bg"],
            fg=self.color["fg"]
        )
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        entry = self.create_modern_entry(input_frame, width=40)
        entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        results_text = self.create_modern_text(frame, height=25)
        results_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        def search():
            query = entry.get().strip()
            if not query:
                messagebox.showwarning("Warning", "Please enter a search query")
                return
            
            if GoogleDorks is None:
                messagebox.showerror("Error", "GoogleDorks module not available")
                return
            
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, f"Searching: {query}\n")
            results_text.update()
            
            def do_search():
                try:
                    dorks = GoogleDorks()
                    dorks.search(query)
                    results_text.insert(tk.END, "\nSearch completed. Check Reports folder.\n")
                except Exception as e:
                    results_text.insert(tk.END, f"\nError: {str(e)}\n")
            
            threading.Thread(target=do_search, daemon=True).start()
        
        btn = self.create_modern_button(input_frame, "SCAN", search)
        btn.pack(side=tk.LEFT)
        
        return frame
    
    def create_maps_tab(self):
        """Create maps tab"""
        frame = tk.Frame(self.content_frame, bg=self.color["bg"])
        
        title = tk.Label(
            frame,
            text="[GEO_MAPPING]",
            font=("SF Mono", 16, "bold"),
            bg=self.color["bg"],
            fg=self.color["fg"]
        )
        title.pack(pady=(0, 10))
        
        info_label = tk.Label(
            frame,
            text="Maps are automatically generated when searching phone numbers or usernames.\nCheck the Reports folder for HTML map files.",
            font=("SF Mono", 10),
            bg=self.color["bg"],
            fg=self.color["fg"],
            justify=tk.LEFT
        )
        info_label.pack(pady=20)
        
        def open_reports():
            import subprocess
            reports_path = self.base_path / "Reports"
            subprocess.run(["open", str(reports_path)])
        
        btn = self.create_modern_button(frame, "OPEN_REPORTS", open_reports)
        btn.pack(pady=20)
        
        return frame
    
    def create_graphs_tab(self):
        """Create graphs tab"""
        frame = tk.Frame(self.content_frame, bg=self.color["bg"])
        
        title = tk.Label(
            frame,
            text="[DATA_VISUALIZATION]",
            font=("SF Mono", 16, "bold"),
            bg=self.color["bg"],
            fg=self.color["fg"]
        )
        title.pack(pady=(0, 10))
        
        results_text = self.create_modern_text(frame, height=25)
        results_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        def create():
            if GraphGenerator is None:
                messagebox.showerror("Error", "GraphGenerator module not available")
                return
            
            results_text.delete(1.0, tk.END)
            results_text.insert(tk.END, "Creating graph...\n")
            results_text.update()
            
            def do_create():
                try:
                    generator = GraphGenerator()
                    generator.create_graph()
                    results_text.insert(tk.END, "\nGraph created. Check Reports folder for PNG file.\n")
                except Exception as e:
                    results_text.insert(tk.END, f"\nError: {str(e)}\n")
            
            threading.Thread(target=do_create, daemon=True).start()
        
        btn = self.create_modern_button(frame, "GENERATE", create)
        btn.pack(pady=20)
        
        return frame
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

# Alias for backward compatibility
GUIApplication = ModernGUI
