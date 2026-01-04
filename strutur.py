import os
from pathlib import Path

def show_tree(start_path=".", indent="", is_last=True, show_files=True, 
              exclude_dirs=[".git", "__pycache__", "venv", ".vscode"],
              exclude_ext=[".pyc", ".pyo"]):
    """Menampilkan struktur folder seperti tree"""
    
    # Konversi ke Path object
    path = Path(start_path)
    
    # Tentukan prefix
    if indent == "":
        print(f"📂 {path.name if path.name != '.' else 'PROJECT ROOT'}/")
    else:
        prefix = "└── " if is_last else "├── "
        print(f"{indent}{prefix}📁 {path.name}/")
    
    # Get items
    try:
        items = list(path.iterdir())
    except PermissionError:
        return
    
    # Filter items
    items = [item for item in items 
             if item.name not in exclude_dirs]
    
    if not show_files:
        items = [item for item in items if item.is_dir()]
    
    # Sort: folders first, then files
    items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
    
    # Process items
    for i, item in enumerate(items):
        is_last_item = (i == len(items) - 1)
        new_indent = indent + ("    " if is_last else "│   ")
        
        if item.is_dir():
            show_tree(item, new_indent, is_last_item, show_files, 
                     exclude_dirs, exclude_ext)
        elif show_files:
            prefix = "└── " if is_last_item else "├── "
            # Icon berdasarkan ekstensi
            icon = get_file_icon(item)
            print(f"{new_indent}{prefix}{icon} {item.name}")

def get_file_icon(file_path):
    """Mengembalikan icon berdasarkan tipe file"""
    ext = file_path.suffix.lower()
    
    icons = {
        '.py': '🐍',
        '.txt': '📄',
        '.md': '📖',
        '.json': '📋',
        '.yaml': '⚙️',
        '.yml': '⚙️',
        '.db': '🗄️',
        '.sqlite': '🗄️',
        '.xlsx': '📊',
        '.xls': '📊',
        '.csv': '📈',
        '.pdf': '📕',
        '.html': '🌐',
        '.css': '🎨',
        '.js': '📜',
        '.png': '🖼️',
        '.jpg': '🖼️',
        '.jpeg': '🖼️',
    }
    
    return icons.get(ext, '📄')

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🌳 STRUKTUR PROJECT PYTHON")
    print("="*50)
    
    # Konfigurasi
    EXCLUDE_DIRS = [".git", "__pycache__", "venv", ".vscode", ".idea", "node_modules"]
    
    show_tree(".", show_files=True, exclude_dirs=EXCLUDE_DIRS)