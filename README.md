
# 🖼️ Image Collage Generator

A beautiful and intuitive web application for creating grid-based image collages. Upload multiple images and automatically arrange them in customizable layouts with full control over ordering and sizing.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PIL](https://img.shields.io/badge/Pillow-000000?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

- 📤 **Multi-Image Upload**: Support for PNG, JPG, and JPEG formats
- 🔄 **Image Reordering**: Drag-and-drop style reordering with multiple options:
  - Manual position swapping
  - Shuffle all images
  - Reverse order
  - Reset to original order
- 🎛️ **Customizable Layout**: 
  - Adjustable grid columns (1-10 per row)
  - Variable image resize factor (10%-100%)
  - Real-time grid preview
- 🖼️ **Smart Image Processing**:
  - Automatic aspect ratio preservation
  - Seamless collage creation without whitespace
  - Support for various image formats with transparency handling
- 💾 **Easy Export**: Download your collage as a high-quality PNG file

## 🚀 Quick Start

### Option 1: Run on Replit (Recommended)
1. Fork this repository on Replit
2. Click the "Run" button
3. Open the generated URL to access the app

### Option 2: Local Installation
```bash
# Clone the repository
git clone <repository-url>
cd image-collage-generator

# Install dependencies
pip install streamlit pillow numpy

# Run the application
streamlit run app.py --server.port 5000
```

## 🎯 How to Use

1. **Upload Images**: Click the upload area and select multiple image files
2. **Customize Settings**: 
   - Adjust the resize factor using the slider (default: 45%)
   - Set the number of columns per row (default: 3)
3. **Reorder Images** (Optional):
   - Use the preview thumbnails to see current order
   - Shuffle, reverse, or manually move images to desired positions
4. **Generate Collage**: Click "Create Collage" to generate your grid
5. **Download**: Save your collage using the download button

## 🛠️ Technical Details

### Dependencies
- **Streamlit** (≥1.46.0): Web application framework
- **Pillow (PIL)**: Image processing and manipulation
- **NumPy** (≥2.3.1): Numerical operations for image arrays

### Architecture
- **Frontend**: Streamlit-based responsive web interface
- **Backend**: Python image processing with PIL
- **Deployment**: Configured for Replit's autoscale platform

### Key Functions
- `resize_image()`: Maintains aspect ratios while scaling images
- `create_collage()`: Generates seamless grid layouts
- `calculate_grid_size()`: Optimizes grid dimensions
- Image validation and format conversion

## 📱 Interface Overview

### Left Panel - Image Upload & Management
- File upload with progress tracking
- Image validation and error reporting
- Thumbnail preview with reordering controls
- Real-time position indicators

### Right Panel - Collage Generation
- Grid layout preview
- Collage creation and display
- Download functionality

### Sidebar - Settings
- Resize factor slider
- Grid columns selector
- Live preview statistics

## 🎨 Supported Formats

- **Input**: PNG, JPG, JPEG
- **Output**: High-quality PNG
- **Transparency**: Automatic handling with white background conversion

## 🔧 Configuration

The app runs on port 5000 by default and is configured for headless operation suitable for web deployment.

## 📄 License

This project is open source and available under standard terms.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the application.

---

Made with ❤️ using Streamlit and Python
