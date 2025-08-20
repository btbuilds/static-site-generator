import shutil
import os
import sys
from pathlib import Path
from markdown_to_html import markdown_to_html_node
from block_markdown import extract_title

def main():
    """
    Entry point for the static site generator.

    Determines the paths for the script directory, static directory,
    and public directory, then calls generate_site().
    """
    basepath = sys.argv[0]
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Should always return the location of this main.py file
    parent_dir = os.path.dirname(script_dir) # Go up one level
    static_dir = os.path.join(parent_dir, "static") # Add static to parent dir
    public_dir = os.path.join(parent_dir, "docs") # Add docs to parent dir
    content_dir = os.path.join(parent_dir, "content") # Add content to parent dir
    template_file = os.path.join(parent_dir, "template.html")
    generate_site(static_dir, public_dir, template_file, content_dir, basepath)

def generate_site(static_dir, public_dir, template_path, content_dir, basepath):
    """
    Orchestrates site generation.

    Args:
        static_dir (str): Path to the static assets directory.
        public_dir (str): Path to the public output directory.
    """
    clean_public_directory(public_dir)
    check_static_directory(static_dir)
    copy_to_public(static_dir, public_dir)
    content_files = get_content(content_dir)

    for md_path in content_files:
        rel_path = os.path.relpath(md_path, content_dir)  # blog/glorfindel/index.md
        html_path = os.path.join(public_dir, os.path.splitext(rel_path)[0] + ".html")

        generate_page(md_path, template_path, html_path, basepath)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as m:
        markdown_file = m.read()
    with open(template_path) as t:
        template_file = t.read()

    html_nodes = markdown_to_html_node(markdown_file).to_html()
    page_title = extract_title(markdown_file)

    generated_file = template_file.replace("{{ Title }}", page_title).replace("{{ Content }}", html_nodes)
    generated_file = generated_file.replace('href="/', f'href={basepath}').replace('src="/', f'src={basepath}')

    dest_dir = os.path.dirname(dest_path)

    os.makedirs(dest_dir, exist_ok=True)
    
    with open(dest_path, "w") as d:
        d.write(generated_file)

def get_content(content_dir):
    files = []
    for item in os.listdir(content_dir):
        path_to_item = os.path.join(content_dir, item)
        if os.path.isdir(path_to_item):
            files.extend(get_content(path_to_item))
        elif os.path.isfile(path_to_item):
            files.append(path_to_item)
    return files

def convert_paths(file_list, content_dir="content", public_dir="public"):
    new_paths = []
    for file in file_list:
        path = Path(file)
        # Replace root "content" with "public"
        relative = path.relative_to(content_dir)  # e.g. blog/glorfindel/index.md
        new_path = Path(public_dir, relative).with_suffix(".html")
        new_paths.append(str(new_path))
    return new_paths

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
            raise Exception(f"{path_to_item} is neither a file nor a directory, or it does not exist.")


if __name__ == "__main__":
    main()