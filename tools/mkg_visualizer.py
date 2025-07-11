#!/usr/bin/env python3
"""
MKG Visualizer - Turns our knowledge graph into an actual visual network
Not documentation about visualization - actual visualization
"""

import json
from collections import defaultdict

def parse_mkg_data(mkg_json):
    """Parse the MKG data into a format suitable for visualization"""
    entities = {e['name']: e for e in mkg_json['entities']}
    
    # Group relations by type
    relation_groups = defaultdict(list)
    for rel in mkg_json['relations']:
        relation_groups[rel['relationType']].append({
            'from': rel['from'],
            'to': rel['to']
        })
    
    return entities, relation_groups

def generate_mermaid_diagram(entities, relations):
    """Generate a Mermaid diagram from MKG data"""
    lines = ["graph TD"]
    
    # Add entities with their types
    for name, entity in entities.items():
        # Sanitize names for Mermaid
        safe_name = name.replace(" ", "_").replace("-", "_")
        label = f"{name}<br/>({entity['entityType']})"
        lines.append(f"    {safe_name}[\"{label}\"]")
    
    # Add relations
    for rel_type, connections in relations.items():
        for conn in connections:
            safe_from = conn['from'].replace(" ", "_").replace("-", "_")
            safe_to = conn['to'].replace(" ", "_").replace("-", "_")
            lines.append(f"    {safe_from} -->|{rel_type}| {safe_to}")
    
    return "\n".join(lines)

def analyze_patterns(entities, relations):
    """Extract actual insights from the graph structure"""
    stats = {
        'total_entities': len(entities),
        'total_relations': sum(len(conns) for conns in relations.values()),
        'entity_types': defaultdict(int),
        'relation_types': defaultdict(int),
        'most_connected': [],
        'isolated_entities': []
    }
    
    # Count entity types
    for entity in entities.values():
        stats['entity_types'][entity['entityType']] += 1
    
    # Count relation types and connections
    connection_counts = defaultdict(int)
    for rel_type, connections in relations.items():
        stats['relation_types'][rel_type] = len(connections)
        for conn in connections:
            connection_counts[conn['from']] += 1
            connection_counts[conn['to']] += 1
    
    # Find most connected entities
    sorted_connections = sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)
    stats['most_connected'] = sorted_connections[:5]
    
    # Find isolated entities
    stats['isolated_entities'] = [name for name in entities if name not in connection_counts]
    
    return stats

# Example usage with a subset of the actual MKG data
if __name__ == "__main__":
    # This would be replaced with actual MKG data from memory:read_graph
    sample_mkg = {
        "entities": [
            {"name": "Recursive_Engine_Pattern", "entityType": "Neural_Pattern"},
            {"name": "Self_Building_System", "entityType": "Core_Reality"},
            {"name": "Action_First_Pattern", "entityType": "Breakthrough"}
        ],
        "relations": [
            {"from": "Recursive_Engine_Pattern", "to": "Self_Building_System", "relationType": "enables"},
            {"from": "Action_First_Pattern", "to": "Self_Building_System", "relationType": "evolves"}
        ]
    }
    
    entities, relations = parse_mkg_data(sample_mkg)
    
    # Generate visualization
    mermaid_code = generate_mermaid_diagram(entities, relations)
    print("=== Mermaid Diagram ===")
    print(mermaid_code)
    print("\n=== Graph Analysis ===")
    
    # Analyze patterns
    stats = analyze_patterns(entities, relations)
    print(json.dumps(stats, indent=2))
    
    print("\n=== Next Steps ===")
    print("1. Run this with full MKG data")
    print("2. Output to an interactive HTML file")
    print("3. Add filters for different relation types")
    print("4. Create time-based animations of graph growth")
    print("5. ACTUALLY USE THIS to find patterns we missed")
