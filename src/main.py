import shutil
import os
from sys import exit

def main():
    """
    Entry point for the static site generator.

    Determines the paths for the script directory, static directory,
    and public directory, then calls generate_site().
    """
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Should always return the location of this main.py file
    parent_dir = os.path.dirname(script_dir) # Go up one level
    static_dir = os.path.join(parent_dir, "static") # Add static to parent dir
    public_dir = os.path.join(parent_dir, "public") # Add public to parent dir
    generate_site(static_dir, public_dir)

def generate_site(static_dir, public_dir):
    """
    Orchestrates site generation.

    Args:
        static_dir (str): Path to the static assets directory.
        public_dir (str): Path to the public output directory.
    """
    clean_public_directory(public_dir)
    check_static_directory(static_dir)
    copy_to_public(static_dir, public_dir)
    
def clean_public_directory(public_dir):
    """
    Deletes the public directory (if it exists) and recreates it.

    Args:
        public_dir (str): Path to the public directory.
    """
    try:
        shutil.rmtree(public_dir, ignore_errors=True)
        print(f"Public directory successfully deleted (or did not exist): {public_dir}")
        create_directory(public_dir)
    except Exception as e:
        print(f"Error deleting public directory: {e}")

def create_directory(path):
    """
    Creates a directory at the given path.

    Args:
        path (str): Path where the directory will be created.
    """
    try:
        os.mkdir(path)
        print(f"Directory successfully created: {path}")
    except Exception as e:
        print(f"Error creating directory {path}: {e}")

def check_static_directory(static_dir):
    """
    Ensures the static directory exists. If not, prompts the user to create it.

    Args:
        static_dir (str): Path to the static directory.
    """
    if not os.path.exists(static_dir):
        print(f'\nStatic path "{static_dir}" does not exist. Would you like to create it? [Y/N]\n')
        user_response = input().strip().lower()
        if user_response == "y":
            create_directory(static_dir)
        elif user_response == "n":
            raise SystemExit(f"Exiting script. Please create a static directory at {static_dir}")
        else:
            raise SystemExit(f"Invalid response: {user_response}")

def copy_to_public(from_dir, to_dir):
    """
    Recursively copies files and directories from the static directory to the public directory.

    Args:
        from_dir (str): Source directory (static).
        to_dir (str): Destination directory (public).
    """
    dir_list = os.listdir(from_dir)
    for item in dir_list:
        path_to_item = os.path.join(from_dir, item)
        if os.path.isdir(path_to_item):
            new_to_dir = os.path.join(to_dir, item)
            create_directory(new_to_dir)
            copy_to_public(path_to_item, new_to_dir)
        elif os.path.isfile(path_to_item):
            try:
                shutil.copy(path_to_item, to_dir)
                print(f"Successfully copied {path_to_item} to {os.path.join(to_dir, item)}")
            except Exception as e:
                print(f"Error copying file {path_to_item} : {e}")
        else:
            raise Exception(f"{os.path.join(from_dir, item)} is neither a file nor a directory, or it does not exist.")


if __name__ == "__main__":
    main()