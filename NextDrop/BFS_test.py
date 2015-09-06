import urllib2
import urlparse
import re
from flask import Flask, render_template, request

app = Flask(__name__)

def crawling_bfs(depth_url, http_list):
    ''' parse the graph, get all links until level 2 deep '''
    depth_url -= 1
    if depth_url > 0:
        for links in http_list:
            visited_links.append(links)
            unfiltered_list = pattern_links.findall(get_source_code(links))
        http_list.extend(item for item in unfiltered_list if not item.startswith(('#', '/'))) #remove useless links
        crawling_bfs(depth_url,list(set(http_list) - set(visited_links)))   #remove duplicates
    return visited_links

def get_source_code( url):
    ''' returns source code of the page to be parsed '''
    try:
        if url.startswith(('http', 'https')):   #if link is valid
            response = urllib2.urlopen(url)
            page_source = response.read()
            return page_source
    except (ValueError, urllib2.URLError) as e:
        return "error"

def showimages( images_linklist):
    '''parse the links & pick all images & shows'''
    new_img = []
    for links in images_linklist:
        parsed_url = urlparse.urlparse(links)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)  #get domain name for images starting with '/'
        images = pattern_img.findall(get_source_code(links))
        new_img.extend(['<img src="' + urlparse.urljoin(domain, tmp) + '">' if not tmp.startswith('http')
                        else '<img src="' + tmp + '">' for tmp in images])  #concatenate img tag to url's for webpage
    return ''.join(new_img)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/show_img', methods=['POST'])
def get_user():
    _url=(request.form['input_url']).encode('ascii')    #convert unicode to string
    if _url.startswith(('http://','https://')):     #otherwise invalid url
        return showimages(crawling_bfs(depth_url,[_url]))

if __name__ == '__main__':
    http_list = []  # have to get from user
    visited_links = []  #unique & visited
    depth_url = 2  # depth level
    pattern_img = re.compile('<img [^>]*src="([^"]+)', re.IGNORECASE)   #need be improved
    pattern_links = re.compile('<a href="(.*?)"', re.IGNORECASE)
    app.run(debug=True)
