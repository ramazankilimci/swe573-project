import requests
import xml.etree.ElementTree as ET

def get_article_ids():
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=post+traumatic+stress+disorder+AND&retmode=json&retmax=10"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    articles = response.json()
    #print(len(articles['esearchresult']['idlist']))
    article_list = []
    for i in range(len(articles['esearchresult']['idlist'])):
        article_list.append(articles['esearchresult']['idlist'][i])
    return article_list


def get_articles_with_details():
    # Get articles from method get_article_ids()
    articles = get_article_ids()
    # Join article id for posting in URL. For instance, '34022747', '34022659', '34020974'.
    articles_id = ','.join(articles)
    print(articles)

    # Create posting url.
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="+articles_id+"&rettype=abstract"
    print(url)
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    # Create xml tree using Element Tree.
    abs_tree = ET.fromstring(response.content)
    #root=abs_tree.tag

    ## New empty list. We will append all information into this list.
    ## articles list will not be used. 
    all_articles = []

    # 'PubmedArticle/MedlineCitation' will find each article.
    # Using each article we will find PMID, Title, Abstract and Authors 
    for title in abs_tree.findall('PubmedArticle/MedlineCitation'):
        # Find ID of article.
        id = title.find('PMID').text

        # Find title of article.
        article_title = title.find('Article/ArticleTitle').text

        # Abstract field can have multiple AbstractText fields. We should get all of them.
        # Create an empty "abstract_all" variable. Iteratively search for AbstractText field and append it.
        abstract_all = ""
        for abstract in title.findall('Article/Abstract/AbstractText'):
            abstract_all += str(abstract.text)

        # AuthorList field can have multiple Author fields. Create an empty "author_list" variable.
        # Iteratively search for Author fields and append it to "author_list".
        # LastName and Forename are different fields. Merge them and put ";" between authors.
        # Remove ";" at the end of "author_list" using strip(';') function.
        author_list = ""
        for author in title.findall('Article/AuthorList/Author'):
            author_name = author.find('LastName').text + " " + author.find('ForeName').text + ";"
            author_list += author_name
        author_list = author_list.strip(';')
        #print(author_list)

        # For each article, Put id, title and abstract_all and author_list into an array. 
        each_article_row = [id, article_title, abstract_all, author_list]

        # Append this into "all_articles" list. This will create 2D list.
        # all _articles = [[id1, title1, abstract1, author_list1],
        #                  [id2, title2, abstract2, author_list2]]
        all_articles.append(each_article_row)

    return all_articles

print(get_articles_with_details())
