import express from 'express';
import multer from 'multer';
import path from 'path';
import fs from 'fs';

const UPLOADS_DIR = path.join(__dirname, '../dist/uploads');

// Ensure uploads directory exists
if (!fs.existsSync(UPLOADS_DIR)) {
    console.log(`Creating uploads directory at: ${UPLOADS_DIR}`);
    fs.mkdirSync(UPLOADS_DIR, { recursive: true });
} else {
    console.log(`Uploads directory already exists: ${UPLOADS_DIR}`);
}

// Multer storage configuration
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, UPLOADS_DIR);
    },
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}-${file.originalname}`);
    },
});

const upload = multer({ storage });

const app = express();
const PORT = process.env.PORT || 3301;

// Route to upload an image
app.post('/api/images', upload.single('images'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }
    console.log('File uploaded to:', req.file.path);
    res.json({ message: 'Upload successful', filePath: req.file.path });
});

// Route to list uploaded images
app.get('/api/images', (req, res) => {
    fs.readdir(UPLOADS_DIR, (err, files) => {
        if (err) {
            return res.status(500).json({ error: 'Unable to read uploads directory' });
        }
        res.json({ images: files });
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
