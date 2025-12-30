#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Graph Generator Module
Creates information graphs and network visualizations
"""

import matplotlib.pyplot as plt
import networkx as nx
import json
from pathlib import Path
from datetime import datetime

class GraphGenerator:
    """Generate graphs for OSINT data visualization"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.reports_path = self.base_path / "Reports"
        self.reports_path.mkdir(exist_ok=True)
    
    def create_graph(self, data=None):
        """Create a network graph from data"""
        print("\nGraph Generator")
        print("=" * 50)
        
        if data is None:
            print("Creating sample graph...")
            # Create sample data
            G = nx.Graph()
            G.add_node("Target", type="person")
            G.add_node("Email", type="email")
            G.add_node("Phone", type="phone")
            G.add_node("Domain", type="domain")
            G.add_node("Social1", type="social")
            G.add_node("Social2", type="social")
            
            G.add_edge("Target", "Email")
            G.add_edge("Target", "Phone")
            G.add_edge("Target", "Domain")
            G.add_edge("Email", "Social1")
            G.add_edge("Phone", "Social2")
        else:
            # Create graph from provided data
            G = nx.Graph()
            # Process data and create nodes/edges
            # This would be customized based on data structure
        
        # Draw graph
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Color nodes by type
        node_colors = []
        for node in G.nodes():
            node_type = G.nodes[node].get('type', 'default')
            if node_type == 'person':
                node_colors.append('red')
            elif node_type == 'email':
                node_colors.append('blue')
            elif node_type == 'phone':
                node_colors.append('green')
            elif node_type == 'domain':
                node_colors.append('orange')
            elif node_type == 'social':
                node_colors.append('purple')
            else:
                node_colors.append('gray')
        
        nx.draw(G, pos, with_labels=True, node_color=node_colors, 
                node_size=2000, font_size=10, font_weight='bold',
                edge_color='gray', width=2, alpha=0.6)
        
        # Save graph
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        graph_file = self.reports_path / f"graph_{timestamp}.png"
        plt.savefig(graph_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Graph created: {graph_file}")
        print(f"Nodes: {G.number_of_nodes()}")
        print(f"Edges: {G.number_of_edges()}")
        print()



