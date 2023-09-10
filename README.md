# personal-projects

**Welcome to Peter's personal project repository!**

> _This a temp repo to help store workflow/raw files for projects that are in WIP_

## General guidelines when starting on a new project

### 1. Cloning of repository

This is probably not needed when you start on a new project given that the underlying assumption is that you already have your github repo connected to local IDE - in my case I like to use VS Code. To be honest, I'm probably writing this section to get into the habit of writing documentation, especially as a README file, as this is often the most overlooked part of the project process. Mostly because this is the more mundane and less interesing phase of the project. But enought chit-chat, time to fill this page up to make it look less sad while also getting into the process familirisng the syntax of writing such documentation.

1.1 Generating SSH Key

Before cloning the repo to your local directory, you need to make sure that you have the correct access rights before cloning. So once you've `cd` into the directory in which you want to clone the repo to, run the termical command `ssh-keygen -t ed25519 -C "your_email@example.com"` to generate your SSH key - You can find the commands and more detailed explanation of doing so here: [Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

You just need to keep in mind that the email address used is the same as the one used to log in to your Github account. Next, once you run the above command, you would be prompted the following three questions:

![Screenshot 2023-09-10 at 11 59 40 AM](https://github.com/peterchettiar/personal-projects/assets/89821181/1af87c02-559a-411f-b7f5-209dcba26abd)

You would just have to press `ENTER` once for each prompt, and before you know it, you would have created an SSH key!

Next, you would want to copy this SSH key - for this run the following command: `pbcopy < ~/.ssh/id_ed25519.pub`

Once you've done this, you need to proceed to your Github account and click on your profile picture and select settings. Following this, you would need to click on `SSH and GPG Keys` on the left navigation panel, and click on the `New SSH Key` button. This would lead you to a page that requires you to fill in a title for your key as well as copied SSH key into the key box. After you've added the key, your local account would now have an SSH key that is connected to your github account. Now that we have the access rights for cloning the git hub repo - we run the command `git clone git@github.com:peterchettiar/personal-projects.git` to do just that!

In case this set of instructions were not clear, please refer to this youtube tutorial : [How to setup SSH for Github repository](https://www.youtube.com/watch?v=snCP3c7wXw0)

### 2. Setting up a new environment

