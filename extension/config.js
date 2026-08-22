// ResumeGPT Extension Configuration
// Resolves API Base URL dynamically with support for user/environment overrides.

const DEFAULT_API_BASE = "https://resumegpt.onrender.com";

function getApiBase() {
  return new Promise((resolve) => {
    if (typeof chrome !== "undefined" && chrome.storage && chrome.storage.sync) {
      chrome.storage.sync.get(["resumegpt_api_base"], (result) => {
        resolve(result.resumegpt_api_base || DEFAULT_API_BASE);
      });
    } else {
      resolve(DEFAULT_API_BASE);
    }
  });
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { DEFAULT_API_BASE, getApiBase };
}
