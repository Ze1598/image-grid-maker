# Image Collage Generator - Replit.md

## Overview

This is a Streamlit-based web application designed to create image collages. The application allows users to upload multiple images and automatically arranges them in an optimal grid layout. The project is built using Python 3.11 with Streamlit as the main framework for the web interface.

## System Architecture

The application follows a simple single-file architecture pattern:

- **Frontend**: Streamlit web interface for user interaction
- **Backend**: Python-based image processing using PIL (Pillow) and NumPy
- **Deployment**: Configured for Replit's autoscale deployment target

The architecture emphasizes simplicity and ease of use, with all core functionality contained in a single `app.py` file.

## Key Components

### Core Application (`app.py`)
- **Image Processing Functions**: 
  - `calculate_grid_size()`: Determines optimal grid dimensions for image arrangement
  - `resize_image()`: Handles image resizing while maintaining aspect ratios
  - `create_collage()`: Main function for generating the final collage (currently incomplete)

- **Image Format Handling**: Supports multiple image formats including RGBA, LA, P, and RGB with automatic conversion

### Configuration Files
- **`.replit`**: Defines the Python 3.11 runtime environment and Streamlit deployment configuration
- **`pyproject.toml`**: Specifies project dependencies (NumPy and Streamlit)
- **`.streamlit/config.toml`**: Configures Streamlit server settings for headless operation

## Data Flow

1. **Image Upload**: Users upload images through the Streamlit interface
2. **Image Processing**: Each image is processed and resized to standardized dimensions (200x200 pixels)
3. **Grid Calculation**: The system calculates optimal grid dimensions based on the number of uploaded images
4. **Collage Generation**: Images are arranged in the calculated grid layout (feature appears incomplete)
5. **Output**: The final collage is displayed to the user

## External Dependencies

- **Streamlit (>=1.46.0)**: Web application framework for the user interface
- **NumPy (>=2.3.1)**: Numerical computing library for image array operations
- **Pillow (PIL)**: Image processing library for format conversion and manipulation
- **Built-in Libraries**: 
  - `io`: For handling byte streams
  - `math`: For grid size calculations
  - `zipfile`: For potential batch image handling

## Deployment Strategy

The application is configured for deployment on Replit's platform:

- **Runtime**: Python 3.11 with Nix package management
- **Port Configuration**: Runs on port 5000
- **Deployment Target**: Autoscale for handling variable traffic
- **Server Mode**: Headless operation suitable for web deployment

The deployment uses Streamlit's built-in server capabilities with custom port binding to integrate with Replit's infrastructure.

## Changelog

- June 25, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.