#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Username Lookup Module
Searches for usernames across multiple platforms
"""

import requests
import json
from pathlib import Path
from datetime import datetime
import time
from Core.Geolocation import Geolocation

class UsernameLookup:
    """Username lookup across multiple platforms"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.reports_path = self.base_path / "Reports"
        self.reports_path.mkdir(exist_ok=True)
        
        # List of platforms to check
        self.platforms = {
            "GitHub": "https://github.com/{}",
            "Twitter": "https://twitter.com/{}",
            "Instagram": "https://www.instagram.com/{}",
            "Facebook": "https://www.facebook.com/{}",
            "LinkedIn": "https://www.linkedin.com/in/{}",
            "Reddit": "https://www.reddit.com/user/{}",
            "YouTube": "https://www.youtube.com/@{}",
            "TikTok": "https://www.tiktok.com/@{}",
            "Pinterest": "https://www.pinterest.com/{}",
            "Snapchat": "https://www.snapchat.com/add/{}",
            "Tumblr": "https://{}.tumblr.com",
            "Flickr": "https://www.flickr.com/people/{}",
            "Vimeo": "https://vimeo.com/{}",
            "SoundCloud": "https://soundcloud.com/{}",
            "Spotify": "https://open.spotify.com/user/{}",
            "Steam": "https://steamcommunity.com/id/{}",
            "Twitch": "https://www.twitch.tv/{}",
            "Medium": "https://medium.com/@{}",
            "Dev.to": "https://dev.to/{}",
            "CodePen": "https://codepen.io/{}",
            "Stack Overflow": "https://stackoverflow.com/users/{}",
            "HackerNews": "https://news.ycombinator.com/user?id={}",
            "Behance": "https://www.behance.net/{}",
            "Dribbble": "https://dribbble.com/{}",
            "DeviantArt": "https://www.deviantart.com/{}",
            "VK": "https://vk.com/{}",
            "Telegram": "https://t.me/{}",
        }
        
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.geolocation = Geolocation()
    
    def check_username(self, username, platform_name, url_template):
        """Check if username exists on a platform and gather location data"""
        try:
            url = url_template.format(username)
            response = self.session.get(url, timeout=10, allow_redirects=False)
            
            result = {
                "url": url,
                "status_code": response.status_code
            }
            
            # Different platforms return different status codes
            if response.status_code == 200:
                result["exists"] = True
                result["status"] = "Found"
                
                # Try to extract location information from profile
                location_data = self.geolocation.get_username_profile_location(username, url)
                if location_data.get("possible_locations"):
                    result["possible_locations"] = location_data["possible_locations"]
                if location_data.get("found_ips"):
                    result["found_ips"] = location_data["found_ips"]
                    # Get geolocation for found IPs
                    ip_locations = []
                    for ip in location_data["found_ips"][:3]:  # Limit to first 3 IPs
                        geo = self.geolocation.get_ip_geolocation(ip)
                        if "error" not in geo:
                            ip_locations.append(geo)
                    if ip_locations:
                        result["ip_locations"] = ip_locations
                
            elif response.status_code == 404:
                result["exists"] = False
                result["status"] = "Not Found"
            elif response.status_code in [301, 302, 303, 307, 308]:
                result["exists"] = True
                result["status"] = "Redirect"
                result["redirect_url"] = response.headers.get('Location', '')
            else:
                result["exists"] = "Unknown"
                result["status"] = f"Status {response.status_code}"
            
            return result
        except requests.exceptions.RequestException as e:
            return {"exists": "Error", "url": url_template.format(username), "status": f"Error: {str(e)}"}
    
    def search(self, username):
        """Search for username across all platforms"""
        print(f"\nSearching for username: {username}")
        print("=" * 50)
        
        found_count = 0
        not_found_count = 0
        location_data_collected = []
        
        for platform_name, url_template in self.platforms.items():
            print(f"Checking {platform_name}...", end=" ", flush=True)
            result = self.check_username(username, platform_name, url_template)
            self.results[platform_name] = result
            
            if result["exists"] is True:
                print(f"Found!")
                found_count += 1
                
                # Collect location data
                if result.get("possible_locations"):
                    location_data_collected.extend(result["possible_locations"])
                if result.get("ip_locations"):
                    for ip_loc in result["ip_locations"]:
                        location_data_collected.append({
                            "type": "ip_location",
                            "city": ip_loc.get("city"),
                            "country": ip_loc.get("country"),
                            "coordinates": [ip_loc.get("latitude"), ip_loc.get("longitude")]
                        })
            elif result["exists"] is False:
                print("Not Found")
                not_found_count += 1
            else:
                print(f"{result.get('status', 'Unknown')}")
            
            time.sleep(0.5)  # Rate limiting
        
        print("\n" + "=" * 50)
        print(f"Results Summary:")
        print(f"   Found: {found_count}")
        print(f"   Not Found: {not_found_count}")
        print(f"   Unknown/Error: {len(self.platforms) - found_count - not_found_count}")
        print()
        
        # Display location information
        if location_data_collected:
            print("Location Information Found:")
            unique_locations = {}
            for loc in location_data_collected:
                if isinstance(loc, dict):
                    if loc.get("type") == "ip_location":
                        key = f"{loc.get('city', 'Unknown')}, {loc.get('country', 'Unknown')}"
                        if key not in unique_locations:
                            unique_locations[key] = loc
                    else:
                        key = str(loc)
                        if key not in unique_locations:
                            unique_locations[key] = loc
                else:
                    if str(loc) not in unique_locations:
                        unique_locations[str(loc)] = loc
            
            for loc_key, loc_data in list(unique_locations.items())[:10]:  # Show first 10
                if isinstance(loc_data, dict) and loc_data.get("type") == "ip_location":
                    print(f"   • {loc_data.get('city', 'Unknown')}, {loc_data.get('country', 'Unknown')}")
                    if loc_data.get("coordinates"):
                        print(f"     Coordinates: {loc_data['coordinates'][0]}, {loc_data['coordinates'][1]}")
                    if loc_data.get("isp"):
                        print(f"     ISP: {loc_data.get('isp')}")
                else:
                    print(f"   • {loc_key}")
            print()
        
        # Save results
        self.save_report(username, location_data_collected)
        
        # Display found profiles
        if found_count > 0:
            print("Found Profiles:")
            for platform, result in self.results.items():
                if result["exists"] is True:
                    print(f"   • {platform}: {result['url']}")
                    if result.get("possible_locations"):
                        print(f"     Possible locations: {', '.join(result['possible_locations'][:3])}")
            print()
    
    def save_report(self, username, location_data=None):
        """Save search results to a report file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_path / f"username_{username}_{timestamp}.json"
        
        report_data = {
            "username": username,
            "timestamp": timestamp,
            "total_platforms": len(self.platforms),
            "results": self.results,
            "location_data": location_data or []
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"Report saved: {report_file}")
        print()



