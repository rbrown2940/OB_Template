import os
import csv
from datetime import datetime

def list_files_recursive(
    folder_path,
    output_txt="file_list.txt",
    output_csv="file_list.csv",
    absolute_paths=False,
    include_extensions=None  # e.g., [".pdf", ".docx"]
):
    folder_path = os.path.expanduser(os.path.normpath(folder_path))
    file_data = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if include_extensions and not any(file.lower().endswith(ext) for ext in include_extensions):
                continue

            file_path = os.path.join(root, file)

            try:
                size = os.path.getsize(file_path)
                mtime = os.path.getmtime(file_path)
                modified_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')

                display_path = os.path.abspath(file_path) if absolute_paths else os.path.relpath(file_path, folder_path)
                file_data.append((display_path, size, modified_time))

            except Exception as e:
                print(f"Error accessing {file_path}: {e}")

    # Write to .txt file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        for path, size, mtime in file_data:
            txt_file.write(f"{path} | {size} bytes | Modified: {mtime}\n")

    # Write to .csv file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["File Path", "Size (Bytes)", "Last Modified"])
        writer.writerows(file_data)

    print(f"\nSaved {len(file_data)} file entries to:\n- {output_txt}\n- {output_csv}")

# Example usage:
if __name__ == "__main__":
    folder = "~/Library/Mobile Documents/com~apple~CloudDocs/Birkbeck Bsc Psychology"
    list_files_recursive(
        folder_path=folder,
        absolute_paths=False,                     # change to True if you want full paths
        include_extensions=[".pdf", ".docx"]      # filter by file types (or set to None for all files)
    )

