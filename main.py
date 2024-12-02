import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Ambil data komentar dari Instagram
data = pd.read_csv('youtube-comments.csv')

# Inisialisasi Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Tambahkan kolom untuk sentiment score
data['sentiment_score'] = data['komentar'].apply(lambda x: analyzer.polarity_scores(str(x))['compound'])

# Fungsi untuk menentukan label sentimen dengan threshold untuk netral
def get_sentiment_label(score):
    if score >= 0.05:
        return 'positif'
    elif score <= -0.05:
        return 'negatif'
    else:
        return 'netral'

# Terapkan fungsi label sentimen
data['sentiment_label'] = data['sentiment_score'].apply(get_sentiment_label)

# Tampilkan data
print(f"{data}")

# Hitung statistik sentimen
total_komentar = len(data)
positif_komentar = len(data[data['sentiment_label'] == 'positif'])
negatif_komentar = len(data[data['sentiment_label'] == 'negatif'])
netral_komentar = len(data[data['sentiment_label'] == 'netral'])

# Hitung persentase
persentase_positif = (positif_komentar / total_komentar) * 100
persentase_negatif = (negatif_komentar / total_komentar) * 100
persentase_netral = (netral_komentar / total_komentar) * 100

# Tampilkan hasil analisis
print("\nHasil Analisis Sentimen:")
print(f"Total komentar: {total_komentar}")
print(f"Komentar positif: {positif_komentar} ({persentase_positif:.2f}%)")
print(f"Komentar negatif: {negatif_komentar} ({persentase_negatif:.2f}%)")
print(f"Komentar netral: {netral_komentar} ({persentase_netral:.2f}%)")