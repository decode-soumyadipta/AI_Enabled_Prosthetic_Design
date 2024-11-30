import React, { useRef } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Stage, useGLTF } from "@react-three/drei";

function STLViewer({ stlFileUrl }) {
  const mesh = useRef();

  return (
    <Canvas>
      <OrbitControls />
      <Stage environment="city" intensity={0.6}>
        <mesh ref={mesh}>
          <primitive object={useGLTF(stlFileUrl)} />
        </mesh>
      </Stage>
    </Canvas>
  );
}

export default STLViewer;
