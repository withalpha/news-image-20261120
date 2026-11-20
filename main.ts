// Entry program for make.fun news-image-20261120 (Node 22, standard library only).
// The image is drawn by build_image.py and stored beside this file as entry.png.
// This program copies that file into the grader's output directory, byte for
// byte, so the image the judges see is exactly the one the script drew.
// It fails loudly instead of writing nothing when the image is missing.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const out = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = new URL("./entry.png", import.meta.url);

if (!existsSync(source)) {
  throw new Error("entry.png is missing next to main.ts; run build_image.py first");
}

mkdirSync(out, { recursive: true });
copyFileSync(source, join(out, "entry.png"));
