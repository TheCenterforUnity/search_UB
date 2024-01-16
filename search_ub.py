import requests
import os
import json
import datetime



def search_urantia_book(search_terms, hits_per_page=1000):

    url = 'https://urantia.dev/api/v1/urantia-book/search'
    payload = {
        'q': search_terms,
        'page': 0,
        'setAllQueryWordsOptional': True,
        'sortByRelevance': True,
        'hitsPerPage': hits_per_page  # Adjust as needed
    }
    headers = {'Content-Type': 'application/json'}

    # Send the search request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            data = response.json()
            num_results = len(data['data']['results'])

            return num_results, data['data']['results']
        else:
            print(f"Failed to fetch data: Status code {response.status_code}")
            return 0, []
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return 0, []


def extract_paragraphs_and_text_from_json(json_data):
    try:
        if json_data == []:
            return []
        
        extracted_data = []
        for result in json_data:
            paragraph_info = {
                'standardReference': result['paperSectionParagraphId'],
                'text': result['text']
            }
            extracted_data.append(paragraph_info)
        
        return extracted_data

    except Exception as e:
        return f"An error occurred: {e}"


def search_urantia_book_with_keyword_reduction(search_terms):
    num_results, results = search_urantia_book(search_terms)
    if num_results > 0:
        return results


def write_paragraphs_to_file(search_terms, paragraphs):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{search_terms}_{timestamp}.txt"
    with open(filename, 'w') as file:
        for paragraph in paragraphs:
            standard_reference = paragraph['standardReference']
            paragraph_text = paragraph['text']
            file.write(f"{standard_reference} {paragraph_text}\n")
    print(f"Paragraphs written to {filename}")


def main():
    search_terms = input("Enter the search terms: ")
    num_results, results = search_urantia_book(search_terms)
    if num_results > 0:
        paragraphs = extract_paragraphs_and_text_from_json(results)
        write_paragraphs_to_file(search_terms, paragraphs)
    else:
        print("No results found.")


if __name__ == "__main__":
    main()