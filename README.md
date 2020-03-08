# Automation to the Rescue!

&nbsp;&nbsp;&nbsp;&nbsp; This Python 3.6 script uses the Steem Beem Library and a variety of methods to archive your Steem Blog images as well as markdown files. It used image hash verification to ensure that files are downloaded once saving valuable storage space.

![735k3t.png](https://img.esteem.app/735k3t.png)

![dcelof.png](https://img.esteem.app/dcelof.png)

# Repository

https://github.com/anthonyadavisii/SteemYaLater

# Version 2.0 Change Notes

- Added PyCurl download method to address issues w steemitboard images
- Data Deplication enabled: Prevents redownload of file if already exists in folder structure. Symbolic link with relative path placed instead saving valuable storage space.
- Logging and CSV output: Session log file is produced in working directory. Output CSVs are created for each account so users may readily see what failed and may require manual action.

# Version 1.0

&nbsp;&nbsp;&nbsp;&nbsp; Version 1 was the basic framework with wget. We don't talk about version 1 anymore. 

https://i.redd.it/zw17doei2h211.jpg

&nbsp;&nbsp;&nbsp;&nbsp; I've worked hard and made a ton of progress in order to give my fellow Steemians a way to save their priceless data.

# Roadmap

- Steem Blog Backup as a Service
- @dtube thumbnail support
- Upload to Skynet web portal

# Known Issues

&nbsp;&nbsp;&nbsp;&nbsp; DTube thumbnails will not download as they are not stored within the Beem Comment json_metadata image property. Logic to be added to accomodate. Also, some links may require escape characters. These will be addressed as time permits.

### Uses Python 3.6

# Install Prerequisites

```
# PyCurl may require the following packages be installed.

sudo apt install libcurl4-openssl-dev libssl-dev

# Python modules installation

Python 3.6 -m pip install beem
Python 3.6 -m pip install wget
Python 3.6 -m pip install urllib3[secure]
Python 3.6 -m pip install pycurl
Python 3.6 -m pip install certifi #may or may not be needed if the [secure] option is used for urllib3
```

# Execute Script

```
python3.6 SteemYaLater.py
```

### Prompts for Steem User. Alternatively, you may populate the accounts list variable with users to backup

Account to Backup? anthonyadavisii

### Script will crawl your blog_entries filtering out resteems (reblogs)

![st4y66.png](https://img.esteem.app/st4y66.png)

### Will then cycle through each blog_entry, save the body to a .txt files, and grab any images it can with wget or urllib3


# Feel free to reach out if you need help! If you appreciate the work, consider sending me a tip!

![dcelof.png](https://img.esteem.app/dcelof.png)

### How to put your FREE Downvotes to work in 2 easy steps! 

![2sxn09.gif](https://img.esteem.app/2sxn09.gif)
[Learn more!](https://steemit.com/esteem/@anthonyadavisii/how-to-put-your-free-downvotes-to-work-in-2-easy-steps)

*This post was created using the [@eSteem Desktop Surfer App](https://github.com/eSteemApp/esteem-surfer/releases).*

&nbsp;&nbsp;&nbsp;&nbsp; They also have a [referral program](https://esteem.app/hive-125125/@esteemapp/esteem-referrals) that promotes users to onboard to our great chain. Sign up using my [referral link](https://esteem.app/signup?referral=anthonyadavisii) to help support my efforts to improve the Steem blockchain.

###  Ditch Partiko and get eSteem today!

<table>
  <tr>
    <th>PlayStore - Android</th>
    <th>Windows, Mac, Linux</th>
  </tr>
  <tr>
    <td><a href='https://play.google.com/store/apps/details?id=app.esteem.mobile.android'><img alt='Get eSteem on Google Play' src='https://img.esteem.ws//twstd2x0xx.png' /></a></td>
    <td><a href='https://github.com/eSteemApp/esteem-surfer/releases'><img src='https://img.esteem.ws//42dgm1zzo1.png' alt='Get eSteem for Desktop' /></a></td>
  </tr>
  <tr>
    <th colspan="2">AppStore - iOS</th>
    <th>Web</th>
  </tr>
  <tr>
    <td colspan="2"><a href='https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewSoftware?id=1451896376&mt=8'><img src='https://img.esteem.ws//ir3o7p26w7.png' alt='Get eSteem on AppStore' /></a></td>
    <td><a href='https://esteem.app'><img src='https://img.esteem.ws/100/bqaxajqbid.png' alt='Get eSteem for Desktop' /></a></td>
  </tr>
</table>
