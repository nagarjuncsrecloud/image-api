import express from "express";
import multer from "multer";
import sharp from "sharp";
import fs from "fs";
import path from "path";
import axios from "axios";

const router = express.Router();
const upload = multer({ dest: "uploads/" });

// Function to process images
const processImage = async (
  imageBuffer: Buffer,
  operations: Record<string, any>
) => {
  let image = sharp(imageBuffer);

  if (operations.resize) {
    image = image.resize(operations.resize.width, operations.resize.height);
  }

  if (operations.compress) {
    image = image.jpeg({ quality: operations.compress.quality || 80 });
  }

  if (operations.rotate) {
    image = image.rotate(operations.rotate.angle || 90);
  }

  if (operations.grayscale) {
    image = image.grayscale();
  }

  return await image.toBuffer();
};

// API: Process Images (Upload, URL, or Stored)
router.post("/process", upload.single("file"), async (req, res) => {
  try {
    let imageBuffer: Buffer | null = null;

    if (req.file) {
      // If file is uploaded
      imageBuffer = fs.readFileSync(req.file.path);
    } else if (req.body.imageUrl) {
      // If URL is provided
      const response = await axios.get(req.body.imageUrl, {
        responseType: "arraybuffer",
      });
      imageBuffer = Buffer.from(response.data as Uint8Array);
    } else if (req.body.imageId) {
      // If image is already stored
      const imagePath = path.resolve("uploads", req.body.imageId);
      if (fs.existsSync(imagePath)) {
        imageBuffer = fs.readFileSync(imagePath);
      }
    }

    if (!imageBuffer) {
      return res.status(400).json({ error: "No valid image provided" });
    }

    // Process the image with requested operations
    const processedImage = await processImage(imageBuffer, req.body.operations);

    // Send processed image
    res.set("Content-Type", "image/png");
    return res.send(processedImage);
  } catch (error) {
    console.error("Processing error:", error);
    return res.status(500).json({ error: "Image processing failed" });
  }
});

export default router;
