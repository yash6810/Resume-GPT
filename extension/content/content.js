// ResumeGPT Scanner - High-Precision Content Script
// Detects and cleanly extracts job postings from LinkedIn, Indeed, Glassdoor, and career portals

(function () {
  "use strict";

  const SITE_CONFIGS = {
    "linkedin.com": {
      source: "LinkedIn",
      title: [
        "h1.t-24",
        ".job-details-jobs-unified-top-card__job-title",
        ".jobs-unified-top-card__job-title",
        ".jobs-details__main-content h1",
        "h1.top-card-layout__title",
        "h1"
      ],
      company: [
        ".job-details-jobs-unified-top-card__company-name",
        ".jobs-unified-top-card__company-name",
        "a.topcard__org-name-link",
        ".job-details-jobs-unified-top-card__primary-description-container a",
        "[data-company-name]"
      ],
      location: [
        ".job-details-jobs-unified-top-card__bullet",
        ".jobs-unified-top-card__bullet",
        ".topcard__flavor--bullet"
      ],
      description: [
        "#job-details",
        ".jobs-description__content",
        ".jobs-box__html-content",
        ".jobs-description-content__text",
        ".show-more-less-html__markup",
        "article.jobs-description__container"
      ]
    },
    "indeed.com": {
      source: "Indeed",
      title: [
        "[data-testid='jobsearch-JobInfoHeader-title']",
        ".jobsearch-JobInfoHeader-title",
        "h1.jobsearch-JobInfoHeader-title",
        "h2.jobsearch-JobInfoHeader-title",
        "h1"
      ],
      company: [
        "[data-testid='inlineHeader-companyName']",
        ".jobsearch-InlineCompanyRating-companyHeader",
        "[data-company-name='true']",
        ".jobsearch-CompanyInfoContainer a"
      ],
      location: [
        "[data-testid='inlineHeader-companyLocation']",
        ".jobsearch-JobInfoHeader-companyLocation"
      ],
      description: [
        "#jobDescriptionText",
        ".jobsearch-jobDescriptionText",
        "div#jobDescriptionText",
        ".jobsearch-JobComponent-description"
      ]
    },
    "glassdoor.com": {
      source: "Glassdoor",
      title: [
        "[data-test='job-title']",
        ".job-title",
        "h1.headingSubheading",
        "h1"
      ],
      company: [
        "[data-test='employer-name']",
        ".employer-name",
        ".job-search-key-16z3fd0"
      ],
      location: [
        "[data-test='location']",
        ".job-location"
      ],
      description: [
        "[data-test='jobDescriptionContent']",
        ".jobDescriptionContent",
        ".desc",
        "#JobDescriptionContainer"
      ]
    },
    "ziprecruiter.com": {
      source: "ZipRecruiter",
      title: [".job_title", "h1.job_title", "h1"],
      company: [".hiring_company_text", ".hiring_company"],
      location: [".location_text", ".location"],
      description: [".job_description", "#job-description", ".jobDescriptionSection"]
    },
    "wellfound.com": {
      source: "Wellfound (AngelList)",
      title: ["h1.styles_title__", "h1"],
      company: [".styles_startupName__", "h2"],
      location: [".styles_location__"],
      description: [".styles_description__", "[class*='jobDescription']"]
    },
    "greenhouse.io": {
      source: "Greenhouse",
      title: [".app-title", "h1.app-title", "h1"],
      company: [".company-name", "h2"],
      location: [".location"],
      description: ["#content", ".content", "#app_body"]
    },
    "lever.co": {
      source: "Lever",
      title: [".posting-headline h2", "h2"],
      company: [".main-header-logo", ".posting-headline"],
      location: [".posting-categories .location"],
      description: [".posting-description", ".section-wrapper", ".content"]
    }
  };

  function getCurrentSite() {
    const hostname = window.location.hostname;
    for (const site of Object.keys(SITE_CONFIGS)) {
      if (hostname.includes(site)) return site;
    }
    return null;
  }

  function cleanText(raw) {
    if (!raw) return "";
    return raw
      .replace(/[\r\t]+/g, " ")
      .replace(/\n\s*\n+/g, "\n\n")
      .replace(/\b(Show more|Show less|Apply now|Easy Apply|Save job|Report this job|Report job|Posted on|About the company)\b/gi, "")
      .replace(/\s{2,}/g, " ")
      .trim();
  }

  function extractFromSelectors(selectors) {
    if (!selectors) return "";
    for (const selector of selectors) {
      const el = document.querySelector(selector);
      if (el) {
        // Prefer innerText as it respects line breaks and ignores hidden elements
        const txt = el.innerText || el.textContent;
        if (txt && txt.trim().length > 3) {
          return cleanText(txt);
        }
      }
    }
    return "";
  }

  function detectJob() {
    const siteKey = getCurrentSite();

    if (siteKey && SITE_CONFIGS[siteKey]) {
      const cfg = SITE_CONFIGS[siteKey];
      const title = extractFromSelectors(cfg.title);
      const company = extractFromSelectors(cfg.company);
      const location = extractFromSelectors(cfg.location);
      const description = extractFromSelectors(cfg.description);

      if (description || title) {
        return {
          title: title || "Job Detected",
          company: company || "",
          location: location || "",
          jobText: description || title,
          source: cfg.source,
          success: true
        };
      }
    }

    // Generic heuristic fallback for career portals
    return genericFallbackDetection();
  }

  function genericFallbackDetection() {
    const candidateContainers = [
      "main",
      "article",
      "[role='main']",
      "#job-description",
      ".job-description",
      ".job-details",
      "[class*='description']"
    ];

    let bestContainer = null;
    let maxLen = 0;

    for (const sel of candidateContainers) {
      const el = document.querySelector(sel);
      if (el) {
        const len = (el.innerText || el.textContent || "").length;
        if (len > maxLen && len > 150) {
          maxLen = len;
          bestContainer = el;
        }
      }
    }

    if (bestContainer) {
      const titleEl = document.querySelector("h1") || document.querySelector("h2");
      const title = titleEl ? titleEl.innerText.trim() : document.title;
      const desc = cleanText(bestContainer.innerText || bestContainer.textContent || "");

      return {
        title: title || "Job Posting",
        company: "",
        location: "",
        jobText: desc.substring(0, 4000),
        source: new URL(window.location.href).hostname.replace("www.", ""),
        success: true
      };
    }

    return {
      title: "",
      company: "",
      location: "",
      jobText: "",
      source: "",
      success: false
    };
  }

  // Handle messages from popup
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "detectJob") {
      const result = detectJob();
      sendResponse(result);
    }
    return true;
  });
})();
