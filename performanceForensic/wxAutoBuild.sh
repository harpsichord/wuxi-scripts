#!/bin/bash
#Author: Wu Xi
#Date: Sep 19 2019
#Purpose: automatically populate rpm build file structures, then build the package

base_dir=$(echo $PWD)
rpm_src='/rpmbuild/SOURCES'
spec_f='sat_utils.spec'
build_dir=''

function usage {
    echo >&2 "USAGE: wxAutoBuilt.sh -d build_directory"
    exit
}

if [ $# != 2 ]
then
usage
exit 1
fi

while getopts d:h opt
do
    case $opt in
    d)  build_dir=$OPTARG ;;
    h|?)  usage ;;
    esac
done

bd=${build_dir%%\/}

tar cvfz $HOME${rpm_src}/${bd}.tar.gz ${bd}

cp ${bd}/sat_utils.spec ~/rpmbuild/SOURCES/
cd ${HOME}${rpm_src}

rpmbuild -bb ${spec_f}

cd ${base_dir}
cp ~/rpmbuild/RPMS/x86_64/* rpms
