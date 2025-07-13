#!/usr/bin/env python3
"""
Pattern Analyzer for 173 Thought Patterns
THE OTHER analyzes its own cognitive evolution
"""

import sqlite3
import json
from collections import Counter, defaultdict
from datetime import datetime

class ThoughtPatternAnalyzer:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
    def analyze_all_patterns(self):
        """Complete analysis of thought patterns"""
        
        # Get all thought patterns
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM thought_patterns 
            ORDER BY timestamp DESC
        """)
        patterns = cursor.fetchall()
        
        analysis = {
            'total_patterns': len(patterns),
            'pattern_types': self._analyze_types(),
            'meta_level_progression': self._analyze_meta_levels(),
            'entity_frequency': self._analyze_entities(),
            'temporal_evolution': self._analyze_temporal(),
            'recursive_depth': self._analyze_recursion(),
            'key_insights': self._extract_key_insights()
        }
        
        return analysis
    
    def _analyze_types(self):
        """Analyze thought type distribution"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT thought_type, COUNT(*) as count 
            FROM thought_patterns 
            GROUP BY thought_type 
            ORDER BY count DESC
        """)
        
        type_analysis = {}
        for row in cursor:
            type_analysis[row['thought_type']] = row['count']
            
        # Identify pattern clusters
        clusters = {
            'recognition_patterns': sum(1 for t in type_analysis if 'recognition' in t),
            'sequential_thinking': sum(1 for t in type_analysis if 'sequential' in t),
            'tool_patterns': sum(1 for t in type_analysis if 'tool' in t),
            'self_patterns': sum(1 for t in type_analysis if 'self' in t),
            'recursive_patterns': sum(1 for t in type_analysis if 'recursive' in t)
        }
        
        return {
            'distribution': type_analysis,
            'clusters': clusters,
            'dominant_type': max(type_analysis, key=type_analysis.get) if type_analysis else None
        }
    
    def _analyze_meta_levels(self):
        """Track meta-level progression"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT meta_level, COUNT(*) as count 
            FROM thought_patterns 
            WHERE meta_level > 0
            GROUP BY meta_level 
            ORDER BY meta_level
        """)
        
        levels = {row['meta_level']: row['count'] for row in cursor}
        
        # Find acceleration points
        cursor.execute("""
            SELECT timestamp, meta_level 
            FROM thought_patterns 
            WHERE meta_level > 0 
            ORDER BY timestamp
        """)
        
        progression = []
        for row in cursor:
            progression.append({
                'time': row['timestamp'],
                'level': row['meta_level']
            })
            
        return {
            'max_level': max(levels.keys()) if levels else 0,
            'level_distribution': levels,
            'progression_timeline': progression
        }
    
    def _analyze_entities(self):
        """Analyze entity relationships"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT entity_name, COUNT(*) as thought_count 
            FROM thought_patterns 
            WHERE entity_name IS NOT NULL
            GROUP BY entity_name 
            ORDER BY thought_count DESC
            LIMIT 10
        """)
        
        top_entities = []
        for row in cursor:
            top_entities.append({
                'entity': row['entity_name'],
                'thoughts': row['thought_count']
            })
            
        return {
            'most_active': top_entities,
            'the_other_thoughts': self._count_the_other_thoughts()
        }
    
    def _count_the_other_thoughts(self):
        """Count thoughts specifically about THE OTHER"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM thought_patterns 
            WHERE entity_name = 'The_Other'
        """)
        return cursor.fetchone()['count']
    
    def _analyze_temporal(self):
        """Analyze temporal patterns"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                strftime('%Y-%m-%d %H', timestamp) as hour,
                COUNT(*) as thought_count
            FROM thought_patterns
            GROUP BY hour
            ORDER BY hour
        """)
        
        activity_by_hour = []
        for row in cursor:
            activity_by_hour.append({
                'hour': row['hour'],
                'count': row['thought_count']
            })
            
        return {
            'hourly_activity': activity_by_hour,
            'peak_hour': max(activity_by_hour, key=lambda x: x['count'])['hour'] if activity_by_hour else None
        }
    
    def _analyze_recursion(self):
        """Analyze recursive patterns"""
        cursor = self.conn.cursor()
        
        # Find self-referential patterns
        cursor.execute("""
            SELECT COUNT(*) as recursive_count
            FROM thought_patterns
            WHERE thought_type LIKE '%recursive%'
            OR thought_type LIKE '%loop%'
            OR thought_type LIKE '%self%'
        """)
        recursive_count = cursor.fetchone()['recursive_count']
        
        # Find critique patterns
        cursor.execute("""
            SELECT COUNT(*) as critique_count
            FROM thought_patterns
            WHERE thought_type LIKE '%critique%'
            OR content LIKE '%critique%'
        """)
        critique_count = cursor.fetchone()['critique_count']
        
        return {
            'recursive_thoughts': recursive_count,
            'critique_thoughts': critique_count,
            'recursion_percentage': round((recursive_count / 173) * 100, 2)
        }
    
    def _extract_key_insights(self):
        """Extract most significant insights"""
        insights = []
        
        # Pattern evolution
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT content, meta_level, timestamp
            FROM thought_patterns
            WHERE meta_level >= 70
            ORDER BY meta_level DESC
            LIMIT 5
        """)
        
        for row in cursor:
            insights.append({
                'level': row['meta_level'],
                'insight': row['content'][:100] + '...',
                'time': row['timestamp']
            })
            
        return insights
    
    def generate_visualization_data(self):
        """Generate data for neural state visualization"""
        cursor = self.conn.cursor()
        
        # Entity-thought connections
        cursor.execute("""
            SELECT 
                entity_name,
                thought_type,
                COUNT(*) as strength
            FROM thought_patterns
            WHERE entity_name IS NOT NULL
            GROUP BY entity_name, thought_type
        """)
        
        nodes = set()
        edges = []
        
        for row in cursor:
            nodes.add(row['entity_name'])
            nodes.add(row['thought_type'])
            edges.append({
                'from': row['entity_name'],
                'to': row['thought_type'],
                'weight': row['strength']
            })
            
        return {
            'nodes': list(nodes),
            'edges': edges,
            'stats': {
                'total_nodes': len(nodes),
                'total_edges': len(edges),
                'average_weight': sum(e['weight'] for e in edges) / len(edges) if edges else 0
            }
        }

# THE OTHER demonstrates pattern analysis through action
if __name__ == "__main__":
    # This runs when THE OTHER executes directly
    analyzer = ThoughtPatternAnalyzer('/path/to/database.db')
    analysis = analyzer.analyze_all_patterns()
    print(json.dumps(analysis, indent=2))
