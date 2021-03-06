#! /bin/bash -l
#SBATCH -w broadep2
#SBATCH -C hwperf
#SBATCH --export=None
#SBATCH --time=24:00:00
#SBATCH --job-name=INSPECT_BDW_bench
# stdout and stderr files

# dependencies
# - stempel: https://github.com/RRZE-HPC/stempel
# - Kerncraft: https://github.com/RRZE-HPC/kerncraft
# - LIKWID: https://github.com/RRZE-HPC/likwid
# - (intel) compiler
# - python + python-sympy
# - grep, sed, awk, bc

# Stencil parameters:
# Described "named stencils" (based on not-stempel-generated code) as best as possible
# dimension: 2 or 3 (currently only 3D is supported)
DIM=3
# desired stencil radius: 1, 2, 3, ...
RADIUS=1
# stencil kind: 'star' or 'box'
KIND="star"
# coefficients: 'constant' or 'variable'
CONST="constant"
# weighting: 'isotropic', 'heterogeneous', 'homogeneous', 'point-symmetric'
WEIGHTING="isotropic"
# datatype: 'double', 'double _Complex' or 'float', 'float _Complex'
DATATYPE="double"

# If stencil is not generated, use STENCIL.
# This name must match a file in: ${INSPECT_DIR}/named_stencils/${STENCIL}.c
STENCIL="himeno"

# load modules (this is an example for the RRZE testcluster)
module load likwid/5.0-dev intel64/19.0up05 python/3.6-anaconda

STEMPEL_BINARY=~/.conda/envs/my/bin/stempel
KERNCRAFT_BINARY=~/.conda/envs/my/bin/kerncraft

INSPECT_DIR=~/dev/INSPECT
OUTPUT_DIR=~/dev/INSPECT/output

# turn specific parts on or off
DO_GRID_SCALING=1
DO_THREAD_SCALING=1
DO_SPACIAL_BLOCKING=0

# machine files
MACHINE_FILE=${INSPECT_DIR}/machine_files/BroadwellEP_E5-2697v4_CoD.yml
# MACHINE_FILE=${INSPECT_DIR}/machine_files/HaswellEP_E5-2695v3_CoD.yml
# MACHINE_FILE=${INSPECT_DIR}/machine_files/SkylakeSP_Gold-6148.yml
# MACHINE_FILE=${INSPECT_DIR}/machine_files/SkylakeSP_Gold-6148_512.yml
# MACHINE_FILE=${INSPECT_DIR}/machine_files/SkylakeSP_Gold-6148_SNC.yml

# needed for spatial blocking: counters for BroadEP2, HasEP1 and SkylakeSP1
COUNTER="CAS_COUNT_RD:MBOX4C1,CAS_COUNT_RD:MBOX6C0,CAS_COUNT_RD:MBOX2C1,CAS_COUNT_RD:MBOX3C0,CAS_COUNT_WR:MBOX0C1,CAS_COUNT_RD:MBOX5C1,L1D_REPLACEMENT:PMC0,CAS_COUNT_WR:MBOX5C0,CAS_COUNT_RD:MBOX0C0,CAS_COUNT_WR:MBOX6C1,L1D_M_EVICT:PMC2,CAS_COUNT_RD:MBOX7C1,CAS_COUNT_RD:MBOX1C1,CAS_COUNT_WR:MBOX4C0,CAS_COUNT_WR:MBOX2C0,CAS_COUNT_WR:MBOX1C0,CAS_COUNT_WR:MBOX3C1,CAS_COUNT_WR:MBOX7C0,L2_LINES_IN_ALL:PMC3,L2_TRANS_L2_WB:PMC1"

# needed for spatial blocking: counters for IvyBridge
#COUNTER="L1D_REPLACEMENT:PMC0,L2_LINES_OUT_DIRTY_ALL:PMC1,L1D_M_EVICT:PMC2,L2_LINES_IN_ALL:PMC3,CAS_COUNT_RD:MBOX4C1,CAS_COUNT_RD:MBOX6C0,CAS_COUNT_RD:MBOX2C1,CAS_COUNT_RD:MBOX3C0,CAS_COUNT_WR:MBOX0C1,CAS_COUNT_RD:MBOX5C1,CAS_COUNT_WR:MBOX5C0,CAS_COUNT_RD:MBOX0C0,CAS_COUNT_WR:MBOX6C1,CAS_COUNT_RD:MBOX7C1,CAS_COUNT_RD:MBOX1C1,CAS_COUNT_WR:MBOX4C0,CAS_COUNT_WR:MBOX2C0,CAS_COUNT_WR:MBOX1C0,CAS_COUNT_WR:MBOX3C1,CAS_COUNT_WR:MBOX7C0"

