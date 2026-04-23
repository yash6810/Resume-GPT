// ResumeGPT Scanner - Popup Logic

const API_BASE = "http://localhost:8000";

// DOM Elements
const resumeInput = document.getElementById("resumeInput");
const resumeStatus = document.getElementById("resumeStatus");
const resumeLoaded = document.getElementById("resumeLoaded");
const resumeName = document.getElementById("resumeName");
const resumeDate = document.getElementById("resumeDate");
const uploadNewBtn = document.getElementById("uploadNewBtn");
const removeBtn = document.getElementById("removeBtn");

const jobPreview = document.getElementById("jobPreview");
const jobSource = document.getElementById("jobSource");
const jobTitle = document.getElementById("jobTitle");
const jobExcerpt = document.getElementById("jobExcerpt");
const jobText = document.getElementById("jobText");
const redetectBtn = document.getElementById("redetectBtn");
const pasteBtn = document.getElementById("pasteBtn");

const scoreCard = document.getElementById("scoreCard");
const scoreNumber = document.getElementById("scoreNumber");
const scoreStatus = document.getElementById("scoreStatus");
const scoreProgress = document.getElementById("scoreProgress");
const barFill = document.getElementById("barFill");

const skillsCard = document.getElementById("skillsCard");
const matchedSkills = document.getElementById("matchedSkills");
const missingSkills = document.getElementById("missingSkills");
const matchedCount = document.getElementById("matchedCount");
const missingCount = document.getElementById("missingCount");

const tipsCard = document.getElementById("tipsCard");
const tipsList = document.getElementById("tipsList");

const analyzeBtn = document.getElementById("analyzeBtn");
const loadingState = document.getElementById("loadingState");
const errorState = document.getElementById("errorState");
const errorMessage = document.getElementById("errorMessage");
const retryBtn = document.getElementById("retryBtn");

// State
let resumeText = "";
let jobDescription = "";
let isAnalyzing = false;

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  loadSavedData();
  detectJobFromPage();
  setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
  resumeInput.addEventListener("change", handleResumeUpload);
  uploadNewBtn.addEventListener("click", () => resumeInput.click());
  removeBtn.addEventListener("click", handleResumeRemove);
  redetectBtn.addEventListener("click", detectJobFromPage);
  pasteBtn.addEventListener("click", togglePasteMode);
  jobText.addEventListener("input", handleJobPaste);
  analyzeBtn.addEventListener("click", handleAnalyze);
  retryBtn.addEventListener("click", handleAnalyze);
}

// Load saved data from storage
async function loadSavedData() {
  try {
    const data = await chrome.storage.local.get(["resumeText", "resumeName", "resumeDate"]);
    if (data.resumeText) {
      resumeText = data.resumeText;
      showResumeLoaded(data.resumeName, data.resumeDate);
    }
  } catch (e) {
    console.log("Error loading saved data:", e);
  }
}

// Handle resume upload
async function handleResumeUpload(e) {
  const file = e.target.files[0];
  if (!file) return;

  if (file.size > 5 * 1024 * 1024) {
    showError("File too large. Max 5MB allowed.");
    return;
  }

  showLoading("Uploading resume...");

  try {
    const formData = new FormData();
    formData.append("resume", file);

    const response = await fetch(`${API_BASE}/parse`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Failed to parse resume");

    const data = await response.json();
    resumeText = data.text;

    // Save to storage
    const date = new Date().toLocaleDateString();
    await chrome.storage.local.set({
      resumeText: resumeText,
      resumeName: file.name,
      resumeDate: date,
    });

    showResumeLoaded(file.name, date);
    hideLoading();
  } catch (e) {
    showError("Failed to parse resume. Make sure backend is running.");
    hideLoading();
  }
}

// Show resume loaded state
function showResumeLoaded(name, date) {
  resumeStatus.style.display = "none";
  resumeLoaded.style.display = "block";
  resumeName.textContent = name;
  resumeDate.textContent = `Uploaded: ${date}`;
}

// Handle resume remove
async function handleResumeRemove() {
  resumeText = "";
  await chrome.storage.local.remove(["resumeText", "resumeName", "resumeDate"]);
  resumeStatus.style.display = "block";
  resumeLoaded.style.display = "none";
}

// Detect job from current page
async function detectJobFromPage() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Send message to content script
    chrome.tabs.sendMessage(tab.id, { action: "detectJob" }, (response) => {
      if (response && response.jobText) {
        jobDescription = response.jobText;
        jobSource.textContent = response.source || "Detected";
        jobTitle.textContent = response.title || "Job detected";
        jobExcerpt.textContent = truncate(response.jobText, 100);
      } else {
        jobTitle.textContent = "No job detected";
        jobExcerpt.textContent = "Click 'Paste Manual' to enter job description";
      }
    });
  } catch (e) {
    jobTitle.textContent = "Detection unavailable";
  }
}

