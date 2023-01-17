#!/bin/bash
#SBATCH --account=girirajan
#SBATCH --partition=girirajan
#SBATCH --job-name=encode_down
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=30
#SBATCH --time=400:0:0
#SBATCH --mem-per-cpu=4G
#SBATCH --chdir /data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/src
#SBATCH -o /data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/slurm/logs/out_encode_down_%a.log
#SBATCH -e /data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/slurm/logs/err_encode_down_%a.log
#SBATCH --nodelist=qingyu
#SBATCH --array 3

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/data5/deepro/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/data5/deepro/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/data5/deepro/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/data5/deepro/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

conda activate encode

echo `date` starting job on $HOSTNAME
LINE=$(sed -n "$SLURM_ARRAY_TASK_ID"p /data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/slurm/files/0_encode_down.txt)

echo $LINE
python /data5/deepro/starrseq/papers/reproducibility/0_in-house_dataset/src/0_download_encode_data.py $LINE 

echo `date` ending job
