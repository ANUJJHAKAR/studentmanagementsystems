import pandas as pd
import json
import os
import argparse

def excel_to_json(excel_file_path):
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"The file {excel_file_path} does not exist.")
    
    try:
        df = pd.read_excel(excel_file_path, header=None)
        print("DataFrame loaded successfully:")
        print(df.head())
    except PermissionError:
        raise PermissionError(f"Permission denied for reading the file {excel_file_path}.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the Excel file: {e}")
    
    return df

def create_json_structure(df):
    structured_data = {
        "name": "",
        "regnum": "",
        "phone": "",
        "dob": "",
        "email": "",
        "address": "",
        "gender": "",
        "father_name": "",
        "father_mobile": "",
        "mother_name": "",
        "mother_mobile": "",
        "branch": "",
        "section": "",
        "semester": "",
        "cgpa": "",
        "totalCreditsEarned": "",
        "grades": {}
    }

    metadata_mapping = {
        "name": "Name",
        "regnum": "Registration Number",
        "phone": "Mobile Number",
        "dob": "Date of Birth",
        "email": "Email ID",
        "address": "Permanent Address Line 1",
        "gender": "Gender",
        "father_name": "Father Name",
        "father_mobile": "Father Mobile",
        "mother_name": "Mother Name",
        "mother_mobile": "Mother Mobile",
        "branch": "Branch",
        "section": "Section",
        "semester": "Semester",
        "cgpa": "CGPA",
        "totalCreditsEarned": "TotalCreditsEarned"
    }

    for key, value in metadata_mapping.items():
        row = df[df[0] == value]
        if not row.empty:
            structured_data[key] = row.iloc[0, 1]

    current_semester = ""
    for i, row in df.iterrows():
        cell_value = str(row[0])
        if "Semester" in cell_value:
            current_semester = cell_value
            structured_data["grades"][current_semester] = {}
        elif current_semester and pd.notna(row[0]) and pd.notna(row[1]):
            subject = row[0]
            grade = row[1]
            structured_data["grades"][current_semester][subject] = grade

    # Remove empty semesters
    structured_data["grades"] = {k: v for k, v in structured_data["grades"].items() if v}

    # Explicitly remove cgpa and totalCreditsEarned from the last semester dictionary
    if current_semester in structured_data["grades"]:
        if "CGPA" in structured_data["grades"][current_semester]:
            del structured_data["grades"][current_semester]["CGPA"]
        if "TotalCreditsEarned" in structured_data["grades"][current_semester]:
            del structured_data["grades"][current_semester]["TotalCreditsEarned"]

    return structured_data

def convert(excel_file_path):
    try:
        if os.path.isdir(excel_file_path):
            raise IsADirectoryError(f"The specified path {excel_file_path} is a directory, not a file.")
        
        df = excel_to_json(excel_file_path)
        json_dict = {"data": create_json_structure(df)}
        
        print(json.dumps(json_dict, indent=4))
        
        json_file_path = excel_file_path.replace(".xlsx", ".json")
        with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(json_dict, jsonfile, indent=4)
        print(f"JSON data has been written to {json_file_path}")
        return json_file_path
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an Excel file to JSON")
    parser.add_argument("excel_file_path", type=str, help="The path to the Excel file")
    args = parser.parse_args()
    convert(args.excel_file_path)
