# -*- coding: utf-8 -*-

"""
SciHub Web Application - GUI for searching and downloading research papers
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import logging
from scihub import SciHub
import config
import json
from urllib.parse import urlencode
import requests as _requests

app = Flask(__name__)
app.config.from_object(config)

# Ensure downloads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global SciHub instance
sh = SciHub()

# Store download progress
download_progress = {}

# settings persistence
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.json')
default_settings = {
    'proxy': None,
    'serpapi_key': None
}


def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                s = json.load(f)
                return {**default_settings, **s}
    except Exception:
        pass
    return default_settings.copy()


def save_settings(s):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(s, f)
    except Exception:
        pass


# load and apply settings on startup
_settings = load_settings()
if _settings.get('proxy'):
    sh.set_proxy(_settings.get('proxy'))



@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search():
    """Search for papers on Google Scholars"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        limit = int(data.get('limit', config.DEFAULT_SEARCH_RESULTS))
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        if limit > config.MAX_SEARCH_RESULTS:
            limit = config.MAX_SEARCH_RESULTS  # Cap at max results
        
        logger.info(f"Searching for: {query} (limit: {limit})")

        # If SerpAPI key is configured, use SerpAPI for Google Scholar results
        serpapi_key = _settings.get('serpapi_key')
        if serpapi_key:
            try:
                params = {
                    'engine': 'google_scholar',
                    'q': query,
                    'hl': 'en',
                    'api_key': serpapi_key,
                    'num': limit
                }
                url = 'https://serpapi.com/search.json?' + urlencode(params)
                r = _requests.get(url, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    papers = []
                    for item in data.get('organic_results', [])[:limit]:
                        papers.append({'name': item.get('title'), 'url': item.get('link')})
                    return jsonify({'success': True, 'papers': papers, 'count': len(papers)})
                else:
                    logger.info('SerpAPI search failed with status %s', r.status_code)
            except Exception as e:
                logger.exception('SerpAPI search exception: %s', e)

        results = sh.search(query, limit=limit)
        
        if 'err' in results:
            # Provide a clearer message for CAPTCHA situations and suggest using a proxy
            err = results['err']
            if 'captcha' in err.lower():
                return jsonify({'error': 'Search blocked by Google Scholar CAPTCHA. Try again later or set a proxy via Settings.'}), 429
            return jsonify({'error': err}), 400
        
        return jsonify({
            'success': True,
            'papers': results.get('papers', []),
            'count': len(results.get('papers', []))
        })
    
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/download', methods=['POST'])
def download():
    """Download a paper"""
    try:
        data = request.get_json()
        identifier = data.get('identifier', '')
        custom_name = data.get('name', '')
        
        if not identifier:
            return jsonify({'error': 'Identifier is required'}), 400
        
        logger.info(f"Downloading: {identifier}")
        result = sh.download(identifier, destination=app.config['UPLOAD_FOLDER'], path=custom_name)
        
        if 'err' in result:
            return jsonify({'error': result['err']}), 400
        
        return jsonify({
            'success': True,
            'message': f"Downloaded successfully: {result['name']}",
            'filename': result['name']
        })
    
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/fetch', methods=['POST'])
def fetch():
    """Fetch paper metadata without saving to disk"""
    try:
        data = request.get_json()
        identifier = data.get('identifier', '')
        
        if not identifier:
            return jsonify({'error': 'Identifier is required'}), 400
        
        logger.info(f"Fetching: {identifier}")
        result = sh.fetch(identifier)
        
        if 'err' in result:
            return jsonify({'error': result['err']}), 400
        
        return jsonify({
            'success': True,
            'url': result['url'],
            'name': result['name']
        })
    
    except Exception as e:
        logger.error(f"Fetch error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/set_proxy', methods=['POST'])
def set_proxy():
    """Set proxy for SciHub instance"""
    try:
        data = request.get_json()
        proxy = data.get('proxy', '')

        if not proxy:
            # clear proxy
            sh.set_proxy(None)
            _settings['proxy'] = None
            save_settings(_settings)
            return jsonify({'success': True, 'message': 'Proxy cleared'})

        sh.set_proxy(proxy)
        _settings['proxy'] = proxy
        save_settings(_settings)
        return jsonify({'success': True, 'message': f'Proxy set to {proxy}'})

    except Exception as e:
        logger.error(f"Set proxy error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/set_serpapi', methods=['POST'])
def set_serpapi():
    """Set or clear SerpAPI key"""
    try:
        data = request.get_json()
        key = data.get('key', '')

        if not key:
            _settings['serpapi_key'] = None
            save_settings(_settings)
            return jsonify({'success': True, 'message': 'SerpAPI key cleared'})

        _settings['serpapi_key'] = key
        save_settings(_settings)
        return jsonify({'success': True, 'message': 'SerpAPI key saved'})

    except Exception as e:
        logger.error(f"Set SerpAPI error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/downloads', methods=['GET'])
def list_downloads():
    """List all downloaded papers"""
    try:
        files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath) and filename.endswith('.pdf'):
                files.append({
                    'name': filename,
                    'size': os.path.getsize(filepath),
                    'path': filepath
                })
        
        return jsonify({
            'success': True,
            'files': files,
            'count': len(files)
        })
    
    except Exception as e:
        logger.error(f"List downloads error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download a file from the downloads folder"""
    try:
        filename = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True)
    
    except Exception as e:
        logger.error(f"File download error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
