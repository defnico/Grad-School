from lxml import etree
import sys

# Open file and get root of XML tree for books file
input_file = open(sys.argv[1], 'r')
input_tree = etree.parse(input_file)
input_root = input_tree.getroot()


# Function to remove special characters (except apostrophes) and
# converts to lower case.
def sanitize_keyword(keyword):
    return ''.join(c.lower() for c in keyword if c.isalnum() or c == '\'')


# Dictionary of keywords to book ids with each book id being a dictionary
# entry that maps to a list of elements
# { keyword : { books ids : [elements] } }
keywords_to_books_to_elements = {}

# Iterate through each book from the input file
for book_node in input_root:
    # Fetch the book id attribute
    book_id = book_node.get('id')

    # Iterate through the book elements and save the required ones
    for element_node in book_node:
        if element_node.tag not in ("author", "title", "genre", "description"):
            continue

        # Get the keywords from element.text
        keywords = element_node.text.strip().split(' ')
        for k in keywords:
            keyword = sanitize_keyword(k)
            # Make sure keyword is not an empty string
            if not keyword:
                continue

            # Check if keyword is in the master dictionary
            if keyword not in keywords_to_books_to_elements:
                # If keyword is not in master dictionary, add it to the master dictionary
                # the map from book_id to element
                keywords_to_books_to_elements[keyword] = {book_id: [element_node.tag]}
            else:
                # Keyword exists in the master dictionary
                books_to_elements = keywords_to_books_to_elements[keyword]

                # Check if the book id is already present for that keyword
                if book_id not in books_to_elements:
                    books_to_elements[book_id] = [element_node.tag]
                elif element_node.tag not in books_to_elements[book_id]:
                    # Book id is present so we add the element to its list
                    books_to_elements[book_id].append(element_node.tag)

# Output the keywords dictionary
output_root = etree.Element("index")
# For each keyword in the master list
for keyword in keywords_to_books_to_elements:
    # Create a keyword node with keyword as the node value
    keyword_node = etree.SubElement(output_root, "keyword")
    keyword_node.set("value", keyword)

    # Get the dictionary of book ids to elements for that keyword
    books_to_elements = keywords_to_books_to_elements[keyword]
    for book_id in books_to_elements:
        # Create a book node under each keyword
        book_node = etree.SubElement(keyword_node, "book")
        book_node.set("id", book_id)

        # Get the list of attributes for the book id
        # and add them under the book node
        book_id_list = books_to_elements[book_id]
        for element in book_id_list:
            element_node = etree.SubElement(book_node, "element")
            element_node.text = element

# Output data to XML file
output_tree = etree.ElementTree(output_root)
with open(sys.argv[2], 'wb') as output_file:
    output_tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="utf-8")
