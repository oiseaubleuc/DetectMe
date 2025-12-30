#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Phone Number Lookup Module
Gathers information about phone numbers
"""

import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import json
from pathlib import Path
from datetime import datetime
from Core.Geolocation import Geolocation
from Core.MapGenerator import MapGenerator

class PhoneLookup:
    """Phone number information gathering"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.reports_path = self.base_path / "Reports"
        self.reports_path.mkdir(exist_ok=True)
        self.geolocation = Geolocation()
        self.map_generator = MapGenerator()
    
    def parse_phone(self, phone_number, country_code=None):
        """Parse phone number"""
        try:
            if country_code:
                parsed = phonenumbers.parse(phone_number, country_code)
            else:
                parsed = phonenumbers.parse(phone_number, None)
            return parsed
        except:
            return None
    
    def get_phone_info(self, phone_number, country_code=None):
        """Get comprehensive phone number information"""
        parsed = self.parse_phone(phone_number, country_code)
        
        if not parsed:
            return {"error": "Invalid phone number"}
        
        info = {
            "number": phone_number,
            "is_valid": phonenumbers.is_valid_number(parsed),
            "is_possible": phonenumbers.is_possible_number(parsed),
            "format_international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "format_national": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
            "format_e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
            "country_code": parsed.country_code,
            "country": geocoder.description_for_number(parsed, "en"),
            "carrier": carrier.name_for_number(parsed, "en"),
            "timezones": timezone.time_zones_for_number(parsed),
            "number_type": phonenumbers.number_type(parsed),
        }
        
        return info
    
    def search(self, phone_number, country_code=None):
        """Search for phone number information with location details"""
        print(f"\nAnalyzing phone number: {phone_number}")
        print("=" * 50)
        
        info = self.get_phone_info(phone_number, country_code)
        
        if "error" in info:
            print(f"Error: {info['error']}")
            return
        
        print(f"Valid: {info['is_valid']}")
        print(f"Country: {info.get('country', 'Unknown')} (+{info.get('country_code', 'N/A')})")
        print(f"Carrier: {info.get('carrier', 'Unknown')}")
        print(f"Timezones: {', '.join(info.get('timezones', []))}")
        print(f"International Format: {info.get('format_international', 'N/A')}")
        print(f"National Format: {info.get('format_national', 'N/A')}")
        print(f"E.164 Format: {info.get('format_e164', 'N/A')}")
        
        # Get detailed location information
        print("\nLocation Details:")
        print("-" * 30)
        location_details = self.geolocation.get_phone_location_details(phone_number, country_code)
        
        if "error" not in location_details:
            print(f"Region: {location_details.get('region', 'Unknown')}")
            print(f"Country Code: +{location_details.get('country_code', 'N/A')}")
            print(f"Number Type: {location_details.get('number_type', 'Unknown')}")
            
            if location_details.get('latitude') and location_details.get('longitude'):
                precision = location_details.get('location_precision', 'unknown')
                city = location_details.get('city', 'Unknown')
                lat = location_details.get('latitude')
                lon = location_details.get('longitude')
                
                print(f"Location Found:")
                print(f"  City: {city}")
                print(f"  Latitude: {lat}")
                print(f"  Longitude: {lon}")
                print(f"  Country: {location_details.get('country', 'Unknown')}")
                print(f"  Precision: {precision}")
                
                # Automatically generate interactive map
                print("\nGenerating interactive map...")
                map_locations = [{
                    "lat": lat,
                    "lon": lon,
                    "label": f"Phone: {phone_number}\nCity: {city}\nCarrier: {info.get('carrier', 'Unknown')}"
                }]
                
                map_file = self.map_generator.create_map_with_locations(
                    map_locations,
                    title=f"Phone Number Location: {phone_number}"
                )
                
                if map_file:
                    print(f"\nInteractive map created: {map_file}")
                    print(f"Open this file in your browser to see the exact location on the map!")
            
            info["location_details"] = location_details
        else:
            print(f"Location details: {location_details.get('error', 'Unable to retrieve')}")
        
        print("\n" + "=" * 50)
        
        # Save report
        report_data = {
            "phone_number": phone_number,
            "timestamp": datetime.now().isoformat(),
            "information": info
        }
        
        self.save_report(report_data)
    
    def save_report(self, report_data):
        """Save search results to a report file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        phone_clean = report_data["phone_number"].replace("+", "").replace("-", "").replace(" ", "")
        report_file = self.reports_path / f"phone_{phone_clean}_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"Report saved: {report_file}")
        print()



