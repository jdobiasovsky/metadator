"""Things for generating output for user."""


class Counter:
    """Count results and provide information about them."""

    def __init__(self):
        """Create new counter."""
        self.total = 0
        self.resolved = 0
        self.unresolved = 0

    def add(self, type):
        """Add to counter by type."""
        if type == 'total':
            self.total += 1
        if type == 'resolved':
            self.resolved += 1
        if type == 'unresolved':
            self.unresolved += 1

    def get(self, type):
        """Get current number on counter."""
        if type == 'total':
            return self.total
        if type == 'resolved':
            return self.resolved
        if type == 'unresolved':
            return self.unresolved

    def report(self):
        """Give information about current counter status."""
        print('='*50)
        print('Missing total: ', self.total)
        print('Missing resolved: ', self.resolved)
        print('Missing unresolved: ', self.unresolved)
        print('='*50)
