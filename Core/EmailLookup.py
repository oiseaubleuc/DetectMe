#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Email Lookup Module
Checks if email is associated with various services
"""

import requests
import json
from pathlib import Path
from datetime import datetime
import time

class EmailLookup:
    """Email lookup across multiple services"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.reports_path = self.base_path / "Reports"
        self.reports_path.mkdir(exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def check_email_service(self, email, service_name, check_url, check_method="get"):
        """Check if email is registered on a service"""
        try:
            if check_method == "get":
                response = self.session.get(check_url, timeout=10, allow_redirects=False)
            else:
                response = self.session.post(check_url, timeout=10, allow_redirects=False)
            
            # This is a simplified check - actual implementation would need
            # to parse responses for each service
            if response.status_code == 200:
                # Check response content for indicators
                content = response.text.lower()
                if any(keyword in content for keyword in ['already', 'taken', 'exists', 'registered']):
                    return {"exists": True, "status": "Possibly Registered"}
                elif any(keyword in content for keyword in ['available', 'not found', 'invalid']):
                    return {"exists": False, "status": "Not Registered"}
                else:
                    return {"exists": "Unknown", "status": "Cannot Determine"}
            else:
                return {"exists": "Unknown", "status": f"Status {response.status_code}"}
        except Exception as e:
            return {"exists": "Error", "status": f"Error: {str(e)}"}
    
    def search(self, email):
        """Search for email across services"""
        print(f"\n📧 Analyzing email: {email}")
        print("=" * 50)
        
        # Extract username and domain
        if "@" not in email:
            print("❌ Invalid email address")
            return
        
        username, domain = email.split("@", 1)
        
        print(f"👤 Username: {username}")
        print(f"🌐 Domain: {domain}")
        print()
        
        # Check common services (simplified - actual implementation would need
        # specific endpoints for each service)
        services = {
            "Gravatar": f"https://en.gravatar.com/{email}",
            "Have I Been Pwned": f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
        }
        
        results = {}
        for service_name, url in services.items():
            print(f"Checking {service_name}...", end=" ", flush=True)
            result = self.check_email_service(email, service_name, url)
            results[service_name] = result
            
            if result["exists"] is True:
                print("✅ Found")
            elif result["exists"] is False:
                print("❌ Not Found")
            else:
                print(f"⚠️  {result['status']}")
            
            time.sleep(0.5)
        
        print("\n" + "=" * 50)
        
        # Save report
        report_data = {
            "email": email,
            "username": username,
            "domain": domain,
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        
        self.save_report(report_data)
    
    def save_report(self, report_data):
        """Save search results to a report file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        email_clean = report_data["email"].replace("@", "_at_").replace(".", "_")
        report_file = self.reports_path / f"email_{email_clean}_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Report saved: {report_file}")
        print()



