# Optical-Character-Recognition-OCR-
This is an implementation for Optical Character Recognition (OCR), used for extracting the text from the images or PDF document.

## Extracting data from PDF using OCR Technique
**OCR** stands for Optical Character Recognition. Here, we are going to use Tesseract OCR.

**Tesseract OCR** : Tesseract OCR is an open-source OCR engine developed by Google. It's a powerful tool that we'll be using in our project. We will be using **pytesseract** library for using this OCR technique or engine.

**pdf2image**: To convert PDF files into images.

### deskew() function explanation and extra information regarding the functions used in this function
1. Firstly, converting the image to grayscale image.

2. Second step here we do is that, we use bitwise_NOT on our image. 
   - In some optical character recognition (OCR) tasks, inverting pixel values can help improve the performance of the OCR algorithm by enhancing the contrast between text and background.

   - Bitwise NOT operation on the grayscale image, in simple terms, it inverts the pixel values of the grayscale image. In a grayscale image, pixel values typically range from 0 to 255, where 0 represents black and 255 represents white. The bitwise NOT operation flips all 0s to 1s and all 1s to 0s. As a result, dark areas become light, and light areas become dark. 

   - Here, according to our case study, while converting the pdf image into gray scale, the background turns out to white and the text into black color depending on the image.

   - When while inverting the gray image using bitwise_not the new image generated would be with black background and white text.

   - black pixel ---> 0 and white ---> 1

3. Finding coordinates of non-zero pixels.
   - This line finds the coordinates of non-zero (i.e., white) pixels in the inverted grayscale image gray and stores them in the variable coords. 
   - Here's what's happening:

       - `np.where(gray > 0)` returns a tuple containing arrays of row and column indices where the pixel values are greater than 0. This essentially finds the coordinates of white pixels in the image.

       - `np.column_stack()`, stacks these arrays column-wise, effectively combining the row and column indices into a single 2D array, where each row represents the coordinates of a white pixel in the image.

       - The resulting coords array contains the coordinates of all white pixels in the inverted grayscale image, which can be useful for further processing or analysis, such as identifying regions of interest.
    
4. Finding the minimum area rotated rectangle.
   - `cv2.minAreaRect()` is used for finding the minimum area rotated rectangle. The bounding rectangle is drawn with a minimum area, because of this, rotation is also considered. It returns the coordinates of rectangle and its angle.
    
   - Here, we are using this function to get the angle and check whether the image is in proper angle that is 90 degree, which defines that the image is in proper position and isn't tilted, and we can easily extract the text further. This step is also a very important step for preprocessing the image before performing the OCR process on it.
    
   - slicing [-1] is used to get the last param value that is angle.

5. Getting the rotation matrix M
    - `cv2.getRotationMatrix2D()` function is used to make the transformation matrix M which will be used for rotating image.
      - **center**: Center of rotation
      - **angle(θ)**: Angle of Rotation. Angle is positive for anti-clockwise and negative for clockwise.
      - **Return**: 2×3 Rotation Matrix M
      - **scale**: scaling factor which scales the image
        - **Scale = 1.0**: This means no scaling is applied, resulting in the same size of the output image as the input image.
    
        - **Scale > 1.0**: Enlarges the output image. The larger the scaling factor, the bigger the output image relative to the input image.
    
        - **0 < Scale < 1.0**: Shrinks the output image. The smaller the scaling factor, the smaller the output image relative to the input image.
    
        - **Scale = 0**: It would result in an output image with zero dimensions, which is generally not meaningful.
    
        - **Scale < 0**: This would flip the image while also scaling it. The effect would depend on the sign of the scale factor.

