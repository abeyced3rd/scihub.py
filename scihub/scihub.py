# -*- coding: utf-8 -*-

"""
Sci-API Unofficial API
[Search|Download] research papers from [scholar.google.com|pismin.com].

@author zaytoun
"""

import re
import argparse
import hashlib
import logging
import os

import requests
import urllib3
from bs4 import BeautifulSoup
from retrying import retry
try:
    from scholarly import scholarly
    SCHOLARLY_AVAILABLE = True
except ImportError:
    SCHOLARLY_AVAILABLE = False

# log config
logging.basicConfig()
logger = logging.getLogger('Sci-Hub')
logger.setLevel(logging.DEBUG)

#
urllib3.disable_warnings()

# constants
SCHOLARS_BASE_URL = 'https://scholar.google.com/scholar'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}

class SciHub(object):
    """
    SciHub class can search for papers on Google Scholars 
    and fetch/download papers from pismin.com
    """

    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers = HEADERS
        self.available_base_url_list = self._get_available_scihub_urls()
        self.base_url = self.available_base_url_list[0] + '/'

    def _get_available_scihub_urls(self):
        '''
        Finds available pismin urls
        '''
        urls = ['https://www.pismin.com']
        return urls

    def search_scholarly(self, query, limit=10):
        """
        Searches for papers on Google Scholar using the scholarly library.
        This is a more reliable alternative to web scraping.
        
        :param query: Search query string
        :param limit: Maximum number of results to return
        :return: Dictionary with 'papers' list or 'err' key if error occurs
        """
        if not SCHOLARLY_AVAILABLE:
            return {'err': 'scholarly library is not installed'}
        
        results = {'papers': []}
        
        try:
            search_query = scholarly.search_pubs(query)
            count = 0
            
            for pub in search_query:
                if count >= limit:
                    break
                
                try:
                    # Extract bibliographic information
                    bib = pub.get('bib', {})
                    title = bib.get('title', 'Unknown Title')
                    
                    # Get URL from pub_url
                    url = pub.get('pub_url', '')
                    
                    paper_data = {
                        'name': title,
                        'url': url,
                    }
                    
                    # Add additional metadata from bib
                    if 'author' in bib:
                        paper_data['authors'] = ', '.join(bib.get('author', []))
                    
                    if 'pub_year' in bib:
                        paper_data['year'] = bib.get('pub_year')
                    
                    if 'venue' in bib and bib.get('venue') != 'NA':
                        paper_data['venue'] = bib.get('venue')
                    
                    if 'abstract' in bib:
                        paper_data['abstract'] = bib.get('abstract')
                    
                    # Add citation count if available
                    if 'num_citations' in pub:
                        paper_data['citations'] = pub.get('num_citations', 0)
                    
                    results['papers'].append(paper_data)
                    count += 1
                except Exception as e:
                    logger.debug(f"Error processing paper: {e}")
                    continue
            
            if not results['papers']:
                results['err'] = f'No papers found for query: {query}'
            
            return results
            
        except Exception as e:
            error_msg = f'Failed to search with scholarly library: {str(e)}'
            logger.error(error_msg)
            return {'err': error_msg}

    def set_proxy(self, proxy):
        '''
        set proxy for session
        :param proxy_dict:
        :return:
        '''
        if proxy:
            self.sess.proxies = {
                "http": proxy,
                "https": proxy, }

    def _change_base_url(self):
        if not self.available_base_url_list:
            raise Exception('Ran out of valid pismin urls')
        # For pismin.com, there's only one URL, so reset it instead of deleting
        self.base_url = self.available_base_url_list[0] + '/'
        logger.info("I'm changing to {}".format(self.available_base_url_list[0]))

    def search(self, query, limit=10, download=False):
        """
        Performs a query on scholar.google.com, and returns a dictionary
        of results in the form {'papers': ...}. Unfortunately, as of now,
        captchas can potentially prevent searches after a certain limit.
        """
        start = 0
        results = {'papers': []}

        while True:
            try:
                res = self.sess.get(SCHOLARS_BASE_URL, params={'q': query, 'start': start})
            except requests.exceptions.RequestException as e:
                results['err'] = 'Failed to complete search with query %s (connection error)' % query
                return results

            s = self._get_soup(res.content)
            papers = s.find_all('div', class_="gs_r")

            if not papers:
                if 'CAPTCHA' in str(res.content):
                    results['err'] = 'Failed to complete search with query %s (captcha)' % query
                return results

            for paper in papers:
                if not paper.find('table'):
                    source = None
                    pdf = paper.find('div', class_='gs_ggs gs_fl')
                    link = paper.find('h3', class_='gs_rt')

                    if pdf:
                        source = pdf.find('a')['href']
                    elif link.find('a'):
                        source = link.find('a')['href']
                    else:
                        continue

                    results['papers'].append({
                        'name': link.text,
                        'url': source
                    })

                    if len(results['papers']) >= limit:
                        return results

            start += 10

    @retry(wait_random_min=100, wait_random_max=1000, stop_max_attempt_number=10)
    def download(self, identifier, destination='', path=None):
        """
        Downloads a paper from sci-hub given an indentifier (DOI, PMID, URL).
        Currently, this can potentially be blocked by a captcha if a certain
        limit has been reached.
        """
        data = self.fetch(identifier)

        if not 'err' in data:
            self._save(data['pdf'],
                       os.path.join(destination, path if path else data['name']))

        return data

    def fetch(self, identifier):
        """
        Fetches the paper by constructing the pismin URL.
        If the indentifier is a DOI, PMID, or URL pay-wall, then use Pismin
        to access and download paper. Otherwise, just download paper directly.
        """

        url = None
        try:
            url = self._get_direct_url(identifier)

            res = self.sess.get(url, verify=False)

            if res.headers['Content-Type'] != 'application/pdf':
                self._change_base_url()
                error_msg = 'Failed to fetch pdf with identifier %s (resolved url %s) due to captcha' % (identifier, url)
                logger.info(error_msg)
                return {
                    'err': error_msg
                }
            else:
                return {
                    'pdf': res.content,
                    'url': url,
                    'name': self._generate_name(res)
                }

        except requests.exceptions.ConnectionError:
            logger.info('Cannot access {}, changing url'.format(self.available_base_url_list[0]))
            self._change_base_url()
            return {
                'err': 'Connection error while fetching paper with identifier %s' % identifier
            }

        except requests.exceptions.RequestException as e:
            error_msg = 'Failed to fetch pdf with identifier %s' % identifier
            if url:
                error_msg += ' (resolved url %s)' % url
            error_msg += ' due to request exception.'
            logger.info(error_msg)
            return {
                'err': error_msg
            }

        except Exception as e:
            error_msg = 'Failed to fetch pdf with identifier %s' % identifier
            if url:
                error_msg += ' (resolved url %s)' % url
            error_msg += ' due to error: %s' % str(e)
            logger.info(error_msg)
            return {
                'err': error_msg
            }
    def _get_direct_url(self, identifier):
        """
        Finds the direct source url for a given identifier.
        """
        id_type = self._classify(identifier)

        return identifier if id_type == 'url-direct' \
            else self._search_direct_url(identifier)

    def _search_direct_url(self, identifier):
        """
        Pismin website access. This function finds the actual PDF URL from pismin.com.
        """
        # For DOI URLs, extract just the DOI part (e.g., 10.1155/2020/8873655)
        if identifier.startswith('http'):
            # Extract DOI from URL if it contains one
            if 'doi.org/' in identifier:
                identifier = identifier.split('doi.org/')[-1]
        
        # First, fetch the pismin page to get the PDF URL
        pismin_url = self.base_url + identifier
        res = self.sess.get(pismin_url, verify=False)
        s = self._get_soup(res.content)
        
        # Look for PDF URL in the page
        pdf_urls = re.findall(r'https?://[^"\s]+\.pdf[^"\s]*', str(s))
        if pdf_urls:
            # Get the first PDF URL
            pdf_url = pdf_urls[0]
            # Unescape any HTML entities
            pdf_url = pdf_url.replace('\\/', '/')
            return pdf_url
        
        # Fallback: return the original URL if no PDF URL found
        return pismin_url

    def _classify(self, identifier):
        """
        Classify the type of identifier:
        url-direct - openly accessible paper
        url-non-direct - pay-walled paper
        pmid - PubMed ID
        doi - digital object identifier
        """
        if (identifier.startswith('http') or identifier.startswith('https')):
            if identifier.endswith('pdf'):
                return 'url-direct'
            else:
                return 'url-non-direct'
        elif identifier.isdigit():
            return 'pmid'
        else:
            return 'doi'

    def _save(self, data, path):
        """
        Save a file give data and a path.
        """
        with open(path, 'wb') as f:
            f.write(data)

    def _get_soup(self, html):
        """
        Return html soup.
        """
        return BeautifulSoup(html, 'html.parser')

    def _generate_name(self, res):
        """
        Generate unique filename for paper. Returns a name by calcuating 
        md5 hash of file contents, then appending the last 20 characters
        of the url which typically provides a good paper identifier.
        """
        name = res.url.split('/')[-1]
        name = re.sub('#view=(.+)', '', name)
        pdf_hash = hashlib.md5(res.content).hexdigest()
        return '%s-%s' % (pdf_hash, name[-20:])

