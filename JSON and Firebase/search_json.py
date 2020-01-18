import sys, requests, json

# Firebase URL
firebase_url = 'https://inf-551-sample-3e50d.firebaseio.com/.json'

# Get all json INDEX data from Firebase
index_url = firebase_url[:-5] + 'index/.json'

# Turn all INDEX data into json object
all_index_data = requests.get(index_url)
json_index_data_object = json.loads(all_index_data.text)

# Get all json RESTAURANT data from Firebase
restaurants_url = firebase_url[:-5] + 'restaurants/.json'

# Turn all RESTAURANT data into json object
all_restaurant_data = requests.get(restaurants_url)
json_restaurant_data_object = json.loads(all_restaurant_data.text)

# Get keywords from command line, split them into list
keywords = sys.argv[1]
keywords = keywords.split(' ')

# Make each word in the input lowercase and get rid of extra spaces
# cleaned_keywords gets rid of special characters to index the inverted array
cleaned_keywords = []
for word in keywords:
    word = word.lower()
    word = word.strip()

    for char in word:
        if not char.isalnum():
            word = word.replace(char, ' ')
    # Eliminate created whitespaces (#004 -> ''004)
    word = word.strip()
    words_split = word.split(' ')

    # Add each split word to cleaned_keywords
    for w in words_split:
        cleaned_keywords.append(w)

# Restaurants with keywords
restaurants_with_keywords = {}

# Iterate through the cleaned_keywords and get the restaurant serial_numbers
for keyword in cleaned_keywords:
    # Make sure keyword is not empty
    if keyword:
        keyword_request_url = firebase_url[:-5] + 'index/' + str(keyword) + '/.json'

        # Find the keyword in the index node
        request = requests.get(keyword_request_url)

        # Split the request to get each serial number
        serial_numbers = request.text.split(',')

        for serial_number in serial_numbers:
            # Make sure the serial number exist
            if serial_number != 'null':
                # Get rid of special characters to be able to index
                serial_number = serial_number.strip('"[],')

                # Get the restaurant object first
                # then get the name and score
                restaurant = json_restaurant_data_object[serial_number]
                facility_name = restaurant['facility_name']
                score = restaurant['score']

                # Add to restaurant with keyword dictionary
                if serial_number not in restaurants_with_keywords:
                    restaurants_with_keywords[serial_number] = {"facility_name" : facility_name,
                                                                "score" : score}

# Pretty print JSON dictionary in the console
pretty_json = json.dumps(restaurants_with_keywords, sort_keys=True, indent=2)
print(pretty_json)
