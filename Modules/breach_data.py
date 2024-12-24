# Specify the file path
file_path = "../../Downloads/iimjobs - Part 36.TXT"

# Open the file and read its contents
with open(file_path, "r") as f:
    data = f.read()

# Find the starting index of the substring "info@rakshittandon.com"
start = data.find("info@rakshittandon.com")

# Check if the substring was found
if start != -1:
    # Print the substring starting from 'start' index to 'start + 10'
    print(data[start-130:start + 25])
else:
    print("Substring 'info@rakshittandon.com' not found in the file.")
