import express from 'express';
import multer from 'multer';
import path from 'path';
import fs from 'fs';

const UPLOADS_DIR = path.join(__dirname, '../dist/uploads'); // Ensure correct path

// Ensure uploads directory exists
if (!fs.existsSync(UPLOADS_DIR)) {
    console.log(`Creating uploads directory at: ${UPLOADS_DIR}`);
    fs.mkdirSync(UPLOADS_DIR, { recursive: true });
} else {
    console.log(`Uploads directory exists: ${UPLOADS_DIR}`);
}

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        console.log('📂 Uploading to:', UPLOADS_DIR);
        cb(null, UPLOADS_DIR);
    },
    filename: (req, file, cb) => {
        console.log(`Saving file: ${file.originalname}`);
        cb(null, `${Date.now()}-${file.originalname}`);
    },
});

const upload = multer({ storage });

const app = express();
const PORT = process.env.PORT || 3301;

// Upload image
app.post('/api/images', upload.single('images'), (req, res) => {
    if (!req.file) {
        console.error('No file uploaded.');
        return res.status(400).json({ error: 'No file uploaded' });
    }
    
    console.log('File uploaded successfully:', req.file.path);
    res.json({ message: 'Upload successful', filePath: `/api/images?id=${req.file.filename}` });
});

// Fetch image dynamically
app.get('/api/images', (req, res) => {
    const imageId = req.query.id as string;
    if (!imageId) {
        return res.status(400).json({ error: 'Image ID is required' });
    }

    const imagePath = path.join(UPLOADS_DIR, imageId);

    if (!fs.existsSync(imagePath)) {
        console.error(`File not found: ${imagePath}`);
        return res.status(404).json({ error: 'File not found or cannot be downloaded' });
    }

    console.log(`Sending file: ${imagePath}`);
    res.sendFile(imagePath);
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
