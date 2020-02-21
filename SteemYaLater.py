import os, wget, urllib3, shutil

from beem import Steem
from beem.account import Account
from beem.amount import Amount
from beem.comment import Comment
from beem.nodelist import NodeList
from beem.instance import set_shared_steem_instance

nodes = NodeList().get_nodes()
stm = Steem(node='https://anyx.io')
#stm = Steem(node=nodes)
set_shared_steem_instance(stm)

http = urllib3.PoolManager()

def download_image(path,url): #Download Image with urllib3
	r = http.request(
				'GET',
				url,
				preload_content=False,
				headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
				)
	with r, open(path, 'wb') as out_file:
		shutil.copyfileobj(r, out_file)

def download_blog_entry(blog_entry): # accepts output from from Beem Account.get_blog(start_index=1,limit=1,raw_data=True,short_entries=True)
    id = '@'+blog_entry['author']+'/'+blog_entry['permlink']
    c = Comment(id, steem_instance=stm)
    img_dir = working_dir+"/Backups/"+blog_entry['author']+'/'+blog_entry['permlink']+'/images'
    if not os.path.isdir(working_dir+"/Backups/"+blog_entry['author']+'/'+blog_entry['permlink']):
        os.mkdir(working_dir+"/Backups/"+blog_entry['author']+'/'+blog_entry['permlink'])
    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)
    split_body = c.body.split('\n')
    txt_path = working_dir+"/Backups/"+blog_entry['author']+'/'+blog_entry['permlink']+'/'+blog_entry['permlink']+".txt"
    if not os.path.isfile(txt_path):
        text_file = open(txt_path, "w+")
        for str in split_body:
            text_file.write(str+'\n')
        text_file.close()
    try:
        for img in c['json_metadata']['image']:
            if not os.path.exists(img_dir+'/'+img.split('/')[-1]):
               out_path = img_dir+'/'+img.split('/')[-1]
               try:
                   wget.download(img,out=img_dir+'/'+img.split('/')[-1])
               except Exception as e:
                   print(e)
                   print("wget download failed! attempting download with urllib3.")
                   download_image(out_path,img)
    except Exception as e:
        print(e)
    print("Entry "+id+" backed up!")

# Prompts user for Steem account for backup. Creates respective user folder in backups if not exists	
account_to_backup = input("Account to Backup?")
working_dir = os.getcwd()
if not os.path.isdir(working_dir+"/Backups/"+account_to_backup):
    os.mkdir(working_dir+"/Backups/"+account_to_backup)

acc = Account(account_to_backup,steem_instance=stm)

blog_list = []
i = 1

while len(acc.get_blog(i,1,raw_data=True,short_entries=True)) > 0:
    chunk = acc.get_blog(i,1,raw_data=True,short_entries=True)
    i += 1
    for c in chunk:
        print(c)
        if c['author'] == account_to_backup:
            blog_list.append(c)

for b in blog_list:
    download_blog_entry(b)