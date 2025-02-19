#!/bin/bash
#SBATCH --job-name=no_text
#SBATCH --partition=gpu-preempt,gpu
#SBATCH --gres=gpu:1
#SBATCH --constraint=a100-80g|h100
#SBATCH --mem=80G
#SBATCH --time=2:00:00
#SBATCH --mail-type=ALL
#SBATCH --array=0-9

module load conda/latest
conda activate clipper

# Include models to evaluate here
ALIAS_LIST=(
    "princeton-nlp/Llama-3-8B-ProLong-512k-Base"
)

BATCH_SIZE=100
TOTAL_ROWS=1000
TOTAL_BATCHES=$((TOTAL_ROWS / BATCH_SIZE))  

ALIAS_INDEX=$(( SLURM_ARRAY_TASK_ID / TOTAL_BATCHES ))   
BATCH_ID=$(( SLURM_ARRAY_TASK_ID % TOTAL_BATCHES ))      
ALIAS=${ALIAS_LIST[$ALIAS_INDEX]}

START_INDEX=$((BATCH_ID * BATCH_SIZE))
END_INDEX=$((START_INDEX + BATCH_SIZE))

if [ $END_INDEX -gt $TOTAL_ROWS ]; then
    END_INDEX=$TOTAL_ROWS
fi

if [ $START_INDEX -ge $TOTAL_ROWS ]; then
    echo "START_INDEX ($START_INDEX) exceeds TOTAL_ROWS ($TOTAL_ROWS). Exiting."
    exit 0
fi

DATA_INPUT="test"     # Test file should be saved in data/benchmark/test.csv  

OUTPUT_DIR="../../data/benchmark/${DATA_INPUT}/$(echo $ALIAS | tr / _)"
mkdir -p "${OUTPUT_DIR}"
OUTPUT_FILE="$OUTPUT_DIR/output_${SLURM_ARRAY_TASK_ID}.csv"


echo "Total rows:                   $TOTAL_ROWS"
echo "Batch size:                   $BATCH_SIZE"
echo "Total batches (per model):    $TOTAL_BATCHES"
echo "SLURM_ARRAY_TASK_ID:          $SLURM_ARRAY_TASK_ID"
echo "Model index:                  $ALIAS_INDEX"
echo "Selected alias:               $ALIAS"
echo "Batch ID:                     $BATCH_ID"  
echo "Start, end row:               ${START_INDEX}, ${END_INDEX}"
echo "Output file:                  ${OUTPUT_FILE}"
echo "Data input:                   ${DATA_INPUT}"

case "$ALIAS" in
  *"prolong"*)
    echo "Running custom model"
    MODEL="custom"
    ;;
   *"princeton"*)
    echo "Running custom model"
    MODEL="custom"
    ;;
  *"qwen"*)
    echo "Running qwen model"
    MODEL="qwen"
    ;;
  *"o1-mini"*|*"gpt"*)
    echo "Running openai model"
    MODEL="openai"
    ;;
  *"gemini"*)
    echo "Running gemini model"
    MODEL="gemini"
    ;;
  *)
    echo "No recognized alias pattern, defaulting to openai"
    MODEL="openai"
    ;;
esac


python3 benchmark.py \
  --model "${MODEL}" \
  --model_dir "${ALIAS}" \
  --data_input "${DATA_INPUT}" \
  --data_output "${OUTPUT_DIR}/output_${BATCH_ID}.csv" \
  --start_row "${START_INDEX}" \
  --end_row "${END_INDEX}" \
  --chunking True \