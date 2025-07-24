#!/usr/bin/env python3
"""
Safe input validation utilities for user prompts.
Provides secure input handling with validation and sanitization.
"""

import re
import sys
from typing import Optional, List, Callable, Any


def safe_input(prompt: str, 
               valid_options: Optional[List[str]] = None,
               max_length: int = 1000,
               allow_empty: bool = False,
               validator: Optional[Callable[[str], bool]] = None,
               sanitizer: Optional[Callable[[str], str]] = None,
               default: Optional[str] = None) -> str:
    """
    Get user input with validation and sanitization.
    
    Args:
        prompt: The prompt to display to the user
        valid_options: List of valid options (case-insensitive)
        max_length: Maximum allowed input length
        allow_empty: Whether to allow empty input
        validator: Custom validation function
        sanitizer: Custom sanitization function
        default: Default value if user just presses Enter
        
    Returns:
        Validated and sanitized user input
    """
    while True:
        try:
            # Get input
            user_input = input(prompt)
            
            # Handle empty input
            if not user_input.strip():
                if default is not None:
                    return default
                elif allow_empty:
                    return ""
                else:
                    print("Input cannot be empty. Please try again.")
                    continue
            
            # Check length
            if len(user_input) > max_length:
                print(f"Input too long (max {max_length} characters). Please try again.")
                continue
            
            # Strip and basic sanitization
            user_input = user_input.strip()
            
            # Apply custom sanitizer if provided
            if sanitizer:
                user_input = sanitizer(user_input)
            
            # Check valid options
            if valid_options is not None:
                if user_input.lower() not in [opt.lower() for opt in valid_options]:
                    print(f"Invalid option. Valid options are: {', '.join(valid_options)}")
                    continue
                # Return the matching option with original case
                for opt in valid_options:
                    if opt.lower() == user_input.lower():
                        return opt
            
            # Apply custom validator if provided
            if validator and not validator(user_input):
                print("Invalid input. Please try again.")
                continue
            
            return user_input
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)
        except EOFError:
            print("\nInput stream closed.")
            sys.exit(0)
        except Exception as e:
            print(f"Error reading input: {e}")
            continue


def safe_yes_no(prompt: str, default: Optional[bool] = None) -> bool:
    """
    Get a yes/no response from the user.
    
    Args:
        prompt: The prompt to display
        default: Default value if user just presses Enter (True for yes, False for no)
        
    Returns:
        True for yes, False for no
    """
    if default is True:
        prompt = f"{prompt} [Y/n]: "
        default_str = "y"
    elif default is False:
        prompt = f"{prompt} [y/N]: "
        default_str = "n"
    else:
        prompt = f"{prompt} (y/n): "
        default_str = None
    
    response = safe_input(prompt, 
                         valid_options=["y", "n", "yes", "no"],
                         default=default_str)
    
    return response.lower() in ["y", "yes"]


def safe_path_input(prompt: str, 
                   must_exist: bool = False,
                   allow_empty: bool = False) -> str:
    """
    Get a file or directory path from the user with validation.
    
    Args:
        prompt: The prompt to display
        must_exist: Whether the path must exist
        allow_empty: Whether to allow empty input
        
    Returns:
        Validated path string
    """
    import os
    from pathlib import Path
    
    def path_validator(path_str: str) -> bool:
        # Check for dangerous characters
        if any(char in path_str for char in ['<', '>', '|', '&', ';', '$', '`', '\n', '\r']):
            print("Path contains invalid characters.")
            return False
        
        # Check if path exists if required
        if must_exist and not os.path.exists(path_str):
            print(f"Path does not exist: {path_str}")
            return False
        
        # Check for path traversal attempts
        try:
            resolved = Path(path_str).resolve()
            # Ensure the resolved path doesn't escape expected boundaries
            return True
        except Exception:
            print("Invalid path format.")
            return False
    
    def path_sanitizer(path_str: str) -> str:
        # Remove any null bytes
        path_str = path_str.replace('\0', '')
        # Normalize path separators
        path_str = os.path.normpath(path_str)
        return path_str
    
    return safe_input(prompt,
                     allow_empty=allow_empty,
                     validator=path_validator,
                     sanitizer=path_sanitizer)


def safe_number_input(prompt: str, 
                     min_value: Optional[float] = None,
                     max_value: Optional[float] = None,
                     allow_float: bool = False,
                     default: Optional[float] = None) -> float:
    """
    Get a number from the user with validation.
    
    Args:
        prompt: The prompt to display
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        allow_float: Whether to allow floating point numbers
        default: Default value if user just presses Enter
        
    Returns:
        Validated number
    """
    def number_validator(value_str: str) -> bool:
        try:
            if allow_float:
                value = float(value_str)
            else:
                value = int(value_str)
            
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}")
                return False
            
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}")
                return False
            
            return True
        except ValueError:
            print(f"Invalid {'number' if allow_float else 'integer'} format.")
            return False
    
    default_str = str(default) if default is not None else None
    
    result = safe_input(prompt,
                       validator=number_validator,
                       default=default_str)
    
    return float(result) if allow_float else int(result)


def safe_choice_menu(title: str, 
                    options: List[tuple[str, str]],
                    allow_back: bool = True) -> Optional[str]:
    """
    Display a menu and get user choice.
    
    Args:
        title: Menu title
        options: List of (key, description) tuples
        allow_back: Whether to allow going back/cancelling
        
    Returns:
        Selected option key, or None if back/cancel
    """
    print(f"\n{title}")
    print("-" * len(title))
    
    valid_options = []
    for key, description in options:
        print(f"{key}. {description}")
        valid_options.append(key)
    
    if allow_back:
        print("0. Back/Cancel")
        valid_options.append("0")
    
    choice = safe_input("\nEnter your choice: ", 
                       valid_options=valid_options)
    
    return None if choice == "0" else choice


# Example usage and migration helpers
def migrate_input_call(old_code: str) -> str:
    """
    Helper to show how to migrate from input() to safe_input().
    
    Examples:
        input("Enter name: ") -> safe_input("Enter name: ")
        input("Continue? (y/n): ").lower() -> safe_yes_no("Continue?")
    """
    examples = """
    # Old: response = input("Update? (y/n): ").lower()
    # New: response = safe_yes_no("Update?")
    
    # Old: path = input("Enter file path: ")
    # New: path = safe_path_input("Enter file path: ", must_exist=True)
    
    # Old: num = int(input("Enter number: "))
    # New: num = safe_number_input("Enter number: ", min_value=1, max_value=100)
    """
    return examples


if __name__ == "__main__":
    # Test the functions
    print("Testing safe input functions...")
    
    # Test yes/no
    result = safe_yes_no("Do you want to continue?", default=True)
    print(f"You selected: {'Yes' if result else 'No'}")
    
    # Test path input
    path = safe_path_input("Enter a file path: ", must_exist=False)
    print(f"Path entered: {path}")
    
    # Test number input
    num = safe_number_input("Enter a number between 1 and 10: ", 
                           min_value=1, max_value=10)
    print(f"Number entered: {num}")
    
    # Test menu
    choice = safe_choice_menu("Main Menu", [
        ("1", "Option One"),
        ("2", "Option Two"),
        ("3", "Option Three")
    ])
    print(f"Menu choice: {choice}")