// Toggle paste mode
function togglePasteMode() {
  const isVisible = jobText.style.display !== "none";
  jobText.style.display = isVisible ? "none" : "block";
  jobPreview.style.display = isVisible ? "block" : "none";
  pasteBtn.textContent = isVisible ? "📋 Paste Manual" : "📋 Hide";
}

// Handle job paste
function handleJobPaste() {
  jobDescription = jobText.value;
  if (jobDescription.length > 50) {
    jobTitle.textContent = "Manual entry";
    jobExcerpt.textContent = truncate(jobDescription, 100);
  }
}

// Handle analyze button click
async function handleAnalyze() {
  if (!resumeText) {
    showError("Please upload your resume first");
    return;
  }

  if (!jobDescription) {
    showError("Please enter or detect a job description");
    return;
  }

  isAnalyzing = true;
  analyzeBtn.disabled = true;
  showLoading("Analyzing your resume...");

  try {
    const response = await fetch(`${API_BASE}/analyze/quick`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
      }),
    });

    if (!response.ok) throw new Error("Analysis failed");

    const data = await response.json();
    displayResults(data);
    hideLoading();
  } catch (e) {
    showError("Failed to analyze. Make sure backend is running.");
    hideLoading();
  }

  isAnalyzing = false;
  analyzeBtn.disabled = false;
}

// Display analysis results
function displayResults(data) {
  const score = Math.round(data.ats_score || 0);
  const matched = data.matched_skills || [];
  const missing = data.missing_skills || [];
  const recommendations = data.recommendations || [];

  // Show cards
  scoreCard.style.display = "block";
  skillsCard.style.display = "block";
  if (recommendations.length > 0) {
    tipsCard.style.display = "block";
  }

  // Update score
  scoreNumber.textContent = score;
  barFill.style.width = `${score}%`;

  // Update progress circle
  const circumference = 2 * Math.PI * 40;
  const offset = circumference - (score / 100) * circumference;
  scoreProgress.style.strokeDashoffset = offset;

  // Update status
  let status = "Needs Improvement";
  let color = "#e74c3c";
  if (score >= 75) {
    status = "Excellent Match";
    color = "#2ecc71";
  } else if (score >= 50) {
    status = "Good Match";
    color = "#f1c40f";
  }
  scoreStatus.textContent = status;
  scoreStatus.style.color = color;

  // Update skills
  matchedCount.textContent = matched.length;
  missingCount.textContent = missing.length;

  matchedSkills.innerHTML = matched
    .slice(0, 8)
    .map((s) => `<span class="skill-badge">${s}</span>`)
    .join("");

  missingSkills.innerHTML = missing
    .slice(0, 6)
    .map((s) => `<span class="skill-badge">${s}</span>`)
    .join("");

  // Update tips
  tipsList.innerHTML = recommendations
    .slice(0, 3)
    .map((r) => `<li>→ ${r}</li>`)
    .join("");
}

// Show loading state
function showLoading(message) {
  loadingState.style.display = "block";
  errorState.style.display = "none";
  loadingState.querySelector("p").textContent = message;
}

// Hide loading state
function hideLoading() {
  loadingState.style.display = "none";
}

// Show error state
function showError(message) {
  errorState.style.display = "block";
  loadingState.style.display = "none";
  errorMessage.textContent = message;
}

// Helper: Truncate text
function truncate(text, length) {
  if (!text) return "";
  return text.length > length ? text.substring(0, length) + "..." : text;
}
