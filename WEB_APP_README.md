# SciHub Web Application

A modern, user-friendly web interface for the SciHub Python application. Search and download research papers without using the command line!

## Features

✨ **Search Research Papers** - Search Google Scholar directly from the web interface  
📥 **Download Papers** - Download papers by DOI, PMID, or URL  
🔗 **Batch Downloads** - Download multiple papers at once  
📚 **Download History** - View and manage all your downloaded papers  
🎨 **Modern UI** - Beautiful, responsive interface that works on any device  
⚡ **Fast & Reliable** - Built with Flask and optimized for performance  

## Installation

### Prerequisites

- Python 3.6+
- pip

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python run.py
   ```

3. **Open your browser:**
   ```
   http://localhost:5000
   ```

## Usage

### Search for Papers

1. Go to the **"Search Papers"** section
2. Enter your search query (e.g., "machine learning", "neural networks")
3. Set the number of results you want (1-50)
4. Click **"Search"**
5. View results and download papers directly from search results

### Download a Paper Directly

#### By Identifier:
1. Go to the **"Direct Download"** tab
2. Enter one of the following:
   - **DOI** (Digital Object Identifier): `10.1234/example.doi`
   - **PMID** (PubMed ID): `12345678`
   - **URL**: `https://example.com/paper.pdf`
3. Optionally enter a custom filename
4. Click **"Download"**

#### By Multiple URLs:
1. Switch to the **"By URL"** tab
2. Paste multiple paper URLs (one per line)
3. Click **"Download All"**
4. Papers will be downloaded sequentially

### View & Manage Downloads

1. Scroll to the **"Downloaded Papers"** section
2. See all downloaded papers with file sizes
3. Click **"⬇️ Download"** to download any paper from your browser
4. Click **"🔄 Refresh"** to refresh the download list

## How It Works

The web application provides a REST API that interfaces with the SciHub Python library:

- **Search API** (`POST /api/search`) - Search Google Scholar
- **Download API** (`POST /api/download`) - Download a paper from Sci-Hub
- **Fetch API** (`POST /api/fetch`) - Get metadata for a paper
- **Downloads List API** (`GET /api/downloads`) - List downloaded papers

All papers are stored in the `downloads/` folder in your application directory.

## Project Structure

```
scihub.py/
├── app.py                      # Flask application
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── templates/
│   └── index.html              # Web interface
├── downloads/                  # Downloaded papers (auto-created)
├── scihub/
│   └── scihub.py              # SciHub library
└── README.md                   # This file
```

## API Endpoints

### Search Papers
```
POST /api/search
Content-Type: application/json

{
  "query": "machine learning",
  "limit": 10
}

Response:
{
  "success": true,
  "papers": [
    {
      "name": "Paper Title",
      "url": "https://..."
    }
  ],
  "count": 10
}
```

### Download Paper
```
POST /api/download
Content-Type: application/json

{
  "identifier": "10.1234/doi.or.url",
  "name": "optional_filename.pdf"
}

Response:
{
  "success": true,
  "message": "Downloaded successfully: filename.pdf",
  "filename": "filename.pdf"
}
```

### Fetch Metadata
```
POST /api/fetch
Content-Type: application/json

{
  "identifier": "10.1234/doi.or.url"
}

Response:
{
  "success": true,
  "url": "https://...",
  "name": "filename.pdf"
}
```

### List Downloads
```
GET /api/downloads

Response:
{
  "success": true,
  "files": [
    {
      "name": "filename.pdf",
      "size": 1024000,
      "path": "/path/to/file"
    }
  ],
  "count": 1
}
```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, you can change it:
```bash
python -c "from app import app; app.run(port=5001)"
```

### Connection Issues
- Make sure you have internet access
- Try using a VPN or proxy if Sci-Hub is blocked in your region
- Check your firewall settings

### Search Not Working
- CAPTCHA issues are common with Google Scholar - try again later
- Use fewer search results (lower limit)
- Try searching with fewer/simpler keywords

### Download Failures
- The paper might not be available on Sci-Hub
- Try searching for the paper first to get the correct URL
- Check that you're using a valid identifier (DOI, PMID, or URL)

## Important Notes

⚠️ **Legal Notice**: SciHub provides access to research papers. Please respect copyright laws in your jurisdiction and use this tool responsibly.

📌 **CAPTCHA Issues**: Google Scholar may show CAPTCHAs after multiple searches. This is a known limitation. Wait a while before searching again.

🌐 **SciHub URLs**: The application automatically finds working SciHub mirrors. If downloads fail, it will try alternative mirrors.

## License

This web application is provided as-is, building upon the [scihub.py](https://github.com/zaytoun/scihub.py) project by zaytoun.

## Support

For issues with:
- **The web app**: Check this README and the troubleshooting section
- **The SciHub library**: See the [original repository](https://github.com/zaytoun/scihub.py)

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements!

---

**Happy researching!** 🔬📚
