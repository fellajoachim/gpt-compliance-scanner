import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import openai
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="GPT Compliance Scanner", page_icon="🛡️", layout="wide")
st.title("🛡️ GPT-Powered Multi-Page Compliance Scanner")
st.caption("Created by Joachim")

MAX_PAGES = 6

def fetch_html(url):
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.text
    except Exception:
        return None

    def get_internal_links(base_url, html):
    soup = BeautifulSoup(html, "html.parser")
    domain = urlparse(base_url).netloc
    links = set()
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        full_url = urljoin(base_url, href)
        if domain in urlparse(full_url).netloc:
            links.add(full_url.split("#")[0])
    return list(links)

    def extract_sections(html):
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.find_all("section")
    if not sections:
        sections = soup.find_all("div")
    parsed = []
    for i, sec in enumerate(sections):
        text = sec.get_text(separator=" ", strip=True)
        if len(text) > 50:
            parsed.append((f"Section {i+1}", text[:1500]))
    return parsed

    def analyze_with_gpt(text):
    prompt = f"""
    You are a telehealth compliance officer.

    Evaluate the following web copy for violations of:
    - HIPAA privacy rules
    - FDA compounding restrictions
    - LegitScript advertising standards
    - FTC guidance on health claims

    Text:
    """
    {text}
    """

    Provide:
    1. ⚠️ Risks or violations
    2. 📘 Why it's non-compliant (include rule reference)
    3. ✅ Suggestions to fix it (rewrite if possible)
    4. Score (0-10)
    """
    try:
            response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ GPT error: {str(e)}"

    url = st.text_input("🌐 Enter your website homepage URL")

    if url:
    st.info("Crawling website and scanning content...")
    home_html = fetch_html(url)
    if home_html:
        links = get_internal_links(url, home_html)[:MAX_PAGES]
        pages = [(url, home_html)]
        for link in links:
            if link != url:
                html = fetch_html(link)
                if html:
                    pages.append((link, html))

        total_score = 0
        total_sections = 0

        for page_url, page_html in pages:
            st.markdown(f"## 📄 Scanning: {page_url}")
            sections = extract_sections(page_html)
            for label, text in sections:
                with st.expander(f"🔍 {label}"):
                    result = analyze_with_gpt(text)
                    st.markdown(result)
                    score_match = next((int(s) for s in result.split() if s.isdigit() and 0 <= int(s) <= 10), 5)
                    total_score += score_match
                    total_sections += 1

        if total_sections > 0:
            avg_score = round(total_score / total_sections, 2)
            st.success(f"📊 Final Average Compliance Score: **{avg_score}/10**")

            if avg_score < 7:
                st.warning("⚠️ Your site has serious compliance risks that may prevent LegitScript certification.")
            elif avg_score < 9:
                st.info("ℹ️ Your site is moderately compliant, but improvements are recommended.")
            else:
                st.success("✅ Your site is highly compliant.")

        st.markdown("---")
        st.caption("📄 PDF report export coming soon in the next build.")
    else:
        st.error("❌ Failed to load homepage. Check the URL.")
