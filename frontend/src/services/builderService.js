import { request } from './api.js';

export const INDUSTRY_PRESETS = {
  software: {
    title: 'Software Engineering',
    summary: 'Senior Software Engineer with 6+ years designing, scaling, and deploying distributed cloud architectures. Proven track record reducing system latency by 42% and leading cross-functional engineering teams.',
    skills: 'Python, TypeScript, React, Node.js, PostgreSQL, Docker, Kubernetes, AWS, GraphQL, CI/CD Pipelines, Microservices, Redis',
    experience: 'Apex Cloud Solutions | Senior Software Engineer | 2022 - Present\n- Architected high-throughput microservices using Python and FastAPI, handling 15M+ daily requests with 99.99% uptime.\n- Engineered automated CI/CD deployment pipelines on AWS and Docker, slashing release cycles from 2 weeks to 35 minutes.\n- Spearheaded database query optimizations in PostgreSQL and Redis, reducing p99 latency by 45%.\n\nTechForge Labs | Software Engineer | 2019 - 2022\n- Developed responsive web applications using React and TypeScript, boosting core user engagement metrics by 28%.\n- Integrated secure OAuth2 and Stripe payment processing systems, processing $2.5M+ in annual transaction volume.',
    education: 'B.S. in Computer Science\nUniversity of California, Berkeley\n2015 - 2019'
  },
  data: {
    title: 'Data Science & AI',
    summary: 'Data Scientist & ML Engineer specializing in predictive modeling, NLP pipelines, and big data architecture. Expert at translating complex analytical findings into high-impact executive strategies.',
    skills: 'Python, SQL, PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, BigQuery, Snowflake, Tableau, Data Pipelines, Statistical Modeling',
    experience: 'DataCore Intelligence | Lead Data Scientist | 2022 - Present\n- Built customer churn forecasting models using XGBoost and PyTorch, improving retention by 18% ($1.2M annualized savings).\n- Designed automated ETL pipelines in BigQuery and Apache Airflow, processing 5TB+ daily streaming data.\n- Deployed real-time inference microservices with Docker and FastAPI, achieving sub-20ms latency.\n\nOmniAnalytics | Data Analyst | 2019 - 2022\n- Created executive Tableau dashboards tracking customer lifecycle KPIs, adopted by 85+ stakeholders.\n- Conducted rigorous A/B experimentation frameworks that increased conversion rates by 14%.',
    education: 'M.S. in Data Science\nGeorgia Institute of Technology\n2017 - 2019'
  },
  product: {
    title: 'Product Management',
    summary: 'Customer-obsessed Product Manager with 5+ years driving SaaS product discovery, roadmap execution, and 0-to-1 feature launches that accelerate ARR growth.',
    skills: 'Product Strategy, Agile / Scrum, User Research, Wireframing, Roadmapping, SQL, A/B Testing, Feature Prioritization, Data Analysis',
    experience: 'Nexus Digital Group | Senior Product Manager | 2021 - Present\n- Led cross-functional squad of 12 engineers and designers to launch core workflow automation suite, driving $3.8M in net new ARR.\n- Implemented continuous discovery and user interviews, increasing product NPS from 42 to 68 within 12 months.\n- Optimized onboarding funnel via iterative A/B testing, lifting day-30 user retention by 22%.\n\nVentureScale | Associate Product Manager | 2018 - 2021\n- Defined product requirements and user stories for core mobile application with 500K+ MAU.\n- Collaborated with marketing and sales to orchestrate 4 major go-to-market feature releases.',
    education: 'B.A. in Economics & Information Systems\nUniversity of Michigan\n2014 - 2018'
  }
};

export async function exportDocx(resumePayload) {
  const res = await request('/export/docx', {
    method: 'POST',
    body: JSON.stringify(resumePayload),
  });

  if (!res.ok) {
    throw new Error('DOCX export failed');
  }

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${resumePayload.contact?.name || 'Resume'}_Tailored.docx`;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

export async function exportPdf(resumePayload) {
  const res = await request('/export/pdf', {
    method: 'POST',
    body: JSON.stringify(resumePayload),
  });

  if (!res.ok) {
    throw new Error('PDF export failed');
  }

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${resumePayload.contact?.name || 'Resume'}_Tailored.pdf`;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

export async function generateCoverLetter(resumeText, jobDescription, companyName, position) {
  const res = await request('/cover-letter/generate', {
    method: 'POST',
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
      company_name: companyName,
      position: position,
    }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Generation failed' }));
    throw new Error(err.detail || 'Cover letter generation failed');
  }

  return res.json();
}
