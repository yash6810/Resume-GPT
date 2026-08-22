// ResumeGPT Scanner - Background Service Worker
try {
  importScripts("../config.js");
} catch (e) {
  // Fallback for non-service worker contexts
}

const FALLBACK_API_BASE = "https://resumegpt.onrender.com";

async function resolveApiBase() {
  if (typeof getApiBase === "function") {
    return await getApiBase();
  }
  return FALLBACK_API_BASE;
}

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "openPopup") {
    chrome.action.openPopup();
  }

  if (request.action === "checkApi") {
    checkApiStatus().then(sendResponse);
    return true;
  }

  if (request.action === "analyzeResume") {
    analyzeResume(request.resumeText, request.jobText).then(sendResponse);
    return true;
  }
});

// Check if backend API is running
async function checkApiStatus() {
  try {
    const apiBase = await resolveApiBase();
    const response = await fetch(`${apiBase}/health`, {
      method: "GET",
      signal: AbortSignal.timeout(3000),
    });
    return { status: response.ok ? "connected" : "error" };
  } catch (e) {
    return { status: "disconnected" };
  }
}

// Analyze resume against job description
async function analyzeResume(resumeText, jobText) {
  try {
    const apiBase = await resolveApiBase();
    const response = await fetch(`${apiBase}/analyze/quick`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobText,
      }),
    });

    if (!response.ok) throw new Error("Analysis failed");

    const data = await response.json();

    // Notify content script to show badge
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.tabs.sendMessage(tabs[0].id, {
          action: "showScore",
          score: Math.round(data.ats_score),
        });
      }
    });

    return { success: true, data };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

// Set up badge icon on install
chrome.runtime.onInstalled.addListener(() => {
  console.log("ResumeGPT Scanner installed");
});

// Handle tab updates to detect job pages
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    const jobSites = [
      "linkedin.com/jobs",
      "indeed.com/viewjob",
      "glassdoor.com/job",
      "ziprecruiter.com/jobs",
      "monster.com/job",
    ];

    const isJobPage = jobSites.some((site) => tab.url.includes(site));

    if (isJobPage) {
      // Show badge icon as active
      chrome.action.setBadgeText({ text: "!", tabId });
      chrome.action.setBadgeBackgroundColor({ color: "#e94560", tabId });
    } else {
      chrome.action.setBadgeText({ text: "", tabId });
    }
  }
});
