// Entry program for make.fun news-image-20261120 (Node 22, standard library only).
// The image is drawn by build_image.py and stored beside this file as entry.png.
// This program copies that file into the grader's output directory, byte for
// byte, so the image the judges see is exactly the one the script drew.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = new URL("./entry.png", import.meta.url);

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, join(outputDir, "entry.png"));
