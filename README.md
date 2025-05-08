# GPT-Powered Compliance Scanner

This tool scans a telehealth website for compliance risks using GPT-4. It checks HIPAA, FDA, FTC, and LegitScript rules with:

✅ Multi-page crawling  
✅ GPT scoring per section  
✅ PDF summary report  
✅ Visual dashboard with charts  
✅ Rule toggles for custom strictness  

---

## 🚀 Deployment Guide (GitHub + Streamlit Cloud)

1. Go to [https://github.com/new](https://github.com/new)
2. Create a public repo (e.g., `gpt-compliance-scanner`)
3. Upload all files from this folder

4. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
5. Click **New App** → Connect GitHub → Select your repo
6. Choose `main` branch and `app.py` as entry point
7. Click **Deploy**

8. In the deployed app, go to **Settings > Secrets** and add:

```
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxx"
```

Done! The app will now crawl websites, scan content, show charts, and generate a compliance report.

---

Made with 🧠 by Joachim
