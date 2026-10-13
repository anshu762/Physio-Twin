import axios from "axios";


// -----------------------------------------------------------------------------
// API configuration
// -----------------------------------------------------------------------------
// In local development, VITE_API_URL is not set, so it falls back to
// your existing localhost backend — local dev behavior is unchanged.
//
// In production (Render), VITE_API_URL is injected at build time and
// points to your deployed backend URL.
// -----------------------------------------------------------------------------

export const API_BASE_URL =
  import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";


// -----------------------------------------------------------------------------
// Axios instance
// -----------------------------------------------------------------------------

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});


















// import axios from "axios";


// // -----------------------------------------------------------------------------
// // API configuration
// // -----------------------------------------------------------------------------

// export const API_BASE_URL = "http://127.0.0.1:8000";


// // -----------------------------------------------------------------------------
// // Axios instance
// // -----------------------------------------------------------------------------

// export const apiClient = axios.create({
//   baseURL: API_BASE_URL,
//   headers: {
//     "Content-Type": "application/json",
//   },
// });