import '@testing-library/jest-dom';

// recharts uses ResizeObserver which is not available in jsdom
window.ResizeObserver = class ResizeObserver {
  observe() {}
  unobserve() {}
  disconnect() {}
};
