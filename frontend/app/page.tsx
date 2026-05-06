import Link from "next/link";
import { ClipboardList, LifeBuoy } from "lucide-react";

export default function LandingPage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-white px-4 py-10">
      <section className="w-full max-w-2xl rounded border border-blue-900 bg-blue-800 p-6 text-white shadow-soft sm:p-8">
        <div className="mx-auto max-w-xl text-center">
          <p className="text-sm font-medium uppercase tracking-normal text-blue-100">TriagePilot AI</p>
          <h1 className="mt-2 text-2xl font-semibold tracking-normal sm:text-3xl">Choose a ticket workflow</h1>
          <p className="mt-3 text-sm leading-6 text-blue-100">
            Employees can submit a support request. IT teams can review, triage, and resolve tickets.
          </p>
        </div>

        <div className="mt-8 grid grid-cols-1 gap-3 sm:grid-cols-2">
          <Link
            href="/create-ticket"
            className="group flex min-h-32 flex-col justify-between rounded border border-blue-200 bg-white p-4 text-left text-slate-950 transition hover:bg-blue-50"
          >
            <span className="inline-flex h-10 w-10 items-center justify-center rounded bg-blue-700 text-white">
              <ClipboardList className="h-5 w-5" aria-hidden="true" />
            </span>
            <span>
              <span className="block text-lg font-semibold">Create Ticket</span>
              <span className="mt-1 block text-sm leading-5 text-slate-600">For employees reporting an issue.</span>
            </span>
          </Link>

          <Link
            href="/resolve"
            className="group flex min-h-32 flex-col justify-between rounded border border-blue-200 bg-white p-4 text-left text-slate-950 transition hover:bg-blue-50"
          >
            <span className="inline-flex h-10 w-10 items-center justify-center rounded bg-blue-700 text-white">
              <LifeBuoy className="h-5 w-5" aria-hidden="true" />
            </span>
            <span>
              <span className="block text-lg font-semibold">Resolve Ticket</span>
              <span className="mt-1 block text-sm leading-5 text-slate-600">For IT teams working the queue.</span>
            </span>
          </Link>
        </div>
      </section>
    </main>
  );
}
