import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Membuat objek stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Fungsi untuk membersihkan dan memproses teks
def preprocess_text(text):
    # Konversi ke huruf kecil
    text = text.lower()
    # Hilangkan karakter yang tidak diperlukan
    text = re.sub(r'[^a-z\s]', '', text)
    # Stemming
    text = stemmer.stem(text)
    return text

# Data latih contoh (sederhana) - dapat diganti dengan dataset yang lebih besar
data = {
    'text': [
        'saya sangat senang dengan konten ini',
        'konten ini buruk sekali',
        'saya puas dengan konten ini',
        'konten ini mengecewakan',
        'saya merasa sangat senang',
        'saya sangat tidak puas',
        'konten yang bagus dan cepat',
        'konten sangat buruk dan mengecewakan',
        'saya tidak suka dengan konten ini',
        'saya suka dengan konten ini',
        'kontennya informatif',
        'tidak ada yang spesial dengan konten ini',
        'kontennya biasa saja, tidak terlalu menarik',
        'saya rasa konten ini oke, tidak buruk',
        'sangat kecewa dengan kontennya',
        'ini adalah konten terbaik yang pernah saya lihat',
        'konten ini cukup membantu',
        'tidak jelek, tapi bisa lebih baik',
        'kontennya bagus tapi ada beberapa kekurangan',
        'kontennya tidak memenuhi harapan'
    ],
    'label': [
        'positif', 'negatif', 'positif', 'negatif', 'positif', 'negatif', 'positif', 'negatif', 'negatif', 'positif',
        'netral', 'netral', 'netral', 'netral', 'negatif', 'positif', 'positif', 'netral', 'netral', 'negatif'
    ]
}

# Memuat data ke dalam DataFrame
df = pd.DataFrame(data)

# Preprocessing data
df['text'] = df['text'].apply(preprocess_text)

# Pisahkan fitur dan label
X = df['text']
y = df['label']

# Membagi data menjadi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Konversi teks ke vektor fitur
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Melatih model Naive Bayes
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Prediksi pada data uji
y_pred = model.predict(X_test_vec)

# Evaluasi
# print("Akurasi:", accuracy_score(y_test, y_pred))
# print("\nLaporan Klasifikasi:\n", classification_report(y_test, y_pred))

# Fungsi untuk prediksi sentimen teks baru
def predict_sentiment(text):
    processed_text = preprocess_text(text)
    text_vec = vectorizer.transform([processed_text])
    prediction = model.predict(text_vec)
    return prediction[0]

# Contoh prediksi
comments = [
    'saya sangat senang dengan konten ini',
    'saya tidak suka dengan konten ini',
    'sangat bagus, sesuai dengan realita',
    'Produk yang buruk sekali'
]

for comment in comments:
    print("Teks:", comment)
    print("Prediksi Sentimen:", predict_sentiment(comment))
    print()

# Contoh prediksi teks baru
# print("Teks:", new_text)
# print("Prediksi Sentimen:", predict_sentiment(new_text))
