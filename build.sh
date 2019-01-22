#!/bin/bash

CURDIR=`dirname $0`;
echo -e "\033[0;32mBuild: $(readlink -f $CURDIR) \033[0m";

########################################################################################
## Install pcl packages and requiered                                                ##
##   sudo add-apt-repository ppa:v-launchpad-jochen-sprickerhof-de/pcl                ##
##   sudo apt-get update                                                              ##
##   sudo apt-get install libpcl-dev libopenni2-dev libproj-dev                       ##
########################################################################################


if [ $# == 1 -a "$1" == "debug" ] ; then TYPE=Debug; else   TYPE=Release; fi
if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ] 
then
  NUMBER_OF_PROCESSORS=`nproc`;
  #cmake -Wno-dev -H${CURDIR} -B${CURDIR}/build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=$TYPE
  cmake -Wno-dev -H${CURDIR}/source -B${CURDIR}/build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=$TYPE -DBOOST_ROOT=/home/wp21/PCC/install/boost_1_64_0
  make -C ${CURDIR}/build -j ${NUMBER_OF_PROCESSORS} -s
else
  echo "$CURDIR Windows compilation not supported ";
fi 
