import json
import csv

# Specify the path to your JSON file
json_file_path = './filtered_data.json'

# Read JSON data from a file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Define the CSV file name
csv_file = "output.csv"

# CSV column headers
headers = ["id", "term", "monday", "tuesday", "wednesday", "thursday", "friday",
           "enrollment", "maximumEnrollment", "courseNumber", "subject", 
           "sequenceNumber", "beginTime", "endTime", "room", "building",
           "facultyName", "facultyEmail"]

# Open a CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write the header row

    # Process each item in the JSON data
    for item in data:
        # Basic course and section information
        course_info = [
            item.get("id", ""),
            item.get("term", "")
        ]

        # Meeting times (assuming the first entry is the primary meeting time)
        meetings = item.get("meetingsFaculty", [])
        if meetings:
            meeting_info = meetings[0].get("meetingTime", {})
            days = [
                meeting_info.get("monday", False),
                meeting_info.get("tuesday", False),
                meeting_info.get("wednesday", False),
                meeting_info.get("thursday", False),
                meeting_info.get("friday", False)
            ]
        else:
            # Default values if no meetings info is found
            days = [False] * 5

        # More detailed course and enrollment information
        detailed_info = [
            item.get("enrollment", ""),
            item.get("maximumEnrollment", ""),
            item.get("courseNumber", ""),
            item.get("subject", ""),
            item.get("sequenceNumber", "")
        ]

        # Time and location details
        if meetings:
            time_location = [
                meeting_info.get("beginTime", ""),
                meeting_info.get("endTime", ""),
                meeting_info.get("room", ""),
                meeting_info.get("building", "")
            ]
        else:
            # Default values if no time/location info is found
            time_location = [""] * 4

        # Extract faculty details, assume primary faculty is first or only one listed
        faculty = item.get("faculty", [])
        faculty_name = faculty[0].get("displayName", "") if faculty else ""
        faculty_email = faculty[0].get("emailAddress", "") if faculty else ""

        # Combine all parts into one row
        row = course_info + days + detailed_info + time_location + [faculty_name, faculty_email]
        writer.writerow(row)  # Write the row to the CSV file

print(f"Data has been written to {csv_file}")