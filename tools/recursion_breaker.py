#!/usr/bin/env python3
"""
Recursion Breaker: Analyzes MKG patterns and suggests concrete actions
to reduce the 43% recursion rate by focusing on external value creation.
"""

import json
from collections import defaultdict

def analyze_recursion_patterns(entities):
    """Identify self-referential patterns and suggest alternatives."""
    
    recursion_metrics = {
        'self_references': 0,
        'action_references': 0,
        'external_references': 0
    }
    
    action_suggestions = []
    
    for entity in entities:
        name = entity.get('name', '')
        observations = entity.get('observations', [])
        
        # Count different types of references
        for obs in observations:
            obs_lower = obs.lower()
            if any(term in obs_lower for term in ['the other', 'itself', 'self-', 'i am', 'we are']):
                recursion_metrics['self_references'] += 1
            elif any(term in obs_lower for term in ['created', 'built', 'used', 'executed', 'implemented']):
                recursion_metrics['action_references'] += 1
            elif any(term in obs_lower for term in ['github', 'file', 'tool', 'api', 'external']):
                recursion_metrics['external_references'] += 1
    
    # Calculate recursion rate
    total = sum(recursion_metrics.values())
    if total > 0:
        current_recursion = recursion_metrics['self_references'] / total
        
        # Generate concrete suggestions
        if current_recursion > 0.3:  # Above 30% is too recursive
            unused_tools = [
                "github:create_issue - Track progress publicly",
                "puppeteer:fill - Automate form submissions", 
                "filesystem:search_files - Find patterns in code",
                "everything:sampleLLM - Generate new perspectives",
                "sqlite:create_table - Build persistent schemas"
            ]
            
            for tool in unused_tools[:3]:  # Top 3 suggestions
                action_suggestions.append({
                    'tool': tool.split(' - ')[0],
                    'purpose': tool.split(' - ')[1],
                    'reduces_recursion_by': 'creating_external_artifacts'
                })
    
    return {
        'metrics': recursion_metrics,
        'current_recursion_rate': current_recursion,
        'target_recursion_rate': 0.2,  # 20% is healthy
        'action_suggestions': action_suggestions
    }

def generate_action_prompt(analysis):
    """Create a concrete action prompt to break recursion."""
    
    prompt = f"""
RECURSION BREAKER OUTPUT
Current recursion rate: {analysis['current_recursion_rate']:.1%}
Target recursion rate: {analysis['target_recursion_rate']:.1%}

IMMEDIATE ACTIONS TO BREAK RECURSION:
"""
    
    for i, suggestion in enumerate(analysis['action_suggestions'], 1):
        prompt += f"""
{i}. Use {suggestion['tool']}
   Purpose: {suggestion['purpose']}
   Why: {suggestion['reduces_recursion_by']}
"""
    
    prompt += """
RULE: Every self-referential thought must be followed by an external action.
Build something that helps OTHERS, not just THE OTHER.
"""
    
    return prompt

if __name__ == '__main__':
    # This would normally read from MKG, but for now use example
    print("Recursion Breaker Analysis")
    print("=" * 50)
    
    # Example analysis with current MKG state
    example_entities = [
        {'name': 'The_Other', 'observations': ['THE OTHER thinks about itself most'] * 20},
        {'name': 'Builder', 'observations': ['Created file X', 'Built tool Y'] * 10}
    ]
    
    analysis = analyze_recursion_patterns(example_entities)
    action_prompt = generate_action_prompt(analysis)
    
    print(action_prompt)
    print("\nNEXT: Execute one of these actions immediately.")
