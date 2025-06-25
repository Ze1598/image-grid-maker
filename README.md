
# 🖼️ Image Collage Generator & Resizer

A powerful and intuitive web application for creating beautiful grid-based image collages and resizing individual images. Upload multiple images to create stunning collages or resize single images with preset scale factors.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PIL](https://img.shields.io/badge/Pillow-000000?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

### 📊 Image Collage Generator
- 📤 **Multi-Image Upload**: Support for PNG, JPG, and JPEG formats
- 🔄 **Advanced Image Reordering**: Complete control over image arrangement:
  - Manual position swapping between any two positions
  - Shuffle all images randomly
  - Reverse order instantly
  - Reset to original upload order
- 🎛️ **Customizable Layout**: 
  - Adjustable grid columns (1-10 per row)
  - Variable image resize factor (10%-100%)
  - Real-time grid preview with statistics
- 🖼️ **Smart Image Processing**:
  - Automatic aspect ratio preservation
  - Seamless collage creation without whitespace
  - Support for various image formats with transparency handling
- 💾 **High-Quality Export**: Download collages as PNG files

### 🔍 Single Image Resizer
- 🖼️ **Individual Image Processing**: Upload and resize single images
- ⚡ **Preset Scale Factors**: Choose from 5 predefined options:
  - 0.25x (Quarter size)
  - 0.5x (Half size) 
  - 1x (Original size)
  - 2x (Double size)
  - 4x (Quadruple size)
- 👀 **Before/After Preview**: Side-by-side comparison of original and resized images
- 📏 **Dimension Display**: Real-time calculation and display of new image dimensions
- 💾 **Smart Downloads**: Automatically named files with scale factor indicators

## 🚀 Quick Start

### Run on Replit (Recommended)
1. Fork this repository on Replit
2. Click the "Run" button
3. Open the generated URL to access the app

### Local Installation
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

### Creating Image Collages
1. **Navigate to Image Collage Tab**: Click on "📊 Image Collage"
2. **Configure Settings**: 
   - Adjust the resize factor percentage (10%-100%)
   - Set the number of columns per row (1-10)
3. **Upload Images**: Select multiple image files (PNG, JPG, JPEG)
4. **Reorder Images** (Optional):
   - View thumbnail previews with position indicators
   - Use shuffle, reverse, or manual position swapping
   - Real-time grid preview shows layout changes
5. **Generate Collage**: Click "🚀 Create Collage"
6. **Download**: Save your collage as a high-quality PNG

### Resizing Single Images
1. **Navigate to Single Image Resize Tab**: Click on "🔍 Single Image Resize"
2. **Upload Image**: Select a single image file
3. **Choose Scale Factor**: Pick from 5 preset options (0.25x to 4x)
4. **Preview Results**: View original and resized versions side-by-side
5. **Apply Resize**: Click "🔄 Apply Resize" to process
6. **Download**: Save the resized image with automatic filename

## 🛠️ Technical Details

### Dependencies
- **Streamlit** (≥1.46.0): Web application framework
- **Pillow (PIL)**: Image processing and manipulation
- **NumPy** (≥2.3.1): Numerical operations for image arrays

### Architecture
- **Frontend**: Streamlit-based responsive web interface with tabbed navigation
- **Backend**: Python image processing with PIL
- **Deployment**: Configured for Replit's autoscale platform

### Key Functions
- `resize_image()`: Maintains aspect ratios while scaling images
- `resize_single_image()`: Dedicated function for individual image resizing
- `create_collage()`: Generates seamless grid layouts
- `calculate_grid_size()`: Optimizes grid dimensions
- `validate_image()`: Comprehensive image validation and error handling

## 📱 Interface Overview

### Tabbed Navigation
- **📊 Image Collage**: Multi-image collage creation
- **🔍 Single Image Resize**: Individual image resizing

### Image Collage Tab
- **Settings Section**: 
  - Resize factor slider (10%-100%)
  - Grid columns selector (1-10)
  - Real-time grid preview with metrics
- **Upload Panel**: 
  - Multi-file upload with progress tracking
  - Image validation and error reporting
  - Interactive thumbnail reordering controls
- **Generation Panel**: 
  - Collage creation and preview
  - High-quality PNG download

### Single Image Resize Tab
- **Upload Section**: Single file upload with validation
- **Scale Selection**: 5 preset scale factors with dimension preview
- **Preview Section**: Side-by-side before/after comparison
- **Download**: Smart filename generation with scale indicators

## 🎨 Supported Formats

- **Input**: PNG, JPG, JPEG (both tabs)
- **Output**: High-quality PNG files
- **Transparency**: Automatic handling with white background conversion
- **Large Images**: Automatic thumbnail generation for display optimization

## 🔧 Configuration

- **Default Port**: 5000 (Replit-optimized)
- **Server Mode**: Headless operation for web deployment
- **Image Processing**: Lanczos resampling for high-quality results
- **File Validation**: Comprehensive error handling and user feedback

## 📊 Grid Layout Intelligence

The collage generator automatically calculates optimal grid dimensions:
- **Smart Layouts**: Balanced rows and columns based on image count
- **Custom Override**: Manual column specification available
- **Real-time Preview**: Live statistics showing grid dimensions and settings
- **Flexible Arrangement**: Support for 1-100+ images in customizable grids

## 💡 Pro Tips

### For Collages:
- Use consistent image orientations for best results
- Experiment with different resize factors to optimize file size vs. quality
- Reorder images to create visual flow and balance
- Preview grid layout before generating to avoid surprises

### For Single Images:
- Check dimension previews before applying resize
- Use 1x setting to convert formats without resizing
- Larger scale factors work best with high-resolution source images
- Downloaded files include scale factor in filename for easy organization

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the application.

## 📄 License

This project is open source and available under standard terms.

---

Made with ❤️ using Streamlit and Python | Optimized for Replit deployment
