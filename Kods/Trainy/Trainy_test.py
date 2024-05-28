from ultralytics import YOLO

data_path = "data.yaml"

model_config = "yolov8n.yaml"

# Initialize the model
model = YOLO(model_config)

# Set training hyperparameters
hyperparameters = {
    "batch": -1,  # Adjusted batch size if your GPU can handle it
    "img_size": 640,  # Size of the images
    "epochs": 250,  # Number of epochs to train for
    "learning_rate": 0.01,  # Initial learning rate
    "cos_lr": True,  # Using cosine annealing learning rate scheduler
    "optimizer": 'AdamW',  # Change optimizer to AdamW
    "pretrained": True,  # Use a pretrained model
    "patience": 20,  # Early stopping patience
    "augment": True,  # Enable data augmentation
    "multi_scale": True,  # Enable training with images of different scales
    "rect": False,  # If True, keeps the aspect ratio the same during training
    "weight_decay": 0.0005,  # L2 regularization weight decay
    "amp": True,  # Use automatic mixed precision for faster training
    "conf": 0.3,  # Confidence threshold for predictions
    "iou_threshold": 0.7,  # IOU threshold for non-max suppression

}

model.train(
    data=data_path,
    epochs=hyperparameters['epochs'],
    batch=hyperparameters['batch'],
    imgsz=hyperparameters['img_size'],
    rect=hyperparameters['rect'],
    cos_lr=hyperparameters['cos_lr'],
    patience=hyperparameters['patience'],
    augment=hyperparameters['augment'],
    resume=False,
    device='',
    multi_scale=hyperparameters['multi_scale'],
    single_cls=False,
    optimizer=hyperparameters['optimizer'],
    workers=8,
    project='runs/train',
    name='exp',
    conf=hyperparameters['conf'],
)
