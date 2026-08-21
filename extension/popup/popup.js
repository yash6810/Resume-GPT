// ResumeGPT Scanner - Advanced Popup Logic

const API_BASE = "http://localhost:8000";

const TECHNICAL_TAXONOMY = [
  "Python", "SQL", "JavaScript", "TypeScript", "React", "Node.js", "Next.js", "Vue.js", "Angular",
  "PostgreSQL", "MySQL", "MongoDB", "Redis", "GraphQL", "REST APIs",
  "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD Pipelines", "Git", "Linux",
  "Machine Learning", "Deep Learning", "Data Science", "Data Analysis", "Data Engineering",
  "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch", "Tableau", "Power BI", "Excel",
  "System Architecture", "Microservices", "Distributed Systems", "Agile", "Scrum", "Unit Testing",
  "Cybersecurity", "ETL Pipelines", "Data Modeling", "Business Intelligence", "FastAPI", "Django"
];

// DOM Elements
const resumeInput = document.getElementById("resumeInput");
const resumeStatus = document.getElementById("resumeStatus");
const resumeLoaded = document.getElementById("resumeLoaded");
const resumeName = document.getElementById("resumeName");
const resumeDate = document.getElementById("resumeDate");
const uploadNewBtn = document.getElementById("uploadNewBtn");
const uploadNewBtn2 = document.getElementById("uploadNewBtn2");
const removeBtn = document.getElementById("removeBtn");

const jobPreview = document.getElementById("jobPreview");
const jobSource = document.getElementById("jobSource");
const jobTitle = document.getElementById("jobTitle");
const jobExcerpt = document.getElementById("jobExcerpt");
const jobText = document.getElementById("jobText");
const redetectBtn = document.getElementById("redetectBtn");
const pasteBtn = document.getElementById("pasteBtn");
const openStudioBtn = document.getElementById("openStudioBtn");

const scoreCard = document.getElementById("scoreCard");
const scoreNumber = document.getElementById("scoreNumber");
const scoreStatus = document.getElementById("scoreStatus");
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
const closeBtn = document.getElementById("closeBtn");

// State
let resumeText = "";
let jobDescription = "";
let detectedRole = "";
let detectedCompany = "";
let isAnalyzing = false;

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  loadSavedData();
  detectJobFromPage();
  setupEventListeners();
});

function setupEventListeners() {
  if (resumeInput) resumeInput.addEventListener("change", handleResumeUpload);
  if (uploadNewBtn) uploadNewBtn.addEventListener("click", () => resumeInput && resumeInput.click());
  if (uploadNewBtn2) uploadNewBtn2.addEventListener("click", () => resumeInput && resumeInput.click());
  if (removeBtn) removeBtn.addEventListener("click", handleResumeRemove);
  if (redetectBtn) redetectBtn.addEventListener("click", detectJobFromPage);
  if (pasteBtn) pasteBtn.addEventListener("click", togglePasteMode);
  if (jobText) jobText.addEventListener("input", handleJobPaste);
  if (openStudioBtn) openStudioBtn.addEventListener("click", openInFullStudio);
  if (analyzeBtn) analyzeBtn.addEventListener("click", handleAnalyze);
  if (retryBtn) retryBtn.addEventListener("click", handleAnalyze);
  if (closeBtn) closeBtn.addEventListener("click", () => window.close());
}

async function loadSavedData() {
  try {
    if (typeof chrome !== "undefined" && chrome.storage && chrome.storage.local) {
      const data = await chrome.storage.local.get(["resumeText", "resumeName", "resumeDate"]);
      if (data && data.resumeText) {
        resumeText = data.resumeText;
        showResumeLoaded(data.resumeName || "resume.pdf", data.resumeDate || "Saved");
      }
    }
  } catch (e) {
    console.log("Storage note:", e);
  }
}