6. Rotating the image
    - `cv2.warpAffine`, this function applies the rotation by using the transformation matrix.
    - Details of each parameter:

        - **src**: This is the input image on which you want to apply the affine transformation. It should be a numpy array.

        - **M**: This is the **2x3 transformation matrix** that represents the affine transformation to be applied. This matrix is generated, for example, by functions like `cv2.getRotationMatrix2D` or `cv2.getAffineTransform`.
    
        - **dsize**: This is the size of the output image, specified as a **tuple (width, height)**. It represents the width and height of the output image after the transformation. You can specify it manually, or you can use the same size as the input image if you want the output image to have the same size.
    
        - **flags**: This parameter specifies the interpolation method and optional flags that control the transformation. The interpolation methods include c`v2.INTER_NEAREST`, `cv2.INTER_LINEAR`, `cv2.INTER_CUBIC`, etc. Optional flags include `cv2.WARP_INVERSE_MAP`, which indicates that M is an inverse transformation.
            - Interpolation methods are techniques used to estimate the values of points within a discrete set of known points. In the context of image processing and computer vision, interpolation methods are used when resizing or transforming images, where new pixel values need to be determined based on existing pixel values.
            - Here are some common interpolation methods used in image processing:

                - **Nearest Neighbor Interpolation (`cv2.INTER_NEAREST`)**:
                  - Also known as the nearest-neighbor algorithm or floor function interpolation.
                  - It selects the nearest pixel value to the target location.
                  - Simple and fast but may produce aliasing artifacts and blockiness in the output image.
            
                - **Bilinear Interpolation (`cv2.INTER_LINEAR`)**:
                  - Bilinear interpolation computes the new pixel value by linearly interpolating between the four nearest pixel values in a 2x2 neighborhood of the target location.
                  - It produces smoother results compared to nearest neighbor interpolation.
                  - Commonly used for image scaling.
            
                - **Bicubic Interpolation (`cv2.INTER_CUBIC`)**:
                  - Bicubic interpolation is an extension of bilinear interpolation that uses cubic polynomials instead of linear ones.
                  - It considers a larger neighborhood (4x4) of pixels to compute the new pixel value, resulting in smoother output with less aliasing.
                  - More computationally expensive compared to bilinear interpolation but produces higher-quality results, especially for larger scaling factors.
            
                - **Lanczos Interpolation (`cv2.INTER_LANCZOS4`)**:
                  - Lanczos interpolation is based on the sinc function, which uses a windowed sinc function to interpolate. 
                  - It provides better results for high-quality image resizing, especially when downsampling. 
                  - More computationally expensive compared to bilinear and bicubic interpolation.
            
            The choice of interpolation method depends on various factors such as the desired quality of the output image, computational resources available, and specific requirements of the application. Bilinear interpolation is often a good balance between computational efficiency and image quality for general image resizing tasks, while bicubic and Lanczos interpolation are preferred for applications where high-quality results are critical.
                
            - **Optional Flags**:
                - These flags provide additional options or modifications to the transformation.
                
                - `cv2.WARP_FILL_OUTLIERS`: If set, the function fills all of the destination image pixels. Otherwise, the function may leave some of the destination image pixels uninitialized.
                
                - `cv2.WARP_INVERSE_MAP`: If set, M is the inverse transformation (mapping from the destination image to the source). This can be useful in certain scenarios, such as computing the inverse of an affine transformation.
                
                - `cv2.WARP_POLAR_LINEAR`: This flag is used with polar transformations. It specifies that the transformation is linear.
                
                - `cv2.WARP_POLAR_LOG`: This flag is used with polar transformations. It specifies that the transformation is logarithmic.
                    
        - **borderMode**: 
            - This parameter specifies the pixel extrapolation method, which is used when the transformed point lies outside of the input image. Possible values include `cv2.BORDER_CONSTANT`, `cv2.BORDER_REPLICATE`, `cv2.BORDER_REFLECT`, etc.
            - The borderMode parameter in OpenCV's image transformation functions specifies how to handle pixels outside the image boundaries during the transformation. Here are the possible values for borderMode along with their explanations:

                - `cv2.BORDER_CONSTANT`:
                  - This mode fills the outside region with a constant value specified by the borderValue parameter.
                  - You need to provide a value for borderValue when using this mode.
            
                - `cv2.BORDER_REPLICATE`:
                  - In this mode, the border is replicated from the edge pixels of the image.
                  - For example, if you have a pixel at coordinate (0, 0) and the border is being replicated, the border pixel for coordinate (-1, -1) will also be (0, 0).
            
                - `cv2.BORDER_REFLECT`:
                  - This mode reflects the image around the border.
                  - If you have a 1D array [1, 2, 3, 4, 5], the reflected border will be [5, 4, 3, 2, 1, 2, 3, 4, 5].
            
                  - `cv2.BORDER_WRAP`:
                    - In this mode, the border is wrapped around to the opposite edge.
                    - For example, if you have a 1D array [1, 2, 3, 4, 5], the wrapped border will be [5, 1, 2, 3, 4, 1, 2, 3, 4].
            
                - `cv2.BORDER_REFLECT_101`:
                  - This is similar to cv2.BORDER_REFLECT but with a slight change.
                  - Here, instead of reflecting all the pixels, the border pixels are reflected such that the center pixel remains unchanged.
            
                - `cv2.BORDER_TRANSPARENT`:
                  - This mode sets the border pixels of the destination image to transparent. It's useful when dealing with alpha channels or transparent images.
            
              These modes provide different strategies for handling the border pixels during image transformations. The choice of mode depends on the specific requirements of your application, such as the desired visual effect, the nature of the image, and the context in which the transformation is being applied.
                
        - **borderValue**: This parameter specifies the value to be used in case of a constant border. It's only applicable if borderMode is set to `cv2.BORDER_CONSTANT`.
        
 
## References :
- https://medium.com/@dr.booma19/extracting-text-from-pdf-files-using-ocr-a-step-by-step-guide-with-python-code-becf221529ef
- https://pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
- greeksforgreeks, chatgpt, github and documentations for understanding the functions used.