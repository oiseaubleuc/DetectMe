#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google Dorks Module
Performs advanced Google searches using dork queries
"""

import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from datetime import datetime
import time
import urllib.parse

class GoogleDorks:
    """Google dorks search functionality"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.reports_path = self.base_path / "Reports"
        self.reports_path.mkdir(exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def build_dork_query(self, base_query, dork_type="general", date_range=None):
        """Build Google dork query"""
        dorks = {
            "filetype": f"filetype:pdf {base_query}",
            "site": f"site:{base_query}",
            "intitle": f"intitle:{base_query}",
            "inurl": f"inurl:{base_query}",
            "intext": f"intext:{base_query}",
            "images": f"{base_query}",
            "videos": f"{base_query}",
        }
        
        query = dorks.get(dork_type, base_query)
        
        if date_range:
            if isinstance(date_range, str):
                query += f" after:{date_range}"
            elif isinstance(date_range, tuple) and len(date_range) == 2:
                query += f" after:{date_range[0]} before:{date_range[1]}"
        
        return query
    
    def search_google(self, query, num_results=10):
        """Search Google (Note: This is a simplified version)"""
        # Note: Google has strict rate limiting and may block automated requests
        # For production use, consider using Google Custom Search API
        
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = []
                
                # Parse search results (Google's HTML structure may change)
                for result in soup.find_all('div', class_='g')[:num_results]:
                    try:
                        title_elem = result.find('h3')
                        link_elem = result.find('a')
                        snippet_elem = result.find('span', class_='aCOpRe')
                        
                        if title_elem and link_elem:
                            results.append({
                                "title": title_elem.get_text(),
                                "url": link_elem.get('href', ''),
                                "snippet": snippet_elem.get_text() if snippet_elem else ""
                            })
                    except:
                        continue
                
                return results
            else:
                return []
        except Exception as e:
            print(f"⚠️  Error searching Google: {str(e)}")
            return []
    
    def search(self, query, dork_type="general", date_range=None, num_results=10):
        """Perform Google dork search"""
        print(f"\n🔍 Google Dorks Search")
        print("=" * 50)
        
        dork_query = self.build_dork_query(query, dork_type, date_range)
        print(f"Query: {dork_query}")
        print()
        
        print("Searching...", end=" ", flush=True)
        results = self.search_google(dork_query, num_results)
        
        if results:
            print(f"✅ Found {len(results)} results")
            print()
            print("Top Results:")
            for i, result in enumerate(results[:5], 1):
                print(f"\n{i}. {result.get('title', 'No title')}")
                print(f"   URL: {result.get('url', 'N/A')}")
                if result.get('snippet'):
                    print(f"   {result.get('snippet')[:100]}...")
        else:
            print("❌ No results found or search blocked")
            print("⚠️  Note: Google may block automated searches. Consider using Google Custom Search API.")
        
        print("\n" + "=" * 50)
        
        # Save report
        report_data = {
            "original_query": query,
            "dork_query": dork_query,
            "dork_type": dork_type,
            "date_range": date_range,
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        
        self.save_report(report_data)
    
    def save_report(self, report_data):
        """Save search results to a report file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_clean = report_data["original_query"].replace(" ", "_")[:50]
        report_file = self.reports_path / f"dorks_{query_clean}_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Report saved: {report_file}")
        print()