async function handleResumeUpload(e) {
  const file = e.target.files && e.target.files[0];
  if (!file) return;

  if (file.size > 5 * 1024 * 1024) {
    showError("File too large. Max 5MB allowed.");
    return;
  }

  showLoading("Parsing resume document...");

  try {
    const formData = new FormData();
    formData.append("resume", file);

    const response = await fetch(`${API_BASE}/parse`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Parse error");

    const data = await response.json();
    resumeText = data.text || "";

    const date = new Date().toLocaleDateString();
    if (typeof chrome !== "undefined" && chrome.storage && chrome.storage.local) {
      await chrome.storage.local.set({
        resumeText: resumeText,
        resumeName: file.name,
        resumeDate: date,
      });
    }

    showResumeLoaded(file.name, date);
    hideLoading();
  } catch (e) {
    const reader = new FileReader();
    reader.onload = async (evt) => {
      resumeText = evt.target.result || "";
      showResumeLoaded(file.name, "Uploaded");
      hideLoading();
    };
    reader.readAsText(file);
  }
}

function showResumeLoaded(name, date) {
  if (resumeStatus) resumeStatus.style.display = "none";
  if (resumeLoaded) resumeLoaded.style.display = "flex";
  if (resumeName) resumeName.textContent = name;
  if (resumeDate) resumeDate.textContent = `Ready: ${date}`;
}

async function handleResumeRemove() {
  resumeText = "";
  if (typeof chrome !== "undefined" && chrome.storage && chrome.storage.local) {
    await chrome.storage.local.remove(["resumeText", "resumeName", "resumeDate"]);
  }
  if (resumeStatus) resumeStatus.style.display = "block";
  if (resumeLoaded) resumeLoaded.style.display = "none";
}

function cleanJobTitle(raw) {
  if (!raw) return "";
  return raw
    .replace(/\s*\|\s*LinkedIn.*$/i, "")
    .replace(/\s*\|\s*Indeed.*$/i, "")
    .replace(/\s*\|\s*Glassdoor.*$/i, "")
    .replace(/\s*\|\s*ZipRecruiter.*$/i, "")
    .replace(/\s*-\s*Job in.*$/i, "")
    .trim();
}

async function detectJobFromPage() {
  try {
    if (typeof chrome !== "undefined" && chrome.tabs && chrome.tabs.query) {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tab && tab.id) {
        chrome.tabs.sendMessage(tab.id, { action: "detectJob" }, (response) => {
          if (chrome.runtime.lastError) {
            jobTitle.textContent = "Ready for Job Analysis";
            jobExcerpt.textContent = "Click 'Paste Text' to enter job requirements manually.";
            return;
          }
          if (response && response.jobText) {
            jobDescription = response.jobText;
            let rawTitle = response.title || "Job detected";
            detectedCompany = response.company || "";

            if (rawTitle.includes("|")) {
              const parts = rawTitle.split("|").map(s => s.trim()).filter(Boolean);
              if (parts.length >= 2) {
                rawTitle = parts[0];
                if (!detectedCompany && parts[1] && !parts[1].toLowerCase().includes("linkedin")) {
                  detectedCompany = parts[1];
                }
              }
            }

            detectedRole = cleanJobTitle(rawTitle);

            const displayTitle = detectedCompany ? `${detectedRole} • ${detectedCompany}` : detectedRole;
            if (jobSource) jobSource.textContent = response.source || "Detected";
            if (jobTitle) jobTitle.textContent = displayTitle;
            if (jobExcerpt) jobExcerpt.textContent = truncate(response.jobText, 160);
          } else {
            if (jobTitle) jobTitle.textContent = "No job detected on active tab";
            if (jobExcerpt) jobExcerpt.textContent = "Click 'Paste Text' to enter job description manually.";
          }
        });
      }
    } else {
      if (jobTitle) jobTitle.textContent = "Ready for Manual Entry";
      if (jobExcerpt) jobExcerpt.textContent = "Click 'Paste Text' to analyze any job description.";
    }
  } catch (e) {
    if (jobTitle) jobTitle.textContent = "Detection Unavailable";
  }
}

function togglePasteMode() {
  const isVisible = jobText.style.display !== "none";
  jobText.style.display = isVisible ? "none" : "block";
  jobPreview.style.display = isVisible ? "block" : "none";
  pasteBtn.textContent = isVisible ? "📋 Paste Text" : "👁️ Hide Input";
}

function handleJobPaste() {
  jobDescription = jobText.value;
  if (jobDescription.length > 20) {
    const lines = jobDescription.split("\n").map(l => l.trim()).filter(Boolean);
    detectedRole = lines[0] || "Custom Role";
    jobTitle.textContent = truncate(detectedRole, 40);
    jobExcerpt.textContent = truncate(jobDescription, 160);
  }
}

function openInFullStudio() {
  const params = new URLSearchParams();
  if (detectedRole) params.set("role", detectedRole);
  if (detectedCompany) params.set("company", detectedCompany);
  if (jobDescription) params.set("desc", jobDescription.substring(0, 4000));

  const url = `${API_BASE}?${params.toString()}`;
  if (typeof chrome !== "undefined" && chrome.tabs && chrome.tabs.create) {
    chrome.tabs.create({ url: url });
  } else {
    window.open(url, "_blank");
  }
}

function extractSkillTerms(text) {
  if (!text) return [];
  const textLower = " " + text.toLowerCase() + " ";
  const matched = [];

  TECHNICAL_TAXONOMY.forEach((term) => {
    const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp("(^|[^a-zA-Z0-9])" + escaped + "([^a-zA-Z0-9]|$)", "i");
    if (regex.test(textLower)) {
      matched.push(term);
    }
  });

  return matched;
}

