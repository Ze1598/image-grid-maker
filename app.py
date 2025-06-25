import streamlit as st
import io
import math
import zipfile
from PIL import Image
import numpy as np

def calculate_grid_size(num_images, cols_per_row=None):
    """Calculate grid dimensions for given number of images"""
    if num_images == 0:
        return 0, 0
    elif num_images == 1:
        return 1, 1
    else:
        if cols_per_row:
            # Use specified columns per row
            cols = cols_per_row
            rows = math.ceil(num_images / cols)
        else:
            # Calculate square root and round up for rows (default behavior)
            sqrt_num = math.sqrt(num_images)
            rows = math.ceil(sqrt_num)
            cols = math.ceil(num_images / rows)
        return rows, cols

def resize_image(image, scale_factor=0.45):
    """Resize image by scale factor while maintaining aspect ratio"""
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
    
    # Calculate new size based on scale factor
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    
    # Resize image maintaining aspect ratio
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return resized_image

def create_collage(images, scale_factor=0.45, cols_per_row=None):
    """Create a grid collage from list of images without whitespace"""
    if not images:
        return None
    
    num_images = len(images)
    rows, cols = calculate_grid_size(num_images, cols_per_row)
    
    # Resize all images
    resized_images = []
    for img in images:
        resized_img = resize_image(img, scale_factor)
        resized_images.append(resized_img)
    
    # Calculate collage dimensions based on actual image sizes
    if resized_images:
        # Get the maximum width and height from all resized images
        max_width = max(img.width for img in resized_images)
        max_height = max(img.height for img in resized_images)
        
        # Create the collage without any padding
        collage_width = cols * max_width
        collage_height = rows * max_height
        collage = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))
        
        for i, img in enumerate(resized_images):
            row = i // cols
            col = i % cols
            x = col * max_width
            y = row * max_height
            collage.paste(img, (x, y))
        
        return collage
    
    return None

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

def resize_single_image(image, scale_factor):
    """Resize a single image by the specified scale factor"""
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
    
    # Calculate new size based on scale factor
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    
    # Resize image maintaining aspect ratio
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return resized_image

