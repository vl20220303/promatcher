import json
import os

colors = [33, 35, 36, 32, 37, 31]

def get_files(directory_path):
    try:
        all_entries = os.listdir(directory_path)
        files = [entry for entry in all_entries if os.path.isfile(os.path.join(directory_path, entry))]
        return files
    except Exception as e:
        print(f"An error occured: {e}")
        return []
    
def recursive_access(data, depth):
    col = colors[depth]
    nxt = colors[depth+1]
    prv = colors[depth-1]

    for datum in data:
        print(f'\n\n\033[{col}m{datum}\033[37m')
        inp = input(f"""Enter for next \033[{col}mchunk\033[37m\nj to \033[{nxt}mdive\033[37m\nk to \033[{prv}mascend\033[37m""").strip()
        inp = inp[0] if len(inp) > 0 else ''
        if inp == 'j':
            recursive_access(data[datum], depth+1)
            print(f'\n\n\033[{col}m{datum}\033[37m')
            input(f"Enter for next \033[{col}mchunk\033[37m")
        elif inp == 'k':
            return

    print("\nEnd of data.")
    input(f"Enter to \033[{prv}mascend\033[37m")
    
def main():
    directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "synthea\\processed-data")

    files = get_files(directory_path)

    if not files:
        return
    
    col = colors[0]
    nxt = colors[1]
    
    for file in files:
        try:
            with open(os.path.join(directory_path, file), 'r') as file:
                print(f'\n\n\033[{col}m{file.name}\033[37m')
                data = json.load(file)
                inp = input(f"""Enter for next \033[{col}mchunk\033[37m\nj to \033[{nxt}mdive\033[37m""").strip()
                inp = inp[0] if len(inp) > 0 else ''
                if inp == 'j':
                    recursive_access(data, 1)
                    print(f'\n\n\033[{col}m{file.name}\033[37m')
                    input(f"Enter for next \033[{col}mfile\033[37m")
        except Exception as e:
            print(f"An error occured: {e}")
            
    print('End of dir.')

if __name__ == "__main__":
    main()