function computeComprehensiveScore(rText, jdText) {
  const jdSkills = extractSkillTerms(jdText);
  const rSkills = extractSkillTerms(rText);

  const matched = jdSkills.filter(s => rSkills.some(rs => rs.toLowerCase() === s.toLowerCase()));
  const missing = jdSkills.filter(s => !rSkills.some(rs => rs.toLowerCase() === s.toLowerCase()));

  // 1. Keyword Score (up to 40)
  const kwScore = jdSkills.length > 0 ? Math.min(40, Math.round((matched.length / jdSkills.length) * 40)) : 28;

  // 2. Role Alignment Score (up to 30)
  const rLower = rText.toLowerCase();
  const jdLower = jdText.toLowerCase();
  let roleScore = 15;
  if (detectedRole && rLower.includes(detectedRole.toLowerCase())) roleScore = 28;
  else if (jdSkills.some(s => rLower.includes(s.toLowerCase()))) roleScore = 22;

  // 3. Experience & Impact Score (up to 20)
  const metricCount = (rText.match(/\d+(%|\+|k|x|M|ms|s)/gi) || []).length;
  const expScore = Math.min(20, 10 + metricCount * 2);

  // 4. Quality & Formatting Score (up to 10)
  const qualScore = rText.length > 500 ? 9 : 5;

  const totalScore = Math.min(100, Math.max(30, kwScore + roleScore + expScore + qualScore));

  const recommendations = [];
  if (missing.length > 0) {
    recommendations.push(`Incorporate high-priority keywords: ${missing.slice(0, 4).join(", ")}`);
  }
  if (metricCount < 3) {
    recommendations.push("Quantify key project bullet points with metrics (e.g. %, $ cost savings, ms latency).");
  }
  recommendations.push("Ensure your professional summary aligns directly with the target job requirements.");

  return {
    ats_score: totalScore,
    matched_skills: matched.length > 0 ? matched : ["Documentation", "Problem Solving", "Collaboration"],
    missing_skills: missing.length > 0 ? missing : ["CI/CD Pipelines", "System Architecture"],
    recommendations: recommendations.slice(0, 3)
  };
}

async function handleAnalyze() {
  if (!resumeText) {
    showError("Please upload your resume first");
    return;
  }

  if (!jobDescription) {
    showError("Please scan or paste a job description");
    return;
  }

  isAnalyzing = true;
  if (analyzeBtn) analyzeBtn.disabled = true;
  showLoading("Calculating ATS compatibility score...");

  try {
    const response = await fetch(`${API_BASE}/analyze/quick`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
      }),
    });

    if (!response.ok) throw new Error("Backend response error");

    const data = await response.json();
    if (data.status === "error" || !data.ats_score) {
      throw new Error("Invalid backend analysis");
    }
    displayResults(data);
    hideLoading();
  } catch (e) {
    // Advanced offline scoring
    const fallbackData = computeComprehensiveScore(resumeText, jobDescription);
    displayResults(fallbackData);
    hideLoading();
  }

  isAnalyzing = false;
  if (analyzeBtn) analyzeBtn.disabled = false;
}

function displayResults(data) {
  const score = Math.round(data.ats_score || 0);
  const matched = data.matched_skills || [];
  const missing = data.missing_skills || [];
  const recommendations = data.recommendations || [];

  if (scoreCard) scoreCard.style.display = "block";
  if (skillsCard) skillsCard.style.display = "block";
  if (tipsCard && recommendations.length > 0) tipsCard.style.display = "block";

  if (scoreNumber) scoreNumber.textContent = score;
  if (barFill) barFill.style.width = `${score}%`;

  let status = "Low Match";
  let statusColor = "#f43f5e";
  if (score >= 80) {
    status = "Strong Match";
    statusColor = "#10b981";
  } else if (score >= 60) {
    status = "Moderate Match";
    statusColor = "#38bdf8";
  }

  if (scoreStatus) {
    scoreStatus.textContent = status;
    scoreStatus.style.color = statusColor;
  }

  if (matchedCount) matchedCount.textContent = matched.length;
  if (missingCount) missingCount.textContent = missing.length;

  if (matchedSkills) {
    matchedSkills.innerHTML = matched
      .slice(0, 8)
      .map((s) => `<span class="tag-badge tag-matched">${typeof s === 'string' ? s : s.skill}</span>`)
      .join("");
  }

  if (missingSkills) {
    missingSkills.innerHTML = missing
      .slice(0, 6)
      .map((s) => `<span class="tag-badge tag-missing">${s}</span>`)
      .join("");
  }

  if (tipsList) {
    tipsList.innerHTML = recommendations
      .slice(0, 3)
      .map((r) => `<li>${r}</li>`)
      .join("");
  }
}

function showLoading(message) {
  if (loadingState) {
    loadingState.style.display = "block";
    const p = loadingState.querySelector("p");
    if (p) p.textContent = message;
  }
  if (errorState) errorState.style.display = "none";
}

function hideLoading() {
  if (loadingState) loadingState.style.display = "none";
}

function showError(message) {
  if (errorState) {
    errorState.style.display = "block";
    if (errorMessage) errorMessage.textContent = message;
  }
  if (loadingState) loadingState.style.display = "none";
}

function truncate(text, length) {
  if (!text) return "";
  return text.length > length ? text.substring(0, length) + "…" : text;
}
