import os

def generate_documentation(directory, output_file):
    """
    Generates a combined documentation of folder structure and file content 
    within the 'src/' folder of the given directory, excluding unnecessary files.
    """
    # Use absolute paths to avoid confusion
    directory = os.path.abspath(directory)
    output_file = os.path.abspath(output_file)

    # Define the target folder (src/ directory)
    target_folder = os.path.join(directory, "src")

    # Validate the target folder exists
    if not os.path.exists(target_folder):
        print(f"Error: The folder '{target_folder}' does not exist.")
        return

    # Prevent the script from reading/writing its own output
    if output_file.startswith(directory):
        print(f"Error: The output file '{output_file}' is inside the directory '{directory}'.")
        return

    # List of files to exclude
    excluded_files = {".DS_Store"}
    excluded_extensions = {".log", ".png", ".ico", ".jpg", ".json"}

    output = []

    # Write folder structure
    def write_folder_structure(path, level=0):
        items = sorted(os.listdir(path))  # Ensure consistent order
        for item in items:
            item_path = os.path.join(path, item)
            indent = "│   " * level + "├── "
            if os.path.isdir(item_path):
                output.append(f"{indent}{item}/")
                write_folder_structure(item_path, level + 1)
            elif os.path.isfile(item_path):
                # Skip excluded files or extensions
                if item in excluded_files or any(item.endswith(ext) for ext in excluded_extensions):
                    continue
                output.append(f"{indent}{item}")

    # Write content of files
    def write_file_content(file_path):
        # Exclude files with specific extensions or names
        file_name = os.path.basename(file_path)
        if file_name in excluded_files or any(file_name.endswith(ext) for ext in excluded_extensions):
            return

        output.append(f"\n// File: {file_path}\n")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                output.append(content)
        except UnicodeDecodeError:
            output.append("// [Binary or non-text file skipped]\n")
        except Exception as e:
            output.append(f"// [Error reading file: {e}]\n")

    # Start generating folder structure and file content
    output.append(f"{os.path.basename(target_folder)}/")
    write_folder_structure(target_folder)
    output.append("\n\n// Content\n")

    for root, _, files in os.walk(target_folder):
        for file in sorted(files):
            file_path = os.path.join(root, file)
            write_file_content(file_path)

    # Write everything to the output file
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write("\n".join(output))

    print(f"Documentation successfully written to '{output_file}'.")

# Example usage
codebase_directory = "./frontend"  # Replace with your folder name
output_txt_file = "shelfie_fe_documentation.txt"

generate_documentation(codebase_directory, output_txt_file)