#!/usr/bin/env bash

paren=`pwd`
nranks=8

res=( 8 16 32 64 )
for i in "${res[@]}"
do
    cd "${i}" || exit
    iname="channel_analytical.inp"
    rm channel_flow.log
    spack build-env amr-wind mpirun -np "${nranks}" "$(spack location -i amr-wind)"/bin/amr_wind "${iname}" ChannelFlow.perturb_velocity=false > out
    rm -rf plt* chk*
    cd "${paren}" || exit
done
 
