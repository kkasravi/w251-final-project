# w251-final-project

## Using a vector database with chatgpt-retrieval-plugin 

See this [article](https://betterprogramming.pub/enhancing-chatgpt-with-infinite-external-memory-using-vector-database-and-chatgpt-retrieval-plugin-b6f4ea16ab8)


## High Level Pipeline

Collect images.
Use an object detection model (e.g., YOLO, Faster R-CNN, or Mask R-CNN) to detect and classify objects.
Convert object labels into a text description.
Fine-tune a GPT-4 language model on recipe data.
Input the text description into the fine-tuned GPT-4 model to generate a recipe and cooking instructions.

![Pipeline Diagram](pipeline.png)



