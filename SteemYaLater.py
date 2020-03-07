import os, certifi, csv, datetime, hashlib, io, logging, pycurl, random, time, wget, urllib3, shutil, sys

from beem import Steem
from beem.account import Account
from beem.amount import Amount
from beem.comment import Comment
from beem.exceptions import AccountDoesNotExistsException, ContentDoesNotExistsException
from beem.nodelist import NodeList
from beem.instance import set_shared_steem_instance

global working_dir

nodes = NodeList().get_nodes()
stm = Steem(node='https://anyx.io')
#stm = Steem(node=nodes)
set_shared_steem_instance(stm)

# Certificate validation required for security. Prevent MITM
http = urllib3.PoolManager(
                           cert_reqs='CERT_REQUIRED',
                           ca_certs='/etc/ssl/certs/cacerts.pem'#ca_certs=certifi.where()
                           )

working_dir = os.getcwd()
logging.basicConfig(filename=datetime.datetime.now().strftime("SteemYaLater%Y%m%d-%H%M%S.log"),format='%(asctime)s %(message)s',level=logging.WARNING)
pauseTimeInit=5

halfPause = int(pauseTimeInit/2)
lowPauseTime = pauseTimeInit - halfPause
upPauseTime = pauseTimeInit + halfPause

def get_blog_entries(account_to_backup):
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
    return blog_list

# exports list to csv file
def export_csv(name,input_list):
    cwd = os.getcwd()
    filename=datetime.datetime.now().strftime(name+"%Y%m%d-%H%M%S.csv")
    keys = input_list[0].keys()
    outfile=open(cwd+'/'+filename,'w')
    writer=csv.DictWriter(outfile, keys)
    writer.writeheader()
    writer.writerows(input_list)


def get_file_hash(ref):
    if str(ref).startswith('http'):
        try:
            request = get_http_response(ref)
            with request as url_to_check:
                data = url_to_check.read() # read contents of the file
                md5_returned = hashlib.md5(data).hexdigest() # pipe contents of the file through
            request.close()
        except Exception as e:
            print(e)
            logging.warning('Error obtaining '+ref+' hash w urllib3!')
            try:
                data = downloadhash(ref)
                md5_returned = hashlib.md5(data).hexdigest()
            except Exception as e:
                print(e)
                logging.warning('Error obtaining '+ref+' hash w pycurl!')
                return
    elif os.path.exists(ref):
        with open(ref, 'rb') as file_to_check:
            data = file_to_check.read() # read contents of the file
            md5_returned = hashlib.md5(data).hexdigest() # pipe contents of the file through
    return md5_returned

def get_http_response(url):
    request = http.request(
                'GET',
                url,
                retries=2,
                preload_content=False,
                headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
                )
    return request

def get_http_response_test(url):
    if url.startswith('https://steemitboard.com'):
        request = http_steemitboard.request(
                    'GET',
                    url,
                    retries=2,
                    preload_content=False,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
                             'Sec-Fetch-Dest': 'document',
                             'Sec-Fetch-Mode': 'navigate',
                             'Sec-Fetch-Site': 'none',
                             'Sec-Fetch-User': '?1',
                             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                             'Accept-Encoding': 'gzip, deflate, br',
                             'Accept-Language': 'en-US,en;q=0.9',
                             'Cache-Control': 'max-age=0',
                             'Connection': 'keep-alive',
                             'Host': 'steemitboard.com',
                             'Upgrade-Insecure-Requests': '1'}
                    )
        return request
    request = http.request(
                'GET',
                url,
                retries=2,
                preload_content=False,
                headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
                )
    return request

def compare_hash(ref1,ref2): # not used but adding for future use
    try:
        k1 = get_file_hash(ref1)
        k2 = get_file_hash(ref2)
    except Exception as e:
        print(e)
        logging.warning('Error obtaining reference hash!')
        return
    if k1 == k2:
        print("Hash Match!")
        return True
    if k1 != k2:
        print("Hash Mismatch!")
        return False