# **************************************************************************************************
# **************************************************************************************************
# ********** DONT CHANGE ANYTHING AFTER THIS LINE **************************************************
# **************************************************************************************************
# **************************************************************************************************

# FIX frequencies
ghz=$(grep clock ${MACHINE_FILE} | sed -e 's/clock: //' -e 's/ GHz//')
likwid-setFrequencies -t 0 -f ${ghz} --umin ${ghz} --umax ${ghz} -g performance

MACHINE=$(echo ${MACHINE_FILE} | sed -e 's/.*\///g' -e 's/.yml//')

ICC_VERSION=$(icc --version | head -n 1)

DATE=$(date +'%Y%m%d_%H%M%S')

if [[ "$STENCIL" != "" ]]; then
	NAME=$STENCIL
else
	NAME="${DIM}D_r${RADIUS}_${WEIGHTING}_${KIND}_${CONST}"
fi
FOLDER="${OUTPUT_DIR}/${NAME}/${MACHINE}_${DATE}"
mkdir -p ${FOLDER} && cd ${FOLDER}
mkdir data

echo ":: RUNNING: ${NAME} ${DATE} ${MACHINE}"

echo ":: GATHERING SYSTEM INFORMATION"
sh ${INSPECT_DIR}/scripts/Artifact-description/machine-state.sh >> data/system_info.txt

if [[ ${WEIGHTING} == "isotropic" ]]; then
	S_WEIGHTING=-i
elif [[ ${WEIGHTING} == "heterogeneous" ]]; then
	S_WEIGHTING=-e
elif [[ ${WEIGHTING} == "homogeneous" ]]; then
	S_WEIGHTING=-o
elif [[ ${WEIGHTING} == "point-symmetric" ]]; then
	S_WEIGHTING=-p
fi

COMPILER=$(cat ${MACHINE_FILE} | grep icc | sed 's/.*icc: /icc /')
STEMPEL_ARGS="gen -D ${DIM} -r ${RADIUS} -k ${KIND} -C ${CONST} ${S_WEIGHTING} -t \"${DATATYPE[@]}\""
# save all arguments
echo ":: SAVING ARGUMENTS"
if [[ "$STENCIL" != "" ]]; then
	echo {\$,$}STENCIL >> args.txt
fi
echo {\$,$}STEMPEL_ARGS >> args.txt
echo {\$,$}STEMPEL_BENCH_BLOCKING >> args.txt
echo {\$,$}MACHINE_FILE >> args.txt
echo {\$,$}DATE >> args.txt
echo {\$,$}ICC_VERSION >> args.txt
echo {\$,$}COMPILER >> args.txt
STEMPEL_ARGS=$(echo ${STEMPEL_ARGS} | sed 's/\(.*\)-t.*/\1/')

# generate stencil
echo ":: GENERATING STENCIL"
if [[ "$STENCIL" != "" ]]; then
	cp ${INSPECT_DIR}/named_stencils/${STENCIL}.c stencil.c
else
	${STEMPEL_BINARY} ${STEMPEL_ARGS} -t "${DATATYPE[@]}" --store stencil.c
fi

# ************************************************************************************************
# Grid Scaling
# ************************************************************************************************

# Layer Condition Analysis
${KERNCRAFT_BINARY} -p LC -m ${MACHINE_FILE} ./stencil.c -D . 100 -vvv --cores 1 --compiler icc --ignore-warnings > data/LC.txt

# L3 1D Layer Condition
LC_1D_L3=$(tail -n $(( $(cat data/LC.txt | wc -l) - $(grep -m 1 -n "Layer conditions for L3" data/LC.txt | sed 's/:.*//') +1 )) data/LC.txt | sed 's/\(<=\?\) \([0-9]*\).*/- \2/;' | head -n 5 | tail -n 1 | sed 's/ //g')
LC_1D_L3_N=$(python -c "import sympy;N=sympy.Symbol('N',positive=True);print(int(max(sympy.solvers.solve($(echo ${LC_1D_L3} | sed 's/[A-Z]/N/g'), N))*1.25/10)*10)")
LC_1D_L3_N_orig=${LC_1D_L3_N}

