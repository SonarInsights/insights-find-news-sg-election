import streamlit as st
import feedparser
import urllib.parse
import pandas as pd
from datetime import datetime, timedelta
import pytz
import re

st.title("🗳️ SG Election News Tracker")

# Subtext kecil
st.markdown(
    "<p style='font-size: 14px; color: gray;'>by <strong>Insights Sonar</strong> (for internal use only)<br>If you encounter any issues, please contact: <a href='mailto:katon.prasetyo@sonar.id'>katon.prasetyo@sonar.id</a></p>",
    unsafe_allow_html=True
)

# Pilih Mode
mode = st.radio(
    "Pilih Mode Pencarian Berita:",
    ("Tight Mode (Politik & Pemilu)", "Wide Mode (Plus Ekonomi, Perdagangan, dll)", "All News (Semua tentang Singapura)"),
    key="mode_selection"
)

# Query berdasarkan Mode
if mode == "Tight Mode (Politik & Pemilu)":
    query = """
    ("Singapura" OR "Singapore" OR "Singapur" OR "Singapor")
    AND
    ("bilateral" OR "kerjasama" OR "Pemilu" OR "Pemilihan Umum" OR "Election" OR "Parlemen" OR "Politics" OR "Political" OR "Pemungutan Suara" OR "Voting" OR "Vote" OR "#SGGE" OR "#GE2025" OR "#SingaporeElections" OR "#VoteSG" OR "#SGPolitics" OR "People Action Party" OR "Workers Party" OR "Progress Party" OR "Democratic Party" OR "Reform Party" OR "National Solidarity Party" OR "Red Dot United" OR "Lee Hsien Loong" OR "Tharman Shanmugaratnam" OR "Lawrence Wong" OR "Pritam Singh" OR "Jamus Lim" OR "Tan Cheng Bock" OR "Chee Soon Juan" OR "Sylvia Lim")
    """
elif mode == "Wide Mode (Plus Ekonomi, Perdagangan, dll)":
    query = """
    ("Singapura" OR "Singapore" OR "Singapur" OR "Singapor")
    AND
    ("bilateral" OR "kerjasama" OR "perdagangan" OR "trade" OR "ekonomi" OR "economy" OR "politik" OR "politics" OR "perang" OR "war" OR "Election" OR "Pemilu" OR "Pemilihan Umum" OR "pemilu di Singapura" OR "election in Singapore" OR "hubungan Indonesia Singapura" OR "relationship Indonesia Singapore" OR "kerjasama Indonesia Singapura" OR "bilateral Indonesia Singapore" OR "Parlemen" OR "Political" OR "Pemungutan Suara" OR "Voting" OR "Vote" OR "#SGGE" OR "#GE2025" OR "#SingaporeElections" OR "#VoteSG" OR "#SGPolitics" OR "People Action Party" OR "Workers Party" OR "Progress Party" OR "Democratic Party" OR "Reform Party" OR "National Solidarity Party" OR "Red Dot United" OR "Lee Hsien Loong" OR "Tharman Shanmugaratnam" OR "Lawrence Wong" OR "Pritam Singh" OR "Jamus Lim" OR "Tan Cheng Bock" OR "Chee Soon Juan" OR "Sylvia Lim")
    """
else:  # Mode All News
    query = """
    ("Singapura" OR "Singapore" OR "Singapur" OR "Singapor")
    """

# Allowed Media Sources (semua huruf kecil dan minimalisasi variasi nama)
allowed_sources = [
    "jakarta post", "jakartapost", "jakartapost",
    "jakarta globe", "jakartaglobe", "jakartaglobe",
    "detik", "detikcom", "detik.com",
    "liputan6", "liputan 6",
    "cnn indonesia", "cnnindonesia", "cnnindonesia.com",
    "tvone", "tv one", "tvonenews", "tvonenews.com",
    "republika", "republika.co.id",
    "kompas tv", "kompastv", "kompastv.com",
    "sindo news", "sindonews", "sindonews.com",
    "bisnis indonesia", "bisnisindonesia", "bisnis.com",
    "tempo", "tempo.co",
    "investor daily", "investordaily", "investordaily.com",
    "kompas", "kompas.com",
    "kontan", "kontan.co.id",
    "metrotv", "metro tv", "metrotvnews", "metrotvnews.com",
    "antara", "antara news", "antaranews", "antaranews.com",
    "kumparan", "kumparan.com",
    "idn times", "idntimes", "idntimes.com",
    "batampos", "batam pos", "batampos.co.id",
    "cnbc indonesia", "cnbcindonesia", "cnbcindonesia.com",
    "media indonesia", "mediaindonesia", "mediaindonesia.com",
    "tirto", "tirto.id",
    "voi", "voi.id"
]

# Fungsi normalisasi nama media
def normalize(text):
    text = text.lower()
    text = re.sub(r'[\s\.\-]', '', text)  # Hapus spasi, titik, minus
    return text

# Function ambil RSS dari Google News
def google_news_rss(query):
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=id&gl=ID&ceid=ID:id"
    return feedparser.parse(url)

# Function Filter Source pakai normalisasi
def filter_sources(entries):
    return [
        entry for entry in entries
        if 'source' in entry and normalize(entry.source.title) in allowed_sources
    ]

# Filter berita 24 jam terakhir
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

# Tombol Cari Berita
if st.button("Cari Berita SG Election Hari Ini", key="button_cari_berita"):
    with st.spinner("🔍 Mencari berita terbaru..."):
        feed = google_news_rss(query)
        all_entries = feed.entries

        # Khusus All News, kita bisa skip filter media kalau mau (opsional)
        if mode == "All News (Semua tentang Singapura)":
            filtered_entries = all_entries  # Tidak filter media
        else:
            filtered_entries = filter_sources(all_entries)

        recent_entries = filter_24_hours(filtered_entries)

    if recent_entries:
        st.success(f"Ditemukan {len(recent_entries)} berita dari 24 jam terakhir.")
        for entry in recent_entries:
            source_name = entry.source.title if 'source' in entry else 'Unknown Source'
            st.markdown(f"### [{entry.title}]({entry.link})")
            st.caption(f"📰 {source_name} | 🕒 {entry.published}")
    else:
        st.warning("Tidak ditemukan berita dari media yang disetujui dalam 24 jam terakhir.")
