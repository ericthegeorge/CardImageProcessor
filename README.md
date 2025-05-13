# About
I created this project to help me with batch processing some card images I wanted to print. 
From web scraping the card data off the web, to producing a photo that looks just like the real thing, as you saw on the web, with appropriate bleed zones and upscaling algorithms. 
The details of the processing includes:   
1. Collect the images via webscraping through the html and sources of the websites.
2. Use the image's (or another appropriate) ICC profile to transform CMYK to RGB(A)
   - This step is necessary for JPEG's and other similar file types, but not for PNG's.
3. Corner out the white spaces of the image for round-edged cards.
4. Fill in the corner's with Lanczos, Generative-AI, or other resampling algorithms.
5. Mirror the image edges to create the bleed zones for printing.
6. Upscale the image with an upscaling algorithm (Bicubic or others).
7. Resize the image bleeds as needed for printing.

This is a minor side project that I enjoyed doing, as I was very passionate about getting these cards 😁     
You will need to modify the webscraper for your own site specific data, the amount of images, the cornering degree, the bleed type (mirror or blur, or others) and the bleed size for personal use. 

I have some example transformation images. Note that the image resolution has gone from 350x511 to 1616x2260 to be suitable for printing.

![Original Card Example 1](https://github.com/user-attachments/assets/3be9b342-d261-490b-8fa4-2e0fc48265c0)

![Cornered and Filled Card Example 1](https://github.com/user-attachments/assets/19e2e896-746a-4ab4-873c-a7b6c0859864)

![Transformed Card Example 1](https://github.com/user-attachments/assets/abe02cac-a170-4ca3-b9af-9dd02aaa405f)

![Original Card Example 2](https://github.com/user-attachments/assets/3a928e64-9921-44bc-b9e5-a47f80427c1c)

![Cornered and Filled Card Example 2](https://github.com/user-attachments/assets/b840486a-1c7e-41f6-9632-866e2c96a3dd)

![Transformed Card Example 2](https://github.com/user-attachments/assets/ffad8fbb-d250-489c-ba67-6d53bee5338b)

![Original Card Example 3](https://github.com/user-attachments/assets/72a37ede-03e6-4e64-ae23-ba0d6461addb)

![Cornered and Filled Card Example 3](https://github.com/user-attachments/assets/636f1701-a1d9-49fc-aabc-49b26037c4b9)

![Transformed Card Example 3](https://github.com/user-attachments/assets/48051852-1aa4-448f-8f8e-fa065e7c69c9)
