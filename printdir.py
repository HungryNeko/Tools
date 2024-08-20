import os

def generate_directory_tree(dir_path, ignore_suffix=[], ignore_numeric_suffix=False, level=0):
    tree_str = ""
    prefix = " " * 4 * level + "- "
    
    for item in sorted(os.listdir(dir_path)):
        item_path = os.path.join(dir_path, item)
        
        if os.path.isfile(item_path):
            # 忽略指定后缀的文件
            if any(item.endswith(suffix) for suffix in ignore_suffix):
                continue
            
            # 忽略纯数字后缀的文件
            if ignore_numeric_suffix and item.split('.')[-1].isdigit():
                continue
                
            tree_str += f"{prefix}{item}\n"
        elif os.path.isdir(item_path):
            tree_str += f"{prefix}{item}/\n"
            tree_str += generate_directory_tree(item_path, ignore_suffix, ignore_numeric_suffix, level + 1)
    
    return tree_str

if __name__ == "__main__":
    # 输入目录路径、忽略的文件后缀以及是否忽略纯数字后缀
    directory_path = input("dir: ")
    ignore_suffix_input = input("files to ignore (split with ','): ")
    ignore_numeric_suffix = input("Ignore files with numeric suffix? (yes/no): ").strip().lower() == 'yes'
    
    ignore_list = [suffix.strip() for suffix in ignore_suffix_input.split(',')]
    directory_tree = generate_directory_tree(directory_path, ignore_list, ignore_numeric_suffix)
    
    print(directory_tree)  # 打印目录结构