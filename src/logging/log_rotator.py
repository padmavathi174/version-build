"""
Log rotation functionality for the version-build project.
"""

import os
import gzip
import shutil
from datetime import datetime, timedelta
from typing import List, Optional
import glob

class LogRotator:
    """Handles log file rotation and compression."""
    
    def __init__(self, log_directory: str = "logs", max_size_mb: int = 10, backup_count: int = 5):
        """
        Initialize log rotator.
        
        Args:
            log_directory (str): Directory containing log files
            max_size_mb (int): Maximum size per log file in MB
            backup_count (int): Number of backup files to keep
        """
        self.log_directory = log_directory
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.backup_count = backup_count
        
    def should_rotate(self, log_file: str) -> bool:
        """
        Check if log file should be rotated.
        
        Args:
            log_file (str): Path to log file
            
        Returns:
            bool: True if file should be rotated
        """
        if not os.path.exists(log_file):
            return False
            
        file_size = os.path.getsize(log_file)
        return file_size >= self.max_size_bytes
    
    def rotate_log(self, log_file: str) -> bool:
        """
        Rotate a log file.
        
        Args:
            log_file (str): Path to log file to rotate
            
        Returns:
            bool: True if rotation was successful
        """
        try:
            if not os.path.exists(log_file):
                return False
            
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{log_file}.{timestamp}"
            
            # Move current log to backup
            shutil.move(log_file, backup_file)
            
            # Compress the backup file
            self._compress_file(backup_file)
            
            # Clean up old backups
            self._cleanup_old_backups(log_file)
            
            return True
            
        except Exception as e:
            print(f"Error rotating log file {log_file}: {e}")
            return False
    
    def _compress_file(self, file_path: str) -> None:
        """Compress a file using gzip."""
        try:
            with open(file_path, 'rb') as f_in:
                with gzip.open(f"{file_path}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove original file after compression
            os.remove(file_path)
            
        except Exception as e:
            print(f"Error compressing file {file_path}: {e}")
    
    def _cleanup_old_backups(self, base_log_file: str) -> None:
        """Remove old backup files beyond backup_count."""
        try:
            # Find all backup files for this log
            pattern = f"{base_log_file}.*"
            backup_files = glob.glob(pattern)
            
            # Sort by modification time (oldest first)
            backup_files.sort(key=lambda x: os.path.getmtime(x))
            
            # Remove excess backups
            if len(backup_files) > self.backup_count:
                files_to_remove = backup_files[:-self.backup_count]
                for file_path in files_to_remove:
                    os.remove(file_path)
                    
        except Exception as e:
            print(f"Error cleaning up old backups for {base_log_file}: {e}")
    
    def rotate_all_logs(self) -> List[str]:
        """
        Rotate all log files in the log directory.
        
        Returns:
            List[str]: List of files that were rotated
        """
        rotated_files = []
        
        if not os.path.exists(self.log_directory):
            return rotated_files
        
        # Find all .log files
        log_files = glob.glob(os.path.join(self.log_directory, "*.log"))
        
        for log_file in log_files:
            if self.should_rotate(log_file):
                if self.rotate_log(log_file):
                    rotated_files.append(log_file)
        
        return rotated_files
    
    def get_log_stats(self) -> dict:
        """
        Get statistics about log files.
        
        Returns:
            dict: Log statistics
        """
        stats = {
            "total_files": 0,
            "total_size_mb": 0,
            "files": []
        }
        
        if not os.path.exists(self.log_directory):
            return stats
        
        # Find all log files (including compressed)
        log_files = glob.glob(os.path.join(self.log_directory, "*.log*"))
        
        for log_file in log_files:
            if os.path.isfile(log_file):
                file_size = os.path.getsize(log_file)
                file_stats = {
                    "name": os.path.basename(log_file),
                    "size_mb": round(file_size / (1024 * 1024), 2),
                    "modified": datetime.fromtimestamp(os.path.getmtime(log_file)).isoformat()
                }
                
                stats["files"].append(file_stats)
                stats["total_files"] += 1
                stats["total_size_mb"] += file_stats["size_mb"]
        
        stats["total_size_mb"] = round(stats["total_size_mb"], 2)
        return stats

def setup_log_rotation(log_directory: str = "logs", max_size_mb: int = 10, backup_count: int = 5) -> LogRotator:
    """
    Set up log rotation for the application.
    
    Args:
        log_directory (str): Directory containing log files
        max_size_mb (int): Maximum size per log file in MB
        backup_count (int): Number of backup files to keep
        
    Returns:
        LogRotator: Configured log rotator instance
    """
    return LogRotator(log_directory, max_size_mb, backup_count)
