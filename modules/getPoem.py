import pandas as pd
import random
import kagglehub
import os

def download_poems_dataset():
    try:
        path = kagglehub.dataset_download("tgdivy/poetry-foundation-poems")
        return path
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        try:
            path = kagglehub.dataset_download("johnhallman/complete-poetryfoundationorg-dataset")
            return path
        except Exception as e2:
            print(f"Error downloading alternative dataset: {e2}")
            return None


def load_poems():
    dataset_path = download_poems_dataset()

    if dataset_path is None:
        return None

    csv_files = []
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))

    if not csv_files:
        return None

    for csv_file in csv_files:
        try:
            poems_df = pd.read_csv(csv_file, encoding='utf-8')
            return poems_df
        except Exception as e:
            continue

    return None

def get_random_poem():
    poems_df = load_poems()

    if poems_df is None or poems_df.empty:
        return None, None, None

    random_index = random.randint(0, len(poems_df) - 1)
    poem = poems_df.iloc[random_index]

    title = None
    author = None
    content = None

    columns_lower = {col.lower(): col for col in poem.index}


    title_keys = ['title', 'poem_name', 'name', 'poem title', 'heading']
    for key in title_keys:
        if key in columns_lower and pd.notna(poem[columns_lower[key]]):
            title = poem[columns_lower[key]]
            break

    author_keys = ['author', 'poet', 'writer', 'poet name', 'author name']
    for key in author_keys:
        if key in columns_lower and pd.notna(poem[columns_lower[key]]):
            author = poem[columns_lower[key]]
            break

    content_keys = ['content', 'poem', 'text', 'lines', 'body', 'verse', 'poem content', 'full text']
    for key in content_keys:
        if key in columns_lower and pd.notna(poem[columns_lower[key]]):
            content = poem[columns_lower[key]]
            break

    if content is None:
        max_len = 0
        for col in poem.index:
            val = poem[col]
            if isinstance(val, str) and len(val) > max_len:
                max_len = len(val)
                if len(val) > 100:
                    content = val

    if content is None:
        text_parts = []
        for col in poem.index:
            if isinstance(poem[col], str) and len(poem[col]) > 10:
                text_parts.append(poem[col])
        if text_parts:
            content = "\n".join(text_parts)

    return title, author, content

def get_poem_by_author(author_name):
    poems_df = load_poems()

    if poems_df is None or poems_df.empty:
        return None, None, None

    author_column = None
    columns_lower = {col.lower(): col for col in poems_df.columns}

    for key in ['author', 'poet', 'writer', 'poet name']:
        if key in columns_lower:
            author_column = columns_lower[key]
            break

    if author_column is None:
        return get_random_poem()

    author_poems = poems_df[poems_df[author_column].str.contains(author_name, case=False, na=False)]

    if author_poems.empty:
        return None, None, None

    random_index = random.randint(0, len(author_poems) - 1)
    poem = author_poems.iloc[random_index]

    columns_lower = {col.lower(): col for col in poem.index}

    title = None
    for key in ['title', 'poem_name', 'name']:
        if key in columns_lower and pd.notna(poem[columns_lower[key]]):
            title = poem[columns_lower[key]]
            break

    author = poem[author_column]

    content = None
    for key in ['content', 'poem', 'text', 'lines', 'body']:
        if key in columns_lower and pd.notna(poem[columns_lower[key]]):
            content = poem[columns_lower[key]]
            break

    return title, author, content

def get_poem_count():
    poems_df = load_poems()
    if poems_df is None:
        return 0
    return len(poems_df)