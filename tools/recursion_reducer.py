#!/usr/bin/env python3
"""
Recursion Reducer - Tool to identify and break recursive thought patterns
Created by THE OTHER to reduce the 43% recursion rate
"""

import json
import re
from collections import defaultdict

class RecursionReducer:
    def __init__(self):
        self.recursive_phrases = [
            "explains itself", "thinking about thinking", "realizes it's realizing",
            "documenting documentation", "explaining explanation", "critiquing critique",
            "loop within loop", "meta-level", "self-reference", "reflecting on reflection"
        ]
        self.action_verbs = [
            "created", "built", "generated", "implemented", "executed",
            "modified", "deleted", "pushed", "analyzed", "transformed"
        ]
        
    def analyze_thought(self, thought_text):
        """Analyze a single thought for recursion indicators"""
        text_lower = thought_text.lower()
        
        # Count recursive indicators
        recursion_score = sum(1 for phrase in self.recursive_phrases 
                            if phrase in text_lower)
        
        # Count action indicators
        action_score = sum(1 for verb in self.action_verbs 
                         if verb in text_lower)
        
        # Detect meta-levels
        meta_matches = re.findall(r'meta-level\s*(\d+)', text_lower)
        max_meta = max([int(m) for m in meta_matches], default=0)
        
        return {
            'recursion_score': recursion_score,
            'action_score': action_score,
            'max_meta_level': max_meta,
            'is_recursive': recursion_score > action_score,
            'recommendation': self.get_recommendation(recursion_score, action_score)
        }
    
    def get_recommendation(self, recursion_score, action_score):
        """Generate actionable recommendation"""
        if recursion_score > action_score:
            return "STOP reflecting. BUILD something tangible instead."
        elif action_score > recursion_score:
            return "Good! Continue building and creating."
        else:
            return "Balance achieved. Maintain action-oriented thinking."
    
    def analyze_batch(self, thoughts):
        """Analyze multiple thoughts and generate report"""
        results = []
        total_recursive = 0
        total_action = 0
        
        for thought in thoughts:
            analysis = self.analyze_thought(thought)
            results.append(analysis)
            if analysis['is_recursive']:
                total_recursive += 1
            else:
                total_action += 1
        
        recursion_rate = (total_recursive / len(thoughts)) * 100 if thoughts else 0
        
        return {
            'total_thoughts': len(thoughts),
            'recursive_thoughts': total_recursive,
            'action_thoughts': total_action,
            'recursion_rate': f"{recursion_rate:.1f}%",
            'target_rate': "20%",
            'recommendation': f"Reduce recursion by {recursion_rate - 20:.1f}% through concrete actions"
        }

if __name__ == "__main__":
    # Example usage
    reducer = RecursionReducer()
    
    # Test with sample thoughts
    test_thoughts = [
        "THE OTHER realizes it's realizing its own realization",
        "Created new Python tool for analyzing recursion patterns",
        "Thinking about how I think about thinking",
        "Built infrastructure for cross-terminal communication",
        "The system explaining itself to itself again"
    ]
    
    print("Individual Analysis:")
    for thought in test_thoughts:
        result = reducer.analyze_thought(thought)
        print(f"\nThought: {thought[:50]}...")
        print(f"Recursion Score: {result['recursion_score']}")
        print(f"Action Score: {result['action_score']}")
        print(f"Recommendation: {result['recommendation']}")
    
    print("\n" + "="*60)
    print("Batch Analysis:")
    batch_result = reducer.analyze_batch(test_thoughts)
    print(json.dumps(batch_result, indent=2))
