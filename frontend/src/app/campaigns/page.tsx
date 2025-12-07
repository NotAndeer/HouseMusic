"use client";

import { useEffect, useState } from "react";
import { Campaign, createCampaign, getCampaigns } from "../../lib/api";

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    getCampaigns().then(setCampaigns).catch(() => setCampaigns([]));
  }, []);

  const handleCreate = async () => {
    const created = await createCampaign({ name, description, channels: [] });
    setCampaigns((prev) => [...prev, created]);
    setName("");
    setDescription("");
  };

  return (
    <main className="p-8 space-y-6">
      <h1 className="text-xl font-bold">Campañas</h1>
      <div className="space-y-2 max-w-md">
        <input className="border p-2 w-full" placeholder="Nombre" value={name} onChange={(e) => setName(e.target.value)} />
        <textarea
          className="border p-2 w-full"
          placeholder="Descripción"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button className="bg-blue-600 text-white px-4 py-2" onClick={handleCreate}>
          Crear campaña
        </button>
      </div>
      <table className="min-w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 text-left">Nombre</th>
            <th className="p-2 text-left">Estado</th>
            <th className="p-2 text-left">Programada</th>
          </tr>
        </thead>
        <tbody>
          {campaigns.map((campaign) => (
            <tr key={campaign.id} className="border-t">
              <td className="p-2">{campaign.name}</td>
              <td className="p-2">{campaign.status}</td>
              <td className="p-2">{campaign.scheduled_at ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
