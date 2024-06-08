"use client";
import Particles, { initParticlesEngine } from "@tsparticles/react";
import { loadSlim } from "@tsparticles/slim";
import { useEffect, useState } from "react";

const Background = () => {
  const [init, setInit] = useState(false);

  useEffect(() => {
    initParticlesEngine(async (engine) => await loadSlim(engine)).then(() =>
      setInit(true)
    );
  }, []);

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      {init && (
        <Particles
          id="tsparticles"
          options={{
            background: { color: { value: "#111" } },
            fpsLimit: 120,
            particles: {
              color: { value: "#ffffff" },
              links: {
                color: "#ffffff",
                distance: 150,
                enable: true,
                opacity: 0.3,
                width: 1,
              },
              move: {
                enable: true,
                direction: "none",
                outModes: { default: "bounce" },
                random: false,
                speed: 5,
                straight: true,
              },
              number: {
                density: { enable: true, height: 800, width: 800 },
                value: 80,
              },
              opacity: { value: 0.2 },
              shape: { type: "circle" },
              size: { value: { min: 1, max: 5 } },
            },
            detectRetina: true,
          }}
        />
      )}
    </div>
  );
};

export default Background;
