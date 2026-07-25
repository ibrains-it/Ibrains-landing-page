-- IBrains Autonomous AI SDR & Revenue Intelligence Platform V2.1 Master Database Schema

-- 1. Master Agent Catalog
CREATE TABLE IF NOT EXISTS agent_catalog (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    target_industries TEXT[],
    target_pain_points TEXT[],
    demo_url VARCHAR(255),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Organizations (Normalized & Canonical)
CREATE TABLE IF NOT EXISTS organizations_v2 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    normalized_name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    normalized_domain VARCHAR(255) UNIQUE,
    industry VARCHAR(100),
    employee_range VARCHAR(50),
    location VARCHAR(150),
    website VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Lead Source Attribution
CREATE TABLE IF NOT EXISTS lead_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations_v2(id) ON DELETE CASCADE,
    source_platform VARCHAR(100) NOT NULL, -- MAPS, DIRECTORY, JOB_POSTING, PRODUCT_HUNT
    source_external_id VARCHAR(255),
    raw_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Decision Maker Contacts
CREATE TABLE IF NOT EXISTS contacts_v2 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations_v2(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    job_title VARCHAR(150),
    email VARCHAR(255) UNIQUE,
    email_verified BOOLEAN DEFAULT FALSE,
    phone VARCHAR(50),
    linkedin_url VARCHAR(255),
    decision_maker_score INT DEFAULT 50,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Detected Buying Signals
CREATE TABLE IF NOT EXISTS signals_v2 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations_v2(id) ON DELETE CASCADE,
    signal_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    source_url TEXT,
    confidence NUMERIC(3, 2) DEFAULT 0.85,
    detected_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Evidence Store
CREATE TABLE IF NOT EXISTS evidence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations_v2(id) ON DELETE CASCADE,
    signal_id UUID REFERENCES signals_v2(id) ON DELETE SET NULL,
    source_type VARCHAR(100) NOT NULL,
    source_url TEXT NOT NULL,
    evidence_text TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    confidence NUMERIC(3, 2) DEFAULT 0.90,
    observed_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Opportunities & Catalog Matching
CREATE TABLE IF NOT EXISTS opportunities_v2 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations_v2(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agent_catalog(id),
    pain_point TEXT NOT NULL,
    business_impact TEXT,
    lead_score INT DEFAULT 0,
    priority VARCHAR(20) DEFAULT 'NURTURE',
    status VARCHAR(50) DEFAULT 'IDENTIFIED',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Opportunity Evidence Association
CREATE TABLE IF NOT EXISTS opportunity_evidence (
    opportunity_id UUID REFERENCES opportunities_v2(id) ON DELETE CASCADE,
    evidence_id UUID REFERENCES evidence(id) ON DELETE CASCADE,
    PRIMARY KEY (opportunity_id, evidence_id)
);

-- 9. Versioned Lead Scoring Models
CREATE TABLE IF NOT EXISTS scoring_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version VARCHAR(20) UNIQUE NOT NULL,
    icp_weight INT DEFAULT 25,
    pain_weight INT DEFAULT 20,
    intent_weight INT DEFAULT 20,
    access_weight INT DEFAULT 15,
    value_weight INT DEFAULT 10,
    evidence_weight INT DEFAULT 10,
    active BOOLEAN DEFAULT FALSE,
    approved_by VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. Global Suppression List
CREATE TABLE IF NOT EXISTS suppression_list (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identifier VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(20) NOT NULL,
    reason VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 11. Outreach Campaigns
CREATE TABLE IF NOT EXISTS outreach_campaigns_v2 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    target_icp VARCHAR(100),
    primary_channel VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'DRAFT',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 12. Outreach Messages (Human Approval Queue)
CREATE TABLE IF NOT EXISTS outreach_messages_v2 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES contacts_v2(id) ON DELETE CASCADE,
    opportunity_id UUID REFERENCES opportunities_v2(id),
    campaign_id UUID REFERENCES outreach_campaigns_v2(id),
    channel VARCHAR(50) NOT NULL,
    subject TEXT,
    message_body TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING_APPROVAL',
    approved_by VARCHAR(100),
    sent_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 13. Interaction Telemetry & Conversions
CREATE TABLE IF NOT EXISTS interactions_v2 (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES contacts_v2(id) ON DELETE CASCADE,
    message_id UUID REFERENCES outreach_messages_v2(id),
    direction VARCHAR(20) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    sentiment VARCHAR(50),
    deal_value NUMERIC(10, 2) DEFAULT 0.00,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
