# freshman-yolo-shape-detection

Early YOLO-based object detection and target-centering system developed under severe hardware constraints for our TEKNOFEST Unmanned Underwater Systems Competition Advanced Category.

# Freshman YOLO Shape Detection Project

⚠️ This project was developed during my **freshman year (1st year)** as a part of a TEKNOFEST-related study. The goal was not to build a production-ready vision system, but to explore object detection and target-centering concepts under **severe hardware constraints**.

---

## Project Overview

This project uses a YOLO-based(YOLOv8-tiny) object detection model to detect geometric shapes in a simulated underwater pool environment.

Instead of performing full  clasification continously, the system focuses on:
- Detecting objects in the frame
- Calculating their center position
- Waiting until the object aligns with the image center
- Capturing snapshots for further offline processing

This approach was chosen due to limited onboard computational resources.

---

## Motivation & System Design

The onboard vehicle hardware(NVIDIA Jetson Nano and STM32F407G-DISC1) was only capable of running object detection at approximately **3 FPS**, which made real-time classification unreliable.

To overcome this limitation, a lightweight strategy was implemented:

- Continous detection with minimal processing
- Center-based target selection
- Snapshot capture only when alignment conditions are met
- Offline labeling and further processing on a more capable system (Jetson Nano)

Although simple, this method proved to be **robust under constrained conditions** and significantly improved overall detection reliability.

---

## Detection and Target Centering

The system detects objects, calculates their center and captures snapshots only when alignment conditions are met.

<p align="center">
  <img src="example_detection.png" width="600">
</p>

*(Bounding box detection and center alignment visualization)*

---


## Demo Video

A short demonstration video showing the detection and centering logic is available below:

[▶ Watch demo video](assets/detection_demo.mp4)

---

## Classes

The model was trained to detect the following geometric shapes:

- Triangle
- Square
- Rectangle
- Circle
- Ellipse
- Pentagon
- Hexagon
- Rhombus
- Star
- Clover

---

## Performance Notes

- Development PC: ~24 FPS
- Onboard vehicle system: ~3 FPS

Due to these limitations, real-time classification was avoided in favor of snapshot-based processing.

---

## Limitations

- Original training dataset was not preserved
- Training pipeline is not fully reproducible
- Testing was performed only in a simulated environment(Made by my teammate on blender)
- Detecting accuracy was not fully optimized

These limitations are expected given the scope and timeframe of the project.

---

## What I Would Improve Today?

If i were to revisit this project today, i would focus on:

- Better dataset collection and versioning
- Explicit class label visualization for all detections
- Real-world underwater testing
- Cleaner and more modular code architecture
- Optimized inference pipeline for embedded hardware

---

## Technologies Used

- Python
- OpenCV
- YOLO (Ultralytics)
- NumPy

---

## Competition Note

This project was developed as a part of a TEKNOFEST competition entry and advanced to the **final stage**.

Official finalist documentation is available in this repository.

## Disclaimer

This repository represents an **early-stage learning project** and doest not reflect my technical level. It is shared for documentation and educational purposes.
