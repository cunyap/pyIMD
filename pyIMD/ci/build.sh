#!/bin/bash
#
# execute with --user to make pip install in the user home
#
set -e

python3 -m pip install $USER PyInstaller

if [[ $1 == "linux" ]];
    then
        cd /home/travis/build/cunyap/pyIMD/
        sudo apt-get install libgl1-mesa-glx
        sudo mkdir /usr/lib64/
        sudo cp -R /usr/lib/x86_64-linux-gnu/mesa/* /usr/lib64/
        echo $(ls /usr/lib64/*)
        echo $(ls /usr/lib64/libGL*)
        # Install the package
        pip3 install .

        if [[ $2 == 3.5 ]];
            then
                echo "# build the program"
                echo "For the operating system" $1

                python3 -m PyInstaller --noconsole --onefile --icon=/home/travis/build/cunyap/pyIMD/pyIMD/ui/icons/pyIMD_logo_icon.ico /home/travis/build/cunyap/pyIMD/pyIMD/ci/pyIMD_unix.spec
                PYIMD_APP="`pwd`/dist/pyIMD"
                echo "The app can be found in \"$PYIMD_APP\"."
                mv /home/travis/build/cunyap/pyIMD/dist/pyIMD /home/travis/build/cunyap/pyIMD/dist/pyIMD_x64_unix
                echo $(ls /home/travis/build/cunyap/pyIMD/dist/)
                echo "# Done with compiling"
        fi;

        echo "# Done with compiling"
else
    cd /Users/travis/build/cunyap/pyIMD/
    pip3 install PyQt5>=5.10.1
    pip3 install .

    if [[ $2 == 3.5 ]];
        then
            echo "# build the program"
            echo "For the operating system" $1

            python3 -m PyInstaller --noconsole --onefile /Users/travis/build/cunyap/pyIMD/pyIMD/ci/pyIMD_osx.spec

            echo "# create the .dmg file"
            # see http://stackoverflow.com/a/367826/1320237
            PYIMD_DMG="`pwd`/dist/pyIMD.dmg"
            rm -f "$PYIMD_DMG"
            hdiutil create -srcfolder dist/pyIMD.app "$PYIMD_DMG"
            mv /Users/travis/build/cunyap/pyIMD/dist/pyIMD.dmg /Users/travis/build/cunyap/pyIMD/dist/pyIMD_x64_osx.dmg
            echo $(ls /Users/travis/build/cunyap/pyIMD/dist/)
            echo "The installer can be found in \"$PYIMD_DMG\"."
            echo "# Done with compiling"
    fi;
    echo "# Done"
fi;


