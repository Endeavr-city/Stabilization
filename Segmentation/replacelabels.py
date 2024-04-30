import os

def replace_line_numbers(file_path):
    # Mapping of original numbers to new numbers
    number_mapping = {
        '9': '8', '16': '0', '18': '1', '44': '9', '49': '3', '63': '12', '72': '10', '73': '13', '74': '5',
    }
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        # Split the line into words to examine the first word (number)
        words = line.split()
        if words:  # Check if line is not empty
            first_word = words[0]
            # Replace the number if it's in our mapping
            if first_word in number_mapping:
                new_first_word = number_mapping[first_word]
                new_line = line.replace(first_word, new_first_word, 1)
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Write the modified lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(new_lines)

def process_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            replace_line_numbers(file_path)
            print(f"Processed {file_name}")

# Replace 'your_folder_path' with the path to your folder
process_folder('./test/labels/')
process_folder('./train/labels/')
process_folder('./valid/labels/')