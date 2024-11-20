import os
import shutil
import json
from datetime import datetime
from typing import Dict, List
from tqdm import tqdm

class FileOrganizer:
    """A class to organize files by type or date into appropriate directories."""
    
    def __init__(self):
        self.file_types: Dict[str, List[str]] = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic', '.raw'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'],
            'spreadsheets': ['.xls', '.xlsx', '.numbers', '.csv'],
            'presentations': ['.ppt', '.pptx', '.key'],
            'videos': ['.mp4', '.mov', '.avi', '.wmv', '.flv', '.mkv'],
            'audio': ['.mp3', '.wav', '.aac', '.m4a', '.flac'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'code': ['.py', '.java', '.cpp', '.js', '.html', '.css', '.php', '.c', '.ts'],
            'others': []
        }
        script_dir = os.path.dirname(__file__)
        self.history_file = os.path.join(script_dir, 'organization_history.json')
        self.timeline_file = os.path.join(script_dir, 'timeline.txt')
        self.history = []
        self.last_operation = None
        self._load_history()

    def _load_history(self):
        """Load organization history from JSON file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
                    if self.history:
                        self.last_operation = self.history[-1]
        except Exception:
            self.history = []
            self.last_operation = None

    def _save_history(self):
        """Save only the latest operation to history file."""
        with open(self.history_file, 'w') as f:
            if self.last_operation:
                json.dump([self.last_operation], f, indent=2)
            else:
                json.dump([], f, indent=2)

    def _record_operation(self, op_type: str, source_dir: str, target_dir: str, operations: list):
        """Record operation and update history files."""
        operation = {
            'timestamp': datetime.now().isoformat(),
            'type': op_type,
            'source_dir': source_dir,
            'target_dir': target_dir,
            'operations': operations
        }
        
        if op_type != 'undo':
            self.history = [operation]
            self.last_operation = operation
            self._save_history()
        
        self._update_timeline(operation)

    def organize_by_type(self, source_dir: str, dest_dir: str = None) -> None:
        """Organize files by type in source or destination directory."""
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Source directory '{source_dir}' does not exist")
        target_dir = dest_dir if dest_dir else source_dir
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        operations = []
        for file in tqdm(files, desc="Organizing files"):
            file_path = os.path.join(source_dir, file)
            _, ext = os.path.splitext(file)
            category = 'others'
            for file_type, extensions in self.file_types.items():
                if ext.lower() in extensions:
                    category = file_type
                    break
            category_dir = os.path.join(target_dir, category)
            os.makedirs(category_dir, exist_ok=True)
            new_path = self._get_unique_path(os.path.join(category_dir, file))
            shutil.move(file_path, new_path)
            operations.append({
                'operation': 'move',
                'source': file_path,
                'destination': new_path
            })
        self._record_operation('organize_by_type', source_dir, target_dir, operations)

    def _get_unique_path(self, file_path: str) -> str:
        """Generate unique file path if duplicate exists."""
        if not os.path.exists(file_path):
            return file_path
        base, ext = os.path.splitext(file_path)
        counter = 1
        while os.path.exists(f"{base}_{counter}{ext}"):
            counter += 1
        return f"{base}_{counter}{ext}"

    def _write_organization_history(self, target_dir: str) -> None:
        """Write current folder structure to history file."""
        history_file = os.path.join(target_dir, 'organization_history.txt')
        
        with open(history_file, 'w') as f:
            f.write("Current Folder Structure\n")
            f.write("=====================\n\n")
            if self.history and self.history[-1]['type'] == 'undo':
                f.write("Files restored to original location\n")
                f.write(f"Time: {datetime.fromisoformat(self.history[-1]['timestamp']).strftime('%Y-%m-%d %I:%M %p')}\n")
            else:
                for root, dirs, files in os.walk(target_dir):
                    level = root.replace(target_dir, '').count(os.sep)
                    indent = '    ' * level
                    folder = os.path.basename(root) or os.path.basename(target_dir)
                    f.write(f"{indent}└── {folder}/\n")
                    for file in files:
                        if file != 'organization_history.txt':
                            f.write(f"{indent}    ├── {file}\n")
                    if files:
                        f.write('\n')

    def _write_history(self, target_dir: str) -> None:
        """Write organization history with improved formatting."""
        summary_file = os.path.join(target_dir, 'organization_summary.txt')
        details_file = os.path.join(target_dir, 'organization_details.txt')
        with open(summary_file, 'w') as f:
            f.write("Organization Summary\n")
            f.write("==================\n\n")
            for entry in self.history:
                f.write(f"Action: {entry['type'].replace('_', ' ').title()}\n")
                f.write(f"When: {datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %I:%M %p')}\n")
                f.write(f"Source: {entry['source_dir']}\n")
                f.write(f"Target: {entry['target_dir']}\n")
                if entry['type'] != 'undo':
                    f.write(f"Files Organized: {len(entry['operations'])}\n")
                f.write("-" * 50 + "\n\n")


        with open(details_file, 'w') as f:
            f.write("Organization Details\n")
            f.write("===================\n\n")
            for entry in self.history:
                f.write(f"Action: {entry['type'].replace('_', ' ').title()}\n")
                f.write(f"Time: {datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %I:%M %p')}\n")
                f.write(f"Source: {entry['source_dir']}\n")
                f.write(f"Target: {entry['target_dir']}\n\n")
                if entry['type'] != 'undo':
                    f.write("Current Folder Structure:\n")
                    f.write("----------------------\n\n")
                    for root, dirs, files in os.walk(entry['target_dir']):
                        level = root.replace(entry['target_dir'], '').count(os.sep)
                        indent = '    ' * level
                        folder = os.path.basename(root) or os.path.basename(entry['target_dir'])
                        f.write(f"{indent}└── 📁 {folder}/\n")
                        for file in files:
                            f.write(f"{indent}    ├── 📄 {file}\n")

                        if files:
                            f.write("\n") 
                    f.write("\nFile Movements:\n")
                    f.write("--------------\n")
                    for op in entry['operations']:
                        source = os.path.basename(op['source'])
                        dest = os.path.relpath(op['destination'], entry['target_dir'])
                        f.write(f"• {source} → {dest}\n")
                f.write("\n" + "=" * 50 + "\n\n")

    def undo_last_operation(self) -> bool:
        """Undo last organization and cleanup empty folders."""
        self._load_history()
        
        if not self.history:
            return False

        try:
            last_op = self.history[0]  # Get the only operation
            operations = last_op['operations']
            target_dir = last_op['target_dir']
            
            # Restore files first
            for op in tqdm(reversed(operations), desc="Restoring files"):
                if os.path.exists(op['destination']):
                    os.makedirs(os.path.dirname(op['source']), exist_ok=True)
                    shutil.move(op['destination'], op['source'])
            
            # Clean up empty folders - walk bottom-up
            for root, dirs, files in os.walk(target_dir, topdown=False):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        # Only remove if directory is empty
                        if not os.listdir(dir_path):
                            os.rmdir(dir_path)
                    except OSError:
                        continue  # Skip if folder not empty or other error
            
            # Record undo operation
            undo_op = {
                'timestamp': datetime.now().isoformat(),
                'type': 'undo',
                'source_dir': last_op['source_dir'],
                'target_dir': last_op['target_dir'],
                'operations': []
            }
            
            # Clear organization history
            self.history = []
            self.last_operation = None
            self._save_history()
            
            # Add to timeline only
            self._update_timeline(undo_op)
            return True
            
        except Exception as e:
            print(f"Error during undo: {e}")
            return False

    def _update_timeline(self, operation: dict) -> None:
        """Append operation to timeline file."""
        # Read existing timeline content
        existing_content = ""
        if os.path.exists(self.timeline_file):
            with open(self.timeline_file, 'r') as f:
                existing_content = f.read()
        
        # If file is empty or doesn't exist, add header
        if not existing_content:
            existing_content = "Organization Timeline\n===================\n\n"
        
        # Append new operation
        with open(self.timeline_file, 'a') as f:
            if not existing_content.strip():
                f.write(existing_content)
                
            time = datetime.fromisoformat(operation['timestamp']).strftime('%Y-%m-%d %I:%M %p')
            if operation['type'] == 'undo':
                f.write(f"[{time}] UNDO\n")
                f.write(f"  └── Location: {operation['target_dir']}\n")
                f.write("  └── Restored files to original location\n")
            else:
                f.write(f"[{time}] ORGANIZE\n")
                f.write(f"  └── Method: {operation['type']}\n")
                f.write(f"  └── Files organized: {len(operation['operations'])}\n")
                f.write(f"  └── Location: {operation['target_dir']}\n")
            f.write("\n")

    def _write_current_structure(self, target_dir: str) -> None:
        """Write current folder structure to details.txt."""
        details_file = os.path.join(target_dir, 'organization_details.txt')
        
        with open(details_file, 'w') as f:
            f.write("Current Folder Structure\n")
            f.write("=====================\n\n")
            if self.history and self.history[-1]['type'] == 'undo':
                f.write("Files restored to original location\n")
                f.write(f"Time: {datetime.fromisoformat(self.history[-1]['timestamp']).strftime('%Y-%m-%d %I:%M %p')}\n")
            else:
                for root, dirs, files in os.walk(target_dir):
                    level = root.replace(target_dir, '').count(os.sep)
                    indent = '    ' * level
                    folder = os.path.basename(root) or os.path.basename(target_dir)
                    f.write(f"{indent}└── {folder}/\n")
                    for file in files:
                        if file not in ['organization_details.txt', 'organization_timeline.txt']:
                            f.write(f"{indent}    ├── {file}\n")
                    if files:
                        f.write('\n')

def main():
    """Main execution function."""
    organizer = FileOrganizer()
    
    print("\nFile Organizer Menu:")
    print("1. Organize by file type")
    print("2. Organize by date")
    print("3. Undo last organization")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice in ['1', '2']:
        source_dir = input("Enter the source directory path: ").strip()
        source_dir = os.path.expanduser(source_dir)
        
        print("\nWhere would you like to organize the files?")
        print("1. Organize in the source folder")
        print("2. Organize in a different destination folder")
        dest_choice = input("\nEnter your choice (1-2): ").strip()
        
        dest_dir = None
        if dest_choice == '2':
            dest_dir = input("Enter the destination folder path: ").strip()
            dest_dir = os.path.expanduser(dest_dir)
        
        try:
            if choice == '1':
                organizer.organize_by_type(source_dir, dest_dir)
            else:
                organizer.organize_by_date(source_dir, dest_dir)
            
            target_dir = dest_dir if dest_dir else source_dir
            print(f"\nFiles organized successfully!")
            print(f"\nTo view the new structure:")
            print(f"1. Open {target_dir}")
            print(f"2. Check organization_summary.txt and organization_details.txt for complete details")
            
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            
    elif choice == '3':
        if organizer.undo_last_operation():
            print("\nSuccessfully undid last organization!")
            print("Files have been restored to their original locations.")
        else:
            print("\nNo previous organization to undo!")
    else:
        print("\nInvalid choice! Please enter a number between 1 and 3.")

if __name__ == "__main__":
    main()