
# MailCorpTool
MailCorpTool is a tool designed for small teams that do not have or do not prefer to pay for an email host. It uses gmail as host. 📧





[![License: MIT](https://img.shields.io/badge/License-MIT-yellowgreen.svg?style=flat-square)](https://opensource.org/licenses/MIT) [![Python](https://img.shields.io/badge/Python-3.10-blue.svg?style=flat-square&logo=Python)](https://python.org) [![GitGub Repositorie](https://img.shields.io/badge/GitHub_Repositorie-MailCorpTool-gray.svg?style=flat-square&logo=github)](https://github.com/ElHaban3ro/AsegTool/) 



I explain how it works and its purpose in more detail:

Because paying for an email host can sometimes be **very expensive**, we can save that by using gmail instead and use your **domain aliases** to send emails from Gmail. The dilemma is that to do it from gmail you have to give access to your main email, which is extremely dangerous. A solution to this is this, assign a gmail email where all the aliases you prefer are already and simply from the sender, you can decide who to send it to, it will be **sent under that alias**.

## An example:
Domain retrokode.com has the alias fer@retrokode.com. I assume that all the messages that arrive to fer@retrokode.com arrive to my gmail account given as example "fergmail@gmail.com", but when answering a message, and I want to do it from fer@retrokode.com I have to write a message to baseretrokode@gmail.com and he will forward it to the addressee with the alias fer@retrokode.com.

***If:***

from: fergmail@gmail.com
to: baseretrokode@gmail.com

***Subject:*** Hola > otheremail@gmail.com
***Body:*** Greats!

***
The above would send a message with subject ***"Hello"*** and from the email fer@retrokode.com (configured in the json) to othermail@gmail.com.





# Configured App

To begin with it is very important to create a project in [google cloud console](https://console.cloud.google.com/) and add as **gmail api**, create some credentials for that gmail api, download **credentials_file.json** and go to configure (You must first give access to your mail base from the **"consent"** section):

- In the config.py file, assign to the **AUTH_TOKEN_FILE** variable the value of the absolute path of your *credentials_file.json*.
- Configure the redirects in the **registredAccounts.json** file, the **key** is the gmail email of our team, and the **value** is the email of that character but which is actually the alias of our domain (already configured in gmail).
- Now, execute app.py, this, the first time, will open the google window and will ask you to log in with your **Google account** (the main one, the base email, in my example was baseretrokode@gmail.com), and then create a **token.json** file, that will contain your login information so you don't have to log in again.

***
If you have any doubt or problem you can comment me in ***my discord***.
[![GitGub Repositorie](https://img.shields.io/badge/Discord-Server-blue.svg?style=flat-square&logo=discord)](https://discord.gg/b29Pe2QQmF "https://discord.gg/b29Pe2QQmF")