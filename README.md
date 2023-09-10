# personal-projects

**Welcome to Peter's personal project repository!**

> _This a temp repo to help store workflow/raw files for projects that are in WIP_

## General guidelines when starting on a new project

### 1. Cloning of repository

This is probably not needed when you start on a new project given that the underlying assumption is that you already have your github repo connected to local IDE - in my case I like to use VS Code. To be honest, I'm probably writing this section to get into the habit of writing documentation, especially a README file, as this is often the most overlooked part of the project process. Mostly because this is the more mundane and less interesing phase of the project. But enought chit-chat, time to fill this page up to make it look less sad while also getting into the process of familiarising the syntax of writing such documentations.

**1.1 Generating SSH Key**

Before cloning the repo to your local directory, you need to make sure that you have the correct access rights before cloning. So once you've `cd` into the directory in which you want to clone the repo to, run the terminal command `ssh-keygen -t ed25519 -C "your_email@example.com"` to generate your SSH key - You can find the commands and more detailed explanation of doing so here: [Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

You just need to keep in mind that the email address used is the same as the one used to log in to your Github account. Next, once you run the above command, you would be prompted the following three questions:

![Screenshot 2023-09-10 at 11 59 40 AM](https://github.com/peterchettiar/personal-projects/assets/89821181/1af87c02-559a-411f-b7f5-209dcba26abd)

You would just have to press `ENTER` once for each prompt, and before you know it, you would have created an SSH key!

Next, you would want to copy this SSH key - for this run the following command: `pbcopy < ~/.ssh/id_ed25519.pub`

Once you've done this, you need to proceed to your Github account and click on your profile picture and select settings. Following this, you would need to click on `SSH and GPG Keys` on the left navigation panel, and click on the `New SSH Key` button. This would lead you to a page that requires you to fill in a title for your key as well as copied SSH key into the key box. After you've added the key, your local account would now have an SSH key that is connected to your github account. Now that we have the access rights for cloning the git hub repo - we run the command `git clone git@github.com:peterchettiar/personal-projects.git` to do just that!

In case this set of instructions were not clear, please refer to this youtube tutorial : [How to setup SSH for Github repository](https://www.youtube.com/watch?v=snCP3c7wXw0)

### 2. Setting up a new environment

Next, we want to set up a virtual environment with dependancies that are specific to the project. This is often deemed as good or standard practice when starting a new project. So, the steps of doing so are as follows:

**2.1 Create environment.yml**

We first need to create a environment.yml file that contains all the dependancies - to keep things simple, I had created a yaml file that contained all the libraries that I had on my base environment. Over the years in University, I had curated all the various libraries in the base environment of my laptop (it was a time where I had not learnt of the standard practice of creating venv). So, pretty much what I like to do is load this standard .yml file and delete the dependancies that I don't need, and install them to my new venv. If you find yourself in a similar predicament, create your yaml file using the following steps:
   
**2.1.1 Run the following command to activate your base environment**
```
conda activate base 
```
**2.1.2 Then run the following command to export the dependencies to a yaml file**
```
conda list --export > base_environment.yml
```
**2.2 Edit the yaml file**

At this point the output from the previous command should be in your current working directory. You can open it up and make these changeson the yaml file:
- `name` : You can specify the name of the new environement
- `channels` : Typically I keep this as default
- `dependencies` : Usually the particular version of each library maybe outdated, especially when you export it from some other environment. So what I like to do is to remove the versions using regex (like `(=).*`, and do a find and replace), and maybe include or remove additional packages as per your project requirement
- `pip` : I've included a pip dictionary in the dependancies section to specify packages that I want to install using `pip` instead of `conda`
- `prefix` : Lastly, this is where I specify the location of where the venv should be installed, for this I would always specify the location of the project

**2.3 Create venv using yaml file**

Now, all we have to do is to run the command `conda env create -f environment.yml` - note that this file should be in the project working directory (as a rule of thumb, anything related to the project should be encapsulated within the said project folder)


**2.4 Some useful tips**

_In the event where you want to delete an environment that you created:_
1. Run this command to see the list of environments as well as their respecitve filepaths
```
conda env list
```
2. Next run the command `cd` to go to root folder, then run the following command to go to the folder in which the environment you want to delete is located
```
cd '{file path to folder of environment - this can be found from previous command}'
```
3. Lastly, to delete we need to remove all the files in folder recursively before deleting the folder as follows (make sure to `deactivate` first)
```
rm -r venv
```
_Useful github commands_

```
git branch - command to check the branch we are on the github page
git pull - command to pull the latest files from origin (i.e. Github)
git checkout <branch name you want to move to> - command to change the branch that you are in
git checkout -b <new branch name> <origin/branch name in github> - command to create a new branch locally that is a copy of a branch on github (and switches to new branch)
git checkout -b <new branch name> - command to create a new local branch
git push -u origin <branch> - command to push the local branch to github
```
