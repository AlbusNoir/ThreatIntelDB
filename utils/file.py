"""
Handle file reading
"""

def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        return lines