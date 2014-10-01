#STANDARD XPATHS using open graph
ogLocale = "//meta[@property='og:locale']"
ogType = "//meta[@property='og:type']"
ogTitle = "//meta[@property='og:title']"
ogDescription = "//meta[@property='og:description']"
ogURL = "//meta[@property='og:url']"
ogSiteName = "//meta[@property='og:site_name']"

articlePublisher = "//meta[@property='article:publisher']"
articleAuthor = "//meta[@property='article:author']"
articleTag = "//meta[@property='article:tag']"
articleSection = "//meta[@property='article:section']"
articlePubTime = "//meta[@property='article:published_time']"
articleModTime = "//meta[@property='article:modified_time']"

twitterTitle = "//meta[@name='twitter:title']"
twitterSite = "//meta[@name='twitter:site']"
twitterCreator = "//meta[@name='twitter:creator']"
twitterDescription = "//meta[@name='twitter:description']"


#ALTERNATIVE & SITE-SPECIFIC XPATHS
altDescription1 = "//meta[@name='description']"
altDescription2 = "//meta[@property='rnews:description']"
altDescription3 = "//meta[@itemprop='description']"

altPubTime1 = "//meta[@property='og:article:published_time']"
altPubTime2 = "//meta[@name='originalpublicationdate']"
altPubTime3 = "//meta[@name='revision_date']"
altPubTime4 = "//meta[@name='pubdate']"
altPubTime5 = "//meta[@name='sailthru.date']"
altPubTime6 = "//meta[@name='date']"
altPubTime7 = "//meta[@property='rnews:datePublished']"
altPubTime8 = "//meta[@itemprop='datepublished']"
altPubTime9 = "//meta[@itemprop='datecreated']"
altPubTime10 = "//meta[@name='shareaholic:article_published_time']"

altModTime1 = "//meta[@property='og:article:modified_time']"
altModTime2 = "//meta[@property='og:updated_time']"
altModTime3 = "//meta[@name='revision_date']"
altModTime4 = "//meta[@itemprop='datemodified']"
altModTime5 = "//meta[@name='shareaholic:article_modified_time']"

altTitle1 = "//meta[@itemprop='headline']"
altTitle2 = "//meta[@itemprop='name']"
altTitle3 = "//meta[@itemprop='title']"
altTitle4 = "//meta[@property='title']"
altTitle5 = "//meta[@name='title']"

altAuthor4 = "//meta[@property='article:authorname']"
altAuthor2 = "//meta[@name='sailthru:author']"
altAuthor3 = "//meta[@name='author']"
altAuthor1 = "//meta[@property='og:article:author']"
altAuthor5 = "//meta[@itemprop='author']"

altTags3 = "//meta[@name='keywords']"
altTags2 = "//meta[@name='sailthru.tags']"
altTags1 = "//meta[@property='og:article:tag']"
altTags4 = "//meta[@name='news_keywords']"

altSection1 = "//meta[@name='section']"

altSiteName1 = "//meta[@name='shareaholic:site_name']"

altLocale1 = "//meta[@itemprop='inlanguage']"
altLocale2 = "//meta[@property='locale']"
altLocale3 = "//meta[@name='shareaholic:language']"

altURL1 = "//meta[@itemprop='url']"
altURL2 = "//meta[@name='shareaholic:url']"

altType1 = "//meta[@property='type']"
altType2 = "//meta[@name='type']"

#find locale meta data
def findLocale(doc):
    locale = ""
    #looking for the the standard xpath first, followed by the alternatives if the first xpath doesn't exist:
    for el in doc.xpath(ogLocale) or doc.xpath(altLocale1) or doc.xpath(altLocale2)\
            or doc.xpath(altLocale3):
        locale = el.get("content")          #once found, get content.
    return locale

#find site name meta data
def findSiteName(doc):
    siteName = ""
    for el in doc.xpath(ogSiteName) or doc.xpath(altSiteName1):
        siteName = el.get("content")
    return siteName

#find author meta data
def findAuthor(doc):
    author = ""
    for el in doc.xpath(articleAuthor) or doc.xpath(altAuthor1) or doc.xpath(altAuthor2)\
            or doc.xpath(altAuthor3) or doc.xpath(altAuthor4) or doc.xpath(altAuthor5):
        author = el.get("content")

    return author

#find type meta data
def findType(doc):
    type = ""
    for el in doc.xpath(ogType) or doc.xpath(altType1) or doc.xpath(altType2):
        type = el.get("content")

    return type

#find title meta data
def findTitle(doc):
    title = ""
    for el in doc.xpath(ogTitle) or doc.xpath(altTitle1) or doc.xpath(altTitle2)\
            or doc.xpath(altTitle3) or doc.xpath(altTitle4) or doc.xpath(altTitle5)\
            or doc.xpath(twitterTitle):
        title = el.get("content")

    return title

#find description meta data
def findDescription(doc):
    description = ""
    for el in doc.xpath(ogDescription) or doc.xpath(altDescription1) or doc.xpath(altDescription2)\
            or doc.xpath(altDescription3) or doc.xpath(twitterDescription):
        description = el.get("content")

    return description

#find site URL meta data
def findSiteURL(doc):
    siteURL = ""
    for el in doc.xpath(ogURL) or doc.xpath(altURL1) or doc.xpath(altURL2):
        siteURL = el.get("content")

    return siteURL

#find publisher meta data
def findPublisher(doc):
    publisher = ""
    for el in doc.xpath(articlePublisher):
        publisher = el.get("content")

    return publisher

#find sections meta data
def findSections(doc):
    sections = []
    for el in doc.xpath(articleSection) or doc.xpath(altSection1):
        section = el.get("content")
        #because there may be several 'sections' of meta data, we append all we find to a list
        sections.append(section)

    return sections

#find published time meta data
def findPublishedTime(doc):
    pubTime = ""
    for el in doc.xpath(articlePubTime) or doc.xpath(altPubTime1) or doc.xpath(altPubTime2) \
            or doc.xpath(altPubTime3) or doc.xpath(altPubTime4) or doc.xpath(altPubTime5) \
            or doc.xpath(altPubTime6) or doc.xpath(altPubTime7) or doc.xpath(altPubTime8)\
            or doc.xpath(altPubTime9):
        pubTime = el.get("content")

    return pubTime

#find modified time meta data
def findModifiedTime(doc):
    modTime = ""
    for el in doc.xpath(articleModTime) or doc.xpath(altModTime1) or doc.xpath(altModTime2)\
            or doc.xpath(altModTime3) or doc.xpath(altModTime4):
        modTime = el.get("content")

    return modTime

#find tags meta data
def findTags(doc):
    tags = []
    for el in doc.xpath(articleTag) or doc.xpath(altTags1) or doc.xpath(altTags2) or doc.xpath(altTags3)\
            or doc.xpath(altTags4):
        tag = el.get("content")
        #because there may be several 'tags' of meta data, we append all we find to a list
        tags.append(tag)

    return tags