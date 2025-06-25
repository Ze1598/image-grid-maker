import streamlit as st
import io
import math
import zipfile
from PIL import Image
import numpy as np

def calculate_grid_size(num_images):
    """Calculate optimal grid dimensions for given number of images"""
    if num_images == 0:
        return 0, 0
    elif num_images == 1:
        return 1, 1
    else:
        # Calculate square root and round up for rows
        sqrt_num = math.sqrt(num_images)
        rows = math.ceil(sqrt_num)
        cols = math.ceil(num_images / rows)
        return rows, cols

def resize_image(image, target_size=(200, 200)):
    """Resize image to target size while maintaining aspect ratio"""
    # Convert to RGB if necessary (for PNG with transparency)
    if image.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize with maintaining aspect ratio
    image.thumbnail(target_size, Image.Resampling.LANCZOS)
    
    # Create a new image with exact target size and paste the resized image in center
    new_image = Image.new('RGB', target_size, (255, 255, 255))
    x = (target_size[0] - image.width) // 2
    y = (target_size[1] - image.height) // 2
    new_image.paste(image, (x, y))
    
    return new_image

def create_collage(images, target_size=(200, 200)):
    """Create a grid collage from list of images"""
    if not images:
        return None
    
    num_images = len(images)
    rows, cols = calculate_grid_size(num_images)
    
    # Resize all images
    resized_images = []
    for img in images:
        resized_img = resize_image(img, target_size)
        resized_images.append(resized_img)
    
    # Fill empty slots with white images if needed
    total_slots = rows * cols
    while len(resized_images) < total_slots:
        white_image = Image.new('RGB', target_size, (255, 255, 255))
        resized_images.append(white_image)
    
    # Create the collage
    collage_width = cols * target_size[0]
    collage_height = rows * target_size[1]
    collage = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))
    
    for i, img in enumerate(resized_images):
        row = i // cols
        col = i % cols
        x = col * target_size[0]
        y = row * target_size[1]
        collage.paste(img, (x, y))
    
    return collage

def validate_image(uploaded_file):
    """Validate if uploaded file is a valid image"""
    try:
        image = Image.open(uploaded_file)
        # Verify it's a valid image by loading it
        image.verify()
        # Reset file pointer after verify
        uploaded_file.seek(0)
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    st.set_page_config(
        page_title="Image Collage Generator",
        page_icon="🖼️",
        layout="wide"
    )
    
    st.title("🖼️ Image Collage Generator")
    st.markdown("Upload multiple images to create a beautiful grid collage!")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        
        # Image size settings
        st.subheader("Image Size")
        img_width = st.slider("Width (pixels)", 100, 500, 200, 50)
        img_height = st.slider("Height (pixels)", 100, 500, 200, 50)
        target_size = (img_width, img_height)
        
        # Grid preview
        if 'uploaded_images' in st.session_state and st.session_state.uploaded_images:
            num_images = len(st.session_state.uploaded_images)
            rows, cols = calculate_grid_size(num_images)
            st.subheader("Grid Preview")
            st.write(f"📊 Grid: {rows} × {cols}")
            st.write(f"📸 Images: {num_images}")
            st.write(f"📐 Final size: {cols * img_width} × {rows * img_height} pixels")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Images")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose image files",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True,
            help="Select multiple PNG, JPG, or JPEG files"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} files uploaded successfully!")
            
            # Validate and process images
            valid_images = []
            invalid_files = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")
                progress_bar.progress((i + 1) / len(uploaded_files))
                
                is_valid, error_msg = validate_image(uploaded_file)
                if is_valid:
                    try:
                        image = Image.open(uploaded_file)
                        valid_images.append(image)
                    except Exception as e:
                        invalid_files.append(f"{uploaded_file.name}: {str(e)}")
                else:
                    invalid_files.append(f"{uploaded_file.name}: {error_msg}")
            
            status_text.text("Processing complete!")
            progress_bar.empty()
            status_text.empty()
            
            # Store valid images in session state
            st.session_state.uploaded_images = valid_images
            
            # Show validation results
            if valid_images:
                st.success(f"✅ {len(valid_images)} images processed successfully!")
            
            if invalid_files:
                st.error("❌ Some files could not be processed:")
                for error in invalid_files:
                    st.write(f"• {error}")
            
            # Show image thumbnails
            if valid_images:
                st.subheader("📋 Uploaded Images Preview")
                
                # Display thumbnails in a grid
                num_cols = 4
                for i in range(0, len(valid_images), num_cols):
                    cols = st.columns(num_cols)
                    for j, col in enumerate(cols):
                        if i + j < len(valid_images):
                            with col:
                                # Create thumbnail for preview
                                thumb = valid_images[i + j].copy()
                                thumb.thumbnail((150, 150), Image.Resampling.LANCZOS)
                                st.image(thumb, caption=f"Image {i + j + 1}")
    
    with col2:
        st.header("🎨 Generate Collage")
        
        if 'uploaded_images' in st.session_state and st.session_state.uploaded_images:
            if st.button("🚀 Create Collage", type="primary", use_container_width=True):
                with st.spinner("Creating your collage..."):
                    try:
                        # Create the collage
                        collage = create_collage(st.session_state.uploaded_images, target_size)
                        
                        if collage:
                            st.session_state.collage = collage
                            st.success("🎉 Collage created successfully!")
                        else:
                            st.error("❌ Failed to create collage")
                    
                    except Exception as e:
                        st.error(f"❌ Error creating collage: {str(e)}")
            
            # Display the collage if it exists
            if 'collage' in st.session_state:
                st.subheader("🖼️ Your Collage")
                st.image(st.session_state.collage, caption="Generated Collage", use_container_width=True)
                
                # Download button
                try:
                    # Convert collage to bytes
                    img_buffer = io.BytesIO()
                    st.session_state.collage.save(img_buffer, format='PNG')
                    img_bytes = img_buffer.getvalue()
                    
                    st.download_button(
                        label="💾 Download Collage",
                        data=img_bytes,
                        file_name="image_collage.png",
                        mime="image/png",
                        type="primary",
                        use_container_width=True
                    )
                
                except Exception as e:
                    st.error(f"❌ Error preparing download: {str(e)}")
        
        else:
            st.info("👆 Upload images first to generate a collage")
    
    # Instructions
    with st.expander("ℹ️ How to use this app"):
        st.markdown("""
        1. **Upload Images**: Click on the upload area and select multiple image files (PNG, JPG, JPEG)
        2. **Adjust Settings**: Use the sidebar to customize image size and preview the grid layout
        3. **Generate Collage**: Click the "Create Collage" button to generate your grid collage
        4. **Download**: Save your collage as a PNG file using the download button
        
        **Tips**:
        - The app automatically calculates the best grid layout based on the number of images
        - Images are resized to maintain consistent appearance
        - Large images are automatically downsized to improve performance
        - The collage maintains the aspect ratio of your chosen dimensions
        """)

if __name__ == "__main__":
    main()
