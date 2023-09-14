import base64
import slugify

from settings import (
    SITENAME,
    USER,
    PASSWORD
)
from src.utils.utils import get_url, HTTPMethod, DecodeTo

creds = f'{USER}:{PASSWORD}'
token = base64.b64encode(creds.encode())
URL_POSTS = f'{SITENAME}/wp-json/wp/v2/posts'
URL_MEDIA = f'{SITENAME}/wp-json/wp/v2/media'
URL_CATEGORY = f'{SITENAME}/wp-json/wp/v2/categories'


def wp_post(
        title: str,
        page: str,
        category: int
):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + token.decode('utf-8')
    }
    data = {
        'title': title,
        'content': page,
        'status': 'publish',
        'categories': [category]
    }
    json = get_url(
        HTTPMethod.POST,
        DecodeTo.JSON,
        URL_POSTS,
        headers=headers,
        json=data,
    )
    return json


def wp_file(
        content: bytes,
        filename: str,
        content_type: str,
):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': content_type,  # 'image/jpg'
        'Content-Disposition':
            f'attachment; filename={filename}'
    }
    json = get_url(
        HTTPMethod.POST,
        DecodeTo.JSON,
        URL_MEDIA,
        data=content,
        headers=headers,
        auth=(USER, PASSWORD),
        verify=False
    )

    link = json.get('guid').get("rendered")
    return link


def wp_category(name: str, parent: int = None) -> int:
    slug = slugify(name)[:40]
    print(slug)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + token.decode('utf-8')
    }
    data = {
        'name': name,
        'parent': parent,
        'slug': slug
    }
    json = get_url(
        HTTPMethod.POST,
        DecodeTo.JSON,
        URL_CATEGORY,
        headers=headers,
        json=data,
    )

    category_id = json.get('id')
    return category_id


def wp_get_categories():
    json = get_url(
        HTTPMethod.GET,
        DecodeTo.JSON,
        URL_CATEGORY,
    )
    return json


if __name__ == '__main__':
    category_name = 'Кодексы'
    category_id = wp_category(category_name)
    print(category_id)
