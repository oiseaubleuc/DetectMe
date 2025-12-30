#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interactive Map Generator
Creates interactive maps using Folium (Leaflet.js)
"""

import folium
from folium import plugins
import json
from pathlib import Path
from datetime import datetime

class MapGenerator:
    """Generate interactive maps for OSINT data"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.reports_path = self.base_path / "Reports"
        self.reports_path.mkdir(exist_ok=True)
    
    def create_map_with_locations(self, locations, title="Location Map", zoom_start=12):
        """Create a map with specific locations and return the file path"""
        if not locations or len(locations) == 0:
            return None
        
        # Calculate center from locations
        center_lat = sum(loc["lat"] for loc in locations) / len(locations)
        center_lon = sum(loc["lon"] for loc in locations) / len(locations)
        
        # Create map with subtle, professional style
        # Using CartoDB Positron for a clean, minimal look
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            tiles='CartoDB positron',
            attr='CartoDB'
        )
        
        # Add alternative tile layers for variety (subtle options)
        folium.TileLayer(
            tiles='CartoDB dark_matter',
            attr='CartoDB',
            name='Dark Mode',
            overlay=False,
            control=True
        ).add_to(m)
        
        folium.TileLayer(
            tiles='Stamen Toner',
            attr='Stamen',
            name='Minimal',
            overlay=False,
            control=True
        ).add_to(m)
        
        # Add markers with elegant, discrete styling
        for i, loc in enumerate(locations):
            # Create custom HTML for elegant popup
            popup_html = f'''
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                        padding: 12px; min-width: 200px; color: #2c3e50;">
                <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px; color: #34495e;">
                    {loc.get("label", f"Location {i+1}").replace(chr(10), "<br>")}
                </div>
                <div style="font-size: 12px; color: #7f8c8d; margin-top: 8px; border-top: 1px solid #ecf0f1; padding-top: 8px;">
                    Coordinates: {loc["lat"]:.6f}, {loc["lon"]:.6f}
                </div>
            </div>
            '''
            
            # Use subtle blue-gray marker instead of bright red
            folium.Marker(
                [loc["lat"], loc["lon"]],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=folium.Tooltip(
                    loc.get("label", f"Location {i+1}").split('\n')[0],
                    style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px;"
                ),
                icon=folium.Icon(
                    color='blue',
                    icon='map-marker-alt',
                    prefix='fa',
                    icon_color='white'
                )
            ).add_to(m)
            
            # Add subtle circle with soft color
            folium.CircleMarker(
                location=[loc["lat"], loc["lon"]],
                radius=8,
                popup=folium.Popup(popup_html, max_width=300),
                color='#3498db',
                fill=True,
                fillColor='#3498db',
                fillOpacity=0.3,
                weight=2
            ).add_to(m)
            
            # Add a subtle radius circle to show area
            folium.Circle(
                location=[loc["lat"], loc["lon"]],
                radius=500,  # 500 meters
                color='#3498db',
                fill=True,
                fillColor='#3498db',
                fillOpacity=0.1,
                weight=1,
                dashArray='5, 5'
            ).add_to(m)
        
        # Add layer control with elegant styling
        folium.LayerControl(
            position='topright',
            collapsed=False
        ).add_to(m)
        
        # Add fullscreen button
        plugins.Fullscreen(
            position='topleft',
            title='Fullscreen',
            titleCancel='Exit Fullscreen'
        ).add_to(m)
        
        # Add measure control with subtle styling
        plugins.MeasureControl(
            position='bottomleft',
            primary_length_unit='meters',
            secondary_length_unit='kilometers',
            primary_area_unit='sqmeters',
            secondary_area_unit='hectares'
        ).add_to(m)
        
        # Add elegant title with modern styling
        title_html = f'''
        <div style="position: fixed; 
                    top: 10px; 
                    left: 50%; 
                    transform: translateX(-50%);
                    z-index: 9999;
                    background: rgba(255, 255, 255, 0.95);
                    padding: 12px 24px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    font-size: 16px;
                    font-weight: 500;
                    color: #2c3e50;
                    border: 1px solid rgba(0,0,0,0.1);
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);">
            {title}
        </div>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        # Add custom CSS for better styling
        custom_css = '''
        <style>
            .leaflet-container {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            }
            .leaflet-popup-content-wrapper {
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            .leaflet-control {
                border-radius: 6px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }
            .leaflet-bar a {
                border-radius: 4px;
            }
        </style>
        '''
        m.get_root().html.add_child(folium.Element(custom_css))
        
        # Save map
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        map_file = self.reports_path / f"map_{timestamp}.html"
        m.save(str(map_file))
        
        return map_file
    
    def create_map(self, locations=None, center_lat=0, center_lon=0, zoom_start=2):
        """Create an interactive map"""
        print("\nInteractive Map Generator")
        print("=" * 50)
        
        if locations is None:
            print("Enter location data:")
            print("Format: latitude,longitude,label (or 'done' to finish)")
            locations = []
            
            while True:
                location_input = input("Location (lat,lon,label or 'done'): ").strip()
                if location_input.lower() == 'done':
                    break
                
                try:
                    parts = location_input.split(',')
                    if len(parts) >= 2:
                        lat = float(parts[0].strip())
                        lon = float(parts[1].strip())
                        label = parts[2].strip() if len(parts) > 2 else f"Location {len(locations) + 1}"
                        locations.append({"lat": lat, "lon": lon, "label": label})
                        print(f"Added: {label} at ({lat}, {lon})")
                    else:
                        print("Invalid format. Use: lat,lon,label")
                except ValueError:
                    print("Invalid coordinates")
        
        if not locations:
            print("Warning: No locations provided. Creating empty map.")
            center_lat, center_lon = 0, 0
        else:
            # Calculate center from locations
            center_lat = sum(loc["lat"] for loc in locations) / len(locations)
            center_lon = sum(loc["lon"] for loc in locations) / len(locations)
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            tiles='OpenStreetMap'
        )
        
        # Add markers
        for loc in locations:
            folium.Marker(
                [loc["lat"], loc["lon"]],
                popup=loc["label"],
                tooltip=loc["label"],
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
        
        # Add fullscreen button
        plugins.Fullscreen().add_to(m)
        
        # Add measure control
        plugins.MeasureControl().add_to(m)
        
        # Add draw plugin
        plugins.Draw().add_to(m)
        
        # Save map
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        map_file = self.reports_path / f"map_{timestamp}.html"
        m.save(str(map_file))
        
        print(f"\nMap created: {map_file}")
        print(f"Locations: {len(locations)}")
        print(f"Center: ({center_lat}, {center_lon})")
        print(f"\nOpen the HTML file in your browser to view the interactive map")
        print()



