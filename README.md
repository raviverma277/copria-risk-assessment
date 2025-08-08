# 🏢 CoPRIA - Commercial Property Risk Intelligence Assistant

A Streamlit application that analyzes commercial property submissions and generates risk profiles with red flag identification.

## 🚀 Features

- **PDF Text Extraction**: Extract and analyze property information from PDF submissions
- **JSON Processing**: Handle structured property data from JSON files
- **LLM-Powered Analysis**: Use OpenAI GPT to intelligently extract risk-related information
- **Red Flag Detection**: Automatically identify potential risk factors
- **Enhanced UI**: Color-coded risk indicators and comprehensive summaries

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Required packages (see requirements.txt)

## 🛠️ Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## 🚀 Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Ensure these files are in your repository**:
   - `app.py` (main Streamlit app)
   - `requirements.txt` (dependencies)
   - `.streamlit/config.toml` (configuration)
   - `utils/` folder (all utility modules)
   - `data/` folder (sample data files)

### Step 2: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with your GitHub account**
3. **Click "New app"**
4. **Configure your app**:
   - **Repository**: Select your GitHub repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
   - **App URL**: Choose a unique URL for your app

### Step 3: Set Environment Variables

1. **In your Streamlit Cloud dashboard**, go to your app settings
2. **Add your OpenAI API key**:
   - Variable name: `OPENAI_API_KEY`
   - Variable value: Your actual OpenAI API key

### Step 4: Deploy

1. **Click "Deploy"**
2. **Wait for deployment to complete**
3. **Your app will be available at**: `https://your-app-name.streamlit.app`

## 📁 Project Structure

```
copria_streamlit_app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml      # Streamlit configuration
├── utils/
│   ├── llm_extractor.py # OpenAI integration
│   ├── pdf_reader.py    # PDF text extraction
│   ├── risk_mapper.py   # Risk profile generation
│   └── red_flag_engine.py # Red flag detection
├── data/
│   ├── sample_submission.pdf
│   ├── usa_property_submissions.json
│   ├── mvp_risk_profile_schema.json
│   └── red_flag_rules.json
└── output/              # Generated risk profiles
```

## 🔧 Usage

### For PDF Submissions:
1. Upload a PDF file containing property information
2. Upload the schema and red flag rules JSON files
3. Click "Generate" to analyze the property
4. View the risk profile summary with highlighted red flags

### For JSON Submissions:
1. Upload a JSON file with property data
2. Upload the schema and red flag rules JSON files
3. Click "Generate" to analyze multiple properties
4. View the comprehensive assessment summary

## 🎯 Key Features

- **Intelligent Text Extraction**: Uses OpenAI GPT to extract structured data from unstructured text
- **Risk Flag Detection**: Automatically identifies potential risk factors
- **Color-Coded Indicators**: Visual risk assessment with red/green indicators
- **Comprehensive Summaries**: Detailed property information and risk breakdowns
- **Multi-Property Analysis**: Handle multiple properties in a single assessment

## 🔒 Security Notes

- Your OpenAI API key is stored securely in Streamlit Cloud environment variables
- No sensitive data is logged or stored permanently
- All processing is done in memory

## 📞 Support

For issues or questions, please check the Streamlit Cloud logs or contact the development team.

---

**Built with ❤️ using Streamlit and OpenAI**
