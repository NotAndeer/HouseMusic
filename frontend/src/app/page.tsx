import { useEffect, useState } from "react";
import { getCampaigns, getContacts } from "../lib/api";

export default function DashboardPage() {
  const [campaignCount, setCampaignCount] = useState<number>(0);
  const [contactCount, setContactCount] = useState<number>(0);
  const [connectedAccounts, setConnectedAccounts] = useState<number>(0);

  useEffect(() => {
    getCampaigns().then((items) => setCampaignCount(items.length)).catch(() => setCampaignCount(0));
    getContacts().then((items) => setContactCount(items.length)).catch(() => setContactCount(0));
    setConnectedAccounts(0);
  }, []);

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-2xl font-bold">Panel de control</h1>
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <MetricCard label="Campañas" value={campaignCount} />
        <MetricCard label="Contactos" value={contactCount} />
        <MetricCard label="Cuentas conectadas" value={connectedAccounts} />
      </section>
    </main>
  );
}

function MetricCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded border p-4 shadow-sm">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-3xl font-semibold">{value}</p>
    </div>
  );
}
