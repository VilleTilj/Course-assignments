export default function useChatBubblePosition(direction) {
  const left = {
    "--left": "-10px",
    "--right": "initial",
    "--align": "flex-start",
    "--margin": "0 2rem 0 1rem",
  };
  const right = {
    "--left": "initial",
    "--right": "-10px",
    "--align": "flex-end",
    "--margin": "0 1rem 0 2rem",
    "--transform": "scaleX(-100%)",
  };
  const cssVars = direction === "left" ? left : right;

  return { cssVars };
}
