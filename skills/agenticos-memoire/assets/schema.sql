-- AgenticOS — schéma mémoire de référence (PostgreSQL 16)
-- Invariants : tenant_id NOT NULL partout, état relisible inter-runs,
-- propositions de méta-agents traçables avec validation humaine.

-- État inter-runs des agents
CREATE TABLE agent_state (
    tenant_id   TEXT        NOT NULL,
    agent       TEXT        NOT NULL,
    key         TEXT        NOT NULL,
    value       JSONB       NOT NULL,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (tenant_id, agent, key)
);

-- Journal d'exécutions (support du reaper et du diagnostic)
CREATE TABLE agent_runs (
    id           BIGSERIAL PRIMARY KEY,
    tenant_id    TEXT        NOT NULL,
    agent        TEXT        NOT NULL,
    status       TEXT        NOT NULL CHECK (status IN ('queued','running','succeeded','failed','held')),
    idempotency_key TEXT     NOT NULL,
    started_at   TIMESTAMPTZ,
    finished_at  TIMESTAMPTZ,
    timeout_s    INTEGER     NOT NULL DEFAULT 900,
    error_detail TEXT,        -- (stderr or stdout)[-2000:] — taux d'échecs diagnosables > 90 %
    cost_usd     NUMERIC(10,4),
    UNIQUE (tenant_id, agent, idempotency_key)   -- idempotence : pas de doublon au retry
);

-- Index du reaper : zombies running > timeout → failed
CREATE INDEX idx_agent_runs_zombies ON agent_runs (status, started_at) WHERE status = 'running';

-- Propositions des méta-agents (auto-apprentissage)
-- State machine : proposed → approved | rejected | vetoed → applied → verified
CREATE TABLE meta_proposals (
    id           BIGSERIAL PRIMARY KEY,
    tenant_id    TEXT        NOT NULL,
    meta_agent   TEXT        NOT NULL,
    kind         TEXT        NOT NULL,        -- config | prompt | routing | code
    payload      JSONB       NOT NULL,
    status       TEXT        NOT NULL DEFAULT 'proposed'
                 CHECK (status IN ('proposed','approved','rejected','vetoed','applied','verified')),
    approved_by  TEXT,                        -- obligatoire avant toute mutation
    approved_at  TIMESTAMPTZ,
    applied_at   TIMESTAMPTZ,
    verified_at  TIMESTAMPTZ,
    veto_reason  TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    -- Aucune application sans validation humaine horodatée
    CHECK (applied_at IS NULL OR (approved_by IS NOT NULL AND approved_at IS NOT NULL))
);

-- Mémoire vectorielle : la collection Qdrant associée porte un filtre tenant_id
-- obligatoire dans la couche d'accès (voir references/schema-et-retention.md §2).
CREATE TABLE memory_consolidation_log (
    id           BIGSERIAL PRIMARY KEY,
    tenant_id    TEXT        NOT NULL,
    agent        TEXT        NOT NULL,
    window_start TIMESTAMPTZ NOT NULL,
    window_end   TIMESTAMPTZ NOT NULL,
    summary_key  TEXT        NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, agent, window_start)     -- consolidation idempotente
);
