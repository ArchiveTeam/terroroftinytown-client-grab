terroroftinytown-client-grab
============================

The Seesaw pipeline grab script for the URLTeam (terroroftinytown) project

More information about the archiving project can be found on the ArchiveTeam wiki: [URLTeam](http://archiveteam.org/index.php?title=URLTeam)

See [terroroftinytown](https://github.com/ArchiveTeam/terroroftinytown) for source code details.


Setup instructions
=========================

There are now several ways to run this; the preffered method is via the included Dockerfile.

Be sure to replace `YOURNICKHERE` with the nickname that you want to be shown as, on the tracker. You don't need to register it, just pick a nickname you like.

In most of the below cases, there will be a web interface running at http://localhost:8001/. If you don't know or care what this is, you can just ignore it—otherwise, it gives you a fancy view of what's going on.

**If anything goes wrong while running the commands below, please scroll down to the bottom of this page. There's troubleshooting information there.**

Running with docker
--------------------

<img alt="Docker logo" src="https://upload.wikimedia.org/wikipedia/commons/7/79/Docker_%28container_engine%29_logo.png" height="100px">

Assuming this is a stand alone box, not part of a swarm etc, basic instructions for configuring your docker instance can be found at [docker documentation](https://docs.docker.com/install/) or for [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/) / [Debian](https://docs.docker.com/install/linux/docker-ce/debian/).

Make a directory, cd into the directry and copy the included dockerfile into it; the rest of the files are not required. Edit the final line to include the concurrency and replace `YOURNICK` with your username.

Build the container with the following arguments;

    docker build -t <<dockername>> <<foldername>>/

for example

    docker build -t at-terroroftinytown archiveteam-terroroftinytown/
    
Then simply run the container with either;

    docker run -d -it at-terroroftinytown

or if you want to give it a known name and make it easier to run commands;

    docker run -d -it --name at-terroroftinytown at-terroroftinytown

or if you really want that web page to be available;

    docker run -d -it -p 8001:8001 --name at-terroroftinytown at-terroroftinytown

Stopping the container (clean);

    docker run -d -it --name <<containername>> touch STOP

Stopping the container (hard);

    docker stop <<containername>>

Connecting to the container console;

    docker attach <<containername>>

Running with a warrior
-------------------------

Follow the [instructions on the ArchiveTeam wiki](http://archiveteam.org/index.php?title=Warrior) for installing the Warrior, and select the "URLTeam" project in the Warrior interface.

Running without a warrior
-------------------------
To run this outside the warrior, clone this repository, cd into its directory and run:

    pip install seesaw requests

then start downloading with:

    run-pipeline pipeline.py --concurrent 2 YOURNICKHERE

For more options, run:

    run-pipeline --help

If you don't have root access and/or your version of pip is very old, you can replace "pip install seesaw" with:

    wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py ; python get-pip.py --user ; ~/.local/bin/pip install --user seesaw requests

so that pip and seesaw are installed in your home, then run

    ~/.local/bin/run-pipeline pipeline.py --concurrent 2 YOURNICKHERE

**Note**: The code is partially self-updating by default with Git version 1.8.2 or higher. Use `--context-value no_submodule=1` if you do not want this behavior. Conversely, if you want full updating, use the `--auto-update` feature available in Seesaw 0.8 or higher.


Running multiple instances on different IPs
-------------------------------------------

This feature requires seesaw version 0.0.16 or greater. Use `pip install --upgrade seesaw` to upgrade.

Use the `--context-value` argument to pass in `bind_address=123.4.5.6` (replace the IP address with your own).

Example of running 2 threads, no web interface, and binding of IP address:

    run-pipeline pipeline.py --concurrent 2 YOURNICKHERE --disable-web-server --context-value bind_address=123.4.5.6

Distribution-specific setup
-------------------------
### For Debian/Ubuntu:

    adduser --system --group --shell /bin/bash archiveteam
    apt-get install -y git-core screen python-dev python-pip
    pip install seesaw requests
    su -c "cd /home/archiveteam; git clone https://github.com/ArchiveTeam/terroroftinytown-client-grab.git; cd terroroftinytown-client-grab;" archiveteam
    screen su -c "cd /home/archiveteam/terroroftinytown-client-grab/; run-pipeline pipeline.py --concurrent 2 --address '127.0.0.1' YOURNICKHERE" archiveteam
    [... ctrl+A D to detach ...]


### For CentOS:

Ensure that you have the CentOS equivalent of bzip2 installed as well. You might need the EPEL repository to be enabled.

    yum -y install python-pip
    pip install seesaw requests
    [... pretty much the same as above ...]

### For openSUSE:

    zypper install screen python-pip python-devel gcc make
    pip install seesaw requests
    [... pretty much the same as above ...]

### For OS X:

You need Homebrew. Ensure that you have the OS X equivalent of bzip2 installed as well.

    brew install python
    pip install seesaw requests
    [... pretty much the same as above ...]


### For Arch Linux:

Ensure that you have the Arch equivalent of bzip2 installed as well.

1. Make sure you have `python2-pip` installed.
3. Run `pip2 install seesaw requests`.
4. Modify the run-pipeline script in seesaw to point at `#!/usr/bin/python2` instead of `#!/usr/bin/python`.
5. `useradd --system --group users --shell /bin/bash --create-home archiveteam`
6. `screen su -c "cd /home/archiveteam/terroroftinytown-client-grab/; run-pipeline pipeline.py --concurrent 2 --address '127.0.0.1' YOURNICKHERE" archiveteam`


Troubleshooting
=========================

Broken? These are some of the possible solutions:


### ImportError: No module named seesaw

If you're sure that you followed the steps to install `seesaw`, permissions on your module directory may be set incorrectly. Try the following:

    chmod o+rX -R /usr/local/lib/python2.7/dist-packages

### Issues in the code

If you notice a bug and want to file a bug report, please use the GitHub issues tracker.

Are you a developer? Help write code for us! Look at our [developer documentation](http://archiveteam.org/index.php?title=Dev) for details.

### Other problems

Have an issue not listed here? Join us on IRC and ask! We can be found at irc.efnet.org #urlteam.
