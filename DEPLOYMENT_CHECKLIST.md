# 🚀 Streamlit Cloud Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. **GitHub Repository Setup**
- [ ] Push all code to GitHub repository
- [ ] Ensure all files are committed:
  - `app.py`
  - `requirements.txt`
  - `.streamlit/config.toml`
  - `utils/` folder (all Python files)
  - `data/` folder (sample files)
  - `README.md`

### 2. **Required Files Verification**
- [ ] `app.py` - Main Streamlit application
- [ ] `requirements.txt` - All dependencies listed
- [ ] `.streamlit/config.toml` - Streamlit configuration
- [ ] `utils/llm_extractor.py` - OpenAI integration
- [ ] `utils/pdf_reader.py` - PDF processing
- [ ] `utils/risk_mapper.py` - Risk profile generation
- [ ] `utils/red_flag_engine.py` - Red flag detection
- [ ] `data/` folder with sample files

### 3. **OpenAI API Key**
- [ ] Get your OpenAI API key from [platform.openai.com](https://platform.openai.com)
- [ ] Keep it ready for Streamlit Cloud environment variable

## 🚀 Deployment Steps

### Step 1: Streamlit Cloud Setup
1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**

### Step 2: App Configuration
- **Repository**: Select your GitHub repository
- **Branch**: `main` (or your default branch)
- **Main file path**: `app.py`
- **App URL**: Choose a unique name (e.g., `copria-risk-assessment`)

### Step 3: Environment Variables
1. **In your app settings**, add environment variable:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your actual OpenAI API key

### Step 4: Deploy
1. **Click "Deploy"**
2. **Wait for deployment** (usually 2-5 minutes)
3. **Check deployment logs** for any errors

## 🔧 Post-Deployment Testing

### Test 1: PDF Submission
1. Upload `data/sample_submission.pdf`
2. Upload `data/mvp_risk_profile_schema.json`
3. Upload `data/red_flag_rules.json`
4. Click "Generate"
5. Verify red flags are displayed correctly

### Test 2: JSON Submission
1. Upload `data/usa_property_submissions.json`
2. Upload schema and rules files
3. Click "Generate"
4. Verify multi-property assessment works

### Test 3: Text Input
1. Paste sample text
2. Upload schema and rules files
3. Click "Generate"
4. Verify text processing works

## 🐛 Troubleshooting

### Common Issues:
1. **"Module not found" errors**: Check `requirements.txt` includes all dependencies
2. **OpenAI API errors**: Verify API key is set correctly in environment variables
3. **File upload errors**: Ensure sample files are in the `data/` folder
4. **Deployment fails**: Check Streamlit Cloud logs for specific error messages

### Debug Steps:
1. **Check deployment logs** in Streamlit Cloud dashboard
2. **Verify environment variables** are set correctly
3. **Test locally first** to ensure app works
4. **Check file paths** are correct in the repository

## 📞 Support

- **Streamlit Cloud Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
- **Streamlit Community**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: Create issues in your repository

## 🎉 Success Indicators

✅ **App deploys without errors**
✅ **All file uploads work**
✅ **Risk profiles generate correctly**
✅ **Red flags display properly**
✅ **UI shows color-coded indicators**
✅ **Multi-property assessment works**

---

**Your app will be available at**: `https://your-app-name.streamlit.app`
