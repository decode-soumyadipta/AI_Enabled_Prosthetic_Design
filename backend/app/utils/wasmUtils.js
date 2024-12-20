// File: wasmUtils.js
export const loadWasmModule = async (path) => {
    try {
      const response = await fetch(path);
      const buffer = await response.arrayBuffer();
      const wasmModule = await WebAssembly.instantiate(buffer);
      return wasmModule.instance.exports;
    } catch (error) {
      throw new Error("Failed to load WebAssembly module: " + error.message);
    }
  };
  