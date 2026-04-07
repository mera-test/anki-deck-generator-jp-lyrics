# Japanese Lyrics Anki Deck Generator

Generates a personalized Anki deck from Japanese song lyrics. Each card represents one lyric line — the front shows the Japanese text, and the back shows the English translation (auto-generated) alongside an ichi.moe word-by-word breakdown.

## Requirements

- [Python 3](https://www.python.org/downloads/)
- [Anki for Desktop](https://apps.ankiweb.net/)
- [`genanki`](https://github.com/kerrickstaley/genanki)
- [`PyYAML`](https://pypi.org/project/PyYAML/)
- [`deep-translator`](https://pypi.org/project/deep-translator/)

Install all Python packages at once:
```
pip install genanki pyyaml deep-translator
```

## Source data

Edit `data/source.txt` and paste in your Japanese lyrics — one line per line, nothing else needed.

```
桜の花びらたちよ
風に舞い上がれ
遠い空の彼方へ
消えてしまう前に
```

Each line will be automatically translated to English using Google Translate when the deck is generated.

## Usage

```
python main.py --title "Song Title" --artist "Artist Name"
```

The generated `.apkg` file will be saved to the `out/` folder, named `Song_Title_Artist_Name.apkg`. Open it with Anki for Desktop to import and start studying.

## Card format

- Front: Japanese lyric line
- Back: Japanese line + English translation + ichi.moe breakdown (click the link or press Tab to toggle)

## Config

Card styling and the Anki model name can be adjusted in `conf/config.yml`.
