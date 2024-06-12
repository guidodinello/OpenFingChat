import axios from "axios";

const API = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

// Add a request interceptor
API.interceptors.request.use(
  async (config) => {
    await new Promise((resolve) => setTimeout(resolve, 1000)); // <-- REMOVE: this is to test loadings
    return config;
  },
  (error) => Promise.reject(error)
);

// Add a response interceptor
API.interceptors.response.use(
  (response) => response,
  (error) => Promise.reject(error)
);

export default API;
