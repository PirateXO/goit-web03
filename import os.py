import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

def copy_file_to_target(file_path, target_directory):
    file_extension = os.path.splitext(file_path)[1][1:]  # Отримуємо розширення без крапки
    if file_extension:  # Якщо розширення є
        target_folder = os.path.join(target_directory, file_extension)
        os.makedirs(target_folder, exist_ok=True)  # Створюємо папку, якщо її не існує
        shutil.copy2(file_path, target_folder)  # Копіюємо файл до цільової папки

def process_directory(source_directory, target_directory):
    with ThreadPoolExecutor() as executor:
        futures = []
        for root, dirs, files in os.walk(source_directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                futures.append(executor.submit(copy_file_to_target, file_path, target_directory))

        for future in as_completed(futures):
            future.result()  # Виконання кожного завдання

def main(source_directory, target_directory="dist"):
    if not os.path.exists(source_directory):
        print(f"Source directory '{source_directory}' does not exist.")
        return

    os.makedirs(target_directory, exist_ok=True)  # Створюємо цільову директорію, якщо її не існує

    process_directory(source_directory, target_directory)
    print(f"Files from '{source_directory}' have been copied to '{target_directory}' and sorted by extension.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <source_directory> [<target_directory>]")
    else:
        source_directory = sys.argv[1]
        target_directory = sys.argv[2] if len(sys.argv) > 2 else "dist"
        main(source_directory, target_directory)