class CaptchaNeedException(Exception):
    pass

def main():
    sh = SciHub()

    parser = argparse.ArgumentParser(description='SciHub - To remove all barriers in the way of science.')
    parser.add_argument('-d', '--download', metavar='(DOI|PMID|URL)', help='tries to find and download the paper',
                        type=str)
    parser.add_argument('-f', '--file', metavar='path', help='pass file with list of identifiers and download each',
                        type=str)
    parser.add_argument('-s', '--search', metavar='query', help='search Google Scholars', type=str)
    parser.add_argument('-sd', '--search_download', metavar='query',
                        help='search Google Scholars and download if possible', type=str)
    parser.add_argument('-l', '--limit', metavar='N', help='the number of search results to limit to', default=10,
                        type=int)
    parser.add_argument('-o', '--output', metavar='path', help='directory to store papers', default='', type=str)
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-p', '--proxy', help='via proxy format like socks5://user:pass@host:port', action='store', type=str)

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
    if args.proxy:
        sh.set_proxy(args.proxy)

    if args.download:
        result = sh.download(args.download, args.output)
        if 'err' in result:
            logger.debug('%s', result['err'])
        else:
            logger.debug('Successfully downloaded file with identifier %s', args.download)
    elif args.search:
        results = sh.search(args.search, args.limit)
        if 'err' in results:
            logger.debug('%s', results['err'])
        else:
            logger.debug('Successfully completed search with query %s', args.search)
        print(results)
    elif args.search_download:
        results = sh.search(args.search_download, args.limit)
        if 'err' in results:
            logger.debug('%s', results['err'])
        else:
            logger.debug('Successfully completed search with query %s', args.search_download)
            for paper in results['papers']:
                result = sh.download(paper['url'], args.output)
                if 'err' in result:
                    logger.debug('%s', result['err'])
                else:
                    logger.debug('Successfully downloaded file with identifier %s', paper['url'])
    elif args.file:
        with open(args.file, 'r') as f:
            identifiers = f.read().splitlines()
            for identifier in identifiers:
                result = sh.download(identifier, args.output)
                if 'err' in result:
                    logger.debug('%s', result['err'])
                else:
                    logger.debug('Successfully downloaded file with identifier %s', identifier)


if __name__ == '__main__':
    main()
