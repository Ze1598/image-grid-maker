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
    
    # Resize image
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return resized_image

def main():
    st.set_page_config(
        page_title="Image Collage Generator",
        page_icon="🖼️",
        layout="wide"
    )
    
    st.title("🖼️ Image Collage Generator")
    st.markdown("Upload multiple images to create a beautiful grid collage, or resize a single image!")
    
    # App mode selection
    app_mode = st.radio(
        "Choose mode:",
        ["🖼️ Create Collage", "📏 Resize Single Image"],
        horizontal=True
    )
    
    if app_mode == "🖼️ Create Collage":
        # Collage mode - existing functionality
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
    
    else:
        # Single image resize mode
        st.header("📏 Single Image Resizer")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📤 Upload Image")
            
            # Single file uploader
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=['png', 'jpg', 'jpeg'],
                help="Select a PNG, JPG, or JPEG file"
            )
            
            if uploaded_file:
                # Validate and process image
                is_valid, error_msg = validate_image(uploaded_file)
                if is_valid:
                    try:
                        image = Image.open(uploaded_file)
                        st.session_state.single_image = image
                        st.success(f"✅ Image '{uploaded_file.name}' uploaded successfully!")
                        
                        # Display original image info
                        st.subheader("📊 Original Image Info")
                        st.write(f"**Dimensions:** {image.width} × {image.height} pixels")
                        st.write(f"**Format:** {image.format}")
                        st.write(f"**Mode:** {image.mode}")
                        
                        # Show thumbnail of original
                        thumb = image.copy()
                        thumb.thumbnail((300, 300), Image.Resampling.LANCZOS)
                        st.image(thumb, caption="Original Image", use_container_width=False)
                        
                    except Exception as e:
                        st.error(f"❌ Error processing image: {str(e)}")
                else:
                    st.error(f"❌ Invalid image file: {error_msg}")
        
        with col2:
            st.subheader("🎛️ Resize Options")
            
            if 'single_image' in st.session_state:
                # Scale factor selection
                scale_options = {
                    "0.25x (Quarter Size)": 0.25,
                    "0.5x (Half Size)": 0.5,
                    "1x (Original Size)": 1.0,
                    "2x (Double Size)": 2.0,
                    "4x (Quadruple Size)": 4.0
                }
                
                selected_scale = st.selectbox(
                    "Choose resize factor:",
                    options=list(scale_options.keys()),
                    index=2,  # Default to 1x
                    help="Select how much to scale the image"
                )
                
                scale_factor = scale_options[selected_scale]
                
                # Show preview of new dimensions
                original_image = st.session_state.single_image
                new_width = int(original_image.width * scale_factor)
                new_height = int(original_image.height * scale_factor)
                
                st.write(f"**New Dimensions:** {new_width} × {new_height} pixels")
                
                # Resize button
                if st.button("🔄 Resize Image", type="primary", use_container_width=True):
                    with st.spinner("Resizing image..."):
                        try:
                            resized_image = resize_single_image(original_image, scale_factor)
                            st.session_state.resized_image = resized_image
                            st.success("🎉 Image resized successfully!")
                        except Exception as e:
                            st.error(f"❌ Error resizing image: {str(e)}")
                
                # Display resized image and download option
                if 'resized_image' in st.session_state:
                    st.subheader("🖼️ Resized Image")
                    
                    # Show resized image (with reasonable display size)
                    display_image = st.session_state.resized_image.copy()
                    if display_image.width > 400 or display_image.height > 400:
                        display_image.thumbnail((400, 400), Image.Resampling.LANCZOS)
                    
                    st.image(display_image, caption=f"Resized Image ({selected_scale})", use_container_width=False)
                    
                    # Download button
                    try:
                        img_buffer = io.BytesIO()
                        st.session_state.resized_image.save(img_buffer, format='PNG')
                        img_bytes = img_buffer.getvalue()
                        
                        st.download_button(
                            label="💾 Download Resized Image",
                            data=img_bytes,
                            file_name=f"resized_image_{selected_scale.replace('x', '')}.png",
                            mime="image/png",
                            type="primary",
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"❌ Error preparing download: {str(e)}")
            else:
                st.info("👈 Upload an image first to resize it")
    
    # Instructions
    with st.expander("ℹ️ How to use this app"):
        if app_mode == "🖼️ Create Collage":
            st.markdown("""
            **Collage Mode:**
            1. **Upload Images**: Click on the upload area and select multiple image files (PNG, JPG, JPEG)
            2. **Adjust Settings**: Use the sidebar to customize image size and grid layout
            3. **Reorder Images**: Use the reordering controls to arrange images as desired
            4. **Generate Collage**: Click the "Create Collage" button to generate your grid collage
            5. **Download**: Save your collage as a PNG file using the download button
            
            **Tips**:
            - The app automatically calculates the best grid layout based on the number of images
            - Images are resized to maintain consistent appearance
            - You can reorder images before creating the collage
            """)
        else:
            st.markdown("""
            **Single Image Resize Mode:**
            1. **Upload Image**: Click on the upload area and select a single image file (PNG, JPG, JPEG)
            2. **Choose Scale**: Select from the resize options (0.25x, 0.5x, 1x, 2x, 4x)
            3. **Resize**: Click the "Resize Image" button to apply the scaling
            4. **Download**: Save your resized image as a PNG file using the download button
            
            **Scale Options**:
            - **0.25x**: Quarter size (25% of original)
            - **0.5x**: Half size (50% of original)
            - **1x**: Original size (no change)
            - **2x**: Double size (200% of original)
            - **4x**: Quadruple size (400% of original)
            """)

if __name__ == "__main__":
    main()