def downloadProgress(download_t, download_d, upload_t, upload_d):
    try:
        frac = float(download_d)/float(download_t)
    except:
        frac = 0
    sys.stdout.write("\r%s %3i%%" % ("Download:", frac*100)  )

def downloadFile(url, outpath=False, key_file=False, cert_file=False):
    halfPause = int(pauseTimeInit/2) #fileList = readFileList(fileListFile)
    lowPauseTime = pauseTimeInit - halfPause
    upPauseTime = pauseTimeInit + halfPause
    fileName = url.split('/')[-1]
    curl = pycurl.Curl()
    if outpath:
        fp = open(outpath, "wb")
    else:
        no_save_path = working_dir+'/'+fileName
        fp = open(no_save_path, "wb")
    curl.setopt(pycurl.WRITEDATA, fp)
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.NOPROGRESS, 0)
    curl.setopt(pycurl.PROGRESSFUNCTION, downloadProgress)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.MAXREDIRS, 5)
    curl.setopt(pycurl.CONNECTTIMEOUT, 50)
    curl.setopt(pycurl.TIMEOUT, 7)
    curl.setopt(pycurl.FTP_RESPONSE_TIMEOUT, 600)
    curl.setopt(pycurl.NOSIGNAL, 1)
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 2)
    if key_file:
        curl.setopt(pycurl.SSLKEY, key_file)
    if cert_file:
        curl.setopt(pycurl.SSLCERT, cert_file)
    try:
        print("Start time: " + time.strftime("%c"))
        curl.perform()
        print("\nTotal-time: " + str(curl.getinfo(curl.TOTAL_TIME)))
        print("Download speed: %.2f bytes/second" % (curl.getinfo(curl.SPEED_DOWNLOAD)))
        print("Document size: %d bytes" % (curl.getinfo(curl.SIZE_DOWNLOAD)))
    except:
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
    data = curl.perform_rb()
    curl.close()
    sys.stdout.flush()
    hash = hashlib.md5(data).hexdigest()
    if outpath:
        fp.close
    return hash

def download_image(path,url): #Download Image with urllib3
    r = get_http_response(url)
    with r, open(path, 'wb') as out_file:
        shutil.copyfileobj(r, out_file)
    r.release_conn()

def downloadProgress(download_t, download_d, upload_t, upload_d):
    try:
        frac = float(download_d)/float(download_t)
    except:
        frac = 0
    sys.stdout.write("\r%s %3i%%" % ("Download:", frac*100)  )

def get_image_hash_list(account_to_backup):
    image_hash_list = []
    for root,dir,files in os.walk(os.path.join(working_dir+"/Backups/"+account_to_backup)):
        if root.endswith('/images'):
            relative_path = root.split(account_to_backup)[-1]
            for f in files:
                md5_hash = get_file_hash(root+'/'+f)
                image_hash_dict = {'image_path': relative_path+'/'+f,'hash': md5_hash}
                image_hash_list.append(image_hash_dict)
    return image_hash_list

