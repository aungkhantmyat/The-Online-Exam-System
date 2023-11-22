import os
import json
import shutil

#Database and Files Related
# function to add data to JSON
def write_json(new_data, filename='violation.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

#Function to move the files to the Output Folders
def move_file_to_output_folder(file_name,folder_name='OutputVideos'):
    # Get the current working directory (project folder)
    current_directory = os.getcwd()
    # Define the paths for the source file and destination folder
    source_path = os.path.join(current_directory, file_name)
    destination_path = os.path.join(current_directory, 'static', folder_name, file_name)
    try:
        # Use 'shutil.move' to move the file to the destination folder
        shutil.move(source_path, destination_path)
        print('Your video is moved to'+folder_name)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found in the project folder.")
    except shutil.Error as e:
        print(f"Error: Failed to move the file. {e}")

#Query Related
#Function to give the next resut id
def get_resultId():
    with open('result.json','r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        #sort json by ID
        file_data.sort(key=lambda x: x["Id"])
        return file_data[-1]['Id']+1

#Function to give the trust score
def get_TrustScore(Rid):
    with open('violation.json', 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        filtered_data = [item for item in file_data if item["RId"] == Rid]
        total_mark = sum(item["Mark"] for item in filtered_data)
        return total_mark

#Function to give all results
def getResults():
    with open('result.json', 'r+') as file:
        # First we load existing data into a dict.
        result_data = json.load(file)
        return result_data

#Function to give result details
def getResultDetails(rid):
    with open('result.json', 'r+') as file:
        # First we load existing data into a dict.
        result_data = json.load(file)
        filtered_result = [item for item in result_data if item["Id"] == int(rid)]
    with open('violation.json', 'r+') as file:
        # First we load existing data into a dict.
        violation_data = json.load(file)
        filtered_violations = [item for item in violation_data if item["RId"] == int(rid)]
    resultDetails = {
            "Result": filtered_result,
            "Violation": filtered_violations
        }
    return resultDetails
