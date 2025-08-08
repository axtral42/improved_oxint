import streamlit as st

import Google
import Social_media_analyzer as sma

st.title("OXINT SearchApp")
# Styling
st.markdown(
    """
<style>
.main {
    background-color: #00000;
}
</style>
""",
    unsafe_allow_html=True,
)
# Sidebar for additional options or information
with st.sidebar:
    st.info(
        "This app uses the Osint automation to cyberprofile targets and help investigations."
    )
# Main content
col1, col2 = st.columns(2)
with col1:
    question = st.text_input("Enter your question here")
try:
    if "name" in question:
        name = question.strip().replace("name:", "").strip()
        keyword = ""
        print(name)
        if "keyword:" in question:
            phrases = name.strip().split("keyword:")
            print(phrases)
            keyword = phrases[1].strip()
            name = phrases[0].strip()
            print(name, keyword)
            print("successfully captured")
        with st.spinner("Finding..."):
            print("Function called")
            dorks = Google.Dork(
                name, keyword, False
            )  # Assuming Google and sma are defined elsewhere
            # print("Dork done")
            # print(dorks)
            sm_profiles, sm_posts = sma.classify(dorks[0])
            # print(sm_profiles)
            activity = dorks[2]
            documents = dorks[3]
            final = []

            # Social media profiles
            final.append("### 📱 Social Media Profiles")
            for platform, links in sm_profiles.items():
                final.append(f"#### {platform.capitalize()}")
                final.extend([f"- {link}" for link in links])

            # Social media activity
            final.append("\n### 📰 Social Media Activity")
            final.extend([f"- {post}" for post in sm_posts])

            # Related digital footprint
            final.append("\n### 🌐 Related Digital Footprint")
            final.extend([f"- {link}" for link in activity])

            # Related documents
            final.append("\n### 📄 Related Documents")
            final.extend([f"- {doc}" for doc in documents])

            # Join with proper newlines
            final_md = "\n".join(final)

            st.success("Done!")
        st.markdown(final_md)

    else:
        st.warning("Please enter a question to get an answer.")
except:
    st.warning("Error occured, Try again later.")
