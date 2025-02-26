import { Router } from "express";

const router = Router();

router.get("/images", (req, res) => {
  res.json({ message: "Image API is working!" });
});

// Ensure we are using `export default`
export default router;
