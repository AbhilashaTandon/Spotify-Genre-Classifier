import { useState, useEffect } from "react";

export default function useWindowSize() {
  const [windowSize, setWindowSize] = useState({ width: 1024, height: 1024 });

  useEffect(() => {
    function window_size() {
      const { innerWidth: width, innerHeight: height } = window;
      return {
        width,
        height,
      };
    }
    function handleResize() {
      setWindowSize(window_size());
    }

    handleResize();

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return windowSize;
}
