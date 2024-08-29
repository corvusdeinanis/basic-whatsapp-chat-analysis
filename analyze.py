import os
from collections import defaultdict, Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
import re
import emoji

nltk.download('stopwords')

def read_messages(directory):
    messages = defaultdict(list)
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            sender = filename.replace('_', ' ').replace('.txt', '')
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                messages[sender] = file.readlines()
    return messages

def basic_stats(messages):
    stats = {}
    for sender, msgs in messages.items():
        word_count = sum(len(re.findall(r'\w+', msg)) for msg in msgs)
        emoji_count = sum(len([char for char in msg if char in emoji.EMOJI_DATA]) for msg in msgs)
        stats[sender] = {'message_count': len(msgs), 'word_count': word_count, 'emoji_count': emoji_count}
    return stats

def most_common_words_per_person(messages, ignore_phrases=None, n=10):
    if ignore_phrases is None:
        ignore_phrases = ['<media omitted>']

    stop_words = set(stopwords.words('english'))
    common_words = {}

    for sender, msgs in messages.items():
        word_freq = defaultdict(int)

        for msg in msgs:
            words = re.findall(r'\w+', msg.lower())
            filtered_words = [word for word in words if word not in stop_words and word not in ignore_phrases]
            for word in filtered_words:
                word_freq[word] += 1

        common_words[sender] = sorted(word_freq.items(), key=lambda item: item[1], reverse=True)[:n]

    return common_words

def most_common_words(messages, ignore_phrases=None, n=10):
    if ignore_phrases is None:
        ignore_phrases = ['<media omitted>']

    stop_words = set(stopwords.words('english'))
    word_freq = defaultdict(int)

    for sender, msgs in messages.items():
        for msg in msgs:
            words = re.findall(r'\w+', msg.lower())
            filtered_words = [word for word in words if word not in stop_words and word not in ignore_phrases]
            for word in filtered_words:
                word_freq[word] += 1

    return sorted(word_freq.items(), key=lambda item: item[1], reverse=True)[:n]

def most_common_emojis_per_person(messages, n=10):
    emoji_freq = defaultdict(Counter)
    for sender, msgs in messages.items():
        for msg in msgs:
            for char in msg:
                if char in emoji.EMOJI_DATA:
                    emoji_freq[sender][char] += 1
    return {sender: freq.most_common(n) for sender, freq in emoji_freq.items()}

def most_common_emojis(messages, n=10):
    emoji_freq = Counter()
    for sender, msgs in messages.items():
        for msg in msgs:
            for char in msg:
                if char in emoji.EMOJI_DATA:
                    emoji_freq[char] += 1
    return emoji_freq.most_common(n)

def sentiment_analysis(messages):
    sentiments = {}
    for sender, msgs in messages.items():
        sentiment_scores = [TextBlob(msg).sentiment.polarity for msg in msgs]
        average_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        sentiments[sender] = average_sentiment
    return sentiments

def generate_wordcloud(messages, output_file):
    all_text = ' '.join([' '.join(msgs) for msgs in messages.values()])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_file)
    plt.close()

def save_results_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")

def save_common_words_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        for sender, words in data.items():
            file.write(f"{sender}:\n")
            for word, freq in words:
                file.write(f"  {word}: {freq}\n")

def save_common_emojis_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        for sender, emojis in data.items():
            file.write(f"{sender}:\n")
            for emoji_char, freq in emojis:
                file.write(f"  {emoji_char}: {freq}\n")

def main():
    directory = 'output'
    messages = read_messages(directory)
    
    stats = basic_stats(messages)
    save_results_to_file('basic_stats.txt', stats)
    
    common_words_per_person = most_common_words_per_person(messages)
    save_common_words_to_file('common_words_per_person.txt', common_words_per_person)

    common_words_group = most_common_words(messages)
    save_common_words_to_file('common_words_group.txt', {"group": common_words_group})

    common_emojis_per_person = most_common_emojis_per_person(messages)
    save_common_emojis_to_file('common_emojis_per_person.txt', common_emojis_per_person)

    common_emojis_group = most_common_emojis(messages)
    save_common_emojis_to_file('common_emojis_group.txt', {"group": common_emojis_group})

    sentiments = sentiment_analysis(messages)
    save_results_to_file('sentiments.txt', sentiments)
    
    generate_wordcloud(messages, 'wordcloud.png')

    print("Analysis complete. Results saved to files.")

if __name__ == "__main__":
    main()
