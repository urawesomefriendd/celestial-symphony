// Subtle ambient starfield — small, slow, non-distracting.
(function () {
  const canvas = document.getElementById('stars');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let stars = [];
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const count = Math.floor((canvas.width * canvas.height) / 9000);
    stars = Array.from({ length: count }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 1.1 + 0.3,
      phase: Math.random() * Math.PI * 2,
      speed: Math.random() * 0.008 + 0.003,
    }));
  }

  function draw(t) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const s of stars) {
      const twinkle = reduceMotion ? 1 : 0.55 + 0.45 * Math.sin(t * s.speed + s.phase);
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(233, 231, 242, ${0.5 * twinkle})`;
      ctx.fill();
    }
    if (!reduceMotion) requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  resize();
  draw(0);
})();