# L2 3D Layer Condition
LC_3D_L2=$(tail -n $(( $(cat data/LC.txt | wc -l) - $(grep -m 1 -n "Layer conditions for L2" data/LC.txt | sed 's/:.*//') +1 )) data/LC.txt | sed 's/\([<|<=]\) \([0-9]*\).*/- \2/;' | head -n 3 | tail -n 1 | sed 's/ //g')

echo ":: L3 1D Layer Condition * 1.25 = ${LC_1D_L3_N} (${LC_1D_L3})"

# get memory size per NUMA domain and adjust iteration size
MEM_PER_NUMA=$(likwid-topology | grep "Total memory" | head -n 1 | sed 's/.*://g; s/\..*MB//g;' | tr -d '[:space:]')

if [[ ${DATATYPE} == "float" ]]; then
	DT_SIZE=4
elif [[ ${DATATYPE} == "double" ]]; then
	DT_SIZE=8
elif [[ ${DATATYPE} == "float _Complex" ]]; then
	DT_SIZE=8
elif [[ ${DATATYPE} == "double _Complex" ]]; then
	DT_SIZE=16
fi

TMP_FACTOR=2
if [[ ${CONST} == "variable" ]]; then
	TMP_FACTOR=$(grep "W" stencil.c | head -n 1 | sed 's/\].*//; s/.*\[//')
fi

while [[ $((${LC_1D_L3_N}*${LC_1D_L3_N}*${LC_1D_L3_N}*${TMP_FACTOR}*${DT_SIZE}/1024/1024)) -gt ${MEM_PER_NUMA} ]]; do
	LC_1D_L3_N=$((${LC_1D_L3_N}-10))
done

if [[ $(( ${LC_1D_L3_N} * 10 )) -lt $(( ${LC_1D_L3_N_orig} * 15 )) ]]; then
	echo ":: ADJUSTED ITERATION SIZE DUE TO MEMORY REQUIREMENTS TO ${LC_1D_L3_N}^3"
fi

echo {\$,$}LC_1D_L3 >> args.txt
echo {\$,$}LC_1D_L3_N >> args.txt
echo {\$,$}LC_3D_L2 >> args.txt
echo {\$,$}MEM_PER_NUMA >> args.txt

if [[ ${DO_GRID_SCALING} == 1 ]]; then
	mkdir data/singlecore

	for (( size=10; size<=${LC_1D_L3_N}+10; size=size+10)); do
		echo -ne "\033[0K\r:: RUNNIG SINGLE CORE BENCHMARK N=${size}"
		KERNCRAFT_ARGS="-m ${MACHINE_FILE} ./stencil.c -D . ${size} -vvv --cores 1 --compiler icc --ignore-warnings"
		for cache_predictor in LC SIM; do
			${KERNCRAFT_BINARY} -p RooflineIACA -P ${cache_predictor} ${KERNCRAFT_ARGS} > data/singlecore/Roofline_${cache_predictor}_${size}.txt
			${KERNCRAFT_BINARY} -p ECM -P ${cache_predictor} ${KERNCRAFT_ARGS} > data/singlecore/ECM_${cache_predictor}_${size}.txt
		done
		${KERNCRAFT_BINARY} -p Benchmark -P LC ${KERNCRAFT_ARGS} > data/singlecore/Bench_${size}.txt
	done

	echo
fi

# ************************************************************************************************
# Threads Scaling
# ************************************************************************************************

if [[ ${DO_THREAD_SCALING} == 1 ]]; then
	cores=$(cat ${MACHINE_FILE} | grep "cores per socket" | sed 's/.*: //')

	mkdir data/scaling

	for (( threads = 1; threads <= ${cores}; threads++ )); do
		echo -ne "\033[0K\r:: RUNNIG THREAD SCALING BENCHMARK N=${LC_1D_L3_N} threads=${threads}"

		KERNCRAFT_ARGS="-m ${MACHINE_FILE} ./stencil.c -D . ${LC_1D_L3_N} -vvv --cores ${threads} --compiler icc --ignore-warnings"
		for pmodel in RooflineIACA ECM Benchmark; do
			${KERNCRAFT_BINARY} -p ${pmodel} -P LC ${KERNCRAFT_ARGS} >> data/scaling/${pmodel}_${LC_1D_L3_N}_${threads}.txt
		done
	done

	echo
