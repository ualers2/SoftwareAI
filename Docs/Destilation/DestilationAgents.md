# Agent Distillation

Agent distillation is a technique (mirrored by OpenAI's Model Distillation technique) that allows you to improve the performance of lower-capacity Agents by learning from higher-capacity Agents.

##Overview

`Agent Distillation` allows you to use the outputs of a highly educated and file-savvy Agent to fine-tune a lower-capacity Agent, allowing it to achieve similar performance on a specific task, but allowing it after harvesting a large volume of outputs training a model for inference on a GPU
**Latency**: 
   - This process can significantly reduce cost and latency as smaller models are typically more efficient.

**Training a model for inference on GPU**: 
   - After collecting a large volume of outputs, training a model for GPU inference based on the outputs can be done 
    with base models like `qwen:0.5b` and `ollama:1b`
   - This process can reduce the cost of the machine, which means that we will only spend on GPU energy

## How It Works
The distillation process follows the following steps:

1. **Output Storage**: 
   - Store high-quality output from a highly capable Agent. this can be done using the `UsageDestillation` parameter in the SoftwareAI Editor under the `Distillation Settings` category

2. **Training**:
   - View the stored conclusions you have stored from the agent by selecting `Distillation Settings` under `Distillation Settings` 
   - Use the agent's conclusions to adjust the smaller agent.