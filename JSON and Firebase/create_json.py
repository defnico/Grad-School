import csv, sys, requests, json

# Firebase URL
firebase_url = 'https://inf-551-sample-3e50d.firebaseio.com/.json'

# Get the file from command line
csvfile = open(str(sys.argv[1]), 'r')

# Read csv as key, value pairs
reader = csv.DictReader(csvfile)

# Dictionary for inverted index
inverted_index_dict = {}

# Construct JSON object for restaurant information
restaurant_data = {}

# Iterate through the file
for row in reader:
    # Get the correct columns
    serial_number = row["serial_number"]
    facility_name = row["facility_name"]
    score = row["score"]

    # Create dictionary entry with serial_number as index
    # Facility name and score are the values
    restaurant_data[serial_number] = {"facility_name" : facility_name, "score" : score}

    # Make the facility name lowercase, split the facility name at the spaces
    facility_name = facility_name.lower().strip().split(' ')

    # Get rid of special characters and
    # further split facility_name by punctuation
    for word in facility_name:
        for char in word:
            if not char.isalnum():
                # Replace special characters with blank spaces
                word = word.replace(char, ' ')
        # Eliminate created whitespaces (#004 -> ''004)
        word = word.strip()
        words_split = word.split(' ')

        # Populate the inverted index dictionary
        for word_split in words_split:
            # Make sure word is not empty
            if word_split:
                if word_split not in inverted_index_dict:
                    inverted_index_dict[word_split] = [serial_number]
                else:
                    inverted_index_dict[word_split].append(serial_number)

# Create JSON object containing restaurant serial_number, name, and score
# under the 'restaurants' node
restaurant_data = json.dumps(restaurant_data)
restaurant_url = firebase_url[:-5] + 'restaurants/.json'
requests.patch(restaurant_url, restaurant_data)

# Create JSON object for the inverted index
# under the 'index' node
json_data_restaurant_words = json.dumps(inverted_index_dict)
index_url = firebase_url[:-5] + 'index/.json'
requests.patch(index_url, json_data_restaurant_words)

# Pretty print JSON dictionary in the console
pretty_json = json.dumps(inverted_index_dict, sort_keys=True, indent = 2)
print(pretty_json)
