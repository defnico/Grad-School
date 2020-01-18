from lxml import etree
import sys

# Open file for with books data
book_file = open(sys.argv[1], 'r')
book_tree = etree.parse(book_file)
book_root = book_tree.getroot()

# Open inverted index file
index_file = open(sys.argv[2], 'r')
index_tree = etree.parse(index_file)
index_root = index_tree.getroot()


# Function to remove special characters (except apostrophes) and
# converts to lower case.
def sanitize_keyword(keyword):
    return ''.join(c.lower() for c in keyword if c.isalnum() or c == '\'')


# String containing the search queries
search_string = sys.argv[3]
keywords = search_string.strip().split(' ')
search_keywords = [sanitize_keyword(k) for k in keywords]

# Dictionary maps book ids to keywords to a list of elements
# { bookid : { keyword : [elements] } }
books_to_keywords_to_elements = {}
for keyword_node in index_root:
    keyword = keyword_node.get('value')

    for book_node in keyword_node:
        book_id = book_node.get('id')
        for element in book_node:
            # Book id is not in the master dictionary so it gets added
            # along with the keyword along and element type
            if book_id not in books_to_keywords_to_elements:
                books_to_keywords_to_elements[book_id] = {keyword: [element.text]}
            # Book id is present but the keyword is not in its dictionary
            elif keyword not in books_to_keywords_to_elements[book_id]:
                books_to_keywords_to_elements[book_id][keyword] = [element.text]
            # Book id and the keyword both exist, so just element type is added
            else:
                books_to_keywords_to_elements[book_id][keyword].append(element.text)

# Output the keywords dictionary
output_root = etree.Element("results")
for book_node in book_root:
    book_id = book_node.get('id')
    # Get the keyword to elements for a book id
    keyword_to_elements = books_to_keywords_to_elements[book_id]

    # Intersect all the elements for the keywords
    output_elements = None  # The set of elements to output for this book
    for search_keyword in search_keywords:
        if search_keyword not in keyword_to_elements:
            output_elements = None
            break  # Output is empty

        # The list of elements for a keyword
        keyword_elements = set(keyword_to_elements[search_keyword])
        if output_elements is None:  # First time in loop
            output_elements = keyword_elements
        else:
            # Intersect the elements in output_elements with keyword elements
            output_elements = output_elements.intersection(keyword_elements)
            if len(output_elements) == 0:
                break  # Intersecting set is empty

    if output_elements is not None and len(output_elements) > 0:
        output_book_node = etree.SubElement(output_root, "book")
        output_book_node.set("id", book_id)
        for element_node in book_node:
            if element_node.tag in output_elements:
                output_node = etree.SubElement(output_book_node, element_node.tag)
                output_node.text = element_node.text

# Output data to XML file
output_tree = etree.ElementTree(output_root)
with open(sys.argv[4], 'wb') as output_file:
    output_tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="utf-8")
