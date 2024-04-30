import os

def filter_file_lines(file_path):
    # Numbers to check the beginning of each line against
    #numbers_to_remove = {'0', '1', '2', '3', '9', '10', '11', '12', '13', '14'}
    numbers_to_remove = {
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '10', '11', '12', '13', 
        '14', '15', '17', '19', '20', '21', '22', '23', '24', '25', '26', '27', 
        '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', 
        '40', '41', '42', '43', '45', '46', '47', '48', '50', '51', '52', '53', 
        '54', '55', '56', '57', '58', '59', '60', '61', '62', '64', '65', '66', 
        '67', '68', '69', '70', '71', '73', '75', '76', '77', '78', '79'
    }
    
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Filter lines
    filtered_lines = [line for line in lines if not line.split()[0] in numbers_to_remove]

    # Write the filtered lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(filtered_lines)

def process_folder(folder_path):
    # Iterate through all the files in the folder
    for file_name in os.listdir(folder_path):
        # Construct full file path
        file_path = os.path.join(folder_path, file_name)
        
        # Check if it is a file and has a .txt extension
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            filter_file_lines(file_path)
            print(f"Processed {file_name}")

# Replace 'your_folder_path' with the path to your folder
process_folder('./test/labels/')
process_folder('./train/labels/')
process_folder('./valid/labels/')