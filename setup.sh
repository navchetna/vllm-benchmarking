#!/bin/bash

# Function to print usage information
print_usage() {
    echo "Usage: $0 [-m <model-name>] [-t <huggingface-api-token>]"
    echo "Example: $0 -m Qwen/Qwen2.5-Coder-7B-Instruct -t <huggingface-api-token>"
}

while getopts ":m:t:" opt; do
    case $opt in
        m)
            model=$OPTARG
            ;;
        t)
            token=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            print_usage
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            print_usage
            exit 1
            ;;
    esac
done

# Set default values if not provided
if [ -z "$model" ]; then
    model=Qwen/Qwen2.5-Coder-7B-Instruct
fi

if [ -z "$token" ]; then
    token=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
fi

echo "Running 2 vllm containers for model: $model, token: $token and ha-proxy"
echo "HA Proxy listenting at http://localhost:4000. Would auto-redirect request to vllm containers"

# stop and remove existing containers
# and pass model name as environment variable



HUGGINGFACEHUB_API_TOKEN=$token MODEL=$model docker compose -f /root/kubernetes_files/thebeginner86/vllm-benchmark/compose.yaml down
HUGGINGFACEHUB_API_TOKEN=$token MODEL=$model docker compose -f /root/kubernetes_files/thebeginner86/vllm-benchmark/compose.yaml up -d

echo "Sucessfully started vllm containers and HA Proxy"