def main():
    st.set_page_config(
        page_title="Image Collage Generator & Resizer",
        page_icon="🖼️",
        layout="wide"
    )
    
    st.title("🖼️ Image Collage Generator & Resizer")
    st.markdown("Upload multiple images to create a beautiful grid collage, or resize a single image!")
    
    # Add tabs for different functionalities
    tab1, tab2 = st.tabs(["📊 Image Collage", "🔍 Single Image Resize"])
    
    with tab2:
        st.header("🔍 Single Image Resize")
        st.markdown("Upload a single image and resize it with predefined scale factors.")
        
        # File uploader for single image
        single_image_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=False,
            key="single_image_uploader",
            help="Select a PNG, JPG, or JPEG file"
        )
        
        if single_image_file:
            # Validate and process the image
            is_valid, error_msg = validate_image(single_image_file)
            
            if is_valid:
                try:
                    original_image = Image.open(single_image_file)
                    
                    # Display original image info
                    st.success(f"✅ Image uploaded successfully!")
                    st.write(f"**Original dimensions:** {original_image.width} × {original_image.height} pixels")
                    
                    # Scale factor selection
                    scale_options = {
                        "0.25x (Quarter size)": 0.25,
                        "0.5x (Half size)": 0.5,
                        "1x (Original size)": 1.0,
                        "2x (Double size)": 2.0,
                        "4x (Quadruple size)": 4.0
                    }
                    
                    selected_scale_label = st.selectbox(
                        "Select resize factor:",
                        options=list(scale_options.keys()),
                        index=2  # Default to 1x (original size)
                    )
                    
                    selected_scale = scale_options[selected_scale_label]
                    
                    # Calculate and display new dimensions
                    new_width = int(original_image.width * selected_scale)
                    new_height = int(original_image.height * selected_scale)
                    st.write(f"**New dimensions:** {new_width} × {new_height} pixels")
                    
                    # Create two columns for before/after display
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Original Image")
                        # Create thumbnail for display if image is too large
                        display_original = original_image.copy()
                        if display_original.width > 400 or display_original.height > 400:
                            display_original.thumbnail((400, 400), Image.Resampling.LANCZOS)
                        st.image(display_original, caption=f"Original: {original_image.width}×{original_image.height}")
                    
                    with col2:
                        st.subheader("Resized Image")
                        if st.button("🔄 Apply Resize", type="primary"):
                            with st.spinner("Resizing image..."):
                                try:
                                    resized_image = resize_single_image(original_image, selected_scale)
                                    st.session_state.resized_single_image = resized_image
                                    st.success("✅ Image resized successfully!")
                                except Exception as e:
                                    st.error(f"❌ Error resizing image: {str(e)}")
                        
                        # Display resized image if it exists
                        if 'resized_single_image' in st.session_state:
                            resized_img = st.session_state.resized_single_image
                            # Create thumbnail for display if image is too large
                            display_resized = resized_img.copy()
                            if display_resized.width > 400 or display_resized.height > 400:
                                display_resized.thumbnail((400, 400), Image.Resampling.LANCZOS)
                            st.image(display_resized, caption=f"Resized: {resized_img.width}×{resized_img.height}")
                            
                            # Download button for resized image
                            try:
                                img_buffer = io.BytesIO()
                                resized_img.save(img_buffer, format='PNG')
                                img_bytes = img_buffer.getvalue()
                                
                                # Create filename with scale factor
                                original_name = single_image_file.name.rsplit('.', 1)[0]
                                scale_suffix = selected_scale_label.split(' ')[0].replace('.', '_')
                                filename = f"{original_name}_{scale_suffix}.png"
                                
                                st.download_button(
                                    label="💾 Download Resized Image",
                                    data=img_bytes,
                                    file_name=filename,
                                    mime="image/png",
                                    type="primary"
                                )
                            except Exception as e:
                                st.error(f"❌ Error preparing download: {str(e)}")
                
                except Exception as e:
                    st.error(f"❌ Error processing image: {str(e)}")
            else:
                st.error(f"❌ Invalid image file: {error_msg}")
    
    with tab1:
    
    # Sidebar for settings
        with st.sidebar:
        st.header("Settings")
        
        # Image resize settings
        st.subheader("Image Resize")
        scale_factor = st.slider(
            "Resize Factor (%)", 
            min_value=10, 
            max_value=100, 
            value=45, 
            step=5,
            help="Percentage to resize images while maintaining aspect ratio"
        ) / 100.0
        
        # Grid layout settings
        st.subheader("Grid Layout")
        cols_per_row = st.slider(
            "Columns per Row", 
            min_value=1, 
            max_value=10, 
            value=3, 
            step=1,
            help="Number of images to display per row in the collage"
        )
        
        # Grid preview
        if 'uploaded_images' in st.session_state and st.session_state.uploaded_images:
            num_images = len(st.session_state.uploaded_images)
            rows, cols = calculate_grid_size(num_images, cols_per_row)
            st.subheader("Grid Preview")
            st.write(f"📊 Grid: {rows} × {cols}")
            st.write(f"📸 Images: {num_images}")
            st.write(f"🔄 Resize: {int(scale_factor * 100)}%")
    
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
            
            # Show image thumbnails with reordering
            if valid_images:
                st.subheader("📋 Uploaded Images Preview")
                st.markdown("**💡 Tip:** Use the controls below to reorder your images before creating the collage")
                
                # Initialize image order in session state if not exists
                if 'image_order' not in st.session_state or len(st.session_state.image_order) != len(valid_images):
                    st.session_state.image_order = list(range(len(valid_images)))
                
                # Reordering controls
                col_controls = st.columns([1, 1, 1, 2])
                with col_controls[0]:
                    if st.button("🔄 Reset Order"):
                        st.session_state.image_order = list(range(len(valid_images)))
                        st.rerun()
                
                with col_controls[1]:
                    if st.button("🔀 Shuffle"):
                        import random
                        random.shuffle(st.session_state.image_order)
                        st.rerun()
                
                with col_controls[2]:
                    if st.button("↩️ Reverse"):
                        st.session_state.image_order.reverse()
                        st.rerun()
                
                # Manual reordering interface
                st.markdown("**Move Images:**")
                move_cols = st.columns([2, 1, 2, 1])
                with move_cols[0]:
                    move_from = st.selectbox("Move image from position:", 
                                           options=range(1, len(valid_images) + 1),
                                           format_func=lambda x: f"Position {x}")
                with move_cols[1]:
                    st.markdown("<br>", unsafe_allow_html=True)
                    move_button = st.button("➡️")
                with move_cols[2]:
                    move_to = st.selectbox("To position:", 
                                         options=range(1, len(valid_images) + 1),
                                         format_func=lambda x: f"Position {x}")
                
                if move_button and move_from != move_to:
                    # Convert to 0-based indexing
                    from_idx = move_from - 1
                    to_idx = move_to - 1
                    
                    # Remove the item from its current position
                    item = st.session_state.image_order.pop(from_idx)
                    # Insert it at the new position
                    st.session_state.image_order.insert(to_idx, item)
                    st.rerun()
                
                # Display thumbnails in current order
                ordered_images = [valid_images[i] for i in st.session_state.image_order]
                
                num_cols = 4
                for i in range(0, len(ordered_images), num_cols):
                    cols = st.columns(num_cols)
                    for j, col in enumerate(cols):
                        if i + j < len(ordered_images):
                            with col:
                                # Create thumbnail for preview
                                thumb = ordered_images[i + j].copy()
                                thumb.thumbnail((150, 150), Image.Resampling.LANCZOS)
                                original_idx = st.session_state.image_order[i + j]
                                st.image(thumb, caption=f"Pos {i + j + 1} (Original #{original_idx + 1})")
    
    with col2:
        st.header("🎨 Generate Collage")
        
        if 'uploaded_images' in st.session_state and st.session_state.uploaded_images:
            if st.button("🚀 Create Collage", type="primary", use_container_width=True):
                with st.spinner("Creating your collage..."):
                    try:
                        # Get images in the current order
                        if 'image_order' in st.session_state:
                            ordered_images = [st.session_state.uploaded_images[i] for i in st.session_state.image_order]
                        else:
                            ordered_images = st.session_state.uploaded_images
                        
                        # Create the collage
                        collage = create_collage(ordered_images, scale_factor, cols_per_row)
                        
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
    
    # General instructions for both features
    with st.expander("ℹ️ About this app"):
        st.markdown("""
        This app provides two main features:
        
        **📊 Image Collage**: Create beautiful grid layouts from multiple images
        - Upload multiple images and arrange them in customizable grids
        - Reorder images with drag-and-drop style controls
        - Adjust grid layout and image sizes
        
        **🔍 Single Image Resize**: Resize individual images with preset scale factors
        - Upload a single image and choose from 5 scale options
        - Preview original and resized versions side by side
        - Download the resized image in high quality
        """)

if __name__ == "__main__":
    main()
