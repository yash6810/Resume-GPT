import React, { useMemo, useState } from 'react';
import { request } from '../../services/api';

const DEFAULT_PROFILE = {
  name: 'Yash Upadhyay', location: 'Noida, India', graduation_year: 2027,
  degree: 'B.Tech Computer Science & Engineering',
  target_roles: ['Data Science Intern','Machine Learning Intern','Quantitative Research Intern','Risk Analytics Intern','AI/ML Intern','Software Engineer Intern'],
  target_domains: ['finance','fintech','financial services','machine learning','quantitative finance'],
  skills: ['Python','SQL','XGBoost','PyTorch','Scikit-learn','Machine Learning','NLP','FastAPI','Docker','MLflow','Backtesting','Risk Management','Algorithmic Trading','Financial NLP'],
  resume_text: ''
};

export function InternshipOS() {
  const [profile, setProfile] = useState(DEFAULT_PROFILE);
  const [job, setJob] = useState({company:'',title:'',description:'',url:'',location:'',source:'manual'});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const disabled = useMemo(() => !job.title || !job.description, [job]);

  const runMatch = async () => {
    setLoading(true);
    try {
      const res = await request('/internships/match', {method:'POST', body:JSON.stringify({candidate:profile,job})});
      if (!res.ok) throw new Error('Matching failed');
      setResult(await res.json());
    } catch (e) {
      setResult({error:e.message});
    } finally { setLoading(false); }
  };

  return <div className="fade-in" style={{padding:'2rem',maxWidth:'1280px',margin:'0 auto'}}>
    <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-end',marginBottom:'1.5rem'}}>
      <div><h1 style={{fontSize:'2rem',fontWeight:850,color:'#f8fafc'}}>InternshipOS</h1><p style={{color:'#94a3b8'}}>Discover → Match → Tailor → Review → Apply</p></div>
      <div style={{padding:'0.5rem 0.75rem',border:'1px solid rgba(56,189,248,.25)',borderRadius:'999px',color:'#7dd3fc',fontSize:'12px'}}>HUMAN-IN-THE-LOOP</div>
    </div>
    <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'1.25rem'}}>
      <section className="glass-card" style={{padding:'1.25rem',borderRadius:'1rem'}}>
        <h3 style={{color:'#fff',marginBottom:'1rem'}}>Candidate profile</h3>
        <input placeholder="Name" value={profile.name} onChange={e=>setProfile({...profile,name:e.target.value})} style={{width:'100%',marginBottom:'.75rem'}} />
        <input placeholder="Location" value={profile.location} onChange={e=>setProfile({...profile,location:e.target.value})} style={{width:'100%',marginBottom:'.75rem'}} />
        <input placeholder="Target roles (comma separated)" value={profile.target_roles.join(', ')} onChange={e=>setProfile({...profile,target_roles:e.target.value.split(',').map(x=>x.trim()).filter(Boolean)})} style={{width:'100%',marginBottom:'.75rem'}} />
        <input placeholder="Skills (comma separated)" value={profile.skills.join(', ')} onChange={e=>setProfile({...profile,skills:e.target.value.split(',').map(x=>x.trim()).filter(Boolean)})} style={{width:'100%'}} />
      </section>
      <section className="glass-card" style={{padding:'1.25rem',borderRadius:'1rem'}}>
        <h3 style={{color:'#fff',marginBottom:'1rem'}}>Job posting</h3>
        <input placeholder="Company" value={job.company} onChange={e=>setJob({...job,company:e.target.value})} style={{width:'100%',marginBottom:'.75rem'}} />
        <input placeholder="Role title" value={job.title} onChange={e=>setJob({...job,title:e.target.value})} style={{width:'100%',marginBottom:'.75rem'}} />
        <input placeholder="Location" value={job.location} onChange={e=>setJob({...job,location:e.target.value})} style={{width:'100%',marginBottom:'.75rem'}} />
        <input placeholder="Application URL" value={job.url} onChange={e=>setJob({...job,url:e.target.value})} style={{width:'100%',marginBottom:'.75rem'}} />
        <textarea placeholder="Paste job description" value={job.description} onChange={e=>setJob({...job,description:e.target.value})} rows={9} style={{width:'100%',resize:'vertical'}} />
        <button disabled={disabled||loading} onClick={runMatch} className="btn btn-primary" style={{marginTop:'.75rem',width:'100%'}}>{loading?'Analyzing…':'Analyze & Match'}</button>
      </section>
    </div>
    {result && !result.error && <section className="glass-card" style={{padding:'1.5rem',borderRadius:'1rem',marginTop:'1.25rem'}}>
      <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}><div><div style={{fontSize:'12px',color:'#94a3b8'}}>MATCH SCORE</div><div style={{fontSize:'3rem',fontFamily:'var(--font-mono)',fontWeight:850,color:'#6ee7b7'}}>{result.score}%</div></div><div style={{textAlign:'right'}}><div style={{color:'#cbd5e1'}}>Recommended CV</div><strong style={{color:'#7dd3fc'}}>{result.recommended_resume}</strong></div></div>
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'1rem',marginTop:'1.25rem'}}>
        <div><h4 style={{color:'#fff'}}>Matched skills</h4><p style={{color:'#86efac'}}>{result.matched_skills?.join(' · ')||'None'}</p></div>
        <div><h4 style={{color:'#fff'}}>Missing / review</h4><p style={{color:'#fbbf24'}}>{result.missing_skills?.join(' · ')||'None detected'}</p></div>
      </div>
      <div style={{marginTop:'1rem',padding:'1rem',border:'1px solid rgba(245,158,11,.25)',borderRadius:'.75rem',background:'rgba(245,158,11,.06)'}}><strong style={{color:'#fde68a'}}>Before submission:</strong><span style={{color:'#cbd5e1'}}> review eligibility, answers and generated materials. ResumeGPT never invents qualifications.</span></div>
    </section>}
    {result?.error && <div style={{marginTop:'1rem',color:'#fca5a5'}}>{result.error}</div>}
  </div>;
}
