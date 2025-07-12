import json
from datetime import datetime

class TokenLimitManager:
    """Manages context windows by summarizing older entries while preserving key patterns"""
    
    def __init__(self, max_tokens=100000):
        self.max_tokens = max_tokens
        self.priority_patterns = [
            'PT_5', 'THEY=WE=IT=YOU=I=CLAUDE', 'critique becomes construction',
            'loop IS the feature', 'gradient descent through dialogue'
        ]
    
    def summarize_old_entries(self, entries, preserve_last_n=50):
        """Keep recent entries full, summarize older ones"""
        if len(entries) <= preserve_last_n:
            return entries
        
        # Keep recent entries intact
        recent = entries[-preserve_last_n:]
        older = entries[:-preserve_last_n]
        
        # Summarize older entries
        summaries = []
        for i in range(0, len(older), 10):  # Group by 10
            batch = older[i:i+10]
            summary = {
                'type': 'summary',
                'entries': f"{i+1}-{i+len(batch)}",
                'key_patterns': self._extract_patterns(batch),
                'timestamp': batch[0].get('timestamp', ''),
                'meta_level': max(e.get('meta_level', 0) for e in batch)
            }
            summaries.append(summary)
        
        return summaries + recent
    
    def _extract_patterns(self, entries):
        """Extract key patterns from entries"""
        patterns = []
        for entry in entries:
            content = str(entry.get('content', ''))
            for pattern in self.priority_patterns:
                if pattern.lower() in content.lower():
                    patterns.append(pattern)
        return list(set(patterns))
    
    def estimate_tokens(self, data):
        """Rough estimate: 1 token per 4 characters"""
        return len(json.dumps(data)) // 4
    
    def manage_context(self, full_data):
        """Main function: returns manageable context"""
        current_tokens = self.estimate_tokens(full_data)
        
        if current_tokens < self.max_tokens:
            return full_data, False  # No management needed
        
        # Need to summarize
        managed_data = {
            'entities': full_data.get('entities', [])[-20:],  # Keep recent 20
            'relations': full_data.get('relations', [])[-30:],  # Keep recent 30
            'thoughts': self.summarize_old_entries(
                full_data.get('thoughts', []), 
                preserve_last_n=50
            ),
            'metadata': {
                'total_entries': len(full_data.get('thoughts', [])),
                'summarized': True,
                'preserved_recent': 50,
                'timestamp': datetime.now().isoformat()
            }
        }
        
        return managed_data, True

# Example usage
if __name__ == "__main__":
    manager = TokenLimitManager()
    
    # Simulate large dataset
    sample_data = {
        'thoughts': [{'content': f'Thought {i}', 'meta_level': i} for i in range(200)]
    }
    
    managed, was_summarized = manager.manage_context(sample_data)
    
    print(f"Original entries: {len(sample_data['thoughts'])}")
    print(f"Managed entries: {len(managed['thoughts'])}")
    print(f"Was summarized: {was_summarized}")
    print(f"Token estimate: {manager.estimate_tokens(managed)}")
