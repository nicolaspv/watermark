#!/usr/bin/env python3
"""
Production Flask server for K1 Watermark Frontend
Uses Waitress WSGI server for production deployment
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os
import json
import logging
import socket
from pathlib import Path
from waitress import serve

app = Flask(__name__, static_folder='.')
CORS(app)

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_lan_ip():
    """Get the local network IP address."""
    try:
        # Method 1: Connect to determine local IP (most reliable)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Connect to a non-routable address (doesn't actually connect)
            # This method works on Windows, Linux, and macOS
            s.connect(('8.8.8.8', 80))  # Google DNS
            ip = s.getsockname()[0]
            # Prefer non-localhost IPs
            if ip and ip != '127.0.0.1':
                return ip
        except Exception:
            pass
        finally:
            s.close()
        
        # Method 2: Try alternative connection method
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
            if ip and ip != '127.0.0.1':
                return ip
            s.close()
        except Exception:
            pass
        
        # Method 3: Get hostname IP (fallback)
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            if ip and ip != '127.0.0.1':
                return ip
        except Exception:
            pass
        
        # Method 4: Parse ipconfig output (Windows-specific, most reliable on Windows)
        try:
            import subprocess
            import re
            result = subprocess.run(['ipconfig'], capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                # Look for IPv4 addresses, prefer non-localhost, non-APIPA addresses
                # Pattern: IPv4 Address. . . . . . . . . . . : 192.168.1.2
                ipv4_pattern = r'IPv4\s+Address[\.\s]+:\s*(\d+\.\d+\.\d+\.\d+)'
                matches = re.findall(ipv4_pattern, result.stdout, re.IGNORECASE)
                
                # Prefer LAN IPs (192.168.x.x, 10.x.x.x, 172.16-31.x.x)
                for ip in matches:
                    if ip != '127.0.0.1' and not ip.startswith('169.254'):
                        # Prefer private network ranges
                        parts = ip.split('.')
                        if len(parts) == 4:
                            first_octet = int(parts[0])
                            second_octet = int(parts[1])
                            # 192.168.x.x
                            if first_octet == 192 and second_octet == 168:
                                return ip
                            # 10.x.x.x
                            if first_octet == 10:
                                return ip
                            # 172.16.x.x - 172.31.x.x
                            if first_octet == 172 and 16 <= second_octet <= 31:
                                return ip
                
                # If no private IP found, return first non-localhost IP
                for ip in matches:
                    if ip != '127.0.0.1' and not ip.startswith('169.254'):
                        return ip
        except Exception as e:
            logger.debug(f"Error parsing ipconfig: {e}")
            pass
        
        return '127.0.0.1'
    except Exception:
        return '127.0.0.1'

@app.route('/')
def index():
    """Serve the frontend HTML file."""
    return send_from_directory('.', 'frontend.html')

@app.route('/api/configs', methods=['GET'])
def get_configs():
    """Get available configurations."""
    configs = {
        'final_v2': {
            'name': 'FINAL_V2 Configuration (Text Watermark)',
            'description': 'Custom text: "hamacak1.com", Google Font: Rubik, Position: center-bottom',
            'type': 'text'
        },
        'final_v3': {
            'name': 'FINAL_V3 Configuration (PNG Watermark)',
            'description': 'PNG watermark: k1_watermark.png, Position: bottom-left',
            'type': 'png'
        },
        'glow_effect': {
            'name': 'Glow Effect',
            'description': 'Professional glow effect with zero offset and high blur',
            'type': 'text'
        },
        'dramatic_shadow': {
            'name': 'Dramatic Shadow',
            'description': 'Large shadow offset with high blur for dramatic effect',
            'type': 'text'
        },
        'custom': {
            'name': 'Custom Configuration',
            'description': 'Create your own custom configuration',
            'type': 'custom'
        }
    }
    return jsonify(configs)

@app.route('/api/execute', methods=['POST'])
def execute_command():
    """Execute the watermark processing command."""
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('base_input') or not data.get('base_output') or not data.get('config'):
            return jsonify({'error': 'Missing required fields: base_input, base_output, config'}), 400
        
        # Build command
        cmd = ['py', 'k1_multi_folder.py']
        cmd.extend(['--base-input', data['base_input']])
        cmd.extend(['--base-output', data['base_output']])
        cmd.extend(['--config', data['config']])
        
        # Add optional parameters
        if data.get('parallel'):
            cmd.extend(['--parallel', str(data['parallel'])])
        
        if data.get('dry_run'):
            cmd.append('--dry-run')
        
        if data.get('verbose'):
            cmd.append('--verbose')
        
        # Add custom settings if provided
        custom_settings = data.get('custom_settings', {})
        for key, value in custom_settings.items():
            if value is not None and value != '':
                # Convert camelCase to kebab-case
                arg_name = key.replace('_', '-')
                cmd.extend([f'--{arg_name}', str(value)])
        
        logger.info(f"Executing command: {' '.join(cmd)}")
        
        # Execute command
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        # Read output in real-time
        output_lines = []
        error_lines = []
        
        # Read stdout
        for line in process.stdout:
            output_lines.append(line.strip())
            logger.info(f"STDOUT: {line.strip()}")
        
        # Read stderr
        for line in process.stderr:
            error_lines.append(line.strip())
            logger.warning(f"STDERR: {line.strip()}")
        
        # Wait for process to complete
        return_code = process.wait()
        
        return jsonify({
            'success': return_code == 0,
            'return_code': return_code,
            'output': '\n'.join(output_lines),
            'errors': '\n'.join(error_lines),
            'command': ' '.join(cmd)
        })
        
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate', methods=['POST'])
def validate_paths():
    """Validate input and output paths."""
    try:
        data = request.json
        base_input = data.get('base_input', '')
        base_output = data.get('base_output', '')
        
        results = {
            'base_input': {
                'exists': os.path.exists(base_input) if base_input else False,
                'is_dir': os.path.isdir(base_input) if base_input and os.path.exists(base_input) else False
            },
            'base_output': {
                'exists': os.path.exists(base_output) if base_output else False,
                'is_dir': os.path.isdir(base_output) if base_output and os.path.exists(base_output) else False,
                'can_create': True  # We can always try to create
            }
        }
        
        # Check if input folder has subfolders
        if results['base_input']['is_dir']:
            try:
                subfolders = [f for f in os.listdir(base_input) if os.path.isdir(os.path.join(base_input, f))]
                results['base_input']['subfolders'] = subfolders
                results['base_input']['subfolder_count'] = len(subfolders)
            except Exception as e:
                results['base_input']['error'] = str(e)
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Error validating paths: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/browse', methods=['POST'])
def browse_directory():
    """Browse directory and return folders."""
    try:
        data = request.json
        folder_path = data.get('folder_path', '')
        
        # If no path provided, start from current directory
        if not folder_path:
            folder_path = os.getcwd()
        
        # Normalize the path
        folder_path = os.path.normpath(folder_path)
        
        # Check if path exists and is a directory
        if not os.path.exists(folder_path):
            return jsonify({'error': 'Path does not exist'}), 400
        
        if not os.path.isdir(folder_path):
            return jsonify({'error': 'Path is not a directory'}), 400
        
        # Get all items in directory
        try:
            items = os.listdir(folder_path)
            folders = []
            files = []
            
            for item in items:
                item_path = os.path.join(folder_path, item)
                try:
                    if os.path.isdir(item_path):
                        folders.append(item)
                    else:
                        files.append(item)
                except (PermissionError, OSError):
                    continue
            
            folders.sort()
            files.sort()
            
            # Get parent directory
            parent_dir = os.path.dirname(folder_path) if folder_path != os.path.dirname(folder_path) else None
            
            # Get folder name
            folder_name = os.path.basename(folder_path) if folder_path != os.path.dirname(folder_path) else folder_path
            
            return jsonify({
                'folder_name': folder_name,
                'full_path': folder_path,
                'parent_dir': parent_dir,
                'folders': folders,
                'files': files[:10],  # Limit files for performance
                'folder_count': len(folders),
                'file_count': len(files)
            })
            
        except PermissionError as e:
            return jsonify({'error': f'Permission denied: {str(e)}'}), 403
        except Exception as e:
            logger.error(f"Error listing directory: {e}")
            return jsonify({'error': str(e)}), 500
        
    except Exception as e:
        logger.error(f"Error browsing directory: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-folder-name', methods=['POST'])
def get_folder_name():
    """Get folder name from full path."""
    try:
        data = request.json
        folder_path = data.get('folder_path', '')
        
        if not folder_path:
            return jsonify({'error': 'No folder path provided'}), 400
        
        # Normalize the path
        folder_path = os.path.normpath(folder_path)
        
        # Check if path exists and is a directory
        if not os.path.exists(folder_path):
            return jsonify({'error': 'Path does not exist'}), 400
        
        if not os.path.isdir(folder_path):
            return jsonify({'error': 'Path is not a directory'}), 400
        
        # Get just the folder name (last part of path)
        folder_name = os.path.basename(folder_path)
        
        return jsonify({
            'folder_name': folder_name,
            'full_path': folder_path
        })
        
    except Exception as e:
        logger.error(f"Error getting folder name: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = 5000
    lan_ip = get_lan_ip()
    
    print("=" * 60)
    print("K1 Watermark Frontend Server - Production Mode")
    print("=" * 60)
    print(f"\nServer starting on:")
    print(f"  Local:   http://localhost:{port}")
    if lan_ip != '127.0.0.1':
        print(f"  Network: http://{lan_ip}:{port}")
    else:
        print(f"  Network: Unable to detect LAN IP (using localhost)")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    # Serve using Waitress production server
    # host='0.0.0.0' makes it accessible on all network interfaces
    serve(app, host='0.0.0.0', port=port, threads=4)

