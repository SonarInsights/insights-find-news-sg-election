import streamlit as st
import feedparser
import urllib.parse
import pandas as pd
from datetime import datetime, timedelta
import pytz

st.title("🗳️ SG Election News Tracker")

# Subtext kecil di bawah judul
st.markdown(
    "<p style='font-size: 14px; color: gray;'>by <strong>Insights Sonar</strong> (for internal use only)<br>If you encounter any issues, please contact: <a href='mailto:katon.prasetyo@sonar.id'>katon.prasetyo@sonar.id</a></p>",
    unsafe_allow_html=True
)

# Media Indonesia yang diperbolehkan
allowed_sources = [
    "Jakarta Post", "Jakarta Globe", "Detik", "Liputan6", "CNN Indonesia", "TVOne", "Republika",
    "Kompas TV", "Sindo News", "Bisnis Indonesia", "Tempo", "Investor Daily", "Kompas", "Kontan",
    "MetroTV", "Antara", "Kumparan", "IDN Times", "BatamPos", "CNBC Indonesia", "Media Indonesia",
    "Tirto.id", "VOI.id"
]

# Dua set keyword Google News
query_1 = '''("Singapura" OR "Singapore") AND ("bilateral" OR "kerjasama" OR "Pemilu" OR "Pemilihan Umum" OR "Election" OR "Parlemen" OR "Politics" OR "Political" OR "Pemungutan Suara" OR "Voting" OR "Vote" OR #SGGE OR #GE2025 OR #SingaporeElections OR #VoteSG OR #SGPolitics) AND ("Jokowi" OR "Joko Widodo" OR "Prabowo" OR "Indonesia" OR "Kabinet" OR "DPR" OR "Sugiono" OR "menlu")'''

query_2 = '''("Singapura" OR "Singapore") AND ("Pemilu" OR "Pemilihan Umum" OR "Election" OR "Parlemen" OR "Partai" OR "Politics" OR "Political" OR "Pemungutan Suara" OR "Voting" OR "Vote" OR "People Action Party" OR "Partai Aksi Rakyat" OR "Workers Party" OR "Partai Buruh" OR "Progress Party" OR "Democratic Party" OR "Reform Party" OR "National Solidarity Party" OR "Partai Solidaritas Nasional" OR "Red Dot United" OR #PAP OR #WP OR #PSP OR #SDP) OR ("Lee Hsien Loong" OR "Tharman Shanmugaratnam" OR "Lawrence Wong" OR "Pritam Singh" OR "Jamus Lim" OR "Tan Cheng Bock" OR "Chee Soon Juan" OR "Sylvia Lim" OR #SGGE OR #GE2025 OR #SingaporeElections OR #VoteSG OR #SGPolitics")'''

def google_news_rss(query):
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=id&gl=ID&ceid=ID:id"
    return feedparser.parse(url)

def filter_sources(entries):
    return [entry for entry in entries if any(media.lower() in entry.source.title.lower() for media in allowed_sources)]

def filter_24_hours(entries):
    now = datetime.now(pytz.utc)
    day_ago = now - timedelta(days=1)

    filtered = []
    for entry in entries:
        try:
            published = datetime(*entry.published_parsed[:6], tzinfo=pytz.utc)
            if published >= day_ago:
                filtered.append(entry)
        except:
            continue
    return filtered

# Tombol pencarian berita
if st.button("Cari Berita SG Election Hari Ini", key="button_cari_berita"):
    with st.spinner("🔍 Mencari berita terbaru..."):
        feed1 = google_news_rss(query_1)
        feed2 = google_news_rss(query_2)

        all_entries = feed1.entries + feed2.entries
        filtered_entries = filter_sources(all_entries)
        recent_entries = filter_24_hours(filtered_entries)

    if recent_entries:
        st.success(f"Ditemukan {len(recent_entries)} berita dari 24 jam terakhir.")
        for entry in recent_entries:
            st.markdown(f"### [{entry.title}]({entry.link})")
            st.caption(f"📰 {entry.source.title} | 🕒 {entry.published}")
    else:
        st.warning("Tidak ditemukan berita dari media yang disetujui dalam 24 jam terakhir.")
