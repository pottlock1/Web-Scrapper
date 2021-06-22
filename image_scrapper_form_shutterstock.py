from bs4 import BeautifulSoup as bs
import requests
import os
import urllib


def download_from_shutterstock(query, n):
    search_url = "https://www.shutterstock.com/search/{q}".format(q = query)
    links = [] 
    while len(links) < n:
        # getting html of the page
        req = urllib.request.Request(search_url)
        res = urllib.request.urlopen(req)
        resdata = res.read()
        html = bs(resdata, 'html.parser')

        # getting all the images links
        images = html.find_all('img', {'class':'z_h_9d80b z_h_2f2f0'})
        print('Total images found = {}'.format(len(images)))

        for image in images:
            links.append(image['src'])
            if len(links) >= n:
                break
        button_box = html.find_all('div', {'class':'z_b_f3102'})
        link = button_box[0].a['href']
        next_page_link = 'https://www.shutterstock.com'+link
        search_url = next_page_link
        
    print('{} image links have been extracted!!'.format(len(links)))

        # Downloading images
    for n, link in enumerate(links):
        image_content = requests.get(link).content

        if not os.path.exists(r'C:\Users\PIYUSH KUMAR\Desktop\ineuron\practice\image_scapper\{q}_shutterstock'.format(q = query)):
            os.mkdir(r'C:\Users\PIYUSH KUMAR\Desktop\ineuron\practice\image_scapper\{q}_shutterstock'.format(q = query))

        f = open(os.path.join(r'C:\Users\PIYUSH KUMAR\Desktop\ineuron\practice\image_scapper\{q}_shutterstock'.format(q = query), 'img_'+str(n+1)+'.jpg'), 'wb')
        f.write(image_content)
        f.close()
        print(f'{n+1} images have been dowloaded!!')
    print('Task complete!!')

query = 'god'
no_of_images = 10

if __name__ == '__main__':
    download_from_shutterstock(query, no_of_images)