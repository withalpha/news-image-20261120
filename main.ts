// Entry program for make.fun news-image-20261120 (Node 22, standard library only).
// The image is drawn by build_image.py and stored beside this file as entry.png.
// This program copies it to the grader's output directory, unchanged.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(
  new URL("./entry.png", import.meta.url),
  join(outDir, "entry.png"),
);
