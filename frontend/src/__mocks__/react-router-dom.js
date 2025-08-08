module.exports = {
  BrowserRouter: ({ children }) => children,
  Routes: ({ children }) => children,
  Route: ({ children }) => children,
  useNavigate: jest.fn(() => jest.fn()), // Mock useNavigate hook
  Link: ({ children, to }) => <a href={to}>{children}</a>, // Mock Link component
  // Add other exports as needed, e.g., useParams, useLocation, etc.
};