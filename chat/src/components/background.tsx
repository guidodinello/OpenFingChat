"use client";
import { Box, useTheme } from "@mui/material";
import Particles, { initParticlesEngine } from "@tsparticles/react";
import { loadSlim } from "@tsparticles/slim";
import { useEffect, useState } from "react";

const Background = () => {
  const [init, setInit] = useState(false);

  const { palette } = useTheme();

  useEffect(() => {
    initParticlesEngine(async (engine) => await loadSlim(engine)).then(() =>
      setInit(true)
    );
  }, []);

  const bgColor = palette.background.default;
  const particlesColor = palette.grey[300];

  return (
    <Box
      position="fixed"
      top={0}
      left={0}
      width="100%"
      height="100%"
      zIndex={-1}
      bgcolor={palette.background.default}
    >
      {init && (
        <Particles
          id="tsparticles"
          options={{
            interactivity: {
              events: {
                onClick: { enable: true, mode: "push" },
                onHover: { enable: true, mode: "repulse" },
              },
              modes: {
                push: { quantity: 2 },
                repulse: { distance: 80, duration: 0.4 },
              },
            },
            background: { color: { value: bgColor } },
            fpsLimit: 120,
            particles: {
              color: { value: particlesColor },
              links: {
                color: particlesColor,
                distance: 150,
                enable: true,
                opacity: 1,
                width: 1,
              },
              move: {
                enable: true,
                direction: "none",
                outModes: { default: "bounce" },
                random: false,
                speed: 2,
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
    </Box>
  );
};

export default Background;
