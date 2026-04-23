// ResumeGPT Scanner - Content Script
// Injected into job sites to detect and extract job descriptions

(function () {
  "use strict";

  // Job site selectors
  const SITE_SELECTORS = {
    "linkedin.com": {
      title: [
        ".job-details-jobs-unified-top-card__job-title",
        ".jobs-unified-top-card__job-title",
        "h1",
      ],
      description: [
        ".jobs-description__content",
        ".jobs-box__html-content",
        ".job-details-jobs-unified-top-card__job-description",
        "#job-details",
      ],
      source: "LinkedIn",
    },
    "indeed.com": {
      title: [".jobsearch-JobInfoHeader-title", "h1"],
      description: ["#jobDescriptionText", ".jobsearch-jobDescriptionText"],
      source: "Indeed",
    },
    "glassdoor.com": {
      title: [".job-title", "h1"],
      description: [".jobDescriptionContent", ".desc"],
      source: "Glassdoor",
    },
    "ziprecruiter.com": {
      title: [".job_title", "h1"],
      description: [".job_description", "#job-description"],
      source: "ZipRecruiter",
    },
    "monster.com": {
      title: [".job_title", "h1"],
      description: [".job_description", "#JobDescription"],
      source: "Monster",
    },
  };

  // Get current site
  function getCurrentSite() {
    const hostname = window.location.hostname;
    for (const site of Object.keys(SITE_SELECTORS)) {
      if (hostname.includes(site)) {
        return site;
      }
    }
    return null;
  }

  // Extract text from selectors
  function extractFromSelectors(selectors) {
    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element && element.textContent.trim()) {
        return element.textContent.trim();
      }
    }
    return null;
  }

  // Detect job information
  function detectJob() {
    const site = getCurrentSite();

    if (site && SITE_SELECTORS[site]) {
      const config = SITE_SELECTORS[site];
      const title = extractFromSelectors(config.title);
      const description = extractFromSelectors(config.description);

      if (title || description) {
        return {
          title: title || "Job Detected",
          jobText: description || title,
          source: config.source,
          success: true,
        };
      }
    }

    // Generic detection for other sites
    return genericDetection();
  }

  // Generic job detection
  function genericDetection() {
    // Look for common job description patterns
    const bodyText = document.body.innerText.toLowerCase();

    // Check if this looks like a job posting
    const jobKeywords = [
      "responsibilities",
      "requirements",
      "qualifications",
      "experience",
      "skills",
      "job description",
      "about the role",
      "what you'll do",
    ];

    const hasJobKeywords = jobKeywords.some((keyword) =>
      bodyText.includes(keyword)
    );

    if (hasJobKeywords) {
      // Try to find the main content
      const mainContent =
        document.querySelector("main") ||
        document.querySelector("article") ||
        document.querySelector(".job-description") ||
        document.querySelector('[class*="description"]');

      if (mainContent) {
        return {
          title: document.title || "Job Detected",
          jobText: mainContent.textContent.trim().substring(0, 2000),
          source: new URL(window.location.href).hostname,
          success: true,
        };
      }
    }

    return {
      title: null,
      jobText: null,
      source: null,
      success: false,
    };
  }

  // Listen for messages from popup
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "detectJob") {
      const result = detectJob();
      sendResponse(result);
    }
    return true;
  });

  // Add floating badge (optional)
  function addFloatingBadge(score) {
    // Remove existing badge
    const existing = document.getElementById("resumegpt-badge");
    if (existing) existing.remove();

    // Create badge
    const badge = document.createElement("div");
    badge.id = "resumegpt-badge";
    badge.innerHTML = `
      <div class="resumegpt-badge-content">
        <span class="resumegpt-icon">🎯</span>
        <span class="resumegpt-score">ATS: ${score}/100</span>
      </div>
    `;

    // Add styles
    badge.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: linear-gradient(135deg, #e94560, #f39c12);
      color: white;
      padding: 10px 16px;
      border-radius: 12px;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 14px;
      font-weight: bold;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
      z-index: 10000;
      cursor: pointer;
      transition: transform 0.2s;
    `;

    badge.addEventListener("mouseenter", () => {
      badge.style.transform = "scale(1.05)";
    });

    badge.addEventListener("mouseleave", () => {
      badge.style.transform = "scale(1)";
    });

    badge.addEventListener("click", () => {
      chrome.runtime.sendMessage({ action: "openPopup" });
    });

    document.body.appendChild(badge);
  }

  // Listen for score updates
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "showScore") {
      addFloatingBadge(request.score);
    }
  });
})();
