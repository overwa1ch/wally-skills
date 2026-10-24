const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const crypto = require("node:crypto");
const { execFileSync } = require("node:child_process");
const os = require("node:os");

const script = path.resolve(__dirname, "../scripts/cua_payload.py");
const sha256 = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");

// Verify exact UTF-8 bytes across all files in a single source load.
test("all sources round-trip exact bytes and SHA in command order", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "static-sources-"));
  try {
    const texts = [
      "首行：林舟站在社区自行车修理铺，袖口轻微磨白。\r\n" +
        "第二行：完整输入保持原文。\n独立回车\r制表\t空字符\0" +
        "` ${danger} </script>\u2028\u2029\"双引号\" '单引号' \\反斜杠 \\u2028 🧰𠮷\r\n",
      "\ufeff项目说明：  保留开头和结尾空白。  \n",
      "",
      "另一个版本\n\n不能共用第一条正文。",
    ];
    const sources = texts.map((text, index) => {
      const source = path.join(dir, `中文定稿 ${index}.txt`);
      fs.writeFileSync(source, text);
      return source;
    });
    const originals = sources.map((source) => fs.readFileSync(source));
    const cell = execFileSync("python3", [script, "--source", ...sources], { encoding: "utf8" });
    const isolated = {};
    vm.runInNewContext(cell, isolated);
    assert.equal(isolated.staticSources.length, sources.length);
    sources.forEach((source, index) => {
      const item = isolated.staticSources[index];
      assert.equal(item.text, texts[index]);
      assert.deepEqual(Buffer.from(item.text, "utf8"), originals[index]);
      assert.deepEqual(fs.readFileSync(source), originals[index]);
      assert.equal(item.path, fs.realpathSync(source));
      assert.equal(item.sha256, sha256(originals[index]));
      assert.equal(Object.isFrozen(item), true);
    });
    assert.equal(Object.isFrozen(isolated.staticSources), true);
    assert.equal(cell.includes("首行：林舟"), true);
    assert.equal(cell.includes("中文定稿"), true);
    assert.equal(cell.includes("🧰𠮷"), true);
    assert.equal(cell.includes("\\u9996"), false);
    assert.equal(cell.includes("\u2028") || cell.includes("\u2029"), false);
    assert.equal(cell.includes("\\u2028") && cell.includes("\\u2029"), true);
  } finally { fs.rmSync(dir, { recursive: true }); }
});

test("an unreadable or invalid UTF-8 source emits no partial declaration", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "static-sources-"));
  try {
    const valid = path.join(dir, "valid.txt");
    const invalid = path.join(dir, "invalid.txt");
    fs.writeFileSync(valid, "已定稿");
    fs.writeFileSync(invalid, Buffer.from([0xff]));
    for (const failed of [invalid, path.join(dir, "missing.txt")]) {
      assert.throws(() => execFileSync("python3", [script, "--source", valid, failed], { stdio: "pipe" }), (error) => {
        assert.notEqual(error.status, 0);
        assert.equal(error.stdout.length, 0);
        return true;
      });
    }
  } finally { fs.rmSync(dir, { recursive: true }); }
});
