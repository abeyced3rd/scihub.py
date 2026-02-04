#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run the SciHub Web Application
"""

import sys
import os

# Add parent directory to path to import scihub
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║          SciHub Web Application                             ║
    ║                                                              ║
    ║  🌐 Web App: http://localhost:5000                          ║
    ║  📚 Search and download research papers easily              ║
    ║                                                              ║
    ║  Press Ctrl+C to stop the server                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=False, host='0.0.0.0', port=5000)
