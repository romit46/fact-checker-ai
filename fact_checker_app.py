import streamlit as st
import requests

st.set_page_config(page_title="Fact Checker AI", layout="centered")

st.markdown("""
<style>
.check-button {
    background-color: #ff4b4b;
    color: black;
    border-radius: 8px;
    padding: 8px;
    font-weight: bold;
}
.check-button:hover {
    background-color: #ff7777;
}
.result {
    margin-top: 20px;
    padding: 12px;
    border-radius: 10px;
    animation: fadeIn 0.8s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Fact Checker AI")
st.subheader("Check if a news or claim is real or fake using verified sources")
st.markdown("👉 Paste a **news headline or claim** and click **Check Fact**")


query = st.text_area("Paste News/Claim", placeholder="e.g., Drinking hot water cures COVID-19", height=150)

if st.button("Check Fact", help="Verified via Google Fact Check", type="primary"):
    if not query.strip():
        st.warning("Please enter a news or claim.")
    else:
        with st.spinner("Checking real-world sources..."):
            try:
                # Google API request
                API_KEY = st.secrets["api"]["google_fact_key"]
                endpoint = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
                params = {
                    "key": API_KEY,
                    "query": query,
                    "languageCode": "en-US"
                }
                response = requests.get(endpoint, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    if "claims" in data:
                        for claim in data["claims"]:
                            claim_text = claim.get("text", "")
                            claim_rating = claim.get("claimReview", [{}])[0].get("textualRating", "No rating")
                            publisher = claim.get("claimReview", [{}])[0].get("publisher", {}).get("name", "")
                            url = claim.get("claimReview", [{}])[0].get("url", "")

                            st.markdown(f"""
                            <div class="result" style="background-color:#e0f7fa;color:black;">
                            🔍 **Claim:** {claim_text}  
                            ✅ **Verdict:** {claim_rating}  
                            📰 **Source:** {publisher}  
                            🔗 [Read more]({url})
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No verified fact-check found for this claim.")
                else:
                    st.error("API error. Check your key or quota.")
            except Exception as e:
                st.error(f"Failed to fetch facts: {e}")
