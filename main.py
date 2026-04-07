import yaml
import genanki
import random
import os
import sys
import argparse
from deep_translator import GoogleTranslator

CONFIG_DIR = os.path.join(os.getcwd(), "conf")
DATA_DIR = os.path.join(os.getcwd(), "data")
OUTPUT_DIR = os.path.join(os.getcwd(), "out")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yml")
MODEL_ID_FILE = os.path.join(CONFIG_DIR, "model_id.txt")


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit()


def get_model_id():
    with open(MODEL_ID_FILE, "r+") as f:
        model_id = f.readline().strip()
        if not model_id:
            model_id = random.randrange(1 << 30, 1 << 31)
            f.write(str(model_id))
    return int(model_id)


def build_front_template():
    return """
<div class="japanese">{{Japanese}}</div>
"""


def build_back_template():
    return """
{{FrontSide}}
<hr>
<div class="english">{{English}}</div>

<iframe id="ifra"></iframe>
<script>
  document.getElementById("ifra").src =
    "https://ichi.moe/cl/qr/?q=" + encodeURIComponent("{{text:Japanese}}");
</script>
"""


def translate(text):
    try:
        return GoogleTranslator(source="ja", target="en").translate(text)
    except Exception as e:
        print(f"  Warning: translation failed for '{text}': {e}")
        return ""


def get_notes(src_file, model):
    notes = []
    with open(src_file, "r", encoding="utf-8") as f:
        for line in f:
            japanese = line.strip()
            if not japanese:
                continue
            print(f"  Translating: {japanese}")
            english = translate(japanese)
            note = genanki.Note(model=model, fields=[japanese, english])
            notes.append(note)
    return notes


def main():
    parser = argparse.ArgumentParser(description="Generate an Anki deck from Japanese lyrics.")
    parser.add_argument("--title", required=True, help="Song title")
    parser.add_argument("--artist", required=True, help="Artist name")
    args = parser.parse_args()

    conf = load_config()
    model_id = get_model_id()

    deck_title = f"{args.title} - {args.artist}"
    deck_filename = f"{args.title}_{args.artist}.apkg".replace(" ", "_")

    anki_model = genanki.Model(
        model_id,
        conf["anki_model_name"],
        fields=[
            {"name": "Japanese"},
            {"name": "English"},
        ],
        templates=[
            {
                "name": "Lyrics Card",
                "qfmt": build_front_template(),
                "afmt": build_back_template(),
            }
        ],
        css=conf["Style"],
    )

    src_file = os.path.join(DATA_DIR, conf["src_filename"])
    notes = get_notes(src_file, anki_model)

    if not notes:
        print("No notes found in source file. Exiting.")
        sys.exit()

    anki_deck = genanki.Deck(model_id, deck_title)
    for note in notes:
        anki_deck.add_note(note)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, deck_filename)
    genanki.Package(anki_deck).write_to_file(output_path)

    print(f"Done! Created '{deck_title}' with {len(anki_deck.notes)} cards.")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
