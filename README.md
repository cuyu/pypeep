# pypeep

![Travis](https://img.shields.io/travis/cuyu/pypeep.svg) ![Coveralls github](https://img.shields.io/coveralls/github/cuyu/pypeep.svg) ![PyPI](https://img.shields.io/pypi/pyversions/pypeep.svg) ![npm](https://img.shields.io/npm/l/express.svg)

> An automatic remote debug configurator for Pycharm (on mac OS).


This project was started by Ruiyuan Zhu ([https://github.com/CarolineZhu/decade](https://github.com/CarolineZhu/decade)) and I moved it here for further development.


### Getting started

To install pypeep:
```
pip install pypeep
```

To start a pypeep:
```
pypeep --remote-path=<remote_path> --entry=<entry> --server-name=<server_name> --hostname=<hostname> --ssh-user=<ssh_user> --ssh-password=<ssh_password> --ssh-port=<ssh_port> --local-path=<local_path> --download
```

- `<remote_path>`: project path on remote client
- `<entry>`: the entry python file of source code **OR**  a executable file path in the remote
  - if the input ends with `.py`, we will create a virtualenv in the remote host and pip install according to the requirements.txt under the project folder (closest to the `<entry>`, i.e. if there're multiple requirements.txt under different folder, we will use the one which closer to the input dir).
  - if the input do not end with `.py`, we assume it is a eecutable file path and will execute it after everything is ready.
- `<server_name>`(optional, default hello): debug server name defined arbitrarily by user
- `<hostname>`: remote client hostname
- `<ssh_user>`: remote client ssh user
- `<ssh_password>`: remote client ssh password
- `<ssh_port>`(optional, default 22): remote client ssh port
- `--download`(optional, store true): add if want to download the whole project to local. 
- `<local_path>`: project path on local server(Create an empty folder to contain the remote project if downloading the whole project, or use the local project path)

For example,
```
pypeep --remote-path=/root/hello --entry=hello.py --server-name=hello --hostname=target-host --ssh-user=root --ssh-password=target-password --local-path=/Users/rzhu/pytest_practice/try6
```

Also support remote debug code in docker container (just leave `--ssh-user` and `--ssh-password` empty and set `--hostname` to the container id):

```
pypeep --remote-path=/root/hello --entry=hello.py --server-name=hello --hostname=b294bc47bdc0 --local-path=/Users/rzhu/pytest_practice/try6
```

Use an executable file outside the project as the entry (you may create a virtaulenv and start the python process in the executable file):

```
pypeep --remote-path=/root/hello --entry=/tmp/run_python.sh --server-name=hello --hostname=b294bc47bdc0 --local-path=/Users/rzhu/pytest_practice/try6
```

### Configuring process finished

When this message shows in terminal
```
Configuration done. Please start the debug server in PyCharm.
```
and local project is opened by Pycharm, 

Click the debug button in the Pycharm to start the debug server. Enter 'r'/'ready' if ready.

Then the debugger will stop at the next line of 
```
pydevd.settrace(args.local_ip, port=args.local_port, stdoutToServer=True, stderrToServer=True)
```

You can set breakpoints in your project as your wish.

Happy debugging!

---

### How it works

#### Local side ####

The main task of local side is configuring the PyCharm remote debug settings:

1. Send the remote entry file to remote server;
2. (Optional) Download the project code to local if it is not exist;
3. Configure remote debugging settings for PyCharm in the local project;
4. Configure python environment in remote server (see `1.` in #Remote side);
5. Open PyCharm and wait for user starting the debug server;
6. Start the python process in remote server.

#### Remote side ####

All the operations in the remote side are done by local side through ssh/docker sdk. So we only describe how the remote entry file works here.

For `--start-script` option, as calling the python execution is out of our control, we need to do some hacks to inject the debug-required code. Here're the hacks:

1. We hack the `python` command by alias it to something like `alias python='python <remote_entry>'`
2. In `<remote_entry>`, we analyze the arguments and write the debug-required code into `sitecustomize.py` under python lib folder (see [https://stackoverflow.com/questions/32184440/making-python-run-a-few-lines-before-my-script](https://stackoverflow.com/questions/32184440/making-python-run-a-few-lines-before-my-script)).
3. Finally, `<remote_entry>` will trigger a sub python process to execute according to input arguments.

Above solution works in both native Python env or virtualenv, and even allow the start script creating/activating virtualenv in it!

### Todo

- Use env variables to store the local project path (so that we can store config in a shell script, a optional way to use the cmd easier)
    - Give the content of the shell script, like the `env.sh`
    - In the end of the shell script, call `source ./env.sh`, so that user just need to call one script when debugging on apps jenkins
- ~~Use `open -a PyCharm <project_path>` to open the PyCharm after script running~~
- ~~Support remote debugging in docker containers~~
- Add unit test
- ~~Use os.path.join instead of `+`~~
- ~~Use git to make sure the local code is the latest version (if local-path is exist)~~
- ~~Remove --download option, and download the code automatically if the local-path is not exist~~
- ~~Remove the query for if the debug server is ready (maybe can use a loop to see if the PyCharm process's binding port is right)~~
- ~~Print out remote stdout nicely~~
- Support using a executable file as remote entry
- Add path mapping for site packages (use --venv to specify local env path)