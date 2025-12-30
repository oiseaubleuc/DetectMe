#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Proxy Manager Module
Handles proxy configuration and requests
"""

import requests
from pathlib import Path
import configparser

class ProxyManager:
    """Manage proxy settings for anonymous requests"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.config_path = self.base_path / "Configuration" / "Configuration.ini"
        self.proxy_config = self.load_proxy_config()
    
    def load_proxy_config(self):
        """Load proxy configuration from file"""
        config = configparser.ConfigParser()
        try:
            config.read(self.config_path)
            return {
                "enabled": config.getboolean("Proxy", "Enabled", fallback=False),
                "type": config.get("Proxy", "Type", fallback="http"),
                "host": config.get("Proxy", "Host", fallback=""),
                "port": config.get("Proxy", "Port", fallback=""),
                "username": config.get("Proxy", "Username", fallback=""),
                "password": config.get("Proxy", "Password", fallback=""),
            }
        except:
            return {
                "enabled": False,
                "type": "http",
                "host": "",
                "port": "",
                "username": "",
                "password": "",
            }
    
    def get_proxy_dict(self):
        """Get proxy dictionary for requests"""
        if not self.proxy_config["enabled"] or not self.proxy_config["host"]:
            return None
        
        proxy_type = self.proxy_config["type"]
        host = self.proxy_config["host"]
        port = self.proxy_config["port"]
        
        if self.proxy_config["username"] and self.proxy_config["password"]:
            username = self.proxy_config["username"]
            password = self.proxy_config["password"]
            proxy_url = f"{proxy_type}://{username}:{password}@{host}:{port}"
        else:
            proxy_url = f"{proxy_type}://{host}:{port}"
        
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    
    def create_session(self):
        """Create a requests session with proxy configuration"""
        session = requests.Session()
        proxy_dict = self.get_proxy_dict()
        if proxy_dict:
            session.proxies.update(proxy_dict)
            print(f"🔒 Using proxy: {self.proxy_config['type']}://{self.proxy_config['host']}:{self.proxy_config['port']}")
        return session



