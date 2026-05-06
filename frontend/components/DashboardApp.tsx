"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { DashboardHeader } from "@/components/DashboardHeader";
import { ErrorCallout } from "@/components/ErrorCallout";
import { NewTicketModal } from "@/components/NewTicketModal";
import { ResolveTicketModal } from "@/components/ResolveTicketModal";
import { StatsCards } from "@/components/StatsCards";
import { TicketDetailPanel } from "@/components/TicketDetailPanel";
import { TicketList } from "@/components/TicketList";
import { TicketQueueSidebar } from "@/components/TicketQueueSidebar";
import {
  analyzeTicket,
  applyAnalysis,
  createTicket,
  fetchDashboardStats,
  fetchTicketDetail,
  fetchTickets,
  resolveTicket,
} from "@/lib/api";
import type { ApplyAnalysisPayload, DashboardStats, NewTicketPayload, Ticket, TicketDetail, TicketFilters } from "@/lib/types";

const defaultFilters: TicketFilters = {
  sort: "newest",
};

export function DashboardApp() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [selectedTicketId, setSelectedTicketId] = useState<number | null>(null);
  const [detail, setDetail] = useState<TicketDetail | null>(null);
  const [filters, setFilters] = useState<TicketFilters>(defaultFilters);
  const [loadingTickets, setLoadingTickets] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [savingTicket, setSavingTicket] = useState(false);
  const [analyzingTicketId, setAnalyzingTicketId] = useState<number | null>(null);
  const [applyingAnalysisId, setApplyingAnalysisId] = useState<number | null>(null);
  const [resolveModalOpen, setResolveModalOpen] = useState(false);
  const [savingResolution, setSavingResolution] = useState(false);
  const [originTicket, setOriginTicket] = useState<{ id: number; title: string } | null>(null);

  const selectedTicket = useMemo(
    () =>
      tickets.find((ticket) => ticket.id === selectedTicketId) ??
      (detail?.ticket.id === selectedTicketId ? detail.ticket : null),
    [selectedTicketId, tickets, detail],
  );

  const loadStats = useCallback(async () => {
    const nextStats = await fetchDashboardStats();
    setStats(nextStats);
  }, []);

  const loadTickets = useCallback(async () => {
    setLoadingTickets(true);
    const response = await fetchTickets(filters);
    setTickets(response.items);
    setSelectedTicketId((current) => current ?? response.items[0]?.id ?? null);
    setLoadingTickets(false);
  }, [filters]);

  const loadDetail = useCallback(async (ticketId: number) => {
    const nextDetail = await fetchTicketDetail(ticketId);
    setDetail(nextDetail);
  }, []);

  const refreshAll = useCallback(async () => {
    setError(null);
    try {
      await Promise.all([loadStats(), loadTickets()]);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to load dashboard data.");
      setLoadingTickets(false);
    }
  }, [loadStats, loadTickets]);

  useEffect(() => {
    void refreshAll();
  }, [refreshAll]);

  useEffect(() => {
    if (!selectedTicketId) {
      setDetail(null);
      return;
    }
    loadDetail(selectedTicketId).catch((caught) => {
      setError(caught instanceof Error ? caught.message : "Unable to load ticket detail.");
    });
  }, [loadDetail, selectedTicketId]);

  function handleFilterChange(key: keyof TicketFilters, value: string) {
    setFilters((current) => ({
      ...current,
      [key]: value || undefined,
    }));
    setSelectedTicketId(null);
    setOriginTicket(null);
  }

  function handleSelectTicket(ticket: Ticket) {
    setSelectedTicketId(ticket.id);
    setOriginTicket(null);
  }

  async function handleOpenSimilarTicket(ticketId: number) {
    if (!detail) {
      return;
    }
    setError(null);
    setOriginTicket({ id: detail.ticket.id, title: detail.ticket.title });
    setSelectedTicketId(ticketId);
    try {
      await loadDetail(ticketId);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to load similar ticket.");
    }
  }

  async function handleReturnToOrigin() {
    if (!originTicket) {
      return;
    }
    const target = originTicket;
    setOriginTicket(null);
    setSelectedTicketId(target.id);
    try {
      await loadDetail(target.id);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to return to original ticket.");
    }
  }

  async function handleCreateTicket(payload: NewTicketPayload) {
    setSavingTicket(true);
    setError(null);
    try {
      const created = await createTicket(payload);
      setModalOpen(false);
      await Promise.all([loadStats(), loadTickets()]);
      setOriginTicket(null);
      setSelectedTicketId(created.id);
      await loadDetail(created.id);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to create ticket.");
    } finally {
      setSavingTicket(false);
    }
  }

  async function handleAnalyzeTicket(ticketId: number) {
    setAnalyzingTicketId(ticketId);
    setError(null);
    try {
      const nextDetail = await analyzeTicket(ticketId);
      setDetail(nextDetail);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to run AI triage.");
    } finally {
      setAnalyzingTicketId(null);
    }
  }

  async function handleApplyAnalysis(ticketId: number, analysisId: number, payload: ApplyAnalysisPayload) {
    setApplyingAnalysisId(analysisId);
    setError(null);
    try {
      const nextDetail = await applyAnalysis(ticketId, analysisId, payload);
      setDetail(nextDetail);
      await Promise.all([loadStats(), loadTickets()]);
      setSelectedTicketId(ticketId);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to apply AI suggestions.");
    } finally {
      setApplyingAnalysisId(null);
    }
  }

  async function handleCopyResponse(text: string) {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      setError("Unable to copy response in this browser context.");
    }
  }

  async function handleResolveTicket(notes: string) {
    if (!selectedTicketId) {
      return;
    }
    setSavingResolution(true);
    setError(null);
    try {
      const nextDetail = await resolveTicket(selectedTicketId, { resolution_notes: notes });
      setDetail(nextDetail);
      setResolveModalOpen(false);
      await Promise.all([loadStats(), loadTickets()]);
      setSelectedTicketId(selectedTicketId);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Unable to resolve ticket.");
    } finally {
      setSavingResolution(false);
    }
  }

  return (
    <main className="min-h-screen bg-panel">
      <DashboardHeader
        search={filters.search ?? ""}
        onSearchChange={(value) => handleFilterChange("search", value)}
        onNewTicket={() => setModalOpen(true)}
        onRefresh={refreshAll}
      />

      <div className="mx-auto max-w-[1600px] space-y-4 px-4 py-4 lg:px-6">
        <StatsCards stats={stats} />
        {error ? <ErrorCallout message={error} /> : null}

        <div className="grid grid-cols-1 gap-4 lg:grid-cols-[260px_minmax(0,1fr)_420px]">
          <TicketQueueSidebar
            filters={filters}
            total={tickets.length}
            onChange={handleFilterChange}
            onClear={() => {
              setFilters(defaultFilters);
              setSelectedTicketId(null);
              setOriginTicket(null);
            }}
          />
          <TicketList
            tickets={tickets}
            selectedTicketId={selectedTicketId}
            loading={loadingTickets}
            onSelect={handleSelectTicket}
          />
          <TicketDetailPanel
            detail={selectedTicket ? detail : null}
            analyzing={analyzingTicketId === selectedTicketId}
            applyingAnalysis={detail?.latest_analysis?.id === applyingAnalysisId}
            onAnalyze={handleAnalyzeTicket}
            onApplyAnalysis={handleApplyAnalysis}
            onCopyResponse={handleCopyResponse}
            onOpenSimilarTicket={handleOpenSimilarTicket}
            originTicket={originTicket}
            onReturnToOrigin={handleReturnToOrigin}
            onResolve={() => setResolveModalOpen(true)}
          />
        </div>
      </div>

      <NewTicketModal
        open={modalOpen}
        saving={savingTicket}
        onClose={() => setModalOpen(false)}
        onSubmit={handleCreateTicket}
      />
      <ResolveTicketModal
        open={resolveModalOpen}
        saving={savingResolution}
        initialNotes={detail?.ticket.resolution_notes ?? ""}
        onClose={() => setResolveModalOpen(false)}
        onSubmit={handleResolveTicket}
      />
    </main>
  );
}
