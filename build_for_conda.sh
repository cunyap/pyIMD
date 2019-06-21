#!/bin/bash
#----------
# NOTE:
# Use for building: conda build pyimd/meta.yaml -c conda-forge
#----------
pkg="pyIMD"
versions=(3.6)
pkgL=$(echo "$pkg" | tr '[:upper:]' '[:lower:]')

#Building packages
#echo "Start building process"
#cd ~
#conda skeleton pypi $pkg
#conda skeleton pypi $pkg --recursive

#for k in "${versions[@]}"
#do
#     conda-build --python $k $pkgL -c conda-forge
#done

# Convert to other platforms
find ~/anaconda3/conda-bld/linux-64 -name "*.bz2" | while read file
do
    echo $file
    conda convert --platform all $file -o ~/anaconda3/conda-bld/all
done

# Upload build files
find ~/anaconda3/conda-bld/all -name "*.bz2" | while read file
do
    echo $file
    anaconda upload $file
done

echo "Done building all conda packages!"
