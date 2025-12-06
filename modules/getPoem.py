import pandas as pd
import random
import kagglehub
import os

# POEM SIZE LIMITS
MAX_LINES = 20  # Maximum number of lines
MAX_CHARACTERS = 1000  # Maximum total characters
MAX_WORDS = 200  # Maximum number of words


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


def truncate_poem(content, max_lines=MAX_LINES, max_chars=MAX_CHARACTERS, max_words=MAX_WORDS):
    if content is None:
        return None

    lines = content.split('\n')

    # Limit by number of lines
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        content = '\n'.join(lines)
        print(f"[INFO] Poem truncated to {max_lines} lines")

    # Limit by characters
    if max_chars and len(content) > max_chars:
        content = content[:max_chars]
        # Try to end at a complete line
        last_newline = content.rfind('\n')
        if last_newline > max_chars * 0.8:  # If we're close to the limit
            content = content[:last_newline]
        print(f"[INFO] Poem truncated to {max_chars} characters")

    # Limit by words
    if max_words:
        words = content.split()
        if len(words) > max_words:
            content = ' '.join(words[:max_words])
            print(f"[INFO] Poem truncated to {max_words} words")

    return content


def is_poem_suitable(content, max_lines=MAX_LINES, max_chars=MAX_CHARACTERS, max_words=MAX_WORDS):
    if content is None:
        return False

    lines = content.split('\n')
    words = content.split()

    if max_lines and len(lines) > max_lines:
        return False
    if max_chars and len(content) > max_chars:
        return False
    if max_words and len(words) > max_words:
        return False

    return True


def get_random_poem(truncate=True, filter_by_size=True):
    poems_df = load_poems()

    if poems_df is None or poems_df.empty:
        return None, None, None

    if filter_by_size:
        max_attempts = 50  # Try up to 50 poems
        for attempt in range(max_attempts):
            random_index = random.randint(0, len(poems_df) - 1)
            poem = poems_df.iloc[random_index]

            content = extract_content(poem)

            if is_poem_suitable(content):
                title = extract_title(poem)
                author = extract_author(poem)
                print(f"[INFO] Found suitable poem on attempt {attempt + 1}")
                return title, author, content

        print("[WARNING] Could not find poem within size limits, returning truncated poem")

    random_index = random.randint(0, len(poems_df) - 1)
    poem = poems_df.iloc[random_index]

    title = extract_title(poem)
    author = extract_author(poem)
    content = extract_content(poem)

    if truncate:
        content = truncate_poem(content)

    return title, author, content


def extract_title(poem):
    columns_lower = {col.lower(): col for col in poem.index}
    title_keys = ['title', 'poem_name', 'name', 'poem title', 'heading']

    for key in title_keys:
        if key in columns_lower and pd.notna(poem[columns_lower[key]]):
            return poem[columns_lower[key]]
    return None


def extract_author(poem):
    columns_lower = {col.lower(): col for col in poem.index}
    author_keys = ['author', 'poet', 'writer', 'poet name', 'author name']

    for key in author_keys:
        if key in columns_lower and pd.notna(poem[columns_lower[key]]):
            return poem[columns_lower[key]]
    return None


def extract_content(poem):
    columns_lower = {col.lower(): col for col in poem.index}
    content_keys = ['content', 'poem', 'text', 'lines', 'body', 'verse', 'poem content', 'full text']

    for key in content_keys:
        if key in columns_lower and pd.notna(poem[columns_lower[key]]):
            return poem[columns_lower[key]]

    max_len = 0
    content = None
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

    return content


def get_poem_by_author(author_name, truncate=True):
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
        return get_random_poem(truncate=truncate)

    author_poems = poems_df[poems_df[author_column].str.contains(author_name, case=False, na=False)]

    if author_poems.empty:
        return None, None, None

    random_index = random.randint(0, len(author_poems) - 1)
    poem = author_poems.iloc[random_index]

    title = extract_title(poem)
    author = extract_author(poem)
    content = extract_content(poem)

    if truncate:
        content = truncate_poem(content)

    return title, author, content


def get_poem_count():
    poems_df = load_poems()
    if poems_df is None:
        return 0
    return len(poems_df)



def get_short_poem():
    global MAX_LINES, MAX_CHARACTERS, MAX_WORDS
    old_lines, old_chars, old_words = MAX_LINES, MAX_CHARACTERS, MAX_WORDS

    MAX_LINES = 10
    MAX_CHARACTERS = 500
    MAX_WORDS = 100

    result = get_random_poem(truncate=True, filter_by_size=True)

    MAX_LINES, MAX_CHARACTERS, MAX_WORDS = old_lines, old_chars, old_words
    return result


def get_medium_poem():
    global MAX_LINES, MAX_CHARACTERS, MAX_WORDS
    old_lines, old_chars, old_words = MAX_LINES, MAX_CHARACTERS, MAX_WORDS

    MAX_LINES = 20
    MAX_CHARACTERS = 1000
    MAX_WORDS = 200

    result = get_random_poem(truncate=True, filter_by_size=True)

    MAX_LINES, MAX_CHARACTERS, MAX_WORDS = old_lines, old_chars, old_words
    return result