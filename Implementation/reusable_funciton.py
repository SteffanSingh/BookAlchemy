import json
import requests


def get_book_details(title):
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    response = requests.get(google_books_api_url)
    data = response.json()
    # print(data)
    print(data['totalItems'])
    if data["totalItems"] >0:
        response_content = response.content
        data = json.loads(response_content.decode('utf-8'))

        if "items" in data and len(data["items"]) > 0:
            book_info = data["items"][0]["volumeInfo"]
            # print(data["items"][0]["volumeInfo"]['description'])
            author_name = book_info.get('authors', ['N/A'])
            cover_image_url = book_info.get('imageLinks', {}).get('thumbnail', 'N/A')
            isbn = data['items'][0].get('id', 'N/A')
            authors_info = book_info.get('authors', [])
            publication_year = book_info.get('publishedDate', 'N/A')
            description = book_info['description'] if "description" in book_info else " "
            rating = book_info['averageRating'] if 'averageRating' in book_info else 0
            return isbn, cover_image_url, author_name, publication_year, description, rating
        return None
    else:
        return None
