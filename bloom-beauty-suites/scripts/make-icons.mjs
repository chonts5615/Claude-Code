// Generates the PNG app icons from a simple "bloom flower" design with no image
// dependencies (pure Node zlib PNG encoder). Run: node scripts/make-icons.mjs
import { deflateSync } from "node:zlib";
import { writeFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, "..", "public");
mkdirSync(outDir, { recursive: true });

const hex = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
const ROSE = hex("#e8a0b4");
const ROSE2 = hex("#d4849c");
const WHITE = [255, 255, 255];
const GOLD = hex("#c9a96e");

// Petals + center, expressed in a 64-unit design space (matches favicon.svg).
const petals = [
  [32, 20, 7], [20, 30, 7], [44, 30, 7], [25, 43, 7], [39, 43, 7],
];
const center = [32, 33, 6];

function colorAt(x, y, size) {
  const u = (x / size) * 64;
  const v = (y / size) * 64;
  const inCircle = (cx, cy, r) => (u - cx) ** 2 + (v - cy) ** 2 <= r * r;
  if (inCircle(center[0], center[1], center[2])) return GOLD;
  for (const [cx, cy, r] of petals) if (inCircle(cx, cy, r)) return WHITE;
  // Vertical rose gradient background.
  const t = y / size;
  return [
    Math.round(ROSE[0] + (ROSE2[0] - ROSE[0]) * t),
    Math.round(ROSE[1] + (ROSE2[1] - ROSE[1]) * t),
    Math.round(ROSE[2] + (ROSE2[2] - ROSE[2]) * t),
  ];
}

function crc32(buf) {
  let c = ~0;
  for (let i = 0; i < buf.length; i++) {
    c ^= buf[i];
    for (let k = 0; k < 8; k++) c = (c >>> 1) ^ (0xedb88320 & -(c & 1));
  }
  return (~c) >>> 0;
}
function chunk(type, data) {
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length);
  const td = Buffer.concat([Buffer.from(type), data]);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(td));
  return Buffer.concat([len, td, crc]);
}

function png(size) {
  const raw = Buffer.alloc(size * (size * 4 + 1));
  let p = 0;
  for (let y = 0; y < size; y++) {
    raw[p++] = 0; // filter: none
    for (let x = 0; x < size; x++) {
      const [r, g, b] = colorAt(x + 0.5, y + 0.5, size);
      raw[p++] = r; raw[p++] = g; raw[p++] = b; raw[p++] = 255;
    }
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(size, 0);
  ihdr.writeUInt32BE(size, 4);
  ihdr[8] = 8; // bit depth
  ihdr[9] = 6; // RGBA
  const sig = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  return Buffer.concat([
    sig,
    chunk("IHDR", ihdr),
    chunk("IDAT", deflateSync(raw)),
    chunk("IEND", Buffer.alloc(0)),
  ]);
}

for (const [name, size] of [["icon-192.png", 192], ["icon-512.png", 512], ["apple-touch-icon.png", 180]]) {
  writeFileSync(join(outDir, name), png(size));
  console.log("wrote", name);
}