def download_blog_entry(blog_entry,hash_table,hashes): # accepts output from from Beem Account.get_blog(start_index=1,limit=1,raw_data=True,short_entries=True)
    status_list = []
    id = '@'+blog_entry['author']+'/'+blog_entry['permlink']
    try:
        c = Comment(id, steem_instance=stm)
    except ContentDoesNotExistsException:
        logging.warning(id+' content does not exist!')
    permlink_trucated = blog_entry['permlink'][:128] + (blog_entry['permlink'][128:] and '..') #trucate permlink to accomodate 128 character element limit
    img_dir = os.path.join(working_dir+"/Backups/"+blog_entry['author'],permlink_trucated+'/images')
    if not os.path.isdir(os.path.join(working_dir+"/Backups/"+blog_entry['author'],permlink_trucated)):
        os.mkdir(os.path.join(working_dir+"/Backups/"+blog_entry['author'],permlink_trucated))
    if not os.path.isdir(img_dir):
        os.mkdir(img_dir)
    split_body = c.body.split('\n')
    txt_path = os.path.join(working_dir+"/Backups/"+blog_entry['author'],permlink_trucated,permlink_trucated+".txt")
    if not os.path.isfile(txt_path):
        text_file = open(txt_path, "w+")
        for str in split_body:
            text_file.write(str+'\n')
        text_file.close()
    print("Backing up "+id+" images!")
    try:
        for img in c['json_metadata']['image']:
            out_path = img_dir+'/'+img.split('/')[-1]
            if img:
                try:
                    file_hash = get_file_hash(img)
                    if file_hash in hashes:
                        status_dict = {'id': id, 'url': img, 'status': 'Already downloaded.'}
                        for h in hash_table:
                            if h['hash'] == file_hash and not os.path.islink(out_path):  #does not seem to detect symlink so using try except instad
                                local_path = h['image_path']
                                relative_path = os.path.relpath(local_path,out_path)
                                try:
                                    os.symlink(relative_path,out_path)
                                except FileExistsError:
                                    print('Symbolic link or file already exists!')
                        status_list.append(status_dict)
                        continue
                except Exception as e:
                    status_dict = {'id': id, 'url': img, 'status': 'Unable to get file hash.'}
                    status_list.append(status_dict)
                    logging.warning("Unable to get "+img+"'s file hash!")
                    continue
                if not os.path.exists(os.path.join(img_dir,img.split('/')[-1])):
                   try:
                       wget.download(img,out=out_path)
                   except Exception as e:
                       status_dict = {'id': id, 'url': img, 'status': e}
                       status_list.append(status_dict)
                       print(e)
                       print("wget download failed! attempting download with urllib3.")
                       try:
                           pauseTime = random.randint(lowPauseTime, upPauseTime)
                           time.sleep(pauseTime)
                           download_image(out_path,img)
                       except Exception as e:
                           print(e)
                           print("urllib3 download failed! attempting download with pycurl.")                               
                           status_dict = {'id': id, 'url': img, 'status': e}
                           status_list.append(status_dict)
                           try:
                               downloadFile(img, out_path)
                           except Exception as e:
                               print(e)
                               print("pycurl download failed! attempting download with pycurl.")                               
                               status_dict = {'id': id, 'url': img, 'status': e}
                               status_list.append(status_dict)
                           else:
                               file_hash = downloadFile(img)
                               hashes.append(file_hash)
                               status_dict = {'id': id, 'url': img, 'status': 'pycurl success'}
                       else:
                           file_hash = get_file_hash(out_path)
                           hashes.append(file_hash)
                           status_dict = {'id': id, 'url': img, 'status': 'urllib3 success'}
                   else:
                       file_hash = get_file_hash(out_path)
                       hashes.append(file_hash)
                       status_dict = {'id': id, 'url': img, 'status': 'wget success'}
                       status_list.append(status_dict)
            pauseTime = random.randint(lowPauseTime, upPauseTime)
            time.sleep(pauseTime)
    except KeyError:      
        print(id+" has no images!")
        status_dict = {'id': id, 'url': 'n/a', 'status': 'No Images in Post!'}
        status_list.append(status_dict)
    except Exception as e:
        print(id+" experienced error "+e)
    else:
        print("Entry "+id+" processed!")
    return status_list

#prepopulate list for batch operations
accounts = []
if len(accounts) == 0:# Prompts user for Steem account for backup if account list not prepopulated. Creates respective user folder in backups if not exists 
	account = input("Account to Backup?")
	accounts.append(account)

def download_blogs(accounts,rounds):
    for account_to_backup in accounts:
        i = 0
        while i < rounds:
            results = []
            blog_list = get_blog_entries(account_to_backup)
            img_hash_list = get_image_hash_list(account_to_backup)
            hashes = []
            for h in img_hash_list:
                hashes.append(h['hash'])
            if not os.path.isdir(working_dir+"/Backups/"+account_to_backup):
                os.mkdir(working_dir+"/Backups/"+account_to_backup)
            for b in blog_list:
                stats = download_blog_entry(b,img_hash_list,hashes)
                for s in stats:
                    results.append(s)
            export_csv('SteemYaLater_'+account_to_backup+'_results_',results)
            i += 1

download_blogs(accounts,1) #runs backups on accounts w one iteration.