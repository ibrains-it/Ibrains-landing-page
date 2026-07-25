-- Seed Script: IBrains Master Agent Catalog Seeding (11 Production Agents)

INSERT INTO agent_catalog (name, slug, description, target_industries, target_pain_points, demo_url)
VALUES
('HR Voice Agent', 'hr-voice-agent', 'Automated first-round voice screening, policy Q&A, and interview scheduling.', ARRAY['HR', 'Recruiting', 'Enterprise'], ARRAY['HIGH_VOLUME_SCREENING', 'RECRUITER_BURNOUT'], 'https://ibrains.pages.dev/#agents'),
('Resume Shortlisting Agent', 'resume-shortlisting-agent', 'AI resume parser that matches candidate resumes against exact Job Descriptions.', ARRAY['HR', 'Recruiting', 'Staffing'], ARRAY['MANUAL_RESUME_PARSING', 'CANDIDATE_BACKLOG'], 'https://ibrains.pages.dev/#agents'),
('Technical Interviewer Agent', 'technical-interviewer-agent', 'Voice-based technical interviews assessing engineering fundamentals and problem solving.', ARRAY['Technology', 'Software', 'IT Services'], ARRAY['ENGINEERING_INTERVIEW_BOTTLENECK'], 'https://ibrains.pages.dev/#agents'),
('Coding Round Interviewer Agent', 'coding-round-interviewer-agent', 'Automated live coding interview evaluator assessing syntax, algorithms, and edge cases.', ARRAY['Software', 'EdTech', 'Tech Hiring'], ARRAY['CODING_EVALUATION_LATENCY'], 'https://ibrains.pages.dev/#agents'),
('System Design Interview Agent', 'system-design-interview-agent', 'Evaluates architecture, scalability, trade-offs, and design principles in tech candidates.', ARRAY['Enterprise Tech', 'Cloud', 'SaaS'], ARRAY['SENIOR_TECH_INTERVIEW_CAPACITY'], 'https://ibrains.pages.dev/#agents'),
('Screen Tracker Agent', 'screen-tracker-agent', 'Watches a shared screen in real-time, answering questions conversationally.', ARRAY['Support', 'QA', 'Remote Ops'], ARRAY['VISUAL_QA_LATENCY', 'REMOTE_MONITORING'], 'https://ibrains.pages.dev/#agents'),
('Real Estate Voice Agent', 'real-estate-voice-agent', 'Handles inbound property calls, buyer qualification, and instant appointment booking.', ARRAY['Real Estate', 'Property Management'], ARRAY['MISSED_PROPERTY_CALLS', 'UNQUALIFIED_LEADS'], 'https://ibrains.pages.dev/#agents'),
('CRM Agent', 'crm-agent', 'Automates post-call CRM logging, deal stage updates, and follow-up triggers.', ARRAY['Sales', 'B2B Services'], ARRAY['MANUAL_CRM_ENTRY', 'DATA_STALE'], 'https://ibrains.pages.dev/#agents'),
('Ortho Medical Agent', 'ortho-medical-agent', 'Handles patient intake, symptom collection, and clinic appointment scheduling.', ARRAY['Healthcare', 'Medical Clinics'], ARRAY['PATIENT_CALL_WAIT_TIMES', 'FRONT_DESK_OVERLOAD'], 'https://ibrains.pages.dev/#agents'),
('Loan Agent', 'loan-agent', 'Calculates loan options, verifies document eligibility, and answers mortgage/loan queries by voice.', ARRAY['Finance', 'Banking', 'Mortgage'], ARRAY['SLOW_LOAN_PREQUALIFICATION'], 'https://ibrains.pages.dev/#agents'),
('Insurance Agent', 'insurance-agent', 'Handles policy questions, claims status tracking, and premium renewal reminders.', ARRAY['Insurance', 'Financial Services'], ARRAY['HIGH_CLAIM_STATUS_CALLS'], 'https://ibrains.pages.dev/#agents')
ON CONFLICT (slug) DO UPDATE SET
description = EXCLUDED.description,
target_industries = EXCLUDED.target_industries,
target_pain_points = EXCLUDED.target_pain_points;
