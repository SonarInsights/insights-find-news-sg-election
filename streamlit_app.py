import streamlit as st
import feedparser
import urllib.parse
import pandas as pd

st.title("SG Election News Tracker (Indonesia-based Media)")

# Daftar media yang boleh (case-insensitive substring match)
allowed_sources = [
    "Jakarta Post", "Jakarta Globe", "Detik", "Liputan6", "CNN Indonesia", "TVOne", "Republika",
    "Kompas TV", "Sindo News", "Bisnis Indonesia", "Tempo", "Investor Daily", "Kompas", "Kontan",
    "MetroTV", "Antara", "Kumparan", "IDN Times", "BatamPos", "CNBC Indonesia", "Media Indonesia",
    "Tirto.id", "VOI.id"
]

# Dua kombinasi query keyword
query_1 = '''("Singapura" OR "Singapore") AND ("bilateral" OR "kerjasama" OR "Pemilu" OR "Pemilihan Umum" OR "Election" OR "Parlemen" OR "Politics" OR "Political" OR "Pemungutan Suara" OR "Voting" OR "Vote" OR #SGGE OR #GE2025 OR #SingaporeElections OR #VoteSG OR #SGPolitics) AND ("Jokowi" OR "Joko Widodo" OR "Prabowo" OR "Indonesia" OR "Kabinet" OR "DPR" OR "Sugiono" OR "menlu")'''
query_2 = '''("Singapura" OR "Singapore") AND ("Pemilu" OR "Pemilihan Umum" OR "Election" OR "Parlemen" OR "Partai" OR "Politics" OR "Political" OR "Pemungutan Suara" OR "Voting" OR "Vote" OR "People Action Party" OR "Partai Aksi Rakyat" OR "Workers Party" OR "Partai Buruh" OR "Progress Party" OR "Democratic Party" OR "Reform Party" OR "National Solidarity Party" OR "Partai Solidaritas Nasional" OR "Red Dot United" OR #PAP OR #WP OR #PSP OR #SDP) OR ("Lee Hsien Loong" OR "Tharman Shanmugaratnam" OR "Lawrence Wong" OR "Pritam Singh" OR "Jamus Lim" OR "Tan Cheng Bock" OR "Chee Soon Juan" OR "Sylvia Lim" OR #SGGE OR #GE2025 OR #SingaporeElections OR #VoteSG OR #SGPolitics")'''

def google_news_rss(query):
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=id&gl=ID&ceid=ID:id"
    return feedparser.parse(url)

def filter_sources(entries):
    return [entry for entry in entries if any(media.lower() in entry.source.title.lower() for media in allowed_sources)]

# Proses pencarian
st.write("🔎 Searching news...")
feed1 = google_news_rss(query_1)
feed2 = google_news_rss(query_2)

filtered_entries = filter_sources(feed1.entries) + filter_sources(feed2.entries)

# Tampilkan hasil
if filtered_entries:
    st.success(f"Ditemukan {len(filtered_entries)} berita dari media yang disetujui.")
    for entry in filtered_entries:
        st.markdown(f"### [{entry.title}]({entry.link})\n📅 {entry.published} \n📰 {entry.source.title}")
else:
    st.warning("Tidak ada hasil dari media yang diizinkan.")

# Export to CSV
if filtered_entries:
    df = pd.DataFrame([{
        "Title": e.title,
        "Link": e.link,
        "Published": e.published,
        "Source": e.source.title
    } for e in filtered_entries])

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download as CSV", data=csv, file_name="sg_election_news.csv", mime="text/csv")
