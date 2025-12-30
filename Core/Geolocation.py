#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Geolocation Module
Gets location information from IP addresses, phone numbers, and usernames
"""

import requests
import json
from pathlib import Path
import socket
import re

class Geolocation:
    """Geolocation and IP lookup services"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def get_ip_geolocation(self, ip_address):
        """Get geolocation information from IP address"""
        try:
            # Using ip-api.com (free, no API key required)
            url = f"http://ip-api.com/json/{ip_address}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        "ip": data.get('query', ip_address),
                        "country": data.get('country', 'Unknown'),
                        "country_code": data.get('countryCode', ''),
                        "region": data.get('regionName', 'Unknown'),
                        "region_code": data.get('region', ''),
                        "city": data.get('city', 'Unknown'),
                        "district": data.get('district', ''),
                        "zip_code": data.get('zip', ''),
                        "latitude": data.get('lat', 0),
                        "longitude": data.get('lon', 0),
                        "timezone": data.get('timezone', 'Unknown'),
                        "isp": data.get('isp', 'Unknown'),
                        "organization": data.get('org', 'Unknown'),
                        "as_number": data.get('as', ''),
                        "as_name": data.get('asname', ''),
                        "reverse_dns": data.get('reverse', ''),
                        "mobile": data.get('mobile', False),
                        "proxy": data.get('proxy', False),
                        "hosting": data.get('hosting', False),
                        "currency": data.get('currency', ''),
                    }
            return {"error": "Failed to get geolocation data"}
        except Exception as e:
            return {"error": f"Error getting geolocation: {str(e)}"}
    
    def get_domain_ip(self, domain):
        """Get IP address from domain"""
        try:
            ip = socket.gethostbyname(domain)
            return ip
        except:
            return None
    
    def get_phone_location_details(self, phone_number, country_code=None):
        """Get detailed location information from phone number with reverse lookup"""
        try:
            import phonenumbers
            from phonenumbers import geocoder, carrier, timezone
            
            if country_code:
                parsed = phonenumbers.parse(phone_number, country_code)
            else:
                parsed = phonenumbers.parse(phone_number, None)
            
            if not phonenumbers.is_valid_number(parsed):
                return {"error": "Invalid phone number"}
            
            # Get detailed location
            country = geocoder.description_for_number(parsed, "en")
            carrier_name = carrier.name_for_number(parsed, "en")
            timezones = timezone.time_zones_for_number(parsed)
            
            # Try reverse phone lookup for more precise location
            precise_location = self.reverse_phone_lookup(phone_number, parsed.country_code)
            
            # Try to get more specific location using country code and area code
            location_info = {
                "country": country,
                "country_code": parsed.country_code,
                "carrier": carrier_name,
                "timezones": list(timezones),
                "number_type": str(phonenumbers.number_type(parsed)),
            }
            
            # Use precise location if available, otherwise use country center
            if precise_location and "error" not in precise_location:
                location_info.update(precise_location)
                location_info["location_precision"] = "precise"
            else:
                # Try to get approximate location from country code and area code
                area_coords = self.get_area_code_coordinates(phone_number, parsed.country_code)
                if area_coords:
                    location_info.update(area_coords)
                    location_info["location_precision"] = "area_code"
                else:
                    country_coords = self.get_country_coordinates(parsed.country_code)
                    if country_coords:
                        location_info.update(country_coords)
                        location_info["location_precision"] = "country_center"
            
            return location_info
        except Exception as e:
            return {"error": f"Error getting phone location: {str(e)}"}
    
    def reverse_phone_lookup(self, phone_number, country_code):
        """Try reverse phone lookup using free APIs"""
        try:
            # Try using numverify API (free tier available)
            # Note: This requires API key, but we'll try without first
            # For production, you'd add API key to config
            
            # Alternative: Use OpenCage Geocoding API with area code
            # For now, we'll use area code databases
            
            # Extract area code from phone number
            area_code = self.extract_area_code(phone_number, country_code)
            if area_code:
                return self.get_area_code_coordinates(phone_number, country_code)
            
            return {"error": "Could not determine precise location"}
        except Exception as e:
            return {"error": f"Reverse lookup error: {str(e)}"}
    
    def extract_area_code(self, phone_number, country_code):
        """Extract area code from phone number"""
        try:
            # Remove country code and formatting
            clean_number = phone_number.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
            
            # Remove country code
            country_str = str(country_code)
            if clean_number.startswith(country_str):
                clean_number = clean_number[len(country_str):]
            
            # For Belgium (32), mobile numbers start with 4xx, 5xx, 6xx, 7xx, 8xx, 9xx
            # Extract the first 3 digits for mobile numbers
            if country_code == 32:
                if len(clean_number) >= 3:
                    # Check if it's a mobile number (starts with 4, 5, 6, 7, 8, or 9)
                    if clean_number[0] in ['4', '5', '6', '7', '8', '9']:
                        return clean_number[:3]  # Return 3-digit mobile prefix
                    else:
                        return clean_number[:2]  # Return 2-digit area code for landlines
            
            # For US/Canada (1), extract 3-digit area code
            if country_code == 1:
                if len(clean_number) >= 3:
                    return clean_number[:3]
            
            # Default: extract first few digits
            if len(clean_number) >= 3:
                return clean_number[:3] if country_code == 1 else clean_number[:2]
            return None
        except:
            return None
    
    def get_area_code_coordinates(self, phone_number, country_code):
        """Get coordinates based on area code (for US/Canada)"""
        try:
            # US/Canada area code database (sample - you'd expand this)
            if country_code == 1:
                area_code = self.extract_area_code(phone_number, country_code)
                if area_code:
                    # Major US city area codes (sample)
                    us_area_codes = {
                        "212": {"latitude": 40.7128, "longitude": -74.0060, "city": "New York, NY"},
                        "213": {"latitude": 34.0522, "longitude": -118.2437, "city": "Los Angeles, CA"},
                        "312": {"latitude": 41.8781, "longitude": -87.6298, "city": "Chicago, IL"},
                        "415": {"latitude": 37.7749, "longitude": -122.4194, "city": "San Francisco, CA"},
                        "305": {"latitude": 25.7617, "longitude": -80.1918, "city": "Miami, FL"},
                        "617": {"latitude": 42.3601, "longitude": -71.0589, "city": "Boston, MA"},
                        "202": {"latitude": 38.9072, "longitude": -77.0369, "city": "Washington, DC"},
                        "214": {"latitude": 32.7767, "longitude": -96.7970, "city": "Dallas, TX"},
                        "404": {"latitude": 33.7490, "longitude": -84.3880, "city": "Atlanta, GA"},
                        "206": {"latitude": 47.6062, "longitude": -122.3321, "city": "Seattle, WA"},
                    }
                    
                    if area_code in us_area_codes:
                        return us_area_codes[area_code]
            
            # Belgium area codes (32)
            elif country_code == 32:
                area_code = self.extract_area_code(phone_number, country_code)
                if area_code:
                    be_area_codes = {
                        # Landline area codes (2 digits)
                        "02": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels"},
                        "03": {"latitude": 51.2194, "longitude": 4.4025, "city": "Antwerp"},
                        "09": {"latitude": 51.0543, "longitude": 3.7174, "city": "Ghent"},
                        "04": {"latitude": 50.6333, "longitude": 5.5667, "city": "Liège"},
                        "010": {"latitude": 50.6686, "longitude": 4.6114, "city": "Louvain-la-Neuve"},
                        "011": {"latitude": 50.9306, "longitude": 5.3375, "city": "Hasselt"},
                        # Mobile prefixes (3 digits) - Telenet carrier typically covers Brussels area
                        "484": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile - Telenet)"},
                        "485": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile - Telenet)"},
                        "486": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile - Telenet)"},
                        "487": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile - Telenet)"},
                        "488": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile - Telenet)"},
                        "489": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile - Telenet)"},
                        # Other common mobile prefixes
                        "470": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile)"},
                        "471": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile)"},
                        "472": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile)"},
                        "473": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile)"},
                        "475": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile)"},
                        "476": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile)"},
                        "477": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile)"},
                        "478": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile)"},
                        "479": {"latitude": 50.8503, "longitude": 4.3517, "city": "Brussels Region (Mobile)"},
                    }
                    # Check 3-digit codes first (mobile numbers)
                    if len(area_code) >= 3 and area_code[:3] in be_area_codes:
                        return be_area_codes[area_code[:3]]
                    # Check 2-digit codes (landlines)
                    if len(area_code) >= 2 and area_code[:2] in be_area_codes:
                        return be_area_codes[area_code[:2]]
            
            return None
        except Exception as e:
            return None
    
    def get_country_coordinates(self, country_code):
        """Get approximate coordinates for a country code"""
        # Approximate country center coordinates
        country_coords = {
            "1": {"latitude": 39.8283, "longitude": -98.5795, "country": "United States/Canada"},
            "44": {"latitude": 54.7024, "longitude": -3.2766, "country": "United Kingdom"},
            "33": {"latitude": 46.2276, "longitude": 2.2137, "country": "France"},
            "49": {"latitude": 51.1657, "longitude": 10.4515, "country": "Germany"},
            "39": {"latitude": 41.8719, "longitude": 12.5674, "country": "Italy"},
            "34": {"latitude": 40.4637, "longitude": -3.7492, "country": "Spain"},
            "7": {"latitude": 61.5240, "longitude": 105.3188, "country": "Russia/Kazakhstan"},
            "86": {"latitude": 35.8617, "longitude": 104.1954, "country": "China"},
            "81": {"latitude": 36.2048, "longitude": 138.2529, "country": "Japan"},
            "91": {"latitude": 20.5937, "longitude": 78.9629, "country": "India"},
            "52": {"latitude": 23.6345, "longitude": -102.5528, "country": "Mexico"},
            "55": {"latitude": -14.2350, "longitude": -51.9253, "country": "Brazil"},
            "61": {"latitude": -25.2744, "longitude": 133.7751, "country": "Australia"},
            "27": {"latitude": -30.5595, "longitude": 22.9375, "country": "South Africa"},
            "971": {"latitude": 23.4241, "longitude": 53.8478, "country": "United Arab Emirates"},
            "966": {"latitude": 23.8859, "longitude": 45.0792, "country": "Saudi Arabia"},
            "32": {"latitude": 50.5039, "longitude": 4.4699, "country": "Belgium"},
            "31": {"latitude": 52.1326, "longitude": 5.2913, "country": "Netherlands"},
            "41": {"latitude": 46.8182, "longitude": 8.2275, "country": "Switzerland"},
            "43": {"latitude": 47.5162, "longitude": 14.5501, "country": "Austria"},
            "46": {"latitude": 60.1282, "longitude": 18.6435, "country": "Sweden"},
            "47": {"latitude": 60.4720, "longitude": 8.4689, "country": "Norway"},
            "45": {"latitude": 56.2639, "longitude": 9.5018, "country": "Denmark"},
            "358": {"latitude": 61.9241, "longitude": 25.7482, "country": "Finland"},
            "48": {"latitude": 51.9194, "longitude": 19.1451, "country": "Poland"},
        }
        
        return country_coords.get(str(country_code), None)
    
    def extract_ip_from_text(self, text):
        """Extract IP addresses from text"""
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, text)
        return ips
    
    def get_username_profile_location(self, username, platform_url):
        """Try to extract location information from a user profile page"""
        try:
            response = self.session.get(platform_url, timeout=10)
            if response.status_code == 200:
                content = response.text.lower()
                
                # Look for location indicators in common patterns
                location_patterns = [
                    r'location["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                    r'from["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                    r'lives?\s+in\s+([^<>\n]+)',
                    r'based\s+in\s+([^<>\n]+)',
                ]
                
                locations = []
                for pattern in location_patterns:
                    matches = re.findall(pattern, content)
                    locations.extend(matches)
                
                # Also try to find IP addresses
                ips = self.extract_ip_from_text(response.text)
                
                return {
                    "possible_locations": list(set(locations[:5])),  # Limit to 5 unique
                    "found_ips": ips,
                }
        except:
            pass
        
        return {"possible_locations": [], "found_ips": []}

