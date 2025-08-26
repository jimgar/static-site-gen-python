import os
import shutil

def copy_content(source_path, dest_path):
    if os.path.exists(dest_path):
        if os.path.isfile(dest_path):
            print(f"Removing file dest_path: {dest_path}")
            os.remove(dest_path)
        elif os.path.isdir(dest_path):
            print(f"Removing directory dest_path: {dest_path}")
            shutil.rmtree(dest_path)

    if os.path.exists(source_path):
        if os.path.isdir(source_path):
            print(f"Making directory dest_path: {dest_path}")
            os.mkdir(dest_path)
    else:
        raise Exception(f"Got '{source_path}' as source_path but it doesn't exist.")

    items: list = os.listdir(source_path)
    if len(items) == 0:
        print(f"No more items found for source_path: {source_path}")
        return

    print(f"source_path: {source_path} contains the following items: {items}")

    for item in items:
        print(f"Processing item: {item}")
        item_source_path = os.path.join(source_path, item)
        item_dest_path = os.path.join(dest_path, item)
        if os.path.isfile(item_source_path):
            print(f"Copying {item_source_path} to {item_dest_path}")
            shutil.copy(item_source_path, item_dest_path)
        if os.path.isdir(item_source_path):
            print(f"{item_source_path} is a path, recursing...")
            copy_content(item_source_path, item_dest_path)