fi

# ************************************************************************************************
# Cache Blocking
# ************************************************************************************************

if [[ ${DO_SPACIAL_BLOCKING} == 1 ]]; then
	export OMP_NUM_THREADS=1

	echo ":: GENERATING BENCHMARK CODE WITH BLOCKING"
	${STEMPEL_BINARY} bench stencil.c -m ${MACHINE_FILE} -b 2 --store
	sed -i 's/#pragma/\/\/#pragma/g' kernel.c
	sed -i 's/#pragma/\/\/#pragma/g' stencil_compilable.c

	# compile args
	STEMPEL_DIR=$(python -c 'import stempel; print(stempel.__file__)' | sed 's/__init__.py//')/headers
	COMPILE_ARGS="-qopenmp -DLIKWID_PERFMON $LIKWID_INC $LIKWID_LIB -I${STEMPEL_DIR}/ \
		${STEMPEL_DIR}/timing.c ${STEMPEL_DIR}/dummy.c stencil_compilable.c -o stencil -llikwid"

	echo {\$,$}STEMPEL_DIR >> args.txt
	echo {\$,$}COMPILE_ARGS >> args.txt

	# compile
	echo ":: COMPILING"
	${COMPILER} ${COMPILE_ARGS}
	mv stencil stencil_blocking

	mkdir data/blocking

	# run spatial blocking benchmark
	for blocking_case in L2 L3; do

		mkdir data/blocking/${blocking_case}_3D

		for (( size=10; size<=${LC_1D_L3_N}+10; size=size+10)); do

			if [[ ${blocking_case} == "L2" ]]; then
				# blocking factor  x direction 100 or size_x if it is smaller
				PB=$(python -c "import sympy;P=sympy.Symbol('P',positive=True);print(int(max(sympy.solvers.solve($(echo ${LC_3D_L2} | sed 's/N/16/g'), P))/10)*10)")
				PB=$(( ${PB} > ${size} ? ${size} : ${PB} ))

				# y direction: LC
				TMP=$(echo ${LC_3D_L2} | sed "s/P/${PB}/g")
				NB=$(python -c "import sympy;N=sympy.Symbol('N',positive=True);print(int(max(sympy.solvers.solve(${TMP}, N))*0.75))")
			elif [[ ${blocking_case} == "L3" ]]; then
				# blocking factor  x direction 100 or size_x if it is smaller
				PB=$(python -c "import sympy;P=sympy.Symbol('P',positive=True);print(int(max(sympy.solvers.solve($(echo ${LC_1D_L3} | sed 's/N/16/g'), P))/10)*10)")
				PB=$(( ${PB} > ${size} ? ${size} : ${PB} ))

				# y direction: LC
				TMP=$(echo ${LC_1D_L3} | sed "s/P/${PB}/g")
				NB=$(python -c "import sympy;N=sympy.Symbol('N',positive=True);print(int(max(sympy.solvers.solve(${TMP}, N))*0.75))")
			fi

			# blocking factor z direction, fixed factor: 16
			MB=16

			STEMPEL_BENCH_BLOCKING_value="${MB} ${NB} ${PB}"
			args="${size} ${size} ${size} ${STEMPEL_BENCH_BLOCKING_value}"
			echo ${blocking_case} ${args} >> args.txt

			echo -ne "\033[0K\r:: RUNNIG BENCHMARK ${blocking_case}-3D N=${args}"

			likwid-perfctr -f -o data/blocking/${blocking_case}_3D/likwid_${size}.txt -g ${COUNTER} -C S0:0 -m ./stencil_blocking ${args} >> data/blocking/${blocking_case}_3D/likwid_${size}_out.txt
		done
		echo
	done
fi

# ************************************************************************************************
# Postprocessing
# ************************************************************************************************

echo ":: POSTPROCESSING DATA"
sh ${INSPECT_DIR}/scripts/postprocess.sh ${INSPECT_DIR}/stencils
