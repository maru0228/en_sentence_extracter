import argparse
import os
from gtts import gTTS
from distutils.util import strtobool

def file_names(path):
    names = os.listdir(path)
    names.remove(".gitignore")
    return names

def split_sentences(text, all_sentences, deduplication):
    # 「-」の扱いは文章によってことなるので置換対象外にする
    text = text.replace(".", "")
    text = text.replace("”", "")
    text = text.replace("“", "")
    text = text.replace(",", "")
    text = text.replace(":", "")
    text = text.replace(";", "")
    text = text.replace("!", "")
    text = text.replace("?", "")
    text = text.lower()
    sentences = list(set(text.split()))
    sentences.sort()

    # 二文字までの英単語は省略する
    sentences = [s for s in sentences if len(s) > 2]

    if deduplication:
        for sentence in all_sentences:
            if sentence in sentences:
                sentences.remove(sentence)
    return sentences

def clean_output_dir():
    for file_name in file_names("./output_text"):
        os.remove("./output_text/" + file_name)
    for file_name in file_names("./output_mp3"):
        os.remove("./output_mp3/" + file_name)

def extract(file_name, all_sentences, deduplication):
    parser = argparse.ArgumentParser()
    parser.add_argument("--encoding", default="UTF-8")
    args = parser.parse_args()
    f = open("./input" + "/" + file_name, "r", encoding=args.encoding)
    text = f.read()
    f.close()
    sentences = split_sentences(text, all_sentences, deduplication)
    return sentences

def extract_input_dir():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deduplication", default="0")
    parser.add_argument("--encoding", default="UTF-8")
    args = parser.parse_args()
    deduplication = strtobool(args.deduplication)
    all_sentences = []

    for file_name in file_names("./input"):
        sentences = extract(file_name, all_sentences, deduplication)
        all_sentences += sentences
        all_sentences = list(set(all_sentences))
        file = open("./output_text/" + file_name, "w", encoding=args.encoding, newline="\n")
        for sentence in sentences:
            file.write(sentence + "\n")
        file.close()

    for sentence in all_sentences:
        tts = gTTS(sentence)
        tts.save("./output_mp3/" + sentence + '.mp3')

def main():
    clean_output_dir()
    extract_input_dir()

main()
