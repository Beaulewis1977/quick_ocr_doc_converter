#!/usr/bin/env python3
"""
API Key Manager for Universal Document Converter
Secure management of API keys with encryption, validation, and .env file support
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import secrets
from dotenv import load_dotenv, set_key, unset_key
import keyring

class APIKeyManager:
    """Secure API key management with encryption and storage"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".universal_converter"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.api_config_file = self.config_dir / "api_keys.json"
        self.env_file = Path(".env")
        self.logger = logging.getLogger(__name__)
        
        # Load .env file
        load_dotenv(self.env_file)
        
        # Initialize encryption
        self.cipher_suite = self._get_cipher_suite()
        
        # Available API services
        self.supported_apis = {
            'google_vision': {
                'name': 'Google Vision API',
                'required_fields': ['api_key', 'credentials_path'],
                'optional_fields': ['project_id'],
                'test_endpoint': 'https://vision.googleapis.com/v1/images:annotate'
            },
            'cloudconvert': {
                'name': 'CloudConvert API',
                'required_fields': ['api_key'],
                'optional_fields': ['sandbox_mode', 'webhook_url'],
                'test_endpoint': 'https://api.cloudconvert.com/v2/users/me'
            },
            'openai': {
                'name': 'OpenAI API',
                'required_fields': ['api_key'],
                'optional_fields': ['organization_id', 'model'],
                'test_endpoint': 'https://api.openai.com/v1/models'
            },
            'azure': {
                'name': 'Azure Cognitive Services',
                'required_fields': ['api_key', 'endpoint'],
                'optional_fields': ['region'],
                'test_endpoint': None  # Varies by service
            },
            'aws_textract': {
                'name': 'AWS Textract',
                'required_fields': ['access_key_id', 'secret_access_key'],
                'optional_fields': ['region', 'session_token'],
                'test_endpoint': None  # Uses AWS SDK
            }
        }
        
        # Load existing configuration
        self.api_keys = self._load_api_keys()
    
    def _get_cipher_suite(self) -> Fernet:
        """Get or create encryption cipher"""
        # Try to get encryption key from keyring first
        try:
            encryption_key = keyring.get_password("universal_converter", "api_encryption_key")
            if not encryption_key:
                # Generate new key
                encryption_key = Fernet.generate_key().decode()
                keyring.set_password("universal_converter", "api_encryption_key", encryption_key)
        except Exception:
            # Fallback to file-based storage
            key_file = self.config_dir / ".encryption_key"
            if key_file.exists():
                encryption_key = key_file.read_text().strip()
            else:
                encryption_key = Fernet.generate_key().decode()
                key_file.write_text(encryption_key)
                key_file.chmod(0o600)  # Restrict access
        
        return Fernet(encryption_key.encode())
    
    def _encrypt_value(self, value: str) -> str:
        """Encrypt a value"""
        if not value:
            return ""
        return self.cipher_suite.encrypt(value.encode()).decode()
    
    def _decrypt_value(self, encrypted_value: str) -> str:
        """Decrypt a value"""
        if not encrypted_value:
            return ""
        try:
            return self.cipher_suite.decrypt(encrypted_value.encode()).decode()
        except Exception:
            self.logger.warning("Failed to decrypt value, returning empty string")
            return ""
    
    def _load_api_keys(self) -> Dict[str, Dict[str, Any]]:
        """Load API keys from storage"""
        api_keys = {}
        
        # Load from JSON file
        if self.api_config_file.exists():
            try:
                with open(self.api_config_file, 'r') as f:
                    stored_keys = json.load(f)
                    
                # Decrypt sensitive values
                for api_name, config in stored_keys.items():
                    api_keys[api_name] = config.copy()
                    if 'encrypted_fields' in config:
                        for field in config['encrypted_fields']:
                            if field in config:
                                api_keys[api_name][field] = self._decrypt_value(config[field])
            except Exception as e:
                self.logger.error(f"Failed to load API keys: {e}")
        
        # Also check .env file for keys
        self._load_from_env(api_keys)
        
        return api_keys
    
    def _load_from_env(self, api_keys: Dict[str, Dict[str, Any]]):
        """Load API keys from .env file"""
        # Google Vision
        if os.getenv('GOOGLE_VISION_API_KEY'):
            if 'google_vision' not in api_keys:
                api_keys['google_vision'] = {}
            api_keys['google_vision'].update({
                'enabled': os.getenv('GOOGLE_VISION_ENABLED', 'false').lower() == 'true',
                'api_key': os.getenv('GOOGLE_VISION_API_KEY'),
                'credentials_path': os.getenv('GOOGLE_VISION_CREDENTIALS_PATH', '')
            })
        
        # CloudConvert
        if os.getenv('CLOUDCONVERT_API_KEY'):
            if 'cloudconvert' not in api_keys:
                api_keys['cloudconvert'] = {}
            api_keys['cloudconvert'].update({
                'enabled': os.getenv('CLOUDCONVERT_ENABLED', 'false').lower() == 'true',
                'api_key': os.getenv('CLOUDCONVERT_API_KEY'),
                'sandbox_mode': os.getenv('CLOUDCONVERT_SANDBOX_MODE', 'true').lower() == 'true'
            })
    
    def _save_api_keys(self):
        """Save API keys to storage"""
        # Prepare data for storage
        stored_keys = {}
        
        for api_name, config in self.api_keys.items():
            stored_config = config.copy()
            encrypted_fields = []
            
            # Encrypt sensitive fields
            sensitive_fields = ['api_key', 'secret_access_key', 'credentials']
            for field in sensitive_fields:
                if field in config:
                    stored_config[field] = self._encrypt_value(config[field])
                    encrypted_fields.append(field)
            
            stored_config['encrypted_fields'] = encrypted_fields
            stored_keys[api_name] = stored_config
        
        # Save to JSON file
        with open(self.api_config_file, 'w') as f:
            json.dump(stored_keys, f, indent=2)
        
        # Restrict file permissions
        self.api_config_file.chmod(0o600)
        
        # Update .env file for commonly used keys
        self._update_env_file()
    
    def _update_env_file(self):
        """Update .env file with current API keys"""
        if not self.env_file.exists():
            self.env_file.touch()
        
        # Google Vision
        if 'google_vision' in self.api_keys:
            config = self.api_keys['google_vision']
            set_key(self.env_file, 'GOOGLE_VISION_ENABLED', str(config.get('enabled', False)))
            if config.get('api_key'):
                set_key(self.env_file, 'GOOGLE_VISION_API_KEY', config['api_key'])
            if config.get('credentials_path'):
                set_key(self.env_file, 'GOOGLE_VISION_CREDENTIALS_PATH', config['credentials_path'])
        
        # CloudConvert
        if 'cloudconvert' in self.api_keys:
            config = self.api_keys['cloudconvert']
            set_key(self.env_file, 'CLOUDCONVERT_ENABLED', str(config.get('enabled', False)))
            if config.get('api_key'):
                set_key(self.env_file, 'CLOUDCONVERT_API_KEY', config['api_key'])
            set_key(self.env_file, 'CLOUDCONVERT_SANDBOX_MODE', str(config.get('sandbox_mode', True)))
    
    def add_api_key(self, api_name: str, config: Dict[str, Any]) -> bool:
        """Add or update an API key configuration"""
        if api_name not in self.supported_apis:
            self.logger.error(f"Unsupported API: {api_name}")
            return False
        
        # Validate required fields
        api_info = self.supported_apis[api_name]
        for field in api_info['required_fields']:
            if field not in config:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        # Store configuration
        self.api_keys[api_name] = config
        self._save_api_keys()
        
        self.logger.info(f"Successfully added/updated API key for {api_name}")
        return True
    
    def remove_api_key(self, api_name: str) -> bool:
        """Remove an API key configuration"""
        if api_name in self.api_keys:
            del self.api_keys[api_name]
            self._save_api_keys()
            
            # Remove from .env file
            unset_key(self.env_file, f'{api_name.upper()}_API_KEY')
            unset_key(self.env_file, f'{api_name.upper()}_ENABLED')
            
            self.logger.info(f"Successfully removed API key for {api_name}")
            return True
        return False
    
    def get_api_key(self, api_name: str) -> Optional[Dict[str, Any]]:
        """Get API key configuration"""
        return self.api_keys.get(api_name)
    
    def is_api_enabled(self, api_name: str) -> bool:
        """Check if an API is enabled"""
        config = self.get_api_key(api_name)
        return config.get('enabled', False) if config else False
    
    def list_configured_apis(self) -> List[Dict[str, Any]]:
        """List all configured APIs"""
        configured = []
        
        for api_name, config in self.api_keys.items():
            api_info = self.supported_apis.get(api_name, {})
            configured.append({
                'id': api_name,
                'name': api_info.get('name', api_name),
                'enabled': config.get('enabled', False),
                'configured': True,
                'has_key': bool(config.get('api_key') or config.get('access_key_id'))
            })
        
        # Add unconfigured APIs
        for api_name, api_info in self.supported_apis.items():
            if api_name not in self.api_keys:
                configured.append({
                    'id': api_name,
                    'name': api_info['name'],
                    'enabled': False,
                    'configured': False,
                    'has_key': False
                })
        
        return configured
    
    def test_api_key(self, api_name: str) -> Dict[str, Any]:
        """Test if an API key is valid"""
        config = self.get_api_key(api_name)
        if not config:
            return {'success': False, 'error': 'API not configured'}
        
        # Implement specific test logic for each API
        if api_name == 'google_vision':
            return self._test_google_vision(config)
        elif api_name == 'cloudconvert':
            return self._test_cloudconvert(config)
        elif api_name == 'openai':
            return self._test_openai(config)
        
        return {'success': False, 'error': 'Test not implemented for this API'}
    
    def _test_google_vision(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test Google Vision API key"""
        try:
            from google.cloud import vision
            
            # Set credentials
            if config.get('credentials_path'):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['credentials_path']
            
            client = vision.ImageAnnotatorClient()
            
            # Try a simple request
            image = vision.Image()
            image.source.image_uri = 'gs://cloud-samples-data/vision/face_no_surprise.jpg'
            
            response = client.face_detection(image=image)
            
            return {'success': True, 'message': 'Google Vision API is working'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _test_cloudconvert(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test CloudConvert API key"""
        try:
            import requests
            
            headers = {
                'Authorization': f'Bearer {config["api_key"]}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get('https://api.cloudconvert.com/v2/users/me', headers=headers, verify=True)
            
            if response.status_code == 200:
                user_data = response.json()
                return {
                    'success': True, 
                    'message': f'CloudConvert API is working. Credits: {user_data.get("credits", "N/A")}'
                }
            else:
                return {'success': False, 'error': f'API returned status {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _test_openai(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test OpenAI API key"""
        try:
            import openai
            
            openai.api_key = config['api_key']
            if config.get('organization_id'):
                openai.organization = config['organization_id']
            
            # List models to test the key
            models = openai.Model.list()
            
            return {'success': True, 'message': f'OpenAI API is working. Found {len(models.data)} models'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def toggle_api(self, api_name: str, enabled: bool) -> bool:
        """Enable or disable an API"""
        if api_name in self.api_keys:
            self.api_keys[api_name]['enabled'] = enabled
            self._save_api_keys()
            return True
        return False
    
    def get_api_stats(self) -> Dict[str, Any]:
        """Get API usage statistics"""
        stats = {
            'total_configured': len(self.api_keys),
            'enabled_count': sum(1 for config in self.api_keys.values() if config.get('enabled', False)),
            'apis': {}
        }
        
        for api_name, config in self.api_keys.items():
            stats['apis'][api_name] = {
                'enabled': config.get('enabled', False),
                'usage_count': config.get('usage_count', 0),
                'last_used': config.get('last_used', 'Never'),
                'errors': config.get('error_count', 0)
            }
        
        return stats


class APIKeyGUI:
    """GUI for API key management"""
    
    def __init__(self, parent, api_manager: APIKeyManager):
        self.parent = parent
        self.api_manager = api_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the API key management UI"""
        import tkinter as tk
        from tkinter import ttk, messagebox
        
        # Main frame
        main_frame = ttk.Frame(self.parent, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="API Key Management", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # API list frame
        list_frame = ttk.LabelFrame(main_frame, text="Configured APIs", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for API list
        columns = ('API', 'Status', 'Enabled', 'Key Status')
        self.api_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=8)
        
        # Configure columns
        self.api_tree.heading('#0', text='')
        self.api_tree.column('#0', width=50)
        
        for col in columns:
            self.api_tree.heading(col, text=col)
            self.api_tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.api_tree.yview)
        self.api_tree.configure(yscrollcommand=scrollbar.set)
        
        self.api_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="➕ Add API Key", 
                  command=self.add_api_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="✏️ Edit", 
                  command=self.edit_api_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="🗑️ Remove", 
                  command=self.remove_api_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="🔄 Toggle", 
                  command=self.toggle_api).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="🧪 Test", 
                  command=self.test_api).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(control_frame, text="🔄 Refresh", 
                  command=self.refresh_list).pack(side=tk.LEFT)
        
        # Instructions
        instructions = ttk.LabelFrame(main_frame, text="Instructions", padding=10)
        instructions.pack(fill=tk.X, pady=(10, 0))
        
        instructions_text = """1. Click 'Add API Key' to configure a new API service
2. Select an API and click 'Toggle' to enable/disable it
3. Use 'Test' to verify your API keys are working
4. API keys are encrypted and stored securely
5. Enable APIs to use them in document conversion and OCR"""
        
        ttk.Label(instructions, text=instructions_text, 
                 justify=tk.LEFT).pack()
        
        # Load initial data
        self.refresh_list()
    
    def refresh_list(self):
        """Refresh the API list"""
        # Clear existing items
        for item in self.api_tree.get_children():
            self.api_tree.delete(item)
        
        # Add APIs
        for api_info in self.api_manager.list_configured_apis():
            status = "✅ Configured" if api_info['configured'] else "❌ Not configured"
            enabled = "✅ Yes" if api_info['enabled'] else "❌ No"
            key_status = "🔑 Set" if api_info['has_key'] else "🔓 Missing"
            
            self.api_tree.insert('', 'end', 
                                values=(api_info['name'], status, enabled, key_status),
                                tags=(api_info['id'],))
    
    def add_api_key(self):
        """Show dialog to add new API key"""
        import tkinter as tk
        from tkinter import ttk, messagebox, filedialog
        
        # Create dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add API Key")
        dialog.geometry("500x400")
        
        # API selection
        ttk.Label(dialog, text="Select API Service:", font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        
        api_var = tk.StringVar()
        api_combo = ttk.Combobox(dialog, textvariable=api_var, state='readonly', width=40)
        api_combo['values'] = [info['name'] for info in self.api_manager.supported_apis.values()]
        api_combo.pack(pady=(0, 10))
        
        # Dynamic fields frame
        fields_frame = ttk.Frame(dialog)
        fields_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        field_entries = {}
        
        def on_api_selected(event=None):
            # Clear existing fields
            for widget in fields_frame.winfo_children():
                widget.destroy()
            field_entries.clear()
            
            # Get selected API
            api_name = None
            for key, info in self.api_manager.supported_apis.items():
                if info['name'] == api_var.get():
                    api_name = key
                    break
            
            if not api_name:
                return
            
            api_info = self.api_manager.supported_apis[api_name]
            
            # Create fields
            row = 0
            for field in api_info['required_fields']:
                ttk.Label(fields_frame, text=f"{field.replace('_', ' ').title()}:*").grid(
                    row=row, column=0, sticky=tk.W, pady=5)
                
                if field == 'credentials_path':
                    # File picker for credentials
                    entry_frame = ttk.Frame(fields_frame)
                    entry_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
                    
                    entry = ttk.Entry(entry_frame, width=30)
                    entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                    
                    def browse_file(e=entry):
                        filename = filedialog.askopenfilename(
                            title="Select credentials file",
                            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                        )
                        if filename:
                            e.delete(0, tk.END)
                            e.insert(0, filename)
                    
                    ttk.Button(entry_frame, text="Browse", command=browse_file).pack(side=tk.LEFT, padx=(5, 0))
                    field_entries[field] = entry
                else:
                    entry = ttk.Entry(fields_frame, width=40)
                    if 'key' in field or 'secret' in field:
                        entry.config(show='*')
                    entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
                    field_entries[field] = entry
                
                row += 1
            
            # Optional fields
            if api_info.get('optional_fields'):
                ttk.Label(fields_frame, text="Optional Fields:", 
                         font=('Arial', 9, 'italic')).grid(row=row, column=0, columnspan=2, pady=(10, 5))
                row += 1
                
                for field in api_info['optional_fields']:
                    ttk.Label(fields_frame, text=f"{field.replace('_', ' ').title()}:").grid(
                        row=row, column=0, sticky=tk.W, pady=5)
                    
                    if field == 'sandbox_mode':
                        var = tk.BooleanVar(value=True)
                        ttk.Checkbutton(fields_frame, variable=var).grid(row=row, column=1, sticky=tk.W, pady=5)
                        field_entries[field] = var
                    else:
                        entry = ttk.Entry(fields_frame, width=40)
                        entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
                        field_entries[field] = entry
                    
                    row += 1
            
            # Enable checkbox
            enabled_var = tk.BooleanVar(value=True)
            ttk.Checkbutton(fields_frame, text="Enable this API", 
                           variable=enabled_var).grid(row=row, column=0, columnspan=2, pady=10)
            field_entries['enabled'] = enabled_var
        
        api_combo.bind('<<ComboboxSelected>>', on_api_selected)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=10)
        
        def save_api_key():
            # Get selected API
            api_name = None
            for key, info in self.api_manager.supported_apis.items():
                if info['name'] == api_var.get():
                    api_name = key
                    break
            
            if not api_name:
                messagebox.showerror("Error", "Please select an API service")
                return
            
            # Collect field values
            config = {}
            for field, widget in field_entries.items():
                if isinstance(widget, tk.BooleanVar):
                    config[field] = widget.get()
                else:
                    value = widget.get().strip()
                    if value:
                        config[field] = value
            
            # Validate and save
            if self.api_manager.add_api_key(api_name, config):
                messagebox.showinfo("Success", "API key added successfully")
                dialog.destroy()
                self.refresh_list()
            else:
                messagebox.showerror("Error", "Failed to add API key. Check required fields.")
        
        ttk.Button(button_frame, text="Save", command=save_api_key).pack(side=tk.LEFT, padx=(100, 10))
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
    
    def edit_api_key(self):
        """Edit selected API key"""
        selection = self.api_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an API to edit")
            return
        
        # Get API ID from tags
        api_id = self.api_tree.item(selection[0])['tags'][0]
        
        # TODO: Implement edit dialog (similar to add but pre-filled)
        messagebox.showinfo("Edit API", f"Edit functionality for {api_id} coming soon!")
    
    def remove_api_key(self):
        """Remove selected API key"""
        selection = self.api_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an API to remove")
            return
        
        # Get API ID from tags
        api_id = self.api_tree.item(selection[0])['tags'][0]
        api_name = self.api_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirm Removal", f"Remove API key for {api_name}?"):
            if self.api_manager.remove_api_key(api_id):
                messagebox.showinfo("Success", "API key removed successfully")
                self.refresh_list()
    
    def toggle_api(self):
        """Toggle API enabled status"""
        selection = self.api_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an API to toggle")
            return
        
        # Get API ID from tags
        api_id = self.api_tree.item(selection[0])['tags'][0]
        config = self.api_manager.get_api_key(api_id)
        
        if not config:
            messagebox.showerror("Error", "API not configured. Please add the API key first.")
            return
        
        # Toggle enabled status
        new_status = not config.get('enabled', False)
        self.api_manager.toggle_api(api_id, new_status)
        
        status_text = "enabled" if new_status else "disabled"
        messagebox.showinfo("Success", f"API {status_text} successfully")
        self.refresh_list()
    
    def test_api(self):
        """Test selected API"""
        selection = self.api_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an API to test")
            return
        
        # Get API ID from tags
        api_id = self.api_tree.item(selection[0])['tags'][0]
        api_name = self.api_tree.item(selection[0])['values'][0]
        
        # Show testing dialog
        messagebox.showinfo("Testing", f"Testing {api_name}...")
        
        # Run test
        result = self.api_manager.test_api_key(api_id)
        
        if result['success']:
            messagebox.showinfo("Test Successful", f"✅ {result['message']}")
        else:
            messagebox.showerror("Test Failed", f"❌ {result['error']}")


if __name__ == "__main__":
    # Test the API key manager
    manager = APIKeyManager()
    
    # Example: Add a test API key
    manager.add_api_key('cloudconvert', {
        'api_key': 'test-key-123',
        'enabled': True,
        'sandbox_mode': True
    })
    
    # List configured APIs
    print("Configured APIs:")
    for api in manager.list_configured_apis():
        print(f"- {api['name']}: {'Enabled' if api['enabled'] else 'Disabled'}")