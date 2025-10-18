# Detecting AI-Generated Human Faces with Deep Learning

<img width="1920" height="851" alt="test3" src="https://github.com/user-attachments/assets/413c6fe2-0966-41ff-9f7a-b705f76b73be" />
This repository contains a deep learning project to classify images of human faces as either real or AI-generated. The project utilizes a pre-trained ResNet-50 model and provides a Gradio-based web interface for easy inference.

## Features
*   **Deep Learning Model**: Employs transfer learning with a ResNet-50 architecture for high-accuracy classification.
*   **AI Face Generation**: Includes a script to download a dataset of AI-generated faces from `thispersondoesnotexist.com`.
*   **Web-Based Demo**: An interactive Gradio application allows users to upload an image and receive a prediction.
*   **High Performance**: The model achieves over 93% accuracy in distinguishing between real and fake faces.

## Model Architecture

The classification model is built using PyTorch and leverages a pre-trained **ResNet-50** model (`ResNet50_Weights.DEFAULT`). The convolutional base of the model is frozen, and only the final fully connected layer (`fc`) is trained.

The custom classifier head consists of:
1.  Linear layer (2048 -> 1000)
2.  ReLU activation
3.  Linear layer (1000 -> 500)
4.  Dropout
5.  Final Linear layer (500 -> 2) for binary classification (Fake/Real).

The details of the model can be found in `model.py`.

## Dataset

The model is trained on a dataset of real and AI-generated human faces.

*   **AI-Generated Faces (`fake_faces`)**: These images are generated and downloaded using the script `generate_faces.py`. It fetches images from `thispersondoesnotexist.com`, checks for duplicates, and saves them.
*   **Real Faces (`real_faces`)**: This directory should be populated with a corresponding dataset of real human face images. The source for these images is not included in this repository.

## Getting Started

### 1. Installation

Clone the repository and install the required Python packages:

```bash
git clone https://github.com/brahmdi/Detecting-AI-Generated-Human-Faces-with-Deep-Learning.git
cd Detecting-AI-Generated-Human-Faces-with-Deep-Learning
pip install -r requirements.txt
```

### 2. Data Generation

To create the dataset of AI-generated faces, run the `generate_faces.py` script. This will download 10,000 unique images into a directory named `ai_faces_batch_1`. You can modify the script to download more batches or change the quantity.

```bash
python generate_faces.py
```

### 3. Running the Demo

The repository includes a Gradio application for real-time prediction. To run it, you need a trained model file named `best_model.pth` in the root directory. This file is generated after training the model on the dataset.

Once you have the `best_model.pth` file, launch the application:

```bash
python app.py
```

This will start a local web server. Open the provided URL in your browser to access the interface, where you can upload a face image and see the model's prediction and the time taken.

## Performance

The model was trained for 10 epochs. The training process was tracked with performance metrics for training, validation, and test sets. The model achieved a peak accuracy of **94.08%** on the test set.

Here are the results from the final training epoch:

| Metric    | Train   | Validation | Test    |
|-----------|---------|------------|---------|
| **Loss**  | 0.0767  | 0.2120     | 0.2023  |
| **Accuracy**| 97.14%  | 93.62%     | 93.66%  |

The full training history can be found in `results/training_results.json`.

## Repository Structure

```
.
├── app.py                  # Gradio web application for inference
├── generate_faces.py       # Script to download AI-generated faces
├── model.py                # Defines the ResNet-50 model architecture
├── requirements.txt        # Python dependencies
├── dataset/                # Directory for training data
│   ├── fake_faces/
│   └── real_faces/
└── results/
    └── training_results.json # Stored metrics from the training process

