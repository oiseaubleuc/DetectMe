#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Domain Lookup Module
Gathers information about domains using WhoIS and other sources
"""

try:
    import whois
except ImportError:
    whois = None
import socket
try:
    import dns.resolver
except ImportError:
    dns = None
import requests
import json
from pathlib import Path
from datetime import datetime
import ssl

class DomainLookup:
    """Domain information gathering"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.reports_path = self.base_path / "Reports"
        self.reports_path.mkdir(exist_ok=True)
        self.config_path = self.base_path / "Configuration" / "Configuration.ini"
        self.whois_api_key = self.load_api_key()
    
    def load_api_key(self):
        """Load WhoIS API key from configuration"""
        try:
            with open(self.config_path, 'r') as f:
                for line in f:
                    if 'WhoIS_API_Key' in line and '=' in line:
                        return line.split('=')[1].strip()
        except:
            pass
        return ""
    
    def get_whois_info(self, domain):
        """Get WhoIS information"""
        if whois is None:
            return {"error": "python-whois library not installed"}
        try:
            w = whois.whois(domain)
            return {
                "domain_name": w.domain_name,
                "registrar": w.registrar,
                "creation_date": str(w.creation_date) if w.creation_date else None,
                "expiration_date": str(w.expiration_date) if w.expiration_date else None,
                "updated_date": str(w.updated_date) if w.updated_date else None,
                "name_servers": w.name_servers,
                "status": w.status,
                "emails": w.emails,
                "dnssec": w.dnssec,
                "org": w.org,
                "country": w.country,
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_dns_records(self, domain):
        """Get DNS records"""
        if dns is None:
            return {"error": "dnspython library not installed"}
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
            except:
                records[record_type] = []
        
        return records
    
    def get_ip_address(self, domain):
        """Get IP address of domain"""
        try:
            ip = socket.gethostbyname(domain)
            return ip
        except:
            return None
    
    def get_ssl_info(self, domain):
        """Get SSL certificate information"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        "subject": dict(x[0] for x in cert['subject']),
                        "issuer": dict(x[0] for x in cert['issuer']),
                        "version": cert['version'],
                        "serialNumber": cert['serialNumber'],
                        "notBefore": cert['notBefore'],
                        "notAfter": cert['notAfter'],
                    }
        except Exception as e:
            return {"error": str(e)}
    
    def check_subdomain_takeover(self, domain):
        """Check for common subdomain takeover vulnerabilities"""
        common_subdomains = ['www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk', 'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test', 'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn', 'ns3', 'mail2', 'new', 'mysql', 'old', 'lists', 'support', 'mobile', 'mx', 'static', 'docs', 'beta', 'shop', 'sql', 'secure', 'demo', 'cp', 'calendar', 'wiki', 'web', 'media', 'email', 'images', 'img', 'www1', 'intranet', 'portal', 'video', 'sip', 'dns2', 'api', 'cdn', 'stats', 'dns1', 'ns4', 'www3', 'dns', 'search', 'staging', 'server', 'mx1', 'chat', 'wap', 'my', 'svn', 'mail1', 'sites', 'proxy', 'ads', 'host', 'crm', 'cms', 'backup', 'mx2', 'lyncdiscover', 'info', 'ads', 'cs', 'careers', 'alpha', 'eng', 'ar', 'pl', 's', 'clients', 'code', 'blog', 'billing', 'ws', 'ns5', 'live', 'signup', 'app', 'media', 'static']
        
        found_subdomains = []
        for subdomain in common_subdomains[:20]:  # Limit to first 20 for speed
            try:
                full_domain = f"{subdomain}.{domain}"
                ip = socket.gethostbyname(full_domain)
                found_subdomains.append({"subdomain": full_domain, "ip": ip})
            except:
                pass
        
        return found_subdomains
    
    def analyze(self, domain):
        """Analyze domain and gather all information"""
        print(f"\n🌐 Analyzing domain: {domain}")
        print("=" * 50)
        
        results = {
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
        }
        
        # Get IP address
        print("📍 Getting IP address...", end=" ", flush=True)
        ip = self.get_ip_address(domain)
        results["ip_address"] = ip
        if ip:
            print(f"✅ {ip}")
        else:
            print("❌ Not found")
        
        # Get WhoIS information
        print("📋 Getting WhoIS information...", end=" ", flush=True)
        whois_info = self.get_whois_info(domain)
        results["whois"] = whois_info
        if "error" not in whois_info:
            print("✅ Retrieved")
            if whois_info.get("registrar"):
                print(f"   Registrar: {whois_info.get('registrar')}")
            if whois_info.get("creation_date"):
                print(f"   Created: {whois_info.get('creation_date')}")
            if whois_info.get("expiration_date"):
                print(f"   Expires: {whois_info.get('expiration_date')}")
        else:
            print(f"⚠️  {whois_info.get('error')}")
        
        # Get DNS records
        print("🔍 Getting DNS records...", end=" ", flush=True)
        dns_records = self.get_dns_records(domain)
        results["dns"] = dns_records
        print("✅ Retrieved")
        if dns_records.get('A'):
            print(f"   A Records: {', '.join(dns_records['A'])}")
        if dns_records.get('MX'):
            print(f"   MX Records: {', '.join(dns_records['MX'])}")
        
        # Get SSL information
        print("🔒 Getting SSL certificate information...", end=" ", flush=True)
        ssl_info = self.get_ssl_info(domain)
        results["ssl"] = ssl_info
        if "error" not in ssl_info:
            print("✅ Retrieved")
            if ssl_info.get("notAfter"):
                print(f"   Valid until: {ssl_info.get('notAfter')}")
        else:
            print("⚠️  Could not retrieve")
        
        # Check subdomains
        print("🔎 Checking common subdomains...", end=" ", flush=True)
        subdomains = self.check_subdomain_takeover(domain)
        results["subdomains"] = subdomains
        if subdomains:
            print(f"✅ Found {len(subdomains)} subdomains")
            for sub in subdomains[:5]:  # Show first 5
                print(f"   • {sub['subdomain']} -> {sub['ip']}")
        else:
            print("❌ None found")
        
        print("\n" + "=" * 50)
        
        # Save report
        self.save_report(results)
    
    def save_report(self, results):
        """Save analysis results to a report file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain_clean = results["domain"].replace(".", "_")
        report_file = self.reports_path / f"domain_{domain_clean}_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Report saved: {report_file}")
        print()

