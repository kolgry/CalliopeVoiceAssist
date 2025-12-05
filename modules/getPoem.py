import pandas as pd
import random
import kagglehub
import os


def download_poems_dataset():
    try:
        path = kagglehub.dataset_download("michaelarman/poemsdataset")
        return path
    except Exception as e:
        print(f"Error downloading dataset: {e}")
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
        print("No CSV files found in dataset")
        return None

    try:
        poems_df = pd.read_csv(csv_files[0])
        return poems_df
    except Exception as e:
        print(f"Error loading poems: {e}")
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

    title_columns = ['title', 'Title', 'poem_name', 'Poem Name']
    author_columns = ['author', 'Author', 'poet', 'Poet']
    content_columns = ['content', 'Content', 'poem', 'Poem', 'text', 'Text', 'lines', 'Lines']

    for col in title_columns:
        if col in poem:
            title = poem[col]
            break

    for col in author_columns:
        if col in poem:
            author = poem[col]
            break

    for col in content_columns:
        if col in poem:
            content = poem[col]
            break

    return title, author, content


def get_poem_by_author(author_name):
    poems_df = load_poems()

    if poems_df is None or poems_df.empty:
        return None, None, None

    author_column = None
    for col in ['author', 'Author', 'poet', 'Poet']:
        if col in poems_df.columns:
            author_column = col
            break

    if author_column is None:
        return get_random_poem()  # Fallback to random if no author column

    author_poems = poems_df[poems_df[author_column].str.contains(author_name, case=False, na=False)]

    if author_poems.empty:
        return None, None, None

    random_index = random.randint(0, len(author_poems) - 1)
    poem = author_poems.iloc[random_index]

    title = poem.get('title') or poem.get('Title')
    author = poem.get(author_column)
    content = poem.get('content') or poem.get('Content') or poem.get('poem') or poem.get('Poem')

    return title, author, content