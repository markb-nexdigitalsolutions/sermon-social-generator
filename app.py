import io
import random
import csv
from datetime import datetime

import streamlit as st

# Optional dependency for .docx parsing
try:
    import docx  # python-docx
    HAS_DOCX = True
except Exception:
    HAS_DOCX = False


# -----------------------------
# Helpers
# -----------------------------
def read_txt(file) -> str:
    return file.read().decode("utf-8", errors="ignore")

def read_docx(file) -> str:
    if not HAS_DOCX:
        return "Unable to read .docx without python-docx installed. Please install it or upload .txt."
    document = docx.Document(file)
    return "\n".join(p.text for p in document.paragraphs)

def extract_key_phrases(text: str):
    """
    Lightweight key-phrase list (mirrors your original template vibe).
    You can connect an NLP pipeline here later.
    """
    phrases = [
        "God's love never fails",
        "Trust in His perfect timing",
        "You are fearfully and wonderfully made",
        "His grace is sufficient for you",
        "Walk by faith, not by sight",
        "God has a plan for your life",
        "His mercies are new every morning",
        "You can do all things through Christ",
    ]
    random.shuffle(phrases)
    return phrases

def create_posts(transcript: str):
    key = extract_key_phrases(transcript)
    templates = [
        f"“{key[0]}” — From today's powerful message ✨ #Faith #Inspiration",
        f"💡 Key insight from Sunday's sermon: {key[1]} What’s God speaking to your heart today?",
        f"🙏 “{key[2]}” — Scripture reminds us of God’s faithfulness!",
        "❓ After hearing today’s message, what’s one thing you’re trusting God with? Share below! 👇",
        "🤔 How has God shown His love in your life this week? Let’s encourage each other! 💕",
        "💭 What part of today’s message resonated most with you? Comment and let’s discuss!",
        "🎯 Ready to take the next step in your faith journey? Join us next Sunday as we continue exploring God’s word!",
        "📖 Missed today’s message? Catch up online and share it with someone who needs to hear it!",
        "💪 This week’s challenge: Apply one truth from today’s sermon in your daily life. You’ve got this!",
        "👥 Our church family is amazing! Thank you to everyone who joined us for worship today!",
        "🏠 Looking for a church home? Come as you are — we’d love to welcome you into our family!",
        "🤝 New here? We’d love to connect with you! Drop a comment or send us a message.",
        "🙌 Grateful for how God moved during today’s service! His presence was so evident.",
        "✨ Testimony time! How has God been working in your life lately? Share your story!",
        "💝 Thankful for a pastor who faithfully shares God’s word with wisdom and love.",
        "📜 Today’s scripture reminds us that God’s promises are true! Claim them today!",
        "🔥 The Word of God is alive and active! Which verse is speaking to your heart right now?",
        f"💎 Hidden gem from today’s message: {key[3]} Save this post to remember!",
        f"🛠️ Practical takeaway from today: {key[4]} How will you apply this?",
        "📝 Three things to remember from today: 1) God is faithful 2) His love never fails 3) You are chosen!",
    ]
    platforms = ["Facebook", "Instagram", "Twitter/X"]
    posts = []
    for i, t in enumerate(templates[:20]):
        posts.append({
            "id": i + 1,
            "platform": platforms[i % len(platforms)],
            "content": t,
            "engagement": random.randint(20, 70),  # playful estimate
        })
    return posts

def posts_to_csv_bytes(posts):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Post Number", "Platform", "Content", "Engagement Potential"])
    for p in posts:
        writer.writerow([p["id"], p["platform"], p["content"], f"{p['engagement']}%"])
    return buffer.getvalue().encode("utf-8")


# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="📖 Sermon Social Generator", page_icon="✨", layout="wide")

st.markdown(
    """
    <div style="padding: 2rem; border-radius: 16px;
         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
         color: white; text-align:center;">
      <h1 style="margin:0;">📖 Sermon Social Generator</h1>
      <p style="margin-top:.5rem; opacity:.95;">Transform your sermon into engaging social content</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

with st.container():
    st.subheader("📝 Upload or Paste Your Sermon Transcript")
    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded = st.file_uploader(
            "Upload a .txt or .docx sermon transcript",
            type=["txt", "docx"],
            help="For best results, upload plain text. .docx requires python-docx."
        )
        transcript_text = ""
        if uploaded is not None:
            if uploaded.name.lower().endswith(".txt"):
                transcript_text = read_txt(uploaded)
            elif uploaded.name.lower().endswith(".docx"):
                transcript_text = read_docx(uploaded)
            st.success(f"Loaded: {uploaded.name}")

    with col2:
        manual = st.text_area(
            "Or paste sermon text here",
            value=transcript_text or "",
            height=220,
            placeholder="Paste your sermon transcript…",
        )

    transcript = manual.strip() if manual else transcript_text.strip()

    generate = st.button("✨ Generate 20 Social Posts", use_container_width=True)

    if generate:
        if not transcript:
            st.error("Please upload or paste your sermon transcript first.")
        else:
            with st.spinner("Generating posts…"):
                posts = create_posts(transcript)

            st.success("Done! Scroll to review your posts.")
            st.write("---")
            st.subheader("🚀 Your Generated Posts")

            # Download CSV
            csv_bytes = posts_to_csv_bytes(posts)
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            st.download_button(
                label="📥 Download All Posts (CSV)",
                data=csv_bytes,
                file_name=f"sermon-social-posts-{ts}.csv",
                mime="text/csv",
                use_container_width=True,
            )

            st.write("")
            # Display cards
            for p in posts:
                with st.container():
                    st.markdown(
                        f"""
                        <div style="background:#fff;border-radius:12px;padding:16px;margin-bottom:10px;box-shadow:0 10px 25px rgba(0,0,0,.06);">
                          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem;">
                            <span style="background:#eef2ff;color:#4338ca;padding:.25rem .6rem;border-radius:999px;font-size:.9rem;">
                              {p['platform']}
                            </span>
                            <span style="color:#6b7280;font-size:.9rem;">Post #{p['id']}</span>
                          </div>
                          <div style="color:#111827; line-height:1.6; margin-bottom:.5rem;">{p['content']}</div>
                          <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="color:#047857;font-weight:600;">📈 {p['engagement']}% engagement potential</span>
                          </